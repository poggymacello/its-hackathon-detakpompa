"""Tests for the priority fix (gated recordings get no priority -> UKUR ULANG) and fleet triage."""

import os

import numpy as np
import pandas as pd
import pytest

import demo
import triase
from conftest import DATA, FEATURES
from detakpompa.report import format_report
from detakpompa.triage import QUEUES, RMSRecordingTriage, assign_queues, decide_proposal, topk_metrics

needs_feat = pytest.mark.skipif(not os.path.exists(FEATURES), reason="run run_eval.py first")


def test_signal_gated_decision_has_no_priority():
    ok = np.array([True, False, False, False])            # 1/4 windows pass < MIN_OK_SHARE
    P = np.tile([0.01, 0.25, 0.74], (4, 1))                # model would say "rusak", confidently
    d = decide_proposal(ok, P, tau=0.4)
    assert d["status"] == -1 and d["abstain_reason"] == "sinyal"
    assert d["priority"] is None and d["priority_provisional"] is None


def test_unsure_decision_keeps_only_provisional_priority():
    ok = np.ones(4, bool)
    P = np.tile([0.36, 0.32, 0.33], (4, 1))
    d = decide_proposal(ok, P, tau=0.49)
    assert d["status"] == -1 and d["abstain_reason"] == "ragu"
    assert d["priority"] is None and d["priority_provisional"] == pytest.approx(0.5 * 0.32 + 0.33)


def test_gated_never_outranks_assessed_pump():
    rows = [
        {"name": "lepas", "status": -1, "priority": None},          # loose sensor (was 0.87 before fix)
        {"name": "ragu", "status": -1, "priority": None},
        {"name": "rusakA", "status": 2, "priority": 0.80},
        {"name": "waspB", "status": 1, "priority": 0.40},
        {"name": "rusakC", "status": 2, "priority": 0.90},
        {"name": "rusakD", "status": 2, "priority": 0.70},
        {"name": "sehat", "status": 0, "priority": 0.02},
    ]
    q = {r["name"]: r for r in assign_queues(rows, k=3)}
    assert [n for n in q if q[n]["queue"] == QUEUES[0]] == ["rusakC", "rusakA", "rusakD"]
    assert q["waspB"]["queue"] == QUEUES[1] and q["waspB"]["rank"] == 4
    assert q["lepas"]["queue"] == QUEUES[2] and q["lepas"]["rank"] is None
    assert q["ragu"]["queue"] == QUEUES[2]
    assert q["sehat"]["queue"] == QUEUES[3]


def test_topk_metrics():
    rows = [{"name": n, "status": s, "priority": p} for n, s, p in
            [("a", 2, 0.9), ("b", 1, 0.8), ("c", 2, 0.7), ("d", 1, 0.6), ("e", -1, None), ("f", 0, 0.0)]]
    lab = {"a": 2, "b": 0, "c": 1, "d": 2, "e": 2, "f": 1}
    m = topk_metrics(assign_queues(rows, k=3), lab, k=3)
    assert m["n_audit"] == 3 and m["prec_perlu_cek"] == pytest.approx(2 / 3)
    assert m["prec_rusak"] == pytest.approx(1 / 3) and m["n_sehat_in_audit"] == 1
    assert m["fault_to_ukur_ulang"] == pytest.approx(1 / 5) and m["fault_to_aman"] == pytest.approx(1 / 5)


def test_report_gated_prints_no_priority_number():
    r = {"file": "x.npy", "duration_s": 10.0, "n_windows": 10, "fs": 42000, "status": -1,
         "abstain_reason": "sinyal", "abstain_reason_text": "SNR rendah", "next_step": "Ukur ulang 30 detik",
         "priority": None, "priority_provisional": None, "queue": QUEUES[2], "proba": [0.01, 0.25, 0.74],
         "tau_conf": 0.49, "snr_db": 4.5, "snr_min": 11.5, "shaft_hz": 34.1, "n_ok": 2, "top_features": []}
    txt = format_report(r)
    line = [s for s in txt.splitlines() if s.startswith("Prioritas cek")][0]
    assert "UKUR ULANG" in line and "0.87" not in line and not any(ch.isdigit() for ch in line)
    assert "Antrean      : UKUR ULANG" in txt and "TIDAK DIPAKAI" in txt


def test_rms_recording_triage_toy():
    rng = np.random.default_rng(0)
    rows = []
    for u in range(1, 9):
        for k, lv in enumerate((1.0, 3.0, 9.0)):
            for w in range(6):
                rows.append({"recording": f"r{u}_{k}", "unit": u, "state": k,
                             "rms": lv * np.exp(rng.normal(0, 0.1)), "shaft_snr_db": 30.0,
                             "clip_frac": 0.0, "flat_frac": 0.0})
    F = pd.DataFrame(rows)
    m = RMSRecordingTriage().fit(F[F.unit != 1])
    X = F[F.recording == "r1_2"].reset_index(drop=True)
    d = m.decide(X, np.ones(len(X), bool))
    assert d["pred_rule"] == 2 and d["abstain_reason"] in (None, "ragu")
    assert (d["status"] == 2) == (d["priority"] is not None)       # only answered rows are ranked
    assert d["abstain_reason"] is not None or d["priority_provisional"] is None
    d2 = m.decide(X, np.zeros(len(X), bool))                     # gate fails -> no priority
    assert d2["status"] == -1 and d2["abstain_reason"] == "sinyal" and d2["priority"] is None


def test_unit_hint():
    assert triase.unit_hint("x/I_3_1.mat") == (3, 1)
    assert triase.unit_hint("I_3_1_derau_-10dB.npy") == (3, 1)
    assert triase.unit_hint("sensor_lepas.npy") == (None, None)
    assert triase.unit_hint("H_12_0.csv") == (12, 0)


@needs_feat
def test_demo_noise_gets_no_priority_and_ukur_ulang(tmp_path):
    p = tmp_path / "lepas.npy"
    np.save(p, np.random.default_rng(0).normal(size=10 * 42000))
    r = demo.analyse(str(p))
    assert r["abstain_reason"] == "sinyal" and r["priority"] is None and r["queue"] == QUEUES[2]


@needs_feat
@pytest.mark.skipif(not os.path.isdir(DATA), reason="dataset not downloaded")
def test_triase_folder_end_to_end(tmp_path):
    noise = tmp_path / "sensor_lepas.npy"
    np.save(noise, np.random.default_rng(1).normal(size=10 * 42000))
    files = [os.path.join(DATA, f) for f in ("H_3_0.mat", "I_3_1.mat", "C_16_2.mat")] + [str(noise)]
    q = triase.run(files, k=3)
    by = {r["name"]: r for r in q}
    assert by["sensor_lepas"]["queue"] == QUEUES[2] and by["sensor_lepas"]["priority"] is None
    for r in q:                                  # every TIDAK TAHU is in UKUR ULANG, never AUDIT DULU
        assert (r["status"] == -1) == (r["queue"] == QUEUES[2])
        assert r["alasan"] and r["langkah"]
    # one model per held-out bearing; bearing 3 never in its own training set
    cache = triase.ModelCache(pd.read_csv(FEATURES))
    assert 3 not in cache.get(3)[3] and len(cache.get(3)[3]) == 19
