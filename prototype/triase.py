"""DetakPompa triase armada: a folder of recordings (one per pump) -> one queue table.

Usage (from prototype/, after run_eval.py has produced results/features.csv):
    .venv\\Scripts\\python.exe -I -X utf8 triase.py data\\ottawa_uored_vafcls\\mat --out results\\triase\\armada_60
    .venv\\Scripts\\python.exe -I -X utf8 triase.py --daftar results\\triase\\armada_22.lst --out results\\triase\\armada_22
    .venv\\Scripts\\python.exe -I -X utf8 triase.py FOLDER --model rms      # comparator: RMS rule + same SNR gate

Queues (detakpompa/triage.py):
    AUDIT DULU  top-k (default k = 3) of the recordings answered WASPADA/RUSAK, by priority
    PANTAU      answered WASPADA/RUSAK beyond the audit capacity k
    UKUR ULANG  every TIDAK TAHU; signal-gated recordings get NO priority and are never ranked
    AMAN        answered SEHAT

Anti-leakage: a file whose name starts like an Ottawa recording (<F>_<bearing>_<state>, e.g.
I_3_1.mat or I_3_1_derau_-10dB.npy) is scored by a model trained WITHOUT that bearing (one
model per held-out bearing, i.e. leave-one-unit-out). Other files use a model trained on all
20 bearings. Label: "bearing Ottawa sebagai pengganti pompa"; this is not pump data.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from detakpompa.io import load_recording  # noqa: E402
from detakpompa.models import AbstainGate  # noqa: E402
from detakpompa.pipeline import features_for_signal, snr_cfar_threshold  # noqa: E402
from detakpompa.report import NEXT_STEP  # noqa: E402
from detakpompa.triage import (QUEUES, RMSRecordingTriage, assign_queues, decide_proposal,  # noqa: E402
                               fit_proposal)

FEATURES = os.path.join(HERE, "results", "features.csv")
EXTS = (".mat", ".npy", ".csv", ".txt")
UNIT_HINT = re.compile(r"^(?P<ftype>[HIOBC])_(?P<unit>\d+)_(?P<state>[012])(?:_|$)")
STATUS = {0: "SEHAT", 1: "WASPADA", 2: "RUSAK", -1: "TIDAK TAHU"}
ACTION_Q = {
    QUEUES[0]: "Audit minggu ini: flowmeter portable + manometer + power meter, lalu inspeksi bearing.",
    QUEUES[1]: "Antre audit berikutnya (di luar kapasitas minggu ini); rekam ulang di ronde berikut.",
    QUEUES[3]: "Tidak perlu tindakan khusus; rekam ulang sesuai jadwal rutin.",
}


def unit_hint(path: str):
    """(unit, state) if the file name starts like an Ottawa recording, else (None, None)."""
    m = UNIT_HINT.match(os.path.splitext(os.path.basename(path))[0])
    return (int(m["unit"]), int(m["state"])) if m else (None, None)


def collect(paths, daftar=None):
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += [os.path.join(p, f) for f in sorted(os.listdir(p)) if f.lower().endswith(EXTS)]
        elif os.path.isfile(p):
            files.append(p)
        else:
            raise FileNotFoundError(p)
    if daftar:
        base = os.path.dirname(os.path.abspath(daftar))
        with open(daftar, encoding="utf-8") as fh:
            for line in fh:
                line = line.split("#", 1)[0].strip()
                if line:
                    q = line if os.path.isabs(line) else os.path.normpath(os.path.join(HERE, line))
                    if not os.path.exists(q):
                        q = os.path.normpath(os.path.join(base, line))
                    files.append(q)
    return files


class ModelCache:
    """One fitted (proposal, rms_gate) pair per held-out unit (None = no unit held out)."""

    def __init__(self, F: pd.DataFrame):
        self.F, self.cache = F, {}

    def get(self, unit):
        if unit not in self.cache:
            Ftr = self.F if unit is None else self.F[self.F["unit"] != unit].reset_index(drop=True)
            model, tau = fit_proposal(Ftr)
            self.cache[unit] = (model, tau, RMSRecordingTriage().fit(Ftr), sorted(set(Ftr["unit"])))
        return self.cache[unit]


def score_file(path, cache: ModelCache, fs=None, channel=0, which="usulan"):
    x, fs = load_recording(path, channel=channel, fs=fs)
    unit, state = unit_hint(path)
    model, tau, rms, train_units = cache.get(unit if unit in set(cache.F["unit"]) else None)
    assert unit is None or unit not in train_units          # anti-leakage, checked every file
    gate = AbstainGate(snr_min=snr_cfar_threshold(float(fs)))
    name = os.path.splitext(os.path.basename(path))[0]
    row = {"name": name, "file": path, "label_asli": state, "unit": unit}
    if len(x) < 2 * fs:
        return {**row, "status": -1, "abstain_reason": "pendek", "priority": None,
                "priority_provisional": None, "n_ok": 0, "n_windows": 0, "snr_db": float("nan"), "detail": ""}
    X = features_for_signal(x, fs)
    ok = gate.quality_ok(X)
    row.update(snr_db=float(np.median(X["shaft_snr_db"])), snr_min=gate.snr_min)
    if which == "rms":
        d = rms.decide(X, ok)
        det = (f"RMS median {d['rms_median']:.2f} (ambang {rms.rule.sign * rms.rule.t1:.2f} / "
               f"{rms.rule.sign * rms.rule.t2:.2f}); margin {d['conf']:.2f} dekade (tau {rms.tau:.2f})")
    else:
        d = decide_proposal(ok, model.predict_proba(X), tau)
        p = d["proba"]
        det = f"prob sehat/waspada/rusak {p[0]:.2f}/{p[1]:.2f}/{p[2]:.2f} (tau {tau:.2f})"
    return {**row, **d, "detail": det}


def reason_text(r, k):
    q = r["queue"]
    if q == QUEUES[2]:
        if r["abstain_reason"] in ("sinyal", "pendek"):
            if r["abstain_reason"] == "pendek":
                return "rekaman < 2 s", NEXT_STEP["pendek"]
            return (f"sinyal ditolak gerbang SNR: {r['n_ok']}/{r['n_windows']} jendela lolos, SNR median "
                    f"{r['snr_db']:.1f} dB (ambang {r['snr_min']:.1f} dB); TIDAK diberi prioritas",
                    NEXT_STEP["sinyal"])
        pv = r.get("priority_provisional")
        return (f"model ragu ({r['detail']}); prioritas sementara {pv:.2f}, tidak ikut urutan",
                NEXT_STEP["ragu"])
    if q == QUEUES[3]:
        return f"SEHAT; {r['detail']}", ACTION_Q[q]
    extra = "" if q == QUEUES[0] else f"; di luar kapasitas audit k = {k}"
    return f"{STATUS[r['status']]}, prioritas {r['priority']:.2f} (peringkat {r['rank']}); {r['detail']}{extra}", ACTION_Q[q]


def run(files, k=3, which="usulan", features_csv=FEATURES, fs=None, channel=0):
    cache = ModelCache(pd.read_csv(features_csv))
    rows = [score_file(f, cache, fs, channel, which) for f in files]
    queued = assign_queues(rows, k=k)
    for r in queued:
        r["alasan"], r["langkah"] = reason_text(r, k)
    return queued


def format_table(queued, k, which):
    L = ["=" * 100,
         f"DAFTAR TRIASE ARMADA (DetakPompa, purwarupa TKT 3) | model: {which} | kapasitas audit k = {k}",
         "Data: bearing Ottawa sebagai PENGGANTI pompa (bukan pompa PDAM). Unit tiap berkas dikeluarkan dari data latih.",
         "=" * 100]
    for q in QUEUES:
        part = [r for r in queued if r["queue"] == q]
        L.append(f"\n[{q}] ({len(part)} rekaman)")
        for r in part:
            lab = "" if r["label_asli"] is None else f"  [label asli: {STATUS[r['label_asli']]}, tidak dipakai model]"
            rk = f"{r['rank']:>2}. " if r["rank"] is not None and q in QUEUES[:2] else "  - "
            L.append(f"{rk}{r['name']:<20} {STATUS[r['status']]:<10}{lab}")
            L.append(f"      alasan : {r['alasan']}")
            L.append(f"      langkah: {r['langkah']}")
    L.append("\nTIDAK TAHU bukan berarti aman: antrean UKUR ULANG dikerjakan sebelum ronde berikutnya.")
    L.append("Alat ini TIDAK mengukur efisiensi atau kWh; ia hanya memilih pompa mana yang diaudit duluan.")
    return "\n".join(L)


def write(queued, out_dir, k, which):
    os.makedirs(out_dir, exist_ok=True)
    cols = ["queue", "rank", "name", "status_txt", "label_asli_txt", "priority", "priority_provisional",
            "abstain_reason", "n_ok", "n_windows", "snr_db", "alasan", "langkah", "file"]
    with open(os.path.join(out_dir, f"antrean_{which}.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in queued:
            w.writerow({**r, "status_txt": STATUS[r["status"]],
                        "label_asli_txt": "" if r["label_asli"] is None else STATUS[r["label_asli"]],
                        "file": os.path.relpath(r["file"], HERE)})
    with open(os.path.join(out_dir, f"antrean_{which}.txt"), "w", encoding="utf-8") as fh:
        fh.write(format_table(queued, k, which) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="folder(s) and/or recording files (.mat/.npy/.csv)")
    ap.add_argument("--daftar", default=None, help="text file with one recording path per line")
    ap.add_argument("--k", type=int, default=3, help="audit capacity per round (default 3)")
    ap.add_argument("--model", choices=("usulan", "rms"), default="usulan")
    ap.add_argument("--fs", type=float, default=None)
    ap.add_argument("--channel", type=int, default=0)
    ap.add_argument("--out", default=None, help="folder for antrean_<model>.csv/.txt")
    ap.add_argument("--features", default=FEATURES)
    a = ap.parse_args(argv)
    files = collect(a.paths, a.daftar)
    if not files:
        ap.error("no recordings given")
    queued = run(files, a.k, a.model, a.features, a.fs, a.channel)
    print(format_table(queued, a.k, a.model))
    if a.out:
        write(queued, a.out, a.k, a.model)
    return queued


if __name__ == "__main__":
    main()
