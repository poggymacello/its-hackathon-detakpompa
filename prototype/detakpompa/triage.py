"""Recording-level decisions and fleet triage queues (added 28 Okt 2026).

One "pump" = one recording. Every recording gets ONE of four queues:

  AUDIT DULU  the k highest-priority recordings among those the model ANSWERED with status
              WASPADA or RUSAK (k = audit capacity per round, default 3 = Lean Canvas KPI)
  PANTAU      answered WASPADA/RUSAK beyond the audit capacity (next round)
  UKUR ULANG  every TIDAK TAHU (signal gate failed, too short, or model unsure). These
              recordings are NEVER ranked into AUDIT DULU and signal-gated ones get NO priority
              at all: a loose sensor must not outrank a pump that is really broken.
  AMAN        answered SEHAT (until the next routine recording)

Two decision makers share the SAME signal gate (AbstainGate.quality_ok, SNR >= CFAR threshold,
no clipping, not flat) and the SAME recording rule (>= MIN_OK_SHARE of the windows must pass):
  - proposal  : RF on spectral features; priority = 0.5 * P(waspada) + P(rusak)
  - rms_gate  : 2-threshold RMS rule; priority/ranking score = sign * log10(median RMS)
Both confidence thresholds (tau) come from inner grouped 5-fold CV on the TRAINING units only,
at recording level, target coverage 90 %.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .models import ThresholdRule, proposed_rf, rule_margin
from .splits import assert_no_leakage, grouped_kfold

MIN_OK_SHARE = 0.5      # at least half of the windows must pass the signal gate
TARGET_COV = 0.9        # recording-level confidence threshold: 90 % coverage on inner CV
QUEUES = ("AUDIT DULU", "PANTAU", "UKUR ULANG", "AMAN")
NO_PRIORITY_REASONS = ("sinyal", "pendek")   # signal could not be trusted -> no priority at all


def _tau(conf, target_cov=TARGET_COV):
    return float(np.quantile(np.asarray(conf, float), 1 - target_cov))


# ------------------------------------------------------------------------------------------
# proposal (RF)
# ------------------------------------------------------------------------------------------

def fit_proposal(F: pd.DataFrame, target_cov: float = TARGET_COV):
    """RF on all rows of F + recording-level tau from inner grouped 5-fold on F's units."""
    y, units = F["state"].to_numpy(), F["unit"].to_numpy()
    model = proposed_rf().fit(F, y)
    P = np.zeros((len(F), 3))
    for _, tr, te in grouped_kfold(units, k=5, seed=0):
        assert_no_leakage(units, tr, te)
        P[te] = proposed_rf().fit(F.iloc[tr], y[tr]).predict_proba(F.iloc[te])
    rec = F["recording"].to_numpy()
    conf = [P[rec == r].mean(0).max() for r in pd.unique(rec)]
    return model, _tau(conf, target_cov)


def priority_from_proba(p) -> float:
    return float(0.5 * p[1] + p[2])


def decide_proposal(ok: np.ndarray, P: np.ndarray, tau: float) -> dict:
    """Recording-level decision from window gate mask `ok` and window probabilities `P`."""
    ok = np.asarray(ok, bool)
    use = ok if ok.any() else np.ones(len(ok), bool)
    p = np.asarray(P)[use].mean(0)
    d = {"proba": p.tolist(), "n_windows": int(len(ok)), "n_ok": int(ok.sum()), "conf": float(p.max())}
    if ok.mean() < MIN_OK_SHARE:
        d.update(status=-1, abstain_reason="sinyal", priority=None, priority_provisional=None)
    elif p.max() < tau:
        # unsure: a provisional priority is shown (marked "ragu") but it is NOT used for ranking
        d.update(status=-1, abstain_reason="ragu", priority=None,
                 priority_provisional=priority_from_proba(p))
    else:
        d.update(status=int(p.argmax()), abstain_reason=None, priority=priority_from_proba(p),
                 priority_provisional=None)
    return d


# ------------------------------------------------------------------------------------------
# comparator: RMS rule + the same signal gate, at recording level
# ------------------------------------------------------------------------------------------

def _rec_median(X: pd.DataFrame, col: str, mask=None) -> pd.DataFrame:
    """One-row frame with the median of `col` over the (masked) windows."""
    v = np.asarray(X[col], float)
    if mask is not None and np.asarray(mask).any():
        v = v[np.asarray(mask, bool)]
    return pd.DataFrame({col: [float(np.median(v))]})


