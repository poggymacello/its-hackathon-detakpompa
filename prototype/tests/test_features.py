import numpy as np

from detakpompa.features import envelope_features, line_prominence_db, stat_features, window_features
from detakpompa.pipeline import features_for_signal, track_windows
from detakpompa.spectral import psd

FS = 42000


def _machine(f0=29.7, secs=1.0, noise=0.05, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(int(secs * FS)) / FS
    return np.sin(2 * np.pi * f0 * t) + 0.3 * np.sin(2 * np.pi * 2 * f0 * t) + noise * rng.normal(size=len(t))


def test_shaft_peak_and_snr():
    d = window_features(_machine(), FS)
    assert abs(d["shaft_hz"] - 29.7) < 0.3
    assert d["shaft_snr_db"] > 20


def test_noise_has_low_line_snr():
    rng = np.random.default_rng(1)
    vals = [window_features(rng.normal(size=FS), FS)["shaft_snr_db"] for _ in range(10)]
    assert np.median(vals) < 12


def test_kurtosis_impulsive():
    rng = np.random.default_rng(2)
    x = rng.normal(size=FS)
    x[::4200] += 40
    assert stat_features(x)["kurt"] > 10
    assert abs(stat_features(rng.normal(size=FS))["kurt"]) < 0.5


def test_envelope_finds_repetition_rate():
    t = np.arange(FS) / FS
    carrier = np.sin(2 * np.pi * 5000 * t)
    bursts = (np.sin(2 * np.pi * 107 * t) > 0.95).astype(float)
    x = carrier * bursts + 0.01 * np.random.default_rng(3).normal(size=FS)
    e = envelope_features(x, FS, shaft_hz=29.7)
    assert abs(e["env_peak_order"] * 29.7 - 107) < 2
    assert e["env_prom_db"] > 15


def test_viterbi_tracks_slow_drift():
    f_true = np.linspace(19.5, 21.0, 10)
    ws = [_machine(f, noise=0.5, seed=i) for i, f in enumerate(f_true)]
    tr = track_windows(ws, FS)
    assert np.max(np.abs(tr - f_true)) < 0.6


def test_features_for_signal_shape():
    X = features_for_signal(np.concatenate([_machine(seed=i) for i in range(3)]), FS)
    assert len(X) == 3 and "shaft_snr_db" in X and X["window"].tolist() == [0, 1, 2]


def test_line_prominence_nan_safe():
    f, P = psd(np.ones(100), 100.0)
    assert line_prominence_db(f, P, float("nan")) == 0.0
