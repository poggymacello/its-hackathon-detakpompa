import numpy as np
import pandas as pd

from detakpompa.models import AbstainGate
from detakpompa.pipeline import features_for_signal, snr_cfar_threshold

FS = 42000


def _machine(secs=3, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(secs * FS) / FS
    return np.sin(2 * np.pi * 29.7 * t) + 0.05 * rng.normal(size=len(t))


def test_cfar_threshold_reasonable():
    thr = snr_cfar_threshold(float(FS), n_rec=5)
    assert 5 < thr < 20


def test_gate_accepts_machine_rejects_noise():
    gate = AbstainGate(snr_min=snr_cfar_threshold(float(FS), n_rec=5))
    Xm = features_for_signal(_machine(), FS)
    Xn = features_for_signal(np.random.default_rng(5).normal(size=3 * FS), FS)
    assert gate.quality_ok(Xm).all()
    assert gate.quality_ok(Xn).mean() < 0.5


def test_gate_rejects_clipping():
    x = np.clip(_machine() * 5, -1, 1)
    gate = AbstainGate(snr_min=0)
    assert not gate.quality_ok(features_for_signal(x, FS)).any()


def test_confidence_gate_and_reasons():
    gate = AbstainGate(snr_min=-1e9, target_cov=0.9).fit_conf(np.linspace(0.3, 1.0, 101))
    assert abs(gate.tau_conf - 0.37) < 0.01
    X = pd.DataFrame({"shaft_snr_db": [30, 30, -1e10], "clip_frac": [0, 0, 0], "flat_frac": [0, 0, 0]})
    P = np.array([[0.9, 0.05, 0.05], [0.34, 0.33, 0.33], [0.9, 0.05, 0.05]])
    acc, why = gate.decide(X, P)
    assert acc.tolist() == [True, False, False]
    assert why.tolist() == ["ok", "ragu", "sinyal"]
