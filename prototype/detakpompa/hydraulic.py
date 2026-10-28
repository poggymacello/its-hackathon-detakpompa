"""Residual hydraulic model ("normal behaviour conditional on the operating point") for SKAB.

Implements PRAREG_SKAB.md (frozen before the data was downloaded). New module: no existing
DetakPompa module is modified; only `splits.assert_no_leakage` is imported.

Idea (11_RISET_KELEMAHAN.md §2-§3): throttling moves the operating point ALONG the pump curve
(residuals of P|(Q,p) and p|Q stay ~0); a pump fault moves the CURVE (or raises vibration at the
same operating point). Baselines are plain per-sensor robust z thresholds.
"""

from __future__ import annotations

import os
import re

import numpy as np
import pandas as pd
from scipy.stats import rankdata
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

from .splits import assert_no_leakage

SENSORS = ["Accelerometer1RMS", "Accelerometer2RMS", "Current", "Pressure",
           "Temperature", "Thermocouple", "Voltage", "RateRMS"]
Q, P = "RateRMS", "Pressure"
PAPP = "P_app"
ANOMALY_FREE = "anomaly-free"

# Residual targets: name -> (target column, input columns)
TARGETS = {
    "z_P": (PAPP, [Q, P]),
    "z_p": (P, [Q]),
    "z_acc1": ("Accelerometer1RMS", [Q, P]),
    "z_acc2": ("Accelerometer2RMS", [Q, P]),
}
HYD = ["z_P", "z_p"]

SMOOTH = 5          # causal rolling mean, samples (1 Hz)
TAU_Q = 0.99        # threshold quantile on training-normal smoothed scores
RECENTER_N = 120    # S10: first rows of each file used for unlabeled re-centering

# Classes (PRAREG_SKAB §2), from data/README.md
IMBALANCE = [f"other/{k}" for k in (5, 6, 7, 8, 9)]
CAVITATION = [f"other/{k}" for k in (12, 13)]
PROCESS = [f"other/{k}" for k in (1, 2, 3, 4, 10, 11, 14)]


def experiment_class(exp_id: str) -> str:
    """T = throttling (valve closed), F = pump fault, X = process/system change."""
    if exp_id.startswith("valve1/") or exp_id.startswith("valve2/"):
        return "T"
    if exp_id in IMBALANCE or exp_id in CAVITATION:
        return "F"
    if exp_id in PROCESS:
        return "X"
    if exp_id == ANOMALY_FREE:
        return "N"
    raise ValueError(f"unknown SKAB experiment id {exp_id!r}")


def experiment_subclass(exp_id: str) -> str:
    if exp_id.startswith("valve1/"):
        return "T-valve1 (inlet)"
    if exp_id.startswith("valve2/"):
        return "T-valve2 (outlet)"
    if exp_id in IMBALANCE:
        return "F-imbalance"
    if exp_id in CAVITATION:
        return "F-kavitasi"
    if exp_id in PROCESS:
        return "X-proses"
    return "N"


# ----------------------------------------------------------------------------- loading

def _read(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", index_col="datetime", parse_dates=True)
    return df


def load_skab(root: str) -> tuple[dict[str, pd.DataFrame], dict]:
    """root = folder containing anomaly-free/, valve1/, valve2/, other/.

    Returns ({exp_id: df}, info). Each df has SENSORS + P_app + anomaly (int) + t (row order).
    Rows with NaN in used columns are dropped and counted in info.
    """
    out, info = {}, {"dropped_nan": {}, "missing_anomaly_col": []}
    for folder in (ANOMALY_FREE, "valve1", "valve2", "other"):
        d = os.path.join(root, folder)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".csv"):
                continue
            stem = fn[:-4]
            exp_id = ANOMALY_FREE if folder == ANOMALY_FREE else f"{folder}/{stem}"
            df = _read(os.path.join(d, fn))
            df.columns = [c.strip() for c in df.columns]
            # Deviation D1 (results/skab/DEVIASI.md): the CSV header says "Volume Flow RateRMS",
            # the repo README says "RateRMS". Same column, renamed only.
            df = df.rename(columns={"Volume Flow RateRMS": "RateRMS"})
            if "anomaly" not in df.columns:
                info["missing_anomaly_col"].append(exp_id)
                df["anomaly"] = 0
            df = df[SENSORS + ["anomaly"]].astype(float)
            n0 = len(df)
            df = df.dropna()
            if len(df) < n0:
                info["dropped_nan"][exp_id] = n0 - len(df)
            df["anomaly"] = df["anomaly"].astype(int)
            df[PAPP] = df["Voltage"] * df["Current"]
            df["t"] = np.arange(len(df))
            out[exp_id] = df
    return out, info


def sort_key(exp_id: str):
    m = re.match(r"(\w+)/(\d+)$", exp_id)
    return (m.group(1), int(m.group(2))) if m else (exp_id, -1)


# ----------------------------------------------------------------------------- splits

def loeo_folds(exp_ids):
    """Leave-one-experiment-out. anomaly-free is never a test fold and is always in training."""
    tests = sorted([e for e in exp_ids if e != ANOMALY_FREE], key=sort_key)
    for e in tests:
        train = [x for x in exp_ids if x != e]
        yield e, train


