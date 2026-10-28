"""Baselines, proposed model and the abstain gate.

All thresholds/hyper-parameters are fixed in code or fitted on TRAINING units only.
"""

from __future__ import annotations

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import balanced_accuracy_score

from .features import SPEC_COLS, STAT_COLS

RF_PARAMS = dict(n_estimators=300, min_samples_leaf=2, class_weight="balanced",
                 random_state=0, n_jobs=-1)


def _bal_acc(y, p):
    return balanced_accuracy_score(y, p)


class ThresholdRule:
    """3-class ordinal rule on one score: s < t1 -> 0, t1 <= s < t2 -> 1, s >= t2 -> 2.

    Direction (higher = worse or lower = worse) and (t1, t2) are chosen on training data by
    grid search over training quantiles to maximise balanced accuracy.
    """

    def __init__(self, col: str, n_grid: int = 41):
        self.col, self.n_grid = col, n_grid

    def fit(self, X, y):
        s = np.asarray(X[self.col], float)
        y = np.asarray(y)
        best = (-1, 1.0, None, None)
        qs = np.unique(np.quantile(s, np.linspace(0.01, 0.99, self.n_grid)))
        for sign in (1.0, -1.0):
            ss = sign * s
            q = np.sort(sign * qs)
            for i, t1 in enumerate(q):
                for t2 in q[i:]:
                    pred = np.where(ss < t1, 0, np.where(ss < t2, 1, 2))
                    b = _bal_acc(y, pred)
                    if b > best[0]:
                        best = (b, sign, t1, t2)
        _, self.sign, self.t1, self.t2 = best
        return self

    def predict(self, X):
        ss = self.sign * np.asarray(X[self.col], float)
        return np.where(ss < self.t1, 0, np.where(ss < self.t2, 1, 2))


class EnvelopeKurtosisRule:
    """Classical rule: worst of (kurtosis rule, envelope-spectrum peak prominence rule)."""

    def fit(self, X, y):
        self.rk = ThresholdRule("kurt").fit(X, y)
        self.re = ThresholdRule("env_prom_db").fit(X, y)
        return self

    def predict(self, X):
        return np.maximum(self.rk.predict(X), self.re.predict(X))


class RFModel:
    def __init__(self, cols, **kw):
        self.cols = list(cols)
        self.params = {**RF_PARAMS, **kw}

    def fit(self, X, y):
        self.clf = RandomForestClassifier(**self.params).fit(np.asarray(X[self.cols], float), y)
        return self

    def predict_proba(self, X):
        P = self.clf.predict_proba(np.asarray(X[self.cols], float))
        full = np.zeros((len(P), 3))
        full[:, self.clf.classes_.astype(int)] = P
        return full

    def predict(self, X):
        return self.predict_proba(X).argmax(1)


def baseline_rf():
    return RFModel(STAT_COLS)


def proposed_rf():
    return RFModel(SPEC_COLS)


class AbstainGate:
    """Two-stage abstain ("TIDAK TAHU").

    1. Signal-quality gate (SNR): the tracked shaft-rotation line must stand out of the local
       noise floor. Threshold = CFAR-style: the 99th percentile of the same SNR measured on pure
       white noise (pipeline.snr_cfar_threshold), i.e. it uses no dataset label and no test data.
       Also rejects clipped / frozen (flat) signals.
    2. Confidence gate: max class probability below tau_conf. tau_conf is set from INNER
       grouped-CV predictions on the training units only (target coverage `target_cov`).
    """

    def __init__(self, snr_min=None, clip_max=0.01, flat_max=0.2, target_cov=0.9):
        self.clip_max, self.flat_max = clip_max, flat_max
        self.target_cov = target_cov
        self.snr_min = -np.inf if snr_min is None else float(snr_min)
        self.tau_conf = 0.0

    def set_snr(self, snr_min: float):
        self.snr_min = float(snr_min)
        return self

    def fit_conf(self, conf_inner):
        self.tau_conf = float(np.quantile(np.asarray(conf_inner, float), 1 - self.target_cov))
        return self

    def quality_ok(self, X):
        snr = np.asarray(X["shaft_snr_db"], float)
        ok = (snr >= self.snr_min) & (np.asarray(X["clip_frac"]) <= self.clip_max)
        ok &= np.asarray(X["flat_frac"]) <= self.flat_max
        return ok

    def decide(self, X, proba):
        """Return (accept_mask, reason array: 'ok' | 'sinyal' | 'ragu')."""
        q = self.quality_ok(X)
        conf = np.asarray(proba).max(1)
        c = conf >= self.tau_conf
        reason = np.where(~q, "sinyal", np.where(~c, "ragu", "ok"))
        return q & c, reason


def inner_conf(X, y, units, make_model, k=5, seed=0):
    """Out-of-fold max-probabilities on the training units (grouped k-fold)."""
    from .splits import grouped_kfold
    conf = np.full(len(y), np.nan)
    for _, tr, te in grouped_kfold(units, k=k, seed=seed):
        m = make_model().fit(X.iloc[tr], y[tr])
        conf[te] = m.predict_proba(X.iloc[te]).max(1)
    return conf


