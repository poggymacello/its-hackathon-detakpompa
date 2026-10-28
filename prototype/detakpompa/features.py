"""Window-level features.

Groups:
  STAT  - simple time-domain statistics (baseline c, random forest)
  ENV   - classical envelope analysis + kurtosis (baseline b)
  SPEC  - spectral features incl. FaceVitals-style shaft-line tracking (proposed)
  QUAL  - signal-quality indices used ONLY by the abstain gate (shaft-line SNR, clipping)
"""

from __future__ import annotations

import numpy as np
from scipy.signal import butter, hilbert, sosfiltfilt
from scipy.stats import kurtosis, skew

from .spectral import peak_frequency, psd, spectral_snr

SHAFT_BAND = (15.0, 35.0)       # rig runs ~29.8 Hz (units 1-15, 20) and ~19.5 Hz (units 16-19), see data_survey.txt
ENV_BAND = (2000.0, 10000.0)    # fixed demodulation band (geometry-free; bearing geometry not used)
SPEC_BANDS = [(10, 100), (100, 300), (300, 1000), (1000, 2000), (2000, 4000),
              (4000, 8000), (8000, 12000), (12000, 16000), (16000, 20000)]

STAT_COLS = ["rms", "std", "peak", "p2p", "crest", "kurt", "skew", "shape", "impulse", "margin"]
ENV_COLS = ["kurt", "env_prom_db", "env_kurt"]
SPEC_ONLY_COLS = ([f"band_{lo}_{hi}" for lo, hi in SPEC_BANDS] +
                  ["centroid", "spread", "flatness", "entropy",
                   "shaft_hz", "shaft_snr_db", "shaft_snr_fv_db", "h1_rel", "h2_rel", "h3_rel",
                   "env_prom_db", "env_kurt", "env_peak_order", "env_harm_frac"])
SPEC_COLS = STAT_COLS + [c for c in SPEC_ONLY_COLS if c not in STAT_COLS]
QUAL_COLS = ["shaft_snr_db", "clip_frac", "flat_frac"]


def _highpass(x, fs, fc=10.0):
    sos = butter(4, fc, "highpass", fs=fs, output="sos")
    return sosfiltfilt(sos, x)


def stat_features(x: np.ndarray) -> dict:
    a = np.abs(x)
    rms = float(np.sqrt(np.mean(x ** 2))) + 1e-12
    peak = float(a.max()) + 1e-12
    mean_abs = float(a.mean()) + 1e-12
    return {
        "rms": rms, "std": float(x.std()), "peak": peak, "p2p": float(x.max() - x.min()),
        "crest": peak / rms, "kurt": float(kurtosis(x)), "skew": float(skew(x)),
        "shape": rms / mean_abs, "impulse": peak / mean_abs,
        "margin": peak / (float(np.mean(np.sqrt(a))) ** 2 + 1e-12),
    }


def envelope_features(x: np.ndarray, fs: float, shaft_hz: float | None = None) -> dict:
    hi = min(ENV_BAND[1], 0.45 * fs)
    sos = butter(4, [ENV_BAND[0], hi], "bandpass", fs=fs, output="sos")
    xb = sosfiltfilt(sos, x)
    env = np.abs(hilbert(xb))
    env = env - env.mean()
    f, P = psd(env, fs, nfft_min=1 << 16)
    m = (f >= 10) & (f <= 500)
    Pm, fm = P[m], f[m]
    i = int(np.argmax(Pm))
    prom = float(10 * np.log10(Pm[i] / (np.median(Pm) + 1e-30) + 1e-30))
    fpk = float(fm[i])
    # fraction of envelope-band energy in the first 5 harmonics of the top envelope line
    harm = np.zeros_like(fm, bool)
    for k in range(1, 6):
        harm |= np.abs(fm - k * fpk) <= 1.5
    out = {"env_prom_db": prom, "env_kurt": float(kurtosis(env)),
           "env_harm_frac": float(Pm[harm].sum() / (Pm.sum() + 1e-30))}
    out["env_peak_order"] = float(fpk / shaft_hz) if shaft_hz and np.isfinite(shaft_hz) else np.nan
    return out


