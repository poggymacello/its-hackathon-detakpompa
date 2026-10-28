"""Extra experiment: "rms_rule + the SAME SNR gate" vs the proposed RF (rf_spec).

Run from prototype/ (after run_eval.py, which caches results/features.csv):
    .venv\\Scripts\\python.exe -I run_eval_rms_gate.py

Same protocol as run_eval.py: leave-one-bearing-out (20 folds), assert_no_leakage every fold,
fixed RF hyper-parameters, CFAR SNR threshold, tau from inner grouped 5-fold on training units,
per-unit bootstrap (2000, seed 0 -> identical unit draws). Nothing is tuned on test units.
The RMS confidence (models.rule_margin) was fixed before this script was first run (README).

Writes ONLY new files (prefix rmsgate_) to results/; old results are left untouched. As a
reproducibility check, rf_spec out-of-fold probabilities and degradation predictions are
recomputed and compared against results/oof_predictions.csv and degradation_windows.csv.
"""

from __future__ import annotations

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.metrics import balanced_accuracy_score, f1_score  # noqa: E402

from detakpompa import FS_OTTAWA  # noqa: E402
from detakpompa.io import load_recording, windows  # noqa: E402
from detakpompa.metrics import _order, aurc, basic, gated_score, top_coverage, unit_bootstrap_fn  # noqa: E402
from detakpompa.models import AbstainGate, RFPlusRuleFeature, RMSGateBaseline, proposed_rf  # noqa: E402
from detakpompa.pipeline import features_for_signal, snr_cfar_threshold  # noqa: E402
from detakpompa.splits import assert_no_leakage, grouped_kfold, leave_one_unit_out  # noqa: E402

DATA = os.path.join(HERE, "data", "ottawa_uored_vafcls", "mat")
RES = os.path.join(HERE, "results")
N_BOOT = 2000
LOG = None


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


def bacc(y, p):
    return float(balanced_accuracy_score(y, p)) if len(y) and len(np.unique(y)) > 1 else np.nan


def mf1(y, p):
    return float(f1_score(y, p, average="macro", labels=[0, 1, 2], zero_division=0)) if len(y) else np.nan


def recall_k(y, p, k):
    m = y == k
    return float(np.mean(p[m] == k)) if m.any() else np.nan


def f1_k(y, p, k):
    return float(f1_score(y, p, labels=[k], average=None, zero_division=0)[0]) if len(y) else np.nan


def inner_oof_proba(X, y, units, make_model, k=5, seed=0):  # copy of run_eval.inner_oof_proba
    P = np.zeros((len(y), 3))
    for _, tr, te in grouped_kfold(units, k=k, seed=seed):
        assert_no_leakage(units, tr, te)
        P[te] = make_model().fit(X.iloc[tr], y[tr]).predict_proba(X.iloc[te])
    return P


def holm(pvals):
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    adj = np.empty_like(p)
    run = 0.0
    m = len(p)
    for r, i in enumerate(order):
        run = max(run, min(1.0, (m - r) * p[i]))
        adj[i] = run
    return adj


