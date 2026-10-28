"""Mode "deviasi dari baseline unit sendiri" (per-unit anomaly score).

No cross-unit training at all: each unit is compared only with its OWN healthy reference
windows (e.g. recorded at commissioning). Score = RMS of z-scores over a fixed set of
log-scaled features. The std of each feature is floored at FLOOR (log10 units, ~12 %) so a
short reference does not produce huge z-scores.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .features import SPEC_BANDS

FLOOR = 0.05
DEV_COLS = ["rms", "peak", "kurt", "crest", "centroid", "env_prom_db", "env_kurt"] + \
    [f"band_{lo}_{hi}" for lo, hi in SPEC_BANDS]


def transform(X: pd.DataFrame) -> np.ndarray:
    out = []
    for c in DEV_COLS:
        v = np.asarray(X[c], float)
        if c in ("rms", "peak", "crest", "centroid"):
            v = np.log10(np.maximum(v, 1e-12))
        elif c in ("kurt", "env_kurt"):
            v = np.log10(np.maximum(v + 3.0, 1e-3))
        elif c == "env_prom_db":
            v = v / 10.0
        out.append(v)
    return np.stack(out, 1)


class UnitBaseline:
    def fit(self, X_ref: pd.DataFrame):
        Z = transform(X_ref)
        self.mu = Z.mean(0)
        self.sd = np.maximum(Z.std(0, ddof=1) if len(Z) > 1 else np.zeros(Z.shape[1]), FLOOR)
        return self

    def zscores(self, X: pd.DataFrame) -> np.ndarray:
        return (transform(X) - self.mu) / self.sd

    def score(self, X: pd.DataFrame) -> np.ndarray:
        return np.sqrt(np.mean(self.zscores(X) ** 2, 1))

    def rms_only(self, X: pd.DataFrame) -> np.ndarray:
        return np.abs(self.zscores(X)[:, 0])

    def top_features(self, X: pd.DataFrame, k: int = 3):
        z = np.mean(self.zscores(X), 0)
        order = np.argsort(-np.abs(z))[:k]
        return [(DEV_COLS[i], float(z[i])) for i in order]