def build_train(data: dict, train_ids, include_valve_anomaly: bool = False) -> pd.DataFrame:
    """Training-normal rows: anomaly == 0 of every training experiment (+ all of anomaly-free).
    include_valve_anomaly (S4, R-sehat): also valve1/valve2 anomaly rows of TRAINING files."""
    parts = []
    for e in train_ids:
        df = data[e]
        keep = df["anomaly"].to_numpy() == 0
        if include_valve_anomaly and experiment_class(e) == "T":
            keep = np.ones(len(df), bool)
        part = df.loc[keep].copy()
        part["exp"] = e
        parts.append(part)
    return pd.concat(parts, ignore_index=True)


def stack(data: dict, ids) -> pd.DataFrame:
    """All rows (normal + anomaly) of the given experiments, in file/row order, with 'exp'."""
    parts = []
    for e in ids:
        part = data[e].copy()
        part["exp"] = e
        parts.append(part)
    return pd.concat(parts, ignore_index=True)


def check_fold(train_exp, test_exp):
    """Raise if any experiment id appears on both sides (uses splits.assert_no_leakage)."""
    train_exp, test_exp = np.asarray(train_exp), np.asarray(test_exp)
    exp = np.concatenate([train_exp, test_exp])
    tr = np.arange(len(train_exp))
    te = np.arange(len(train_exp), len(exp))
    assert_no_leakage(exp, tr, te)


# ----------------------------------------------------------------------------- models

def _robust_scale(x: np.ndarray) -> float:
    x = np.asarray(x, float)
    s = 1.4826 * np.median(np.abs(x - np.median(x)))
    if not np.isfinite(s) or s <= 0:
        s = float(np.std(x))
    return max(float(s), 1e-9)


def _regressor(kind: str):
    if kind == "ridge":
        return make_pipeline(StandardScaler(), PolynomialFeatures(degree=2, include_bias=False),
                             Ridge(alpha=1.0))
    if kind == "gbm":
        return HistGradientBoostingRegressor(max_iter=200, learning_rate=0.1, random_state=0)
    raise ValueError(kind)


class ResidualModel:
    """Four regressions on training-normal data; z residuals scaled by 1.4826*MAD."""

    def __init__(self, kind: str = "ridge"):
        self.kind = kind
        self.models, self.scale = {}, {}

    def fit(self, df: pd.DataFrame):
        for name, (y, xs) in TARGETS.items():
            m = _regressor(self.kind)
            X = df[xs].to_numpy(float)
            yy = df[y].to_numpy(float)
            m.fit(X, yy)
            self.models[name] = m
            self.scale[name] = _robust_scale(yy - m.predict(X))
        return self

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        out = {}
        for name, (y, xs) in TARGETS.items():
            out[name] = self.models[name].predict(df[xs].to_numpy(float))
        return pd.DataFrame(out, index=df.index)

    def components(self, df: pd.DataFrame) -> pd.DataFrame:
        out = {}
        for name, (y, xs) in TARGETS.items():
            pred = self.models[name].predict(df[xs].to_numpy(float))
            out[name] = (df[y].to_numpy(float) - pred) / self.scale[name]
        return pd.DataFrame(out, index=df.index)