def plot_coverage_risk(out: pd.DataFrame):
    """Coverage-risk curves from rmsgate_oof_predictions.csv columns; writes PNG + curve CSV."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    y, n, q = out["state"].to_numpy(), len(out), out["quality_ok"].to_numpy(bool)
    col = {"rf_spec": "#2a78d6", "rms_rule": "#eb6834", "rf_spec_plus_rmsrule": "#1baf7a"}
    lab = {"rf_spec": "Usulan (RF spektral)", "rms_rule": "Ambang RMS", "rf_spec_plus_rmsrule": "Usulan + fitur aturan RMS (eksp. 2)"}
    fig, ax = plt.subplots(figsize=(7, 4.5))
    cr_rows = []
    for k in col:
        pr, cf = out[f"pred_{k}"].to_numpy(), out[f"conf_{k}"].to_numpy()
        for sc, ls, tag in ((gated_score(cf, q), "-", "gated"), (cf, "--", "ungated")):
            if k == "rf_spec_plus_rmsrule" and tag == "ungated":
                continue
            order = _order(sc)
            err = np.cumsum(pr[order] != y[order]) / np.arange(1, n + 1)
            cov = np.arange(1, n + 1) / n
            for kk in list(range(29, n, 10)) + [n - 1]:
                cr_rows.append({"model": k, "score": tag, "coverage": cov[kk], "error_rate": err[kk]})
            s = cov >= 0.05
            ax.plot(cov[s], err[s], ls, color=col[k], lw=2,
                    label=f"{lab[k]}{' + gerbang SNR' if tag == 'gated' else ' (tanpa gerbang)'}, AURC={aurc(y, pr, sc):.3f}")
    for k, mk in (("rf_spec", "o"), ("rms_rule", "s")):
        a2 = out[f"accept2_{k}"].to_numpy(bool)
        pr = out[f"pred_{k}"].to_numpy()
        ax.scatter([a2.mean()], [np.mean(pr[a2] != y[a2])], marker=mk, s=60, color=col[k],
                   edgecolor="white", linewidth=2, zorder=5)
    ax.axvline(q.mean(), color="#888888", lw=1, ls=":")
    ax.text(q.mean(), 0.42, "batas gerbang SNR ", fontsize=7, color="#555555", va="top", ha="right")
    ax.set_ylim(-0.01, 0.43)
    ax.set_xlabel("cakupan (fraksi jendela yang dijawab)")
    ax.set_ylabel("tingkat galat pada yang dijawab")
    ax.set_title("Cakupan vs risiko: usulan vs ambang RMS + gerbang SNR yang sama\n"
                 "(titik = titik operasi dua tahap; leave-one-bearing-out, Ottawa)", fontsize=9)
    ax.grid(alpha=.25); ax.legend(fontsize=7, loc="lower right", framealpha=0.95)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout(); fig.savefig(os.path.join(RES, "rmsgate_coverage_risk.png"), dpi=130)
    pd.DataFrame(cr_rows).to_csv(os.path.join(RES, "rmsgate_coverage_risk.csv"), index=False)


def main():
    global LOG
    t0 = time.time()
    LOG = open(os.path.join(RES, "rmsgate_log.txt"), "w", encoding="utf-8")
    F = pd.read_csv(os.path.join(RES, "features.csv"))
    SNR_MIN = snr_cfar_threshold(float(FS_OTTAWA))
    log(f"[gate] SNR threshold (CFAR, identical to run_eval.py) = {SNR_MIN:.2f} dB")
    y, units, recs = F["state"].to_numpy(), F["unit"].to_numpy(), F["recording"].to_numpy()
    n = len(y)

    pred = {k: np.full(n, -1) for k in ("rms_rule", "rf_spec", "rf_spec_plus_rmsrule")}
    conf = {k: np.zeros(n) for k in pred}
    acc2 = {k: np.zeros(n, bool) for k in ("rms_rule", "rf_spec")}      # two-stage accept
    qual_ok = np.zeros(n, bool)
    fold_rows, fold_models = [], {}

    for u, tr, te in leave_one_unit_out(units):
        assert_no_leakage(units, tr, te, recs)
        Xtr, Xte, ytr = F.iloc[tr], F.iloc[te], y[tr]
        # comparator: RMS rule + identical gate; tau from inner CV on training units
        rg = RMSGateBaseline(snr_min=SNR_MIN).fit(Xtr, ytr, units[tr])
        p_r, c_r, a_r, _ = rg.decide(Xte)
        pred["rms_rule"][te], conf["rms_rule"][te], acc2["rms_rule"][te] = p_r, c_r, a_r
        # proposal, re-fitted exactly as in run_eval.py
        m = proposed_rf().fit(Xtr, ytr)
        P = m.predict_proba(Xte)
        gate = AbstainGate(snr_min=SNR_MIN)
        gate.fit_conf(inner_oof_proba(Xtr, ytr, units[tr], proposed_rf).max(1))
        a_s, _ = gate.decide(Xte, P)
        pred["rf_spec"][te], conf["rf_spec"][te], acc2["rf_spec"][te] = P.argmax(1), P.max(1), a_s
        qual_ok[te] = gate.quality_ok(Xte)
        assert np.array_equal(gate.quality_ok(Xte), rg.gate.quality_ok(Xte))   # gate is identical
        # experiment 2: proposal + RMS-rule decision as a feature
        mc = RFPlusRuleFeature().fit(Xtr, ytr, units[tr])
        Pc = mc.predict_proba(Xte)
        pred["rf_spec_plus_rmsrule"][te], conf["rf_spec_plus_rmsrule"][te] = Pc.argmax(1), Pc.max(1)
        fold_models[int(u)] = (m, gate, rg)
        fold_rows.append({"test_unit": int(u), "rms_t1": rg.rule.sign * rg.rule.t1,
                          "rms_t2": rg.rule.sign * rg.rule.t2, "rms_sign": rg.rule.sign,
                          "rms_tau_margin_log10": rg.gate.tau_conf, "rf_spec_tau_conf": gate.tau_conf})
        log(f"[fold] unit {u:2d}: rms t1={fold_rows[-1]['rms_t1']:.4g} t2={fold_rows[-1]['rms_t2']:.4g} "
            f"tau_margin={rg.gate.tau_conf:.3f}  bacc rms={bacc(y[te], p_r):.3f} rf_spec={bacc(y[te], P.argmax(1)):.3f}")
    pd.DataFrame(fold_rows).to_csv(os.path.join(RES, "rmsgate_folds.csv"), index=False)

    # ---------- reproducibility check vs the original run
    O = pd.read_csv(os.path.join(RES, "oof_predictions.csv"))
    repro = {"rf_spec_pred_identical": bool(np.array_equal(O["pred_rf_spec"].to_numpy(), pred["rf_spec"])),
             "rms_rule_pred_identical": bool(np.array_equal(O["pred_rms_rule"].to_numpy(), pred["rms_rule"])),
             "rf_spec_accept_identical": bool(np.array_equal(O["accept_rf_spec"].to_numpy(), acc2["rf_spec"])),
             "rf_spec_max_abs_proba_diff": float(np.abs(O[["p0_rf_spec", "p1_rf_spec", "p2_rf_spec"]].to_numpy().max(1)
                                                        - conf["rf_spec"]).max())}
    log(f"[repro] {repro}")

    out = F[["recording", "unit", "state", "ftype", "window", "shaft_snr_db"]].copy()
    out["quality_ok"] = qual_ok
    for k in pred:
        out[f"pred_{k}"], out[f"conf_{k}"] = pred[k], conf[k]
    out["accept2_rms_rule"], out["accept2_rf_spec"] = acc2["rms_rule"], acc2["rf_spec"]
    out.to_csv(os.path.join(RES, "rmsgate_oof_predictions.csv"), index=False)

    # ---------- point estimates
    g = qual_ok
    op_cov = float(acc2["rf_spec"].mean())
    gscore = {k: gated_score(conf[k], qual_ok) for k in pred}
    topm = {k: top_coverage(gscore[k], op_cov) for k in pred}
    rows = []

    def add(setting, model, mask):
        yy, pp = y[mask], pred[model][mask]
        rows.append({"setting": setting, "model": model, "coverage": float(mask.mean()), "n": int(mask.sum()),
                     "balanced_accuracy": bacc(yy, pp), "macro_f1": mf1(yy, pp),
                     "error_rate": float(np.mean(yy != pp)),
                     **{f"recall_{c}": recall_k(yy, pp, k) for k, c in enumerate(("sehat", "waspada", "rusak"))},
                     **{f"f1_{c}": f1_k(yy, pp, k) for k, c in enumerate(("sehat", "waspada", "rusak"))},
                     "confusion": json.dumps(basic(yy, pp)["confusion"])})
    full = np.ones(n, bool)
    for k in pred:
        add("semua_jendela_tanpa_abstain", k, full)
        add("lolos_gerbang_sinyal_sama", k, g)
        add(f"cakupan_disamakan_{op_cov:.3f}", k, topm[k])
    for k in ("rms_rule", "rf_spec"):
        add("titik_operasi_dua_tahap", k, acc2[k])
    A = {k: {"aurc_ungated": aurc(y, pred[k], conf[k]), "aurc_gated": aurc(y, pred[k], gscore[k])} for k in pred}
    M = pd.DataFrame(rows)
    M.to_csv(os.path.join(RES, "rmsgate_metrics.csv"), index=False)
    for r in rows:
        log(f"[metric] {r['setting']:32s} {r['model']:22s} cov={r['coverage']:.3f} bacc={r['balanced_accuracy']:.3f} "
            f"mF1={r['macro_f1']:.3f} err={r['error_rate']:.3f} recall(s/w/r)=({r['recall_sehat']:.3f},"
            f"{r['recall_waspada']:.3f},{r['recall_rusak']:.3f}) cm={r['confusion']}")
    for k, v in A.items():
        log(f"[aurc] {k:22s} ungated={v['aurc_ungated']:.3f} gated={v['aurc_gated']:.3f}")

    # ---------- per-unit paired bootstrap (same unit draws as run_eval.py)
    def stats(idx):
        yy = y[idx]
        o = {}
        for k in pred:
            pp, gi = pred[k][idx], g[idx]
            o[f"{k}|full|bacc"] = bacc(yy, pp)
            o[f"{k}|full|mf1"] = mf1(yy, pp)
            o[f"{k}|gate|bacc"] = bacc(yy[gi], pp[gi])
            o[f"{k}|gate|mf1"] = mf1(yy[gi], pp[gi])
            o[f"{k}|aurc_gated|"] = aurc(yy, pp, gscore[k][idx])
            o[f"{k}|aurc_ungated|"] = aurc(yy, pp, conf[k][idx])
            tm = top_coverage(gscore[k][idx], op_cov)
            o[f"{k}|matched_cov|bacc"] = bacc(yy[tm], pp[tm])
            o[f"{k}|matched_cov|mf1"] = mf1(yy[tm], pp[tm])
            for c, cn in enumerate(("sehat", "waspada", "rusak")):
                o[f"{k}|gate|recall_{cn}"] = recall_k(yy[gi], pp[gi], c)
                o[f"{k}|gate|f1_{cn}"] = f1_k(yy[gi], pp[gi], c)
            if k in acc2:
                ai = acc2[k][idx]
                o[f"{k}|op2|bacc"] = bacc(yy[ai], pp[ai])
                o[f"{k}|op2|mf1"] = mf1(yy[ai], pp[ai])
                o[f"{k}|op2|cov"] = float(ai.mean())
        return o

    B = unit_bootstrap_fn(y, units, stats, n_boot=N_BOOT, seed=0)
    log(f"[boot] valid resamples = {len(next(iter(B.values())))} of {N_BOOT}")
    point = {"full|bacc": lambda k: bacc(y, pred[k]), "full|mf1": lambda k: mf1(y, pred[k]),
             "gate|bacc": lambda k: bacc(y[g], pred[k][g]), "gate|mf1": lambda k: mf1(y[g], pred[k][g]),
             "aurc_gated|": lambda k: A[k]["aurc_gated"], "aurc_ungated|": lambda k: A[k]["aurc_ungated"],
             "matched_cov|bacc": lambda k: bacc(y[topm[k]], pred[k][topm[k]]),
             "matched_cov|mf1": lambda k: mf1(y[topm[k]], pred[k][topm[k]]),
             "op2|bacc": lambda k: bacc(y[acc2[k]], pred[k][acc2[k]]),
             "op2|mf1": lambda k: mf1(y[acc2[k]], pred[k][acc2[k]])}
    for c, cn in enumerate(("sehat", "waspada", "rusak")):
        point[f"gate|recall_{cn}"] = (lambda c_: lambda k: recall_k(y[g], pred[k][g], c_))(c)
        point[f"gate|f1_{cn}"] = (lambda c_: lambda k: f1_k(y[g], pred[k][g], c_))(c)

    # comparison family. "role": U = primary (pre-registered), S = secondary, E2 = experiment 2
    fam = [("U1", "rf_spec", "rms_rule", "gate|bacc"), ("U1", "rf_spec", "rms_rule", "gate|mf1"),
           ("U2", "rf_spec", "rms_rule", "aurc_gated|"),
           ("S", "rf_spec", "rms_rule", "full|bacc"), ("S", "rf_spec", "rms_rule", "full|mf1"),
           ("S", "rf_spec", "rms_rule", "aurc_ungated|"),
           ("S", "rf_spec", "rms_rule", "matched_cov|bacc"), ("S", "rf_spec", "rms_rule", "matched_cov|mf1"),
           ("S", "rf_spec", "rms_rule", "op2|bacc"), ("S", "rf_spec", "rms_rule", "op2|mf1")]
    for cn in ("sehat", "waspada", "rusak"):
        fam += [("S", "rf_spec", "rms_rule", f"gate|recall_{cn}"), ("S", "rf_spec", "rms_rule", f"gate|f1_{cn}")]
    fam += [("E2", "rf_spec_plus_rmsrule", "rf_spec", "full|bacc"), ("E2", "rf_spec_plus_rmsrule", "rms_rule", "full|bacc"),
            ("E2", "rf_spec_plus_rmsrule", "rf_spec", "gate|bacc"), ("E2", "rf_spec_plus_rmsrule", "rms_rule", "gate|bacc"),
            ("E2", "rf_spec_plus_rmsrule", "rf_spec", "aurc_gated|"), ("E2", "rf_spec_plus_rmsrule", "rms_rule", "aurc_gated|")]
    prow = []
    for role, a, b, met in fam:
        d = B[f"{a}|{met}"] - B[f"{b}|{met}"]
        d = d[np.isfinite(d)]
        lower_better = met.startswith("aurc")
        p2 = float(min(1.0, 2 * min(np.mean(d <= 0), np.mean(d >= 0))))
        prow.append({"role": role, "model_a": a, "model_b": b, "metric": met.rstrip("|"),
                     "lower_is_better": lower_better, "a": point[met](a), "b": point[met](b),
                     "diff_point_a_minus_b": point[met](a) - point[met](b),
                     "boot_mean_diff": float(d.mean()), "ci_lo": float(np.percentile(d, 2.5)),
                     "ci_hi": float(np.percentile(d, 97.5)), "share_diff_le_0": float(np.mean(d <= 0)),
                     "p_two_sided_boot": p2, "n_resamples": int(len(d))})
    PR = pd.DataFrame(prow)
    PR["p_holm_all"] = holm(PR["p_two_sided_boot"])
    PR.to_csv(os.path.join(RES, "rmsgate_paired_bootstrap.csv"), index=False)
    for r in PR.itertuples():
        log(f"[paired] {r.role:2s} {r.model_a} - {r.model_b} {r.metric:20s} a={r.a:.3f} b={r.b:.3f} "
            f"diff={r.diff_point_a_minus_b:+.3f} CI95=({r.ci_lo:+.3f},{r.ci_hi:+.3f}) "
            f"p={r.p_two_sided_boot:.3f} p_holm={r.p_holm_all:.3f}")
    # bootstrap CI of each model's own operating-point coverage
    for k in acc2:
        v = B[f"{k}|op2|cov"]
        log(f"[op2] {k}: coverage={acc2[k].mean():.3f} CI95=({np.percentile(v, 2.5):.3f},{np.percentile(v, 97.5):.3f})")

    # ---------- disagreement analysis (gate-passing windows)
    ok_s, ok_r = pred["rf_spec"] == y, pred["rms_rule"] == y
    dis = []
    for k, cn in enumerate(("sehat", "waspada", "rusak")):
        mk = g & (y == k)
        dis.append({"kelas": cn, "n_lolos_gerbang": int(mk.sum()), "keduanya_benar": int((mk & ok_s & ok_r).sum()),
                    "hanya_usulan_benar": int((mk & ok_s & ~ok_r).sum()),
                    "hanya_rms_benar": int((mk & ~ok_s & ok_r).sum()), "keduanya_salah": int((mk & ~ok_s & ~ok_r).sum())})
        log(f"[disagree] {dis[-1]}")
    per_unit = []
    for u in np.unique(units):
        mu = g & (units == u)
        per_unit.append({"unit": int(u), "n": int(mu.sum()), "acc_rf_spec": float(ok_s[mu].mean()),
                         "acc_rms_rule": float(ok_r[mu].mean())})
    PU = pd.DataFrame(per_unit)
    PU["diff"] = PU.acc_rf_spec - PU.acc_rms_rule
    log(f"[per-unit, gate-passing] rf_spec better in {(PU['diff'] > 0).sum()} units, rms better in "
        f"{(PU['diff'] < 0).sum()}, tie {(PU['diff'] == 0).sum()}")
    pd.DataFrame(dis).to_csv(os.path.join(RES, "rmsgate_per_class_disagreement.csv"), index=False)
    PU.to_csv(os.path.join(RES, "rmsgate_per_unit.csv"), index=False)

    # ---------- degradation: same noise as run_eval.py (rng 123, same loop order)
    rng = np.random.default_rng(123)
    levels = [("bersih", None), ("snr_10dB", 10.0), ("snr_0dB", 0.0), ("snr_-10dB", -10.0), ("sensor_lepas", "detached")]
    deg = []
    for u, (m, gate, rg) in fold_models.items():
        for r in sorted(set(recs[units == u])):
            x, fs = load_recording(os.path.join(DATA, r + ".mat"))
            st = int(y[recs == r][0])
            for lname, lev in levels:
                ws = []
                for w in windows(x, fs, 1.0):
                    w = w - w.mean()
                    if lev is None:
                        ws.append(w)
                    elif lev == "detached":
                        ws.append(rng.normal(0, w.std(), len(w)))
                    else:
                        ws.append(w + rng.normal(0, w.std() * 10 ** (-lev / 20), len(w)))
                Xd = features_for_signal(np.concatenate(ws), fs)
                P = m.predict_proba(Xd)
                a_s, _ = gate.decide(Xd, P)
                p_r, c_r, a_r, _ = rg.decide(Xd)
                q = gate.quality_ok(Xd)
                for i in range(len(Xd)):
                    deg.append({"unit": u, "recording": r, "state": st, "level": lname, "window": i,
                                "quality_ok": bool(q[i]), "pred_rf_spec": int(P[i].argmax()), "conf_rf_spec": float(P[i].max()),
                                "accept2_rf_spec": bool(a_s[i]), "pred_rms_rule": int(p_r[i]),
                                "conf_rms_rule": float(c_r[i]), "accept2_rms_rule": bool(a_r[i]),
                                "rms": float(Xd["rms"].iloc[i]), "snr_db": float(Xd["shaft_snr_db"].iloc[i])})
    D = pd.DataFrame(deg)
    D.to_csv(os.path.join(RES, "rmsgate_degradation_windows.csv"), index=False)
    OD = pd.read_csv(os.path.join(RES, "degradation_windows.csv"))
    repro["degradation_rf_spec_pred_identical"] = bool(np.array_equal(OD["pred"].to_numpy(), D["pred_rf_spec"].to_numpy()))
    repro["degradation_quality_ok_identical"] = bool(np.array_equal(OD["quality_ok"].to_numpy(), D["quality_ok"].to_numpy()))
    log(f"[repro] degradation: {repro}")
    agg = []
    for lname, _ in levels:
        d = D[D.level == lname]
        row = {"level": lname, "n": len(d), "snr_gate_abstain_rate": 1 - d.quality_ok.mean()}
        for k in ("rf_spec", "rms_rule"):
            c = d[f"pred_{k}"] == d.state
            gq, a2 = d.quality_ok, d[f"accept2_{k}"]
            row[f"{k}_acc_no_abstain"] = c.mean()
            row[f"{k}_acc_gate_only"] = c[gq].mean() if gq.any() else np.nan
            row[f"{k}_total_abstain_two_stage"] = 1 - a2.mean()
            row[f"{k}_acc_two_stage_accepted"] = c[a2].mean() if a2.any() else np.nan
            row[f"{k}_n_two_stage_accepted"] = int(a2.sum())
            row[f"{k}_pred_share_sehat_waspada_rusak"] = json.dumps(np.round(np.bincount(d[f"pred_{k}"], minlength=3) / len(d), 3).tolist())
        # what share of windows the confidence stage ALONE (no SNR gate) would let through
        tau_r = {u_: rg_.gate.tau_conf for u_, (_, _, rg_) in fold_models.items()}
        tau_s = {u_: g_.tau_conf for u_, (_, g_, _) in fold_models.items()}
        row["rms_rule_conf_only_accept_rate"] = float(np.mean(d.conf_rms_rule >= d.unit.map(tau_r)))
        row["rf_spec_conf_only_accept_rate"] = float(np.mean(d.conf_rf_spec >= d.unit.map(tau_s)))
        row["median_rms_ratio_to_clean"] = np.nan
        agg.append(row)
    clean = D[D.level == "bersih"].set_index(["recording", "window"]).rms
    for row in agg:
        d = D[D.level == row["level"]].set_index(["recording", "window"]).rms
        row["median_rms_ratio_to_clean"] = float(np.median(d / clean.loc[d.index]))
    DA = pd.DataFrame(agg)
    DA.to_csv(os.path.join(RES, "rmsgate_degradation_summary.csv"), index=False)
    for row in agg:
        log(f"[degrade] {row['level']:12s} gate_abstain={row['snr_gate_abstain_rate']:.3f} | "
            f"acc_no_abstain rf={row['rf_spec_acc_no_abstain']:.3f} rms={row['rms_rule_acc_no_abstain']:.3f} | "
            f"acc_gate_only rf={row['rf_spec_acc_gate_only']:.3f} rms={row['rms_rule_acc_gate_only']:.3f} | "
            f"two-stage abstain rf={row['rf_spec_total_abstain_two_stage']:.3f} rms={row['rms_rule_total_abstain_two_stage']:.3f} | "
            f"conf-only accept rf={row['rf_spec_conf_only_accept_rate']:.3f} rms={row['rms_rule_conf_only_accept_rate']:.3f} | "
            f"pred share rf={row['rf_spec_pred_share_sehat_waspada_rusak']} rms={row['rms_rule_pred_share_sehat_waspada_rusak']} | "
            f"rms/clean={row['median_rms_ratio_to_clean']:.2f}")

    # ---------- figure (re-drawable later from the CSV: run_eval_rms_gate.py --plot-only)
    try:
        plot_coverage_risk(out)
    except Exception as e:
        log(f"[plot] skipped: {e}")

    summ = {"protocol": "leave-one-bearing-out 20 folds, per-unit bootstrap 2000 (seed 0), identical SNR gate",
            "snr_min_db": SNR_MIN, "gate_coverage": float(qual_ok.mean()), "rf_spec_op_coverage": op_cov,
            "aurc": A, "reproducibility": repro, "runtime_s": time.time() - t0}
    with open(os.path.join(RES, "rmsgate_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summ, fh, indent=2, default=float)
    log(f"[done] {time.time() - t0:.1f}s")


if __name__ == "__main__":
    if "--plot-only" in sys.argv:
        plot_coverage_risk(pd.read_csv(os.path.join(RES, "rmsgate_oof_predictions.csv")))
    else:
        main()
