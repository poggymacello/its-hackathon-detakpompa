"""Tests for detakpompa.hydraulic + run_skab protocol (PRAREG_SKAB.md).

Synthetic tests always run; tests on the real SKAB files are skipped when data/skab is absent.
"""

import hashlib
import os

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import roc_auc_score

from conftest import ROOT
from detakpompa import hydraulic as hy

SKAB = os.path.join(ROOT, "data", "skab", "data")


def _toy_data(n=300, seed=0):
    rng = np.random.default_rng(seed)
    ids = [hy.ANOMALY_FREE] + [f"valve1/{k}" for k in range(16)] + [f"valve2/{k}" for k in range(4)] \
        + [f"other/{k}" for k in range(1, 15)]
    data = {}
    for e in ids:
        Q = rng.normal(120, 3, n)
        p = 2.0 - 5e-5 * Q ** 2 + rng.normal(0, 0.01, n)
        df = pd.DataFrame({c: rng.normal(1, 0.01, n) for c in hy.SENSORS})
        df["RateRMS"], df["Pressure"] = Q, p
        df["anomaly"] = 0 if e == hy.ANOMALY_FREE else (np.arange(n) >= n // 2).astype(int)
        df[hy.PAPP] = df["Voltage"] * df["Current"]
        df["t"] = np.arange(n)
        data[e] = df
    return data


def test_class_map_counts():
    data = _toy_data(n=10)
    cls = pd.Series({e: hy.experiment_class(e) for e in data})
    assert (cls == "T").sum() == 20 and (cls == "F").sum() == 7 and (cls == "X").sum() == 7
    assert (cls == "N").sum() == 1
    with pytest.raises(ValueError):
        hy.experiment_class("other/99")


def test_loeo_test_experiment_never_in_training():
    data = _toy_data(n=20)
    folds = list(hy.loeo_folds(list(data)))
    assert len(folds) == 34
    assert hy.ANOMALY_FREE not in [t for t, _ in folds]          # never tested
    for test_id, train_ids in folds:
        assert test_id not in train_ids
        assert hy.ANOMALY_FREE in train_ids                      # always trained on
        for include in (False, True):
            tr = hy.build_train(data, train_ids, include_valve_anomaly=include)
            assert test_id not in set(tr["exp"])                  # no row of the test run
            hy.check_fold(tr["exp"].to_numpy(), np.array([test_id] * 5))
        full = hy.stack(data, train_ids)
        assert test_id not in set(full["exp"])


def test_check_fold_detects_leak():
    with pytest.raises(AssertionError):
        hy.check_fold(np.array(["valve1/0", "valve1/1"]), np.array(["valve1/1"]))


def test_build_train_only_normal_rows_unless_sehat():
    data = _toy_data(n=40)
    ids = [e for e in data if e != "valve1/0"]
    tr = hy.build_train(data, ids)
    assert (tr["anomaly"] == 0).all()
    trs = hy.build_train(data, ids, include_valve_anomaly=True)
    extra = trs[trs["anomaly"] == 1]
    assert len(extra) > 0 and set(extra["exp"].map(hy.experiment_class)) == {"T"}


def test_residual_model_along_curve_vs_shifted_curve():
    rng = np.random.default_rng(1)
    n = 4000
    Q = rng.uniform(40, 130, n)
    p = 2.0 - 5e-5 * Q ** 2 + rng.normal(0, 0.01, n)
    P = 200 + 0.5 * Q + 50 * p + rng.normal(0, 1, n)
    df = pd.DataFrame({"RateRMS": Q, "Pressure": p, hy.PAPP: P,
                       "Accelerometer1RMS": rng.normal(0.2, 0.01, n), "Accelerometer2RMS": rng.normal(0.2, 0.01, n)})
    m = hy.ResidualModel("ridge").fit(df.iloc[:3000])
    test = df.iloc[3000:].copy()
    along = hy.score_R(m.components(test)).mean()
    shifted = test.copy()
    shifted["Pressure"] -= 0.2                                    # curve moved (worn / cavitating)
    off = hy.score_R(m.components(shifted)).mean()
    assert along < 2 and off > 5 * along


def test_smooth_is_causal_and_within_file():
    s = np.array([0, 0, 10, 0, 100, 100, 100.0])
    g = np.array(["a", "a", "a", "a", "b", "b", "b"])
    out = hy.smooth(s, g, window=2)
    assert out[0] == 0 and out[2] == 5 and out[3] == 5
    assert out[4] == 100                                          # file b does not see file a


def test_recenter_uses_only_head_rows():
    z = pd.DataFrame({"a": np.r_[np.ones(5), np.full(5, 10.0)]})
    out = hy.recenter(z, np.array(["f"] * 10), n=5)
    assert np.allclose(out["a"].to_numpy(), np.r_[np.zeros(5), np.full(5, 9.0)])


def test_auc_matches_sklearn_and_weighted_equals_duplication():
    rng = np.random.default_rng(0)
    s = np.round(rng.normal(size=200), 1)                         # with ties
    y = (rng.uniform(size=200) < 0.3).astype(int)
    assert abs(hy.auc(s, y) - roc_auc_score(y, s)) < 1e-12
    w = rng.integers(0, 4, 200)
    idx = np.repeat(np.arange(200), w)
    assert abs(hy.WeightedAUC(s, y)(w) - roc_auc_score(y[idx], s[idx])) < 1e-12


def test_stratified_bootstrap_keeps_class_sizes():
    units = np.array([f"u{i}" for i in range(10)])
    strata = np.r_[np.ones(3), np.zeros(7)].astype(int)
    for w in hy.bootstrap_weights(units, 50, 0, strata=strata):
        assert w[strata == 1].sum() == 3 and w[strata == 0].sum() == 7


def test_holm():
    out = hy.holm({"a": 0.001, "b": 0.02}, 0.025)
    assert out["a"][2] and out["b"][2]
    out = hy.holm({"a": 0.02, "b": 0.02}, 0.025)
    assert not out["a"][2] and not out["b"][2]


def _sha_ok(fname):
    path = os.path.join(ROOT, os.path.splitext(fname)[0] + ".sha256")
    line = open(path, encoding="utf-8").readline().split()
    h = hashlib.sha256(open(os.path.join(ROOT, fname), "rb").read()).hexdigest()
    return h == line[0]


def test_prereg_files_unchanged():
    assert _sha_ok("PRAREG_SKAB.md")
    assert _sha_ok("PRAREG_TKT4.md")


@pytest.mark.skipif(not os.path.isdir(SKAB), reason="SKAB data not downloaded")
def test_real_skab_loeo_no_leakage():
    data, _ = hy.load_skab(SKAB)
    assert len(data) == 35
    for test_id, train_ids in hy.loeo_folds(list(data)):
        tr = hy.build_train(data, train_ids)
        assert test_id not in set(tr["exp"])
        hy.check_fold(tr["exp"].to_numpy(), np.array([test_id] * len(data[test_id])))
