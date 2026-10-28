"""Spectral helpers adapted from FaceVitals.

Atribusi: fungsi `psd`, `spectral_snr`, `peak_frequency` dan `viterbi_track` di bawah ini
diadaptasi dari FaceVitals (c) Poggy Macello + Aziz,
`FaceVitals2027-SPCup_GAJADI-DAFTAR/facevitals/signal/quality.py` dan `facevitals/vitals/hr.py`.
Perubahan: pita default diganti dari pita detak jantung (0,6-4 Hz) ke pita mesin (frekuensi
poros 25-35 Hz untuk rig Ottawa), lebar jendela SNR dalam Hz dijadikan parameter, dan
`viterbi_track` bekerja dalam Hz (bukan bpm). Logika intinya (periodogram Hann + zero padding,
SNR de Haan & Jeanne fundamental+harmonik, interpolasi parabola, Viterbi dengan biaya lompatan
kuadratik) sama dengan aslinya. Folder FaceVitals tidak diubah.
"""

from __future__ import annotations

import numpy as np


def psd(x: np.ndarray, fs: float, nfft_min: int = 2048):
    """Hann-windowed periodogram with zero padding. Returns freqs, power. (FaceVitals)"""
    x = np.asarray(x, float)
    x = x - x.mean()
    n = len(x)
    nfft = max(nfft_min, 1 << int(np.ceil(np.log2(max(n, 2)))))
    X = np.fft.rfft(x * np.hanning(n), nfft)
    f = np.fft.rfftfreq(nfft, 1.0 / fs)
    return f, (np.abs(X) ** 2)


def spectral_snr(f: np.ndarray, P: np.ndarray, f0: float, band=(10.0, 200.0),
                 w1: float = 1.0, w2: float = 1.5, harmonic: bool = True) -> float:
    """SNR in dB: energy around f0 (and 2*f0) vs the rest of `band`. (FaceVitals, de Haan & Jeanne 2013)"""
    if not np.isfinite(f0):
        return -30.0
    inb = (f >= band[0]) & (f <= band[1])
    fund = np.abs(f - f0) <= w1
    harm = np.abs(f - 2 * f0) <= w2
    sig = inb & (fund | harm) if harmonic else inb & fund
    noise = inb & ~(fund | harm)
    ps, pn = P[sig].sum(), P[noise].sum()
    if ps <= 0 or pn <= 0:
        return -30.0
    return float(10 * np.log10(ps / pn))


def peak_frequency(f: np.ndarray, P: np.ndarray, band=(25.0, 35.0), local_max: bool = True) -> float:
    """Frequency of the strongest spectral peak in `band` (parabolic interpolation). (FaceVitals)"""
    m = (f >= band[0]) & (f <= band[1])
    if not m.any():
        return float("nan")
    idx = np.flatnonzero(m)
    i = idx[np.argmax(P[m])]
    if local_max:
        lm = idx[(idx > 0) & (idx < len(P) - 1)]
        lm = lm[(P[lm] >= P[lm - 1]) & (P[lm] >= P[lm + 1])]
        if len(lm):
            i = lm[np.argmax(P[lm])]
    if 0 < i < len(P) - 1:
        a, b, c = np.log(P[i - 1] + 1e-30), np.log(P[i] + 1e-30), np.log(P[i + 1] + 1e-30)
        den = a - 2 * b + c
        off = 0.5 * (a - c) / den if den != 0 else 0.0
        return float(f[i] + np.clip(off, -0.5, 0.5) * (f[1] - f[0]))
    return float(f[i])


def viterbi_track(spec: np.ndarray, freqs: np.ndarray, step_s: float, max_jump_hz_per_s: float,
                  penalty: float = 1.0, valid: np.ndarray | None = None) -> np.ndarray:
    """Most likely frequency path (Hz) through a (T, F) spectrogram. (FaceVitals, units Hz)"""
    T, F = spec.shape
    S = spec / (spec.max(axis=1, keepdims=True) + 1e-12)
    emis = -np.log(S + 1e-3)
    if valid is not None:
        emis[~valid] = 0.0
    df = freqs[1] - freqs[0]
    max_bins = max(1, int(np.ceil(max_jump_hz_per_s * step_s / df)))
    offs = np.arange(-max_bins, max_bins + 1)
    trans = penalty * (offs / max_bins) ** 2
    D = emis[0].copy()
    back = np.zeros((T, F), dtype=np.int32)
    for t in range(1, T):
        best = np.full(F, np.inf)
        arg = np.zeros(F, dtype=np.int32)
        for o, c in zip(offs, trans):
            src = np.arange(F) - o
            ok = (src >= 0) & (src < F)
            cand = np.full(F, np.inf)
            cand[ok] = D[src[ok]] + c
            better = cand < best
            best[better] = cand[better]
            arg[better] = src[better]
        D = best + emis[t]
        back[t] = arg
    path = np.zeros(T, dtype=np.int32)
    path[-1] = int(np.argmin(D))
    for t in range(T - 1, 0, -1):
        path[t - 1] = back[t, path[t]]
    return freqs[path]


def track_shaft(x: np.ndarray, fs: float, band=(25.0, 35.0), frame_s: float = 1.0,
                hop_s: float = 0.5, max_jump_hz_per_s: float = 2.0) -> np.ndarray:
    """Track the shaft-rotation line over a recording with the FaceVitals Viterbi tracker."""
    n, h = int(frame_s * fs), int(hop_s * fs)
    frames = [x[i:i + n] for i in range(0, max(len(x) - n + 1, 1), h)]
    rows = []
    for fr in frames:
        f, P = psd(fr, fs, nfft_min=1 << 17)
        m = (f >= band[0]) & (f <= band[1])
        rows.append(P[m])
    spec = np.array(rows)
    return viterbi_track(spec, f[m], hop_s, max_jump_hz_per_s)