# ---------------------------------------------------------------------------------------------
# Comparator added 28 Okt 2026 (experiment "rms_rule + snr_gate"): is the proposed RF needed, or
# does the same SNR gate in front of the 2-threshold RMS rule already give the same thing?
# The confidence score below was fixed BEFORE this comparator was ever evaluated (see README,
# section "Eksperimen tambahan") and was not changed afterwards.
# ---------------------------------------------------------------------------------------------

def rule_margin(rule: ThresholdRule, X) -> np.ndarray:
    """Pre-registered confidence of a fitted ThresholdRule: distance from the score to the
    NEAREST decision threshold, measured in log10 of the score (decades), because RMS is a
    positive, scale-like quantity (a ratio to the threshold is what matters). 0 = exactly on a
    threshold (least sure); larger = further inside its class. If the score or a threshold is
    not positive, the linear distance divided by the training IQR of the score is used instead."""
    s = np.asarray(X[rule.col], float)
    th = np.array([rule.sign * rule.t1, rule.sign * rule.t2], float)
    if np.all(s > 0) and np.all(th > 0):
        d = np.abs(np.log10(s)[:, None] - np.log10(th)[None, :])
    else:
        d = np.abs(s[:, None] - th[None, :]) / max(getattr(rule, "iqr_", 1.0), 1e-12)
    return d.min(1)


class RMSGateBaseline:
    """Comparator: 2-threshold RMS rule + the IDENTICAL abstain gate used by the proposal.

    Stage 1 = AbstainGate.quality_ok (same SNR threshold, clip and flat limits).
    Stage 2 = confidence gate on rule_margin; tau is the (1 - target_cov) quantile of margins
    from INNER grouped k-fold on the training units (same recipe as the RF's tau).
    """

    def __init__(self, snr_min=None, target_cov=0.9, col="rms", inner_k=5, seed=0):
        self.col, self.inner_k, self.seed = col, inner_k, seed
        self.gate = AbstainGate(snr_min=snr_min, target_cov=target_cov)

    def fit(self, X, y, units=None):
        y = np.asarray(y)
        self.rule = ThresholdRule(self.col).fit(X, y)
        s = np.asarray(X[self.col], float)
        self.rule.iqr_ = float(np.subtract(*np.quantile(s, [0.75, 0.25])))
        if units is not None:
            from .splits import assert_no_leakage, grouped_kfold
            units = np.asarray(units)
            m_in = np.full(len(y), np.nan)
            for _, tr, te in grouped_kfold(units, k=self.inner_k, seed=self.seed):
                assert_no_leakage(units, tr, te)
                r = ThresholdRule(self.col).fit(X.iloc[tr], y[tr])
                r.iqr_ = self.rule.iqr_
                m_in[te] = rule_margin(r, X.iloc[te])
            self.gate.fit_conf(m_in)
        return self

    def predict(self, X):
        return self.rule.predict(X)

    def confidence(self, X):
        return rule_margin(self.rule, X)

    def decide(self, X):
        """Return (pred, confidence, accept_mask, reason 'ok' | 'sinyal' | 'ragu')."""
        pred, conf = self.predict(X), self.confidence(X)
        q = self.gate.quality_ok(X)
        c = conf >= self.gate.tau_conf
        reason = np.where(~q, "sinyal", np.where(~c, "ragu", "ok"))
        return pred, conf, q & c, reason


class RFPlusRuleFeature:
    """Experiment 2 (secondary): proposed RF (SPEC_COLS, which ALREADY contain raw `rms`) plus one
    extra feature = the RMS rule's ordinal decision (0/1/2). On training rows the feature is
    out-of-fold (inner grouped k-fold over training units) so the RF does not see a rule that was
    fitted on the same row; on new rows it comes from the rule fitted on all training units."""

    FEAT = "rms_rule_pred"

    def __init__(self, inner_k=5, seed=0):
        self.inner_k, self.seed = inner_k, seed

    def _with(self, X, col):
        Z = X.copy()
        Z[self.FEAT] = col
        return Z

    def fit(self, X, y, units):
        from .splits import assert_no_leakage, grouped_kfold
        y, units = np.asarray(y), np.asarray(units)
        oof = np.full(len(y), -1)
        for _, tr, te in grouped_kfold(units, k=self.inner_k, seed=self.seed):
            assert_no_leakage(units, tr, te)
            oof[te] = ThresholdRule("rms").fit(X.iloc[tr], y[tr]).predict(X.iloc[te])
        self.rule = ThresholdRule("rms").fit(X, y)
        self.rf = RFModel(SPEC_COLS + [self.FEAT]).fit(self._with(X, oof), y)
        return self

    def predict_proba(self, X):
        return self.rf.predict_proba(self._with(X, self.rule.predict(X)))

    def predict(self, X):
        return self.predict_proba(X).argmax(1)