class RMSRecordingTriage:
    """2-threshold RMS rule (thresholds from training WINDOWS, same as models.ThresholdRule) applied
    to the recording's median RMS over gate-passing windows. Confidence = models.rule_margin
    (log10 distance to the nearest threshold, fixed before the rmsgate experiment). tau = 10 %
    quantile of recording-level margins from inner grouped 5-fold on the training units."""

    def __init__(self, col: str = "rms", target_cov: float = TARGET_COV):
        self.col, self.target_cov = col, target_cov

    def fit(self, F: pd.DataFrame):
        y, units = F["state"].to_numpy(), F["unit"].to_numpy()
        self.rule = ThresholdRule(self.col).fit(F, y)
        rec = F["recording"].to_numpy()
        conf = []
        for _, tr, te in grouped_kfold(units, k=5, seed=0):
            assert_no_leakage(units, tr, te)
            r = ThresholdRule(self.col).fit(F.iloc[tr], y[tr])
            Fte = F.iloc[te]
            for name in pd.unique(rec[te]):
                conf.append(float(rule_margin(r, _rec_median(Fte[rec[te] == name], self.col))[0]))
        self.tau = _tau(conf, self.target_cov)
        return self

    def score(self, med: pd.DataFrame) -> float:
        """Severity score used for ranking: sign * log10(median RMS) (ordinal with the rule)."""
        v = float(med[self.col].iloc[0])
        return float(self.rule.sign * (np.log10(v) if v > 0 else v))

    def decide(self, X: pd.DataFrame, ok: np.ndarray) -> dict:
        ok = np.asarray(ok, bool)
        med = _rec_median(X, self.col, ok if ok.any() else None)
        pred = int(self.rule.predict(med)[0])
        conf = float(rule_margin(self.rule, med)[0])
        s = self.score(med)
        d = {"pred_rule": pred, "conf": conf, "n_windows": int(len(ok)), "n_ok": int(ok.sum()),
             "rms_median": float(med[self.col].iloc[0])}
        if ok.mean() < MIN_OK_SHARE:
            d.update(status=-1, abstain_reason="sinyal", priority=None, priority_provisional=None)
        elif conf < self.tau:
            d.update(status=-1, abstain_reason="ragu", priority=None, priority_provisional=s)
        else:
            d.update(status=pred, abstain_reason=None, priority=s, priority_provisional=None)
        return d


# ------------------------------------------------------------------------------------------
# fleet queues + top-k precision
# ------------------------------------------------------------------------------------------

def assign_queues(rows: list[dict], k: int = 3) -> list[dict]:
    """rows: dicts with at least 'name', 'status', 'priority'. Returns new dicts with 'queue' and
    'rank' (1..k for AUDIT DULU, continuing for PANTAU; None elsewhere), ordered by queue then rank.
    Ties in priority are broken by name (deterministic)."""
    flagged = [r for r in rows if r["status"] in (1, 2) and r.get("priority") is not None]
    flagged.sort(key=lambda r: (-r["priority"], str(r["name"])))
    out = []
    for i, r in enumerate(flagged):
        out.append({**r, "queue": QUEUES[0] if i < k else QUEUES[1], "rank": i + 1})
    rest = [r for r in rows if r not in flagged]
    for r in sorted(rest, key=lambda r: str(r["name"])):
        if r["status"] == -1:
            out.append({**r, "queue": QUEUES[2], "rank": None})
        elif r["status"] == 0:
            out.append({**r, "queue": QUEUES[3], "rank": None})
        else:  # flagged but without a priority cannot happen for answered rows; keep it visible
            out.append({**r, "queue": QUEUES[2], "rank": None})
    order = {q: i for i, q in enumerate(QUEUES)}
    out.sort(key=lambda r: (order[r["queue"]], r["rank"] if r["rank"] is not None else 0, str(r["name"])))
    return out


def topk_metrics(queued: list[dict], labels: dict, k: int = 3) -> dict:
    """labels: name -> true state (0/1/2). Precision is over the AUDIT DULU list (<= k items).
    perlu_cek = state >= 1; rusak = state == 2."""
    audit = [r for r in queued if r["queue"] == QUEUES[0]][:k]
    y = np.array([labels[r["name"]] for r in audit], int)
    fault = [r for r in queued if labels[r["name"]] >= 1]
    n_fault = max(len(fault), 1)
    return {
        "n_audit": int(len(audit)),
        "prec_perlu_cek": float(np.mean(y >= 1)) if len(y) else float("nan"),
        "prec_rusak": float(np.mean(y == 2)) if len(y) else float("nan"),
        "n_sehat_in_audit": int(np.sum(y == 0)),
        "fault_to_ukur_ulang": float(sum(r["queue"] == QUEUES[2] for r in fault) / n_fault),
        "fault_to_aman": float(sum(r["queue"] == QUEUES[3] for r in fault) / n_fault),
    }


def queue_single(status: int) -> str:
    """Queue for a single-recording report (no fleet, so no audit capacity): TIDAK TAHU ->
    UKUR ULANG, SEHAT -> AMAN, WASPADA/RUSAK -> AUDIT DULU candidate (order: triase.py)."""
    if status == -1:
        return QUEUES[2]
    if status == 0:
        return QUEUES[3]
    return "KANDIDAT AUDIT"
