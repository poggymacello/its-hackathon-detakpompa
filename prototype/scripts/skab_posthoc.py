"""POST-HOC diagnostics for the SKAB run (NOT pre-registered; written after seeing run_skab results).

Reads only our own output results/skab/points_oof.csv (never the raw data folder) and writes
results/skab/posthoc_*.csv + posthoc_log.txt. Nothing here changes the PRAREG_SKAB status.

Questions:
 (a) Session/regime confound: do the per-file scores on the NORMAL rows (before/around the
     anomaly) already separate fault files from valve files? If yes, the event-level AUROC
     partly measures "which recording session", not "which anomaly".
 (b) How large is the operating-point change caused by a valve closure in SKAB (ΔQ, ΔP_app
     between anomaly rows and normal rows of the same file)?
 (c) Pressure resolution: number of distinct pressure values and step size.

Run from prototype/:  .venv\\Scripts\\python.exe -I scripts\\skab_posthoc.py
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from detakpompa import hydraulic as hy  # noqa: E402

RES = os.path.join(HERE, "results", "skab")
METHODS = ["R", "R_hyd", "R_gbm", "B1", "B2", "B3", "R_rc", "B1_rc", "B2_rc", "B3_rc"]


def main():
    p = pd.read_csv(os.path.join(RES, "points_oof.csv"))
    lines = []

    # (a) per-file median score on normal rows vs on event rows
    rows = []
    for e, d in p.groupby("exp"):
        a = d["anomaly"].to_numpy() == 1
        r = {"exp": e, "cls": d["cls"].iat[0], "sub": d["sub"].iat[0]}
        for m in METHODS:
            r[f"normal_{m}"] = float(np.median(d[m].to_numpy()[~a]))
            r[f"event_{m}"] = float(np.median(d[m].to_numpy()[a]))
        r["Q_normal"] = float(np.median(d["Q"].to_numpy()[~a]))
        r["Q_event"] = float(np.median(d["Q"].to_numpy()[a]))
        r["Papp_normal"] = float(np.median(d["P_app"].to_numpy()[~a]))
        r["Papp_event"] = float(np.median(d["P_app"].to_numpy()[a]))
        r["dQ_pct"] = 100 * (r["Q_event"] - r["Q_normal"]) / r["Q_normal"]
        r["dPapp_pct"] = 100 * (r["Papp_event"] - r["Papp_normal"]) / r["Papp_normal"]
        rows.append(r)
    f = pd.DataFrame(rows)
    f.to_csv(os.path.join(RES, "posthoc_per_file.csv"), index=False)
    h1 = f[f["cls"].isin(["T", "F"])]
    y = (h1["cls"] == "F").astype(int).to_numpy()
    tab = []
    for m in METHODS:
        tab.append({"method": m,
                    "AUROC_F_vs_T_event_rows": hy.auc(h1[f"event_{m}"], y),
                    "AUROC_F_vs_T_NORMAL_rows_only": hy.auc(h1[f"normal_{m}"], y)})
    tab = pd.DataFrame(tab)
    tab.to_csv(os.path.join(RES, "posthoc_session_confound.csv"), index=False)
    lines.append("(a) AUROC F vs T dari median skor per berkas: baris kejadian vs baris NORMAL saja")
    lines.append(tab.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # (b) operating-point change per subclass
    b = f.groupby("sub")[["Q_normal", "Q_event", "dQ_pct", "Papp_normal", "Papp_event", "dPapp_pct"]].median()
    b.to_csv(os.path.join(RES, "posthoc_operating_point.csv"))
    lines.append("\n(b) Titik kerja per jenis (median per berkas): baris normal vs baris kejadian")
    lines.append(b.to_string(float_format=lambda x: f"{x:.1f}"))

    # (c) pressure resolution
    u = np.unique(np.round(p["p"].to_numpy(), 4))
    step = np.median(np.diff(u)) if len(u) > 1 else np.nan
    share = pd.Series(np.round(p["p"], 3)).value_counts(normalize=True).head(3)
    lines.append(f"\n(c) Pressure: {len(u)} nilai unik di {len(p)} baris uji; langkah median {step:.3f} bar; "
                 f"3 nilai tersering: " + ", ".join(f"{k:.3f} ({v:.1%})" for k, v in share.items()))

    txt = "\n".join(lines)
    print(txt)
    with open(os.path.join(RES, "posthoc_log.txt"), "w", encoding="utf-8") as fh:
        fh.write("POST-HOC, tidak diprareg. Lihat docstring scripts/skab_posthoc.py.\n\n" + txt + "\n")


if __name__ == "__main__":
    main()
