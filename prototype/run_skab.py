"""SKAB exploration exactly as frozen in PRAREG_SKAB.md (SHA-256 in PRAREG_SKAB.sha256).

Run from prototype/ (data must be in data/skab/data/{anomaly-free,valve1,valve2,other}):
    .venv\\Scripts\\python.exe -I run_skab.py [--quick]

Leave-one-experiment-out (34 folds), anomaly-free always in training, assert_no_leakage every
fold. Models/baselines/thresholds as defined in PRAREG_SKAB §3; nothing tuned on test files.
Outputs: results/skab/ (CSV, log, JSON, figures). --quick uses fewer bootstrap draws (dev only;
its output must not be reported).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from detakpompa import hydraulic as hy  # noqa: E402

DATA = os.path.join(HERE, "data", "skab", "data")
OUT = os.path.join(HERE, "results", "skab")
B_PRIMARY, B_SECONDARY = 10_000, 2_000
ALPHA_PRIMARY, ALPHA_SECONDARY = 0.025, 0.05
BASE = ["B1", "B2", "B3"]
LOG = None


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


def method_scores(zR, zG, zRs, zB, groups):
    """Raw (unsmoothed) point scores for every method, then causal smoothing within file."""
    zR_rc, zB_rc = hy.recenter(zR, groups), hy.recenter(zB, groups)
    raw = {
        "R": hy.score_R(zR),
        "R_hyd": hy.score_R(zR, hy.HYD),
        "R_gbm": hy.score_R(zG),
        "R_sehat": hy.score_R(zRs),
        "B1": hy.score_B1(zB), "B2": hy.score_B2(zB), "B3": hy.score_B3(zB),
        "R_rc": hy.score_R(zR_rc),
        "B1_rc": hy.score_B1(zB_rc), "B2_rc": hy.score_B2(zB_rc), "B3_rc": hy.score_B3(zB_rc),
    }
    return {k: hy.smooth(v, groups) for k, v in raw.items()}


def run_folds(data):
    ids = list(data)
    rows, taus, comps = [], [], []
    for k, (test_id, train_ids) in enumerate(hy.loeo_folds(ids)):
        assert test_id not in train_ids
        tr_norm = hy.build_train(data, train_ids)
        tr_sehat = hy.build_train(data, train_ids, include_valve_anomaly=True)
        te = data[test_id].copy()
        te["exp"] = test_id
        hy.check_fold(tr_norm["exp"].to_numpy(), te["exp"].to_numpy())
        hy.check_fold(tr_sehat["exp"].to_numpy(), te["exp"].to_numpy())

        R = hy.ResidualModel("ridge").fit(tr_norm)
        G = hy.ResidualModel("gbm").fit(tr_norm)
        Rs = hy.ResidualModel("ridge").fit(tr_sehat)
        Z = hy.SensorZ().fit(tr_norm)

        # thresholds: q99 of smoothed scores on training-normal rows (smoothing over full files)
        full = hy.stack(data, train_ids)
        g = full["exp"].to_numpy()
        s_tr = method_scores(R.components(full), G.components(full), Rs.components(full),
                             Z.components(full), g)
        normal = full["anomaly"].to_numpy() == 0
        tau = {m: float(np.quantile(v[normal], hy.TAU_Q)) for m, v in s_tr.items()}

        zR_te = R.components(te)
        s_te = method_scores(zR_te, G.components(te), Rs.components(te), Z.components(te),
                             te["exp"].to_numpy())
        d = pd.DataFrame({"exp": test_id, "t": te["t"].to_numpy(), "anomaly": te["anomaly"].to_numpy(),
                          "Q": te[hy.Q].to_numpy(), "p": te[hy.P].to_numpy(), "P_app": te[hy.PAPP].to_numpy()})
        for m, v in s_te.items():
            d[m] = v
        for c in zR_te.columns:
            d[c] = zR_te[c].to_numpy()
        rows.append(d)
        taus.append({"exp": test_id, **tau, "n_train_normal": int(len(tr_norm)),
                     "n_train_sehat": int(len(tr_sehat))})
        if k % 5 == 0:
            log(f"[fold {k + 1:2d}/34] test={test_id:10s} n_train_normal={len(tr_norm)} "
                f"tau_R={tau['R']:.3f} tau_B3={tau['B3']:.3f}")
    pts = pd.concat(rows, ignore_index=True)
    tau = pd.DataFrame(taus)
    pts["cls"] = pts["exp"].map(hy.experiment_class)
    pts["sub"] = pts["exp"].map(hy.experiment_subclass)
    return pts, tau


METHODS = ["R", "R_hyd", "R_gbm", "R_sehat", "B1", "B2", "B3", "R_rc", "B1_rc", "B2_rc", "B3_rc"]


def events_table(pts, tau):
    ev = []
    t = tau.set_index("exp")
    for e, d in pts.groupby("exp", sort=False):
        a = d["anomaly"].to_numpy() == 1
        row = {"exp": e, "cls": d["cls"].iat[0], "sub": d["sub"].iat[0], "n_rows": len(d),
               "n_event_rows": int(a.sum())}
        for m in METHODS:
            sc = float(np.median(d[m].to_numpy()[a])) if a.any() else np.nan
            row[f"score_{m}"] = sc
            row[f"tau_{m}"] = float(t.loc[e, m])
            row[f"flag_{m}"] = int(sc > t.loc[e, m]) if a.any() else -1
        for c in hy.TARGETS:
            row[f"med_{c}"] = float(np.median(d[c].to_numpy()[a])) if a.any() else np.nan
        ev.append(row)
    return pd.DataFrame(ev)


def event_test(ev, pos_cls, neg_sel, ref, others, n_boot, name):
    """AUROC per event, positives = rows where pos_cls(ev) True, negatives where neg_sel True."""
    sel = (pos_cls | neg_sel) & (ev["n_event_rows"] > 0)
    e = ev[sel]
    y = pos_cls[sel].astype(int).to_numpy()
    scores = {m: e[f"score_{m}"].to_numpy() for m in [ref, *others]}
    res = hy.paired_auc_bootstrap(scores, y, e["exp"].to_numpy(), ref, others, n_boot, seed=0,
                                  strata=y)
    out = []
    for o, r in res.items():
        out.append({"test": name, "ref": ref, "vs": o, "n_pos": int(y.sum()), "n_neg": int((1 - y).sum()), **r})
    return out


def point_test(pts, sel, ref, others, n_boot, name):
    d = pts[sel]
    y = d["anomaly"].to_numpy()
    scores = {m: d[m].to_numpy() for m in [ref, *others]}
    res = hy.paired_auc_bootstrap(scores, y, d["exp"].to_numpy(), ref, others, n_boot, seed=0)
    out = []
    for o, r in res.items():
        out.append({"test": name, "ref": ref, "vs": o, "n_pos": int(y.sum()), "n_neg": int((1 - y).sum()),
                    "n_files": int(d["exp"].nunique()), **r})
    return out


def point_rates(pts, tau, methods):
    t = tau.set_index("exp")
    out = []
    for m in methods:
        thr = pts["exp"].map(t[m]).to_numpy()
        flag = pts[m].to_numpy() > thr
        y = pts["anomaly"].to_numpy() == 1
        tp, fp, fn = np.sum(flag & y), np.sum(flag & ~y), np.sum(~flag & y)
        prec = tp / (tp + fp) if tp + fp else np.nan
        rec = tp / (tp + fn) if tp + fn else np.nan
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else np.nan
        out.append({"method": m, "F1": f1, "FAR": float(np.mean(flag[~y])), "MAR": float(np.mean(~flag[y])),
                    "precision": prec, "recall": rec})
    return pd.DataFrame(out)


def ba_events(ev, methods, n_boot):
    e = ev[ev["cls"].isin(["T", "F"]) & (ev["n_event_rows"] > 0)]
    y = (e["cls"] == "F").astype(int).to_numpy()
    out = []
    for m in methods:
        pred = e[f"flag_{m}"].to_numpy()
        ba = hy.balanced_accuracy(y, pred)
        vals = []
        for w in hy.bootstrap_weights(e["exp"].to_numpy(), n_boot, 0, strata=y):
            idx = np.repeat(np.arange(len(y)), w.astype(int))
            vals.append(hy.balanced_accuracy(y[idx], pred[idx]))
        out.append({"method": m, "balanced_acc": ba, "lo": float(np.percentile(vals, 2.5)),
                    "hi": float(np.percentile(vals, 97.5)),
                    "recall_F": float(np.mean(pred[y == 1] == 1)),
                    "flag_rate_T": float(np.mean(pred[y == 0] == 1))})
    return pd.DataFrame(out)


def figures(data, pts, ev):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
    C_T, C_F, C_X, C_N = "#2a78d6", "#eb6834", "#1baf7a", "#b9b8b3"
    style = {
        "T-valve1 (inlet)": dict(c=C_T, marker="o", label="Katup inlet ditutup (valve1)"),
        "T-valve2 (outlet)": dict(c=C_T, marker="^", label="Katup outlet ditutup (valve2)"),
        "F-imbalance": dict(c=C_F, marker="s", label="Imbalance rotor (fault)"),
        "F-kavitasi": dict(c=C_F, marker="D", label="Kavitasi (fault)"),
        "X-proses": dict(c=C_X, marker="v", label="Proses/sistem (bocor, volume, suhu)"),
    }
    # descriptive curves: fit on ALL normal rows (not used for any test)
    alln = hy.build_train(data, list(data))
    Rd = hy.ResidualModel("ridge").fit(alln)
    rng = np.random.default_rng(0)
    nidx = rng.choice(len(alln), min(4000, len(alln)), replace=False)
    qgrid = np.linspace(np.percentile(pts["Q"], 0.5), np.percentile(pts["Q"], 99.5), 200)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.4))
    for ax, (ycol, ylab) in zip(axes, [("p", "Tekanan setelah pompa [bar]"), ("P_app", "Daya semu V·I [VA]")]):
        nsrc = alln.iloc[nidx]
        ax.scatter(nsrc[hy.Q], nsrc[hy.P if ycol == "p" else hy.PAPP], s=4, c=C_N, alpha=0.35,
                   linewidths=0, label="Normal (anomaly = 0, semua berkas)")
        a = pts[pts["anomaly"] == 1]
        for sub, st in style.items():
            d = a[a["sub"] == sub]
            if len(d) > 1500:
                d = d.sample(1500, random_state=0)
            ax.scatter(d["Q"], d[ycol], s=9, alpha=0.55, linewidths=0, c=st["c"], marker=st["marker"],
                       label=st["label"])
        if ycol == "p":
            yhat = Rd.models["z_p"].predict(qgrid[:, None])
            ax.plot(qgrid, yhat, color=INK, lw=2, label="Kurva normal p = f(Q) (deskriptif)")
        else:
            phat = Rd.models["z_p"].predict(qgrid[:, None])
            yhat = Rd.models["z_P"].predict(np.c_[qgrid, phat])
            ax.plot(qgrid, yhat, color=INK, lw=2, ls="--", label="Kurva normal P(Q, p̂(Q)) (deskriptif)")
        ax.set_xlabel("Laju alir RateRMS [L/min]", color=INK2)
        ax.set_ylabel(ylab, color=INK2)
        ax.grid(color=GRID, lw=0.6)
        for s in ax.spines.values():
            s.set_color(GRID)
        ax.tick_params(colors=INK2)
    axes[0].set_title("Ruang tekanan–debit: titik anomali per jenis", color=INK, loc="left")
    axes[1].set_title("Ruang daya–debit", color=INK, loc="left")
    h, lab = axes[0].get_legend_handles_labels()
    h2, lab2 = axes[1].get_legend_handles_labels()
    h, lab = h + h2[-1:], lab + lab2[-1:]
    fig.legend(h, lab, loc="lower center", ncol=4, frameon=False, fontsize=8.5, markerscale=2)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    fig.savefig(os.path.join(OUT, "ruang_Q_p_P.png"), dpi=150)
    plt.close(fig)

    # event scores relative to each method's threshold
    meths = ["R", "B1", "B2", "B3"]
    fig, ax = plt.subplots(figsize=(11, 4.8))
    order = list(style)
    for i, m in enumerate(meths):
        for j, sub in enumerate(order):
            d = ev[(ev["sub"] == sub) & (ev["n_event_rows"] > 0)]
            v = d[f"score_{m}"] / d[f"tau_{m}"]
            x = i * (len(order) + 1) + j + rng.uniform(-0.18, 0.18, len(v))
            ax.scatter(x, v, s=34, c=style[sub]["c"], marker=style[sub]["marker"], edgecolors="white",
                       linewidths=1.5, label=style[sub]["label"] if i == 0 else None, zorder=3)
    ax.axhline(1, color=INK2, lw=1, ls="--")
    ax.text(len(meths) * (len(order) + 1) - 1.2, 1.08, "ambang τ (q99 normal latih)", ha="right",
            color=INK2, fontsize=8)
    ax.set_yscale("log")
    ax.set_xticks([i * (len(order) + 1) + (len(order) - 1) / 2 for i in range(len(meths))])
    ax.set_xticklabels(["R: residual hidraulik", "B1: RMS getaran", "B2: arus", "B3: z-maks sensor"],
                       color=INK2)
    ax.set_ylabel("Skor kejadian / τ (log)", color=INK2)
    ax.set_title("Skor tiap kejadian (median di baris anomali), OOF leave-one-experiment-out",
                 color=INK, loc="left")
    ax.grid(axis="y", color=GRID, lw=0.6)
    for s in ax.spines.values():
        s.set_color(GRID)
    ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "skor_kejadian.png"), dpi=150)
    plt.close(fig)


def main():
    global LOG, OUT
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--data", default=DATA, help="dev only: synthetic data folder for dry runs")
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()
    OUT = args.out
    bp, bs = (500, 200) if args.quick else (B_PRIMARY, B_SECONDARY)
    os.makedirs(OUT, exist_ok=True)
    LOG = open(os.path.join(OUT, "run_skab_log.txt" if not args.quick else "quick_log.txt"), "w",
               encoding="utf-8")
    t0 = time.time()
    data, info = hy.load_skab(args.data)
    log(f"SKAB loaded from {args.data}: {len(data)} files; rows={sum(len(d) for d in data.values())}; info={info}")
    for e in sorted(data, key=hy.sort_key):
        d = data[e]
        log(f"  {e:13s} cls={hy.experiment_class(e)} rows={len(d):5d} anomaly_rows={int(d['anomaly'].sum()):4d}")
    n_T = sum(1 for e, d in data.items() if hy.experiment_class(e) == "T" and d["anomaly"].sum() > 0)
    n_F = sum(1 for e, d in data.items() if hy.experiment_class(e) == "F" and d["anomaly"].sum() > 0)
    log(f"events with labels: T={n_T} F={n_F}")
    inconclusive = n_T < 10 or n_F < 5

    pts, tau = run_folds(data)
    ev = events_table(pts, tau)
    pts.to_csv(os.path.join(OUT, "points_oof.csv"), index=False, float_format="%.6g")
    tau.to_csv(os.path.join(OUT, "tau_per_fold.csv"), index=False)
    ev.to_csv(os.path.join(OUT, "events.csv"), index=False)
    log(f"folds done in {time.time() - t0:.0f} s")

    isF, isT = ev["cls"] == "F", ev["cls"] == "T"
    # ---------------- primary
    prim = event_test(ev, isF, isT, "R", BASE, bp, "H1") + point_test(pts, pts["cls"] != "N", "R", BASE, bp, "H2")
    prim = pd.DataFrame(prim)
    pH = {h: float(prim[prim["test"] == h]["p_one_sided"].max()) for h in ("H1", "H2")}
    hol = hy.holm(pH, ALPHA_PRIMARY)
    # guards
    rec_F = float(ev[isF & (ev["n_event_rows"] > 0)]["flag_R"].eq(1).mean())
    rates = point_rates(pts, tau, METHODS)
    far = rates.set_index("method")["FAR"]
    g1 = rec_F >= 0.5
    g2 = bool(far["R"] <= far["B3"] + 0.05)
    status = {}
    for h, g in (("H1", g1), ("H2", g2)):
        if inconclusive:
            status[h] = "TIDAK KONKLUSIF"
        else:
            status[h] = "LULUS" if (hol[h][2] and g) else "GAGAL"
    prim.to_csv(os.path.join(OUT, "primary.csv"), index=False)

    # per-method AUROC + CI (primary sets)
    e1 = ev[(isF | isT) & (ev["n_event_rows"] > 0)]
    y1 = (e1["cls"] == "F").astype(int).to_numpy()
    p2 = pts[pts["cls"] != "N"]
    aucs = []
    for m in METHODS:
        a1 = hy.auc(e1[f"score_{m}"], y1)
        lo1, hi1 = hy.auc_ci(e1[f"score_{m}"], y1, e1["exp"].to_numpy(), bp, 0, strata=y1)
        a2 = hy.auc(p2[m], p2["anomaly"])
        lo2, hi2 = hy.auc_ci(p2[m], p2["anomaly"], p2["exp"].to_numpy(), bp, 0)
        aucs.append({"method": m, "H1_auc_event": a1, "H1_lo": lo1, "H1_hi": hi1,
                     "H2_auc_point": a2, "H2_lo": lo2, "H2_hi": hi2})
    aucs = pd.DataFrame(aucs)
    aucs.to_csv(os.path.join(OUT, "auc_per_method.csv"), index=False)

    # ---------------- secondary
    v1 = ev["exp"].str.startswith("valve1/")
    v2 = ev["exp"].str.startswith("valve2/")
    isFX = ev["cls"].isin(["F", "X"])
    sec = []
    sec += event_test(ev, isF, v2, "R", BASE, bs, "S1 H1 T=valve2")
    sec += event_test(ev, isF, v1, "R", BASE, bs, "S2 H1 T=valve1")
    sec += event_test(ev, isFX, isT, "R", BASE, bs, "S3 H1 F∪X vs T")
    sec += event_test(ev, isF, isT, "R_sehat", BASE, bs, "S4 H1 R-sehat")
    sec += event_test(ev, isF, isT, "R_gbm", BASE, bs, "S5 H1 R-GBM")
    sec += point_test(pts, pts["cls"] != "N", "R_gbm", BASE, bs, "S5 H2 R-GBM")
    sec += event_test(ev, isF, isT, "R_hyd", BASE, bs, "S6 H1 hidraulik saja")
    sec += point_test(pts, pts["cls"].isin(["F", "X"]), "R", BASE, bs, "S9 H2 tanpa valve")
    bases_rc = ["B1_rc", "B2_rc", "B3_rc"]
    sec += event_test(ev, isF, isT, "R_rc", bases_rc, bs, "S10 H1 pemusatan ulang")
    sec += point_test(pts, pts["cls"] != "N", "R_rc", bases_rc, bs, "S10 H2 pemusatan ulang")
    sec = pd.DataFrame(sec)
    sh = hy.holm({i: p for i, p in enumerate(sec["p_two_sided"])}, ALPHA_SECONDARY)
    sec["holm_threshold"] = [sh[i][1] for i in range(len(sec))]
    sec["holm_reject"] = [sh[i][2] for i in range(len(sec))]
    sec.to_csv(os.path.join(OUT, "secondary.csv"), index=False)
    ba = ba_events(ev, METHODS, bs)
    ba.to_csv(os.path.join(OUT, "S7_balanced_acc_event.csv"), index=False)
    rates.to_csv(os.path.join(OUT, "S8_point_rates.csv"), index=False)

    # descriptive: median z per subclass over event rows
    a = pts[pts["anomaly"] == 1]
    desc = a.groupby("sub")[list(hy.TARGETS)].median()
    desc["n_rows"] = a.groupby("sub").size()
    nrm = pts[pts["anomaly"] == 0]
    desc.loc["normal (berkas uji)"] = list(nrm[list(hy.TARGETS)].median()) + [len(nrm)]
    desc.to_csv(os.path.join(OUT, "deskriptif_median_z.csv"))

    # ---------------- report
    log("\n=== PRIMER (Holm m=2, alpha satu sisi 0.025; p_H = max_j p_j, IUT) ===")
    for _, r in prim.iterrows():
        log(f"{r['test']} R vs {r['vs']}: AUROC {r['auc_ref']:.3f} vs {r['auc_other']:.3f}  "
            f"Δ={r['delta']:+.3f} [{r['lo']:+.3f}; {r['hi']:+.3f}]  p1={r['p_one_sided']:.4f}")
    for h in ("H1", "H2"):
        log(f"{h}: p_H={hol[h][0]:.4f} thr={hol[h][1]:.4f} holm_reject={hol[h][2]} -> {status[h]}")
    log(f"G-H1 recall F events at tau_R = {rec_F:.3f} (>=0.5: {g1});  "
        f"G-H2 FAR_R={far['R']:.3f} vs FAR_B3+0.05={far['B3'] + 0.05:.3f} ({g2})")
    log("\nAUROC per metode:\n" + aucs.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    log("\n=== SEKUNDER (Holm dua sisi alpha 0.05 atas semua baris) ===")
    log(sec[["test", "ref", "vs", "n_pos", "n_neg", "auc_ref", "auc_other", "delta", "lo", "hi",
             "p_two_sided", "holm_reject"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    log("\nS7 balanced accuracy per kejadian pada tau:\n" + ba.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    log("\nS8 titik pada tau:\n" + rates.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    log("\nDeskriptif median z residual R (baris anomali per jenis):\n" + desc.to_string(float_format=lambda x: f"{x:.2f}"))

    summary = {"prereg": "PRAREG_SKAB.md", "quick": args.quick, "n_boot_primary": bp, "n_boot_secondary": bs,
               "load_info": info, "status": status, "p_H": pH,
               "holm": {k: {"p": v[0], "threshold": v[1], "reject": bool(v[2])} for k, v in hol.items()},
               "guards": {"G_H1_recall_F": rec_F, "G_H1_ok": bool(g1), "G_H2_FAR_R": float(far["R"]),
                          "G_H2_FAR_B3": float(far["B3"]), "G_H2_ok": g2},
               "primary": prim.to_dict(orient="records"), "auc_per_method": aucs.to_dict(orient="records"),
               "runtime_s": round(time.time() - t0, 1)}
    with open(os.path.join(OUT, "summary.json" if not args.quick else "quick_summary.json"), "w",
              encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=float)
    figures(data, pts, ev)
    log(f"\nselesai dalam {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
