"""Metrics: balanced accuracy, macro-F1, per-unit bootstrap CI, coverage-risk."""

from __future__ import annotations

import numpy as np
from sklearn.metrics import balanced_accuracy_score, confusion_matrix, f1_score


def basic(y, p):
    return {
        "balanced_accuracy": float(balanced_accuracy_score(y, p)),
        "macro_f1": float(f1_score(y, p, average="macro", labels=[0, 1, 2], zero_division=0)),
        "f1_per_class": [float(v) for v in f1_score(y, p, average=None, labels=[0, 1, 2], zero_division=0)],
        "confusion": confusion_matrix(y, p, labels=[0, 1, 2]).tolist(),
        "n": int(len(y)),
    }


def unit_bootstrap(y, preds: dict, units, n_boot=2000, seed=0, metric=balanced_accuracy_score):
    """Resample UNITS with replacement (all windows of a drawn unit come along).

    preds: {model_name: prediction array}. Returns ({name: (lo, hi)} 95 % percentile CIs,
    {name: list of resampled values}); use paired_diff() on the latter (same resamples).
    """
    y, units = np.asarray(y), np.asarray(units)
    uniq = np.unique(units)
    idx_by_u = {u: np.flatnonzero(units == u) for u in uniq}
    rng = np.random.default_rng(seed)
    names = list(preds)
    vals = {n: [] for n in names}
    for _ in range(n_boot):
        draw = rng.choice(uniq, len(uniq), replace=True)
        idx = np.concatenate([idx_by_u[u] for u in draw])
        if len(np.unique(y[idx])) < 3:
            continue
        for n in names:
            vals[n].append(metric(y[idx], np.asarray(preds[n])[idx]))
    ci = {n: (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))) for n, v in vals.items()}
    return ci, vals


def paired_diff(vals, a, b):
    d = np.asarray(vals[a]) - np.asarray(vals[b])
    return float(d.mean()), float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5)), float(np.mean(d <= 0))


def coverage_risk(y, pred, conf, n_points=50):
    """Sweep the confidence threshold: coverage vs risk (1 - balanced accuracy on accepted)
    and vs plain error rate. Returns list of dicts + AURC (area under error-rate curve)."""
    y, pred, conf = map(np.asarray, (y, pred, conf))
    order = np.argsort(-conf)
    rows = []
    n = len(y)
    for k in np.unique(np.linspace(max(1, int(0.05 * n)), n, n_points).astype(int)):
        sel = order[:k]
        err = float(np.mean(pred[sel] != y[sel]))
        bacc = float(balanced_accuracy_score(y[sel], pred[sel])) if len(np.unique(y[sel])) > 1 else float("nan")
        rows.append({"coverage": k / n, "threshold": float(conf[order[k - 1]]), "error_rate": err,
                     "balanced_accuracy": bacc})
    # AURC over every possible cut-off (standard definition)
    cum_err = np.cumsum(pred[order] != y[order]) / np.arange(1, n + 1)
    return rows, float(cum_err.mean())


def unit_bootstrap_fn(y, units, fn, n_boot=2000, seed=0):
    """Generic per-unit bootstrap. Same unit draws (same rng, same skip rule) as unit_bootstrap,
    so resample r here is resample r there. fn(idx) -> {name: value}. Returns {name: array}."""
    y, units = np.asarray(y), np.asarray(units)
    uniq = np.unique(units)
    idx_by_u = {u: np.flatnonzero(units == u) for u in uniq}
    rng = np.random.default_rng(seed)
    out = {}
    for _ in range(n_boot):
        draw = rng.choice(uniq, len(uniq), replace=True)
        idx = np.concatenate([idx_by_u[u] for u in draw])
        if len(np.unique(y[idx])) < 3:
            continue
        for k, v in fn(idx).items():
            out.setdefault(k, []).append(v)
    return {k: np.asarray(v, float) for k, v in out.items()}


def _order(conf, seed=0):
    """Most-confident-first order; ties broken by a fixed random permutation (not by row order,
    which follows recording/class order and would bias tied RF probabilities)."""
    conf = np.asarray(conf, float)
    tb = np.random.default_rng(seed).permutation(len(conf))
    return np.lexsort((tb, -conf))


def aurc(y, pred, conf, seed=0):
    """Area under the error-rate coverage-risk curve over every cut-off (tie-neutral order)."""
    y, pred = np.asarray(y), np.asarray(pred)
    order = _order(conf, seed)
    return float((np.cumsum(pred[order] != y[order]) / np.arange(1, len(y) + 1)).mean())


def top_coverage(conf, coverage, seed=0):
    """Boolean mask of the round(coverage * n) most confident items (tie-neutral order)."""
    conf = np.asarray(conf)
    k = max(1, int(round(coverage * len(conf))))
    m = np.zeros(len(conf), bool)
    m[_order(conf, seed)[:k]] = True
    return m


def gated_score(conf, quality_ok):
    """Confidence for a gated model: windows failing the signal gate are ranked below every window
    that passes (they are abstained first); order inside each group is kept."""
    conf = np.asarray(conf, float)
    span = (np.nanmax(conf) - np.nanmin(conf)) + 1.0
    return np.where(np.asarray(quality_ok, bool), conf, conf - 10 * span - 1.0)