def line_prominence_db(f, P, f0, half=10.0, excl=2.5):
    """Local SNR of a spectral line: peak power within +-1 Hz of f0 over the median power of the
    surrounding +-`half` Hz (excluding +-`excl` Hz). White noise gives ~4-11 dB; a clearly visible
    machine line gives 20-45 dB (results/data_survey.txt, README)."""
    if not np.isfinite(f0):
        return 0.0
    m = np.abs(f - f0) <= 1.0
    n = (np.abs(f - f0) <= half) & (np.abs(f - f0) > excl)
    if not m.any() or not n.any():
        return 0.0
    return float(10 * np.log10(P[m].max() / (np.median(P[n]) + 1e-30) + 1e-30))


def spectral_features(x: np.ndarray, fs: float, f0: float | None = None) -> dict:
    f, P = psd(x, fs, nfft_min=1 << 17)
    tot = P[(f >= 10) & (f <= 0.5 * fs)].sum() + 1e-30
    out = {}
    for lo, hi in SPEC_BANDS:
        m = (f >= lo) & (f < min(hi, 0.5 * fs))
        out[f"band_{lo}_{hi}"] = float(np.log10(P[m].sum() / tot + 1e-12))
    m = (f >= 10) & (f <= 0.5 * fs)
    fm, Pm = f[m], P[m]
    p = Pm / Pm.sum()
    cen = float((fm * p).sum())
    out["centroid"] = cen
    out["spread"] = float(np.sqrt(((fm - cen) ** 2 * p).sum()))
    out["flatness"] = float(np.exp(np.mean(np.log(Pm + 1e-30))) / (Pm.mean() + 1e-30))
    out["entropy"] = float(-(p * np.log(p + 1e-30)).sum() / np.log(len(p)))
    # FaceVitals-style shaft-line estimation + SNR (fundamental + 2nd harmonic vs rest of 10-200 Hz)
    if f0 is None or not np.isfinite(f0):
        f0 = peak_frequency(f, P, SHAFT_BAND, local_max=True)
    out["shaft_hz"] = f0
    out["shaft_snr_db"] = line_prominence_db(f, P, f0)
    out["shaft_snr_fv_db"] = spectral_snr(f, P, f0, band=(10.0, 200.0), w1=2.0, w2=2.5)
    low = P[(f >= 10) & (f <= 1000)].sum() + 1e-30
    for k in (1, 2, 3):
        mk = np.abs(f - k * f0) <= 1.0
        out[f"h{k}_rel"] = float(np.log10(P[mk].sum() / low + 1e-12))
    return out


def quality_features(x_raw: np.ndarray, x: np.ndarray, spec: dict) -> dict:
    """Clipping = share of samples at the extreme value; flat = share of zero first differences."""
    a = np.abs(x_raw - np.median(x_raw))
    mx = a.max()
    clip = float(np.mean(a >= 0.999 * mx)) if mx > 0 else 1.0
    flat = float(np.mean(np.diff(x_raw) == 0))
    return {"shaft_snr_db": spec["shaft_snr_db"], "clip_frac": clip, "flat_frac": flat}


def window_features(x_raw: np.ndarray, fs: float, f0: float | None = None) -> dict:
    """f0 = shaft frequency from the recording-level tracker (None -> per-window peak)."""
    x = _highpass(np.asarray(x_raw, float) - np.mean(x_raw), fs)
    st = stat_features(x)
    sp = spectral_features(x, fs, f0)
    en = envelope_features(x, fs, sp["shaft_hz"])
    q = quality_features(np.asarray(x_raw, float), x, sp)
    out = {}
    out.update(st); out.update(sp); out.update(en)
    out["clip_frac"], out["flat_frac"] = q["clip_frac"], q["flat_frac"]
    return out
