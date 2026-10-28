"""Glue: recording -> window feature table."""

from __future__ import annotations

import numpy as np
import pandas as pd

from functools import lru_cache

from .features import SHAFT_BAND, _highpass, window_features
from .io import list_dataset, load_recording, windows
from .spectral import psd, viterbi_track


def track_windows(ws, fs, band=SHAFT_BAND, max_jump_hz_per_s=1.0, win_s=1.0):
    """FaceVitals Viterbi tracker over the 1 s windows of one recording -> shaft Hz per window."""
    rows = []
    for w in ws:
        f, P = psd(_highpass(w - w.mean(), fs), fs, nfft_min=1 << 17)
        m = (f >= band[0]) & (f <= band[1])
        rows.append(P[m])
    if not rows:
        return np.array([])
    return viterbi_track(np.array(rows), f[m], win_s, max_jump_hz_per_s)


def features_for_signal(x: np.ndarray, fs: float, win_s: float = 1.0, track: bool = True) -> pd.DataFrame:
    ws = windows(x, fs, win_s)
    f0s = track_windows(ws, fs, win_s=win_s) if (track and len(ws) > 1) else [None] * len(ws)
    rows = []
    for i, (w, f0) in enumerate(zip(ws, f0s)):
        d = window_features(w, fs, None if f0 is None else float(f0))
        d["window"] = i
        rows.append(d)
    return pd.DataFrame(rows)


@lru_cache(maxsize=8)
def snr_cfar_threshold(fs: float, win_s: float = 1.0, pfa: float = 0.01, n_rec: int = 30, seed: int = 7) -> float:
    """SNR-gate threshold that does NOT look at any dataset label or test data: the (1 - pfa)
    quantile of the shaft-line SNR measured by the same pipeline on pure white Gaussian noise
    (a "sensor not coupled to the machine" signal). A real line must beat noise at false-alarm 1 %."""
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_rec):
        z = rng.normal(0, 1, int(10 * win_s * fs))
        vals.extend(features_for_signal(z, fs, win_s)["shaft_snr_db"].tolist())
    return float(np.quantile(vals, 1 - pfa))


def build_feature_table(root: str, win_s: float = 1.0) -> pd.DataFrame:
    parts = []
    for path, info in list_dataset(root):
        x, fs = load_recording(path)
        df = features_for_signal(x, fs, win_s)
        df.insert(0, "recording", info.name)
        df.insert(1, "unit", info.unit)
        df.insert(2, "state", info.state)
        df.insert(3, "ftype", info.ftype)
        parts.append(df)
    return pd.concat(parts, ignore_index=True)