class SensorZ:
    """Robust per-sensor z (median / 1.4826*MAD of training-normal rows)."""

    def fit(self, df: pd.DataFrame):
        self.med = {c: float(np.median(df[c])) for c in SENSORS}
        self.scale = {c: _robust_scale(df[c].to_numpy(float)) for c in SENSORS}
        return self

    def components(self, df: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame({c: (df[c].to_numpy(float) - self.med[c]) / self.scale[c] for c in SENSORS},
                            index=df.index)


def score_R(z: pd.DataFrame, cols=None) -> np.ndarray:
    cols = list(TARGETS) if cols is None else cols
    return np.sqrt(np.mean(z[cols].to_numpy(float) ** 2, axis=1))


def score_B1(z: pd.DataFrame) -> np.ndarray:
    return np.maximum(np.abs(z["Accelerometer1RMS"].to_numpy()), np.abs(z["Accelerometer2RMS"].to_numpy()))


def score_B2(z: pd.DataFrame) -> np.ndarray:
    return np.abs(z["Current"].to_numpy())


def score_B3(z: pd.DataFrame) -> np.ndarray:
    return np.max(np.abs(z[SENSORS].to_numpy(float)), axis=1)


def smooth(score: np.ndarray, groups: np.ndarray, window: int = SMOOTH) -> np.ndarray:
    """Causal rolling mean within each group (file); never mixes files."""
    s = pd.Series(np.asarray(score, float))
    g = pd.Series(np.asarray(groups))
    return s.groupby(g, sort=False).transform(lambda x: x.rolling(window, min_periods=1).mean()).to_numpy()


def recenter(z: pd.DataFrame, groups: np.ndarray, n: int = RECENTER_N) -> pd.DataFrame:
    """S10: subtract, per file, the median of each component over that file's first n rows
    (row order). No labels used."""
    z = z.copy()
    groups = np.asarray(groups)
    for g in pd.unique(groups):
        idx = np.flatnonzero(groups == g)
        head = idx[:n]
        z.iloc[idx] = z.iloc[idx].to_numpy() - np.median(z.iloc[head].to_numpy(), axis=0)
    return z


# ----------------------------------------------------------------------------- metrics

def auc(scores, labels) -> float:
    """Mann-Whitney AUROC (ties = 0.5). labels: 1 positive, 0 negative."""
    scores, labels = np.asarray(scores, float), np.asarray(labels, int)
    pos, neg = labels == 1, labels == 0
    n1, n0 = pos.sum(), neg.sum()
    if n1 == 0 or n0 == 0:
        return np.nan
    r = rankdata(scores)
    return float((r[pos].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


class WeightedAUC:
    """AUROC with per-row integer weights (bootstrap counts), O(n) per evaluation.
    Equivalent to AUROC on rows duplicated w times."""

    def __init__(self, scores, labels):
        scores = np.asarray(scores, float)
        self.labels = np.asarray(labels, int)
        _, self.grp = np.unique(scores, return_inverse=True)  # ascending tie groups
        self.ng = self.grp.max() + 1

    def __call__(self, w) -> float:
        w = np.asarray(w, float)
        wp = np.bincount(self.grp, weights=w * (self.labels == 1), minlength=self.ng)
        wn = np.bincount(self.grp, weights=w * (self.labels == 0), minlength=self.ng)
        Wp, Wn = wp.sum(), wn.sum()
        if Wp == 0 or Wn == 0:
            return np.nan
        below = np.cumsum(wn) - wn
        return float(np.sum(wp * (below + 0.5 * wn)) / (Wp * Wn))


def bootstrap_weights(units, n_boot: int, seed: int = 0, strata=None):
    """Yield per-row weight vectors from resampling UNITS with replacement.
    strata: optional per-row stratum label; units resampled within each stratum."""
    units = np.asarray(units)
    uniq, inv = np.unique(units, return_inverse=True)
    rng = np.random.default_rng(seed)
    if strata is None:
        groups = [np.arange(len(uniq))]
    else:
        strata = np.asarray(strata)
        ustr = {}
        for u_i, u in enumerate(uniq):
            ustr.setdefault(strata[np.flatnonzero(units == u)[0]], []).append(u_i)
        groups = [np.array(v) for _, v in sorted(ustr.items())]
    for _ in range(n_boot):
        cnt = np.zeros(len(uniq))
        for g in groups:
            draw = rng.choice(g, len(g), replace=True)
            cnt += np.bincount(draw, minlength=len(uniq))
        yield cnt[inv]


def paired_auc_bootstrap(scores: dict, labels, units, ref: str, others, n_boot: int, seed: int = 0,
                         strata=None):
    """Δ_j = AUC(ref) − AUC(other_j) on the SAME resamples.
    Returns {other: dict(delta, lo, hi, p_one_sided, p_two_sided, n_valid)}."""
    labels = np.asarray(labels, int)
    calc = {k: WeightedAUC(scores[k], labels) for k in [ref, *others]}
    obs = {k: auc(scores[k], labels) for k in [ref, *others]}
    deltas = {o: [] for o in others}
    for w in bootstrap_weights(units, n_boot, seed, strata):
        a_ref = calc[ref](w)
        if not np.isfinite(a_ref):
            continue
        for o in others:
            deltas[o].append(a_ref - calc[o](w))
    res = {}
    for o in others:
        d = np.asarray(deltas[o])
        nb = len(d)
        p1 = (1 + np.sum(d <= 0)) / (nb + 1)
        p2 = min(1.0, 2 * min((1 + np.sum(d <= 0)) / (nb + 1), (1 + np.sum(d >= 0)) / (nb + 1)))
        res[o] = dict(auc_ref=obs[ref], auc_other=obs[o], delta=obs[ref] - obs[o],
                      lo=float(np.percentile(d, 2.5)), hi=float(np.percentile(d, 97.5)),
                      p_one_sided=float(p1), p_two_sided=float(p2), n_valid=int(nb))
    return res


def auc_ci(score, labels, units, n_boot: int, seed: int = 0, strata=None):
    calc = WeightedAUC(score, labels)
    v = [calc(w) for w in bootstrap_weights(units, n_boot, seed, strata)]
    v = np.asarray([x for x in v if np.isfinite(x)])
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


def holm(pvals: dict, alpha: float) -> dict:
    """Holm step-down. Returns {name: (p, threshold, rejected)}."""
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out, still = {}, True
    for i, (k, p) in enumerate(items):
        thr = alpha / (m - i)
        rej = still and p < thr
        if not rej:
            still = False
        out[k] = (p, thr, rej)
    return out


def balanced_accuracy(y_true, y_pred) -> float:
    y_true, y_pred = np.asarray(y_true, int), np.asarray(y_pred, int)
    tpr = np.mean(y_pred[y_true == 1] == 1) if np.any(y_true == 1) else np.nan
    tnr = np.mean(y_pred[y_true == 0] == 0) if np.any(y_true == 0) else np.nan
    return float((tpr + tnr) / 2)
