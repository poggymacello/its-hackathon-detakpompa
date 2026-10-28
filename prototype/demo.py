"""DetakPompa demo: one vibration recording -> "laporan kesehatan pompa" (triage report).

Usage (from prototype/, after run_eval.py has produced results/features.csv):
    .venv\\Scripts\\python.exe -I demo.py data\\ottawa_uored_vafcls\\mat\\I_3_1.mat
    .venv\\Scripts\\python.exe -I demo.py rekaman.csv --fs 42000 --baseline rekaman_sehat.csv
    .venv\\Scripts\\python.exe -I demo.py rekaman.mat --out results\\demo\\laporan.txt

If the input is an Ottawa file (name like I_3_1), ALL recordings of that bearing are removed
from the training table before fitting, so the demo never sees its own unit (no leakage).
"""

from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from detakpompa.deviation import UnitBaseline  # noqa: E402
from detakpompa.io import load_recording, parse_name  # noqa: E402
from detakpompa.models import AbstainGate  # noqa: E402
from detakpompa.pipeline import features_for_signal, snr_cfar_threshold  # noqa: E402
from detakpompa.report import NEXT_STEP, format_report  # noqa: E402
from detakpompa.triage import TARGET_COV, decide_proposal, fit_proposal, queue_single  # noqa: E402

FEATURES = os.path.join(HERE, "results", "features.csv")


def fit_model(F: pd.DataFrame):
    """RF + recording-level confidence threshold from inner grouped CV on the training units only."""
    return fit_proposal(F, TARGET_COV)


def analyse(path: str, fs: float | None = None, channel: int = 0, baseline: str | None = None,
            features_csv: str = FEATURES) -> dict:
    x, fs = load_recording(path, channel=channel, fs=fs)
    F = pd.read_csv(features_csv)
    info = parse_name(path)
    unit_note = None
    if info is not None and info.unit in set(F["unit"]):
        F = F[F["unit"] != info.unit].reset_index(drop=True)
        unit_note = (f"berkas dikenali sebagai bearing #{info.unit} dataset Ottawa; semua rekaman unit itu "
                     f"DIKELUARKAN dari data latih (anti-bocor). Label asli: state {info.state} (tidak dipakai model).")
    model, tau = fit_model(F)
    snr_min = snr_cfar_threshold(float(fs))
    gate = AbstainGate(snr_min=snr_min)
    gate.tau_conf = tau
    r = {"file": path, "unit_note": unit_note, "fs": fs, "duration_s": len(x) / fs,
         "tau_conf": tau, "snr_min": snr_min, "deviation": None}
    if len(x) < 2 * fs:
        r.update({"status": -1, "abstain_reason": "pendek", "abstain_reason_text": "rekaman < 2 s",
                  "next_step": NEXT_STEP["pendek"], "proba": [np.nan] * 3, "priority": None,
                  "priority_provisional": None, "queue": queue_single(-1),
                  "snr_db": float("nan"), "shaft_hz": float("nan"), "n_ok": 0, "n_windows": 0,
                  "top_features": []})
        return r
    X = features_for_signal(x, fs)
    ok = gate.quality_ok(X)
    P = model.predict_proba(X)
    use = ok if ok.any() else np.ones(len(X), bool)
    d = decide_proposal(ok, P, tau)
    p = np.asarray(d["proba"])
    r.update({"n_windows": d["n_windows"], "n_ok": d["n_ok"], "proba": d["proba"],
              "status": d["status"], "abstain_reason": d["abstain_reason"],
              # signal-gated recordings get NO priority (None): they go to the UKUR ULANG queue and
              # are never ranked above a pump that was actually assessed (fix 28 Okt 2026)
              "priority": d["priority"], "priority_provisional": d["priority_provisional"],
              "queue": queue_single(d["status"]),
              "snr_db": float(np.median(X["shaft_snr_db"])), "shaft_hz": float(np.median(X["shaft_hz"][use]))})
    if d["abstain_reason"] == "sinyal":
        r.update({"abstain_reason_text": (f"garis putaran poros tidak terlihat jelas di atas derau "
                                          f"({int(ok.sum())}/{len(X)} jendela lolos; SNR median "
                                          f"{r['snr_db']:.1f} dB < ambang {snr_min:.1f} dB, atau sinyal terpotong/datar)"),
                  "next_step": NEXT_STEP["sinyal"]})
    elif d["abstain_reason"] == "ragu":
        r.update({"abstain_reason_text": f"model ragu: probabilitas tertinggi {p.max():.2f} < ambang {tau:.2f}",
                  "next_step": NEXT_STEP["ragu"]})
    # dominant features: top-3 RF importances, value vs median of healthy training windows
    imp = model.clf.feature_importances_
    top = np.argsort(-imp)[:3]
    healthy = F[F["state"] == 0]
    r["top_features"] = [(model.cols[i], float(np.median(X[model.cols[i]][use])),
                          float(np.median(healthy[model.cols[i]]))) for i in top]
    if baseline:
        xb, fsb = load_recording(baseline, channel=channel, fs=fs)
        Xb = features_for_signal(xb, fsb)
        ub = UnitBaseline().fit(Xb)
        r["deviation"] = {"baseline_file": baseline, "score": float(np.median(ub.score(X))),
                          "ref_score": float(np.median(ub.score(Xb))), "top": ub.top_features(X)}
    return r


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--fs", type=float, default=None, help="sampling rate (default 42000 Hz, Ottawa)")
    ap.add_argument("--channel", type=int, default=0, help="column index (0 = accelerometer)")
    ap.add_argument("--baseline", default=None, help="healthy reference recording of the SAME unit")
    ap.add_argument("--out", default=None, help="also write the report (.txt) and a .json next to it")
    ap.add_argument("--features", default=FEATURES)
    a = ap.parse_args(argv)
    r = analyse(a.file, a.fs, a.channel, a.baseline, a.features)
    txt = format_report(r)
    print(txt)
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(txt + "\n")
        with open(os.path.splitext(a.out)[0] + ".json", "w", encoding="utf-8") as fh:
            json.dump(r, fh, indent=2, default=float)
    return r


if __name__ == "__main__":
    main()
