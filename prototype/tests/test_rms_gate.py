"""Tests for the rms_rule + snr_gate comparator, the stacked experiment and the new metric helpers."""

import os

import numpy as np
import pandas as pd
import pytest

from conftest import FEATURES
from detakpompa.metrics import aurc, gated_score, top_coverage, unit_bootstrap, unit_bootstrap_fn
from detakpompa.models import AbstainGate, RFPlusRuleFeature, RMSGateBaseline, ThresholdRule, rule_margin

needs_feat = pytest.mark.skipif(not os.path.exists(FEATURES), reason="run run_eval.py first")


def _toy(n_units=10, per=12, seed=0):
    """3 ordinal classes whose RMS is ~1, ~3, ~9 (log-spaced) + gate columns."""
    rng = np.random.default_rng(seed)
    rows = []
    for u in range(1, n_units + 1):
        for k, level in enumerate((1.0, 3.0, 9.0)):
            for _ in range(per):
                rows.append({"unit": u, "state": k, "rms": level * np.exp(rng.normal(0, 0.15)),
                             "shaft_snr_db": 30.0, "clip_frac": 0.0, "flat_frac": 0.0})
    return pd.DataFrame(rows)


def test_rule_margin_is_log_distance_to_nearest_threshold():
    r = ThresholdRule("rms")
    r.sign, r.t1, r.t2 = 1.0, 2.0, 20.0
    X = pd.DataFrame({"rms": [2.0, 20.0, 0.2, 200.0, np.sqrt(40.0)]})
    m = rule_margin(r, X)
    assert np.allclose(m, [0.0, 0.0, 1.0, 1.0, 0.5])            # decades from the nearest threshold
    # direction-flipped rule (lower = worse): thresholds are stored as -t, margin is the same
    r2 = ThresholdRule("rms")
    r2.sign, r2.t1, r2.t2 = -1.0, -20.0, -2.0
    assert np.allclose(rule_margin(r2, X), m)


def test_rms_gate_uses_identical_gate_and_learns_from_train_only():
    F = _toy()
    y, units = F.state.to_numpy(), F.unit.to_numpy()
    tr, te = units != 1, units == 1
    m = RMSGateBaseline(snr_min=11.52).fit(F[tr], y[tr], units[tr])
    assert m.gate.snr_min == AbstainGate(snr_min=11.52).snr_min
    pred, conf, acc, why = m.decide(F[te])
    assert (pred == y[te]).mean() > 0.9                          # easy toy problem
    assert 0 < m.gate.tau_conf < conf.max()                      # tau from inner CV, not trivial
    assert set(why) <= {"ok", "ragu", "sinyal"}
    assert np.array_equal(acc, (why == "ok"))
    # the SNR gate overrides everything (sensor off -> 'sinyal', whatever the RMS says)
    bad = F[te].copy()
    bad["shaft_snr_db"] = 5.0
    _, _, acc_b, why_b = m.decide(bad)
    assert not acc_b.any() and set(why_b) == {"sinyal"}
    # predictions do not change when a test row changes (fit only on training rows)
    G = F.copy()
    G.loc[te, "rms"] *= 100
    m2 = RMSGateBaseline(snr_min=11.52).fit(G[tr], y[tr], units[tr])
    assert (m2.rule.t1, m2.rule.t2, m2.gate.tau_conf) == (m.rule.t1, m.rule.t2, m.gate.tau_conf)


def test_low_margin_is_abstained_as_ragu():
    F = _toy()
    y, units = F.state.to_numpy(), F.unit.to_numpy()
    m = RMSGateBaseline(snr_min=0).fit(F, y, units)
    X = F.iloc[:2].copy()
    X["rms"] = [m.rule.sign * m.rule.t1, 1.0]                   # exactly on a threshold vs class centre
    _, conf, acc, why = m.decide(X)
    assert conf[0] == pytest.approx(0.0) and why[0] == "ragu" and not acc[0]


def test_rf_plus_rule_feature_runs_and_adds_column():
    F = _toy(n_units=6, per=6)
    from detakpompa.features import SPEC_COLS
    for c in SPEC_COLS:
        if c not in F:
            F[c] = np.random.default_rng(1).normal(size=len(F))
    y, units = F.state.to_numpy(), F.unit.to_numpy()
    m = RFPlusRuleFeature().fit(F[units != 1], y[units != 1], units[units != 1])
    P = m.predict_proba(F[units == 1])
    assert P.shape == ((units == 1).sum(), 3) and np.allclose(P.sum(1), 1)
    assert RFPlusRuleFeature.FEAT in m.rf.cols and "rms" in m.rf.cols


def test_aurc_perfect_ranking_and_ties():
    y = np.array([0, 0, 1, 1])
    pred = np.array([0, 0, 1, 0])                                # last one wrong
    assert aurc(y, pred, [4, 3, 2, 1]) == pytest.approx(np.mean([0, 0, 0, 0.25]))
    assert aurc(y, pred, [1, 2, 3, 4]) > aurc(y, pred, [4, 3, 2, 1])
    # all-tied scores: order is a fixed random permutation, not row order -> deterministic
    assert aurc(y, pred, [1, 1, 1, 1]) == aurc(y, pred, [1, 1, 1, 1])


def test_gated_score_puts_rejected_last_and_top_coverage():
    conf = np.array([0.9, 0.2, 0.8, 0.95])
    ok = np.array([True, True, True, False])
    s = gated_score(conf, ok)
    assert s[3] < s.min(initial=np.inf, where=ok)
    assert np.argsort(-s)[:3].tolist() == [0, 2, 1]
    assert top_coverage(s, 0.5).tolist() == [True, False, True, False]


def test_unit_bootstrap_fn_matches_unit_bootstrap_draws():
    rng = np.random.default_rng(0)
    units = np.repeat(np.arange(8), 9)
    y = np.tile([0, 1, 2], 24)
    p = np.where(rng.random(len(y)) < 0.7, y, (y + 1) % 3)
    from sklearn.metrics import balanced_accuracy_score
    _, v = unit_bootstrap(y, {"m": p}, units, n_boot=200)
    w = unit_bootstrap_fn(y, units, lambda i: {"m": balanced_accuracy_score(y[i], p[i])}, n_boot=200)
    assert np.allclose(v["m"], w["m"])


@needs_feat
def test_rms_gate_on_real_features_one_fold():
    F = pd.read_csv(FEATURES)
    y, units = F.state.to_numpy(), F.unit.to_numpy()
    tr, te = units != 3, units == 3
    m = RMSGateBaseline(snr_min=11.52).fit(F[tr], y[tr], units[tr])
    pred, conf, acc, why = m.decide(F[te])
    gate = AbstainGate(snr_min=11.52)
    assert np.array_equal(why != "sinyal", gate.quality_ok(F[te]))   # identical signal gate
    assert np.array_equal(pred, ThresholdRule("rms").fit(F[tr], y[tr]).predict(F[te]))
    assert (conf >= 0).all()
