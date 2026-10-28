"""Full evaluation: leave-one-bearing-out (20 folds) on Ottawa UORED-VAFCLS v5.

Run from prototype/:
    .venv\\Scripts\\python.exe -I run_eval.py

Writes everything to results/. No hyper-parameter is tuned on test units: thresholds of the
rules, RF settings (fixed), SNR gate (training quantile) and the confidence threshold
(inner grouped CV on training units) only see training units of each fold.
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
from sklearn.metrics import f1_score  # noqa: E402

from detakpompa import FS_OTTAWA  # noqa: E402
from detakpompa.deviation import UnitBaseline  # noqa: E402
from detakpompa.io import load_recording, windows  # noqa: E402
from detakpompa.metrics import basic, coverage_risk, paired_diff, unit_bootstrap  # noqa: E402
from detakpompa.models import (AbstainGate, EnvelopeKurtosisRule, ThresholdRule,  # noqa: E402
                               baseline_rf, proposed_rf)
from detakpompa.pipeline import build_feature_table, features_for_signal, snr_cfar_threshold  # noqa: E402
from detakpompa.splits import assert_no_leakage, grouped_kfold, leave_one_unit_out  # noqa: E402

DATA = os.path.join(HERE, "data", "ottawa_uored_vafcls", "mat")
RES = os.path.join(HERE, "results")
os.makedirs(RES, exist_ok=True)
LOG = open(os.path.join(RES, "run_eval_log.txt"), "w", encoding="utf-8")


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.write(s + "\n")
    LOG.flush()


def inner_oof_proba(X, y, units, make_model, k=5, seed=0):
    P = np.zeros((len(y), 3))
    for _, tr, te in grouped_kfold(units, k=k, seed=seed):
        assert_no_leakage(units, tr, te)
        P[te] = make_model().fit(X.iloc[tr], y[tr]).predict_proba(X.iloc[te])
    return P


def rec_mean(df_idx_rec, P):
    """Average window probabilities per recording. Returns (recordings, mean P)."""
    recs = pd.unique(df_idx_rec)
    M = np.stack([P[df_idx_rec == r].mean(0) for r in recs])
    return recs, M


def main():
    t0 = time.time()
    feat_path = os.path.join(RES, "features.csv")
    if os.path.exists(feat_path):
        F = pd.read_csv(feat_path)
        log(f"[features] loaded cache {feat_path}")
    else:
        F = build_feature_table(DATA)
        F.to_csv(feat_path, index=False)
        log(f"[features] computed {len(F)} windows in {time.time() - t0:.1f}s -> {feat_path}")
    SNR_MIN = snr_cfar_threshold(float(FS_OTTAWA))
    log(f"[gate] SNR threshold (CFAR on white noise, pfa=1%) = {SNR_MIN:.2f} dB")
    y = F["state"].to_numpy()
    units = F["unit"].to_numpy()
    recs = F["recording"].to_numpy()
    log(f"[data] windows={len(F)} recordings={F.recording.nunique()} units={F.unit.nunique()} "
        f"class counts={np.bincount(y).tolist()}")

    names = ["rms_rule", "env_kurt_rule", "rf_stat", "rf_spec"]
    pred = {n: np.full(len(y), -1) for n in names}
    proba = {n: np.zeros((len(y), 3)) for n in ("rf_stat", "rf_spec")}
    accept = {n: np.zeros(len(y), bool) for n in ("rf_stat", "rf_spec")}
    reason = np.array([""] * len(y), dtype=object)
    qual_ok = np.zeros(len(y), bool)
    fold_rows = []
    fold_models = {}

    for u, tr, te in leave_one_unit_out(units):
        assert_no_leakage(units, tr, te, recs)
        Xtr, Xte, ytr = F.iloc[tr], F.iloc[te], y[tr]
        pred["rms_rule"][te] = ThresholdRule("rms").fit(Xtr, ytr).predict(Xte)
        pred["env_kurt_rule"][te] = EnvelopeKurtosisRule().fit(Xtr, ytr).predict(Xte)
        row = {"test_unit": int(u), "n_train": len(tr), "n_test": len(te)}
        for n, mk in (("rf_stat", baseline_rf), ("rf_spec", proposed_rf)):
            m = mk().fit(Xtr, ytr)
            P = m.predict_proba(Xte)
            proba[n][te] = P
            pred[n][te] = P.argmax(1)
            gate = AbstainGate(snr_min=SNR_MIN)
            Pin = inner_oof_proba(Xtr, ytr, units[tr], mk)
            gate.fit_conf(Pin.max(1))
            acc, rs = gate.decide(Xte, P)
            accept[n][te] = acc
            row[f"{n}_tau_conf"] = gate.tau_conf
            row[f"{n}_snr_min"] = gate.snr_min
            if n == "rf_spec":
                reason[te] = rs
                qual_ok[te] = gate.quality_ok(Xte)
                fold_models[int(u)] = (m, gate)
        fold_rows.append(row)
        log(f"[fold] unit {u:2d}: bacc rf_spec={basic(y[te], pred['rf_spec'][te])['balanced_accuracy']:.3f} "
            f"rf_stat={basic(y[te], pred['rf_stat'][te])['balanced_accuracy']:.3f} "
            f"tau={row['rf_spec_tau_conf']:.3f} snr_min={row['rf_spec_snr_min']:.1f}")
    pd.DataFrame(fold_rows).to_csv(os.path.join(RES, "folds.csv"), index=False)

    # ---------- predictions table
    out = F[["recording", "unit", "state", "ftype", "window", "shaft_hz", "shaft_snr_db"]].copy()
    for n in names:
        out[f"pred_{n}"] = pred[n]
    for n in ("rf_stat", "rf_spec"):
        for k in range(3):
            out[f"p{k}_{n}"] = proba[n][:, k]
        out[f"accept_{n}"] = accept[n]
    out["abstain_reason_rf_spec"] = reason
    out.to_csv(os.path.join(RES, "oof_predictions.csv"), index=False)

    # ---------- window-level metrics + per-unit bootstrap CI
    summary = {"dataset": "Ottawa UORED-VAFCLS v5 (accelerometer, 1 s windows)",
               "split": "leave-one-bearing-out, 20 folds", "n_windows": int(len(y)),
               "class_counts": np.bincount(y).tolist(), "chance_balanced_accuracy": 1 / 3,
               "window": {}, "recording": {}}
    ci, vals = unit_bootstrap(y, pred, units, n_boot=2000)
    ci_f1, vals_f1 = unit_bootstrap(y, pred, units, n_boot=2000,
                                    metric=lambda a, b: f1_score(a, b, average="macro"))
    rows = []
    for n in names:
        b = basic(y, pred[n])
        b["balanced_accuracy_ci95"] = ci[n]
        b["macro_f1_ci95"] = ci_f1[n]
        summary["window"][n] = b
        rows.append({"level": "window", "model": n, "balanced_accuracy": b["balanced_accuracy"],
                     "bacc_ci_lo": ci[n][0], "bacc_ci_hi": ci[n][1], "macro_f1": b["macro_f1"],
                     "f1_ci_lo": ci_f1[n][0], "f1_ci_hi": ci_f1[n][1],
                     "f1_sehat": b["f1_per_class"][0], "f1_waspada": b["f1_per_class"][1],
                     "f1_rusak": b["f1_per_class"][2], "n": b["n"]})
        log(f"[window] {n:14s} bacc={b['balanced_accuracy']:.3f} CI95=({ci[n][0]:.3f},{ci[n][1]:.3f}) "
            f"macroF1={b['macro_f1']:.3f} F1/class={np.round(b['f1_per_class'], 3).tolist()} cm={b['confusion']}")
    diffs = []
    for base in ("rms_rule", "env_kurt_rule", "rf_stat"):
        for metric_name, V in (("balanced_accuracy", vals), ("macro_f1", vals_f1)):
            m_, lo, hi, p_le0 = paired_diff(V, "rf_spec", base)
            diffs.append({"proposed": "rf_spec", "baseline": base, "metric": metric_name, "mean_diff": m_,
                          "ci_lo": lo, "ci_hi": hi, "share_resamples_diff_le_0": p_le0})
            log(f"[paired] rf_spec - {base:14s} {metric_name:17s} diff={m_:+.3f} CI95=({lo:+.3f},{hi:+.3f}) P(diff<=0)={p_le0:.3f}")
    pd.DataFrame(diffs).to_csv(os.path.join(RES, "paired_bootstrap.csv"), index=False)
    summary["paired_bootstrap_window"] = diffs

    # ---------- recording-level (mean proba for RF, majority vote for rules)
    rec_list = pd.unique(recs)
    y_rec = np.array([y[recs == r][0] for r in rec_list])
    u_rec = np.array([units[recs == r][0] for r in rec_list])
    rec_pred = {}
    for n in names:
        if n.startswith("rf_"):
            rec_pred[n] = np.array([proba[n][recs == r].mean(0).argmax() for r in rec_list])
        else:
            rec_pred[n] = np.array([np.bincount(pred[n][recs == r], minlength=3).argmax() for r in rec_list])
    ci_r, _ = unit_bootstrap(y_rec, rec_pred, u_rec, n_boot=2000)
    for n in names:
        b = basic(y_rec, rec_pred[n])
        b["balanced_accuracy_ci95"] = ci_r[n]
        summary["recording"][n] = b
        rows.append({"level": "recording", "model": n, "balanced_accuracy": b["balanced_accuracy"],
                     "bacc_ci_lo": ci_r[n][0], "bacc_ci_hi": ci_r[n][1], "macro_f1": b["macro_f1"],
                     "f1_ci_lo": np.nan, "f1_ci_hi": np.nan,
                     "f1_sehat": b["f1_per_class"][0], "f1_waspada": b["f1_per_class"][1],
                     "f1_rusak": b["f1_per_class"][2], "n": b["n"]})
        log(f"[recording] {n:14s} bacc={b['balanced_accuracy']:.3f} CI95=({ci_r[n][0]:.3f},{ci_r[n][1]:.3f}) "
            f"macroF1={b['macro_f1']:.3f} cm={b['confusion']}")
    pd.DataFrame(rows).to_csv(os.path.join(RES, "metrics_summary.csv"), index=False)
    pd.DataFrame({"recording": rec_list, "unit": u_rec, "state": y_rec,
                  **{f"pred_{n}": rec_pred[n] for n in names}}).to_csv(
        os.path.join(RES, "recording_predictions.csv"), index=False)

    # ---------- selective prediction / coverage-risk (window level)
    sel = {}
    cr_rows = []
    for n in ("rf_stat", "rf_spec"):
        conf = proba[n].max(1)
        curve, aurc = coverage_risk(y, pred[n], conf)
        for r in curve:
            cr_rows.append({"model": n, **r})
        a = accept[n]
        sel[n] = {"aurc_error": aurc, "operating_point": {
            "coverage": float(a.mean()),
            "balanced_accuracy_accepted": float(basic(y[a], pred[n][a])["balanced_accuracy"]),
            "error_rate_accepted": float(np.mean(pred[n][a] != y[a])),
            "error_rate_all": float(np.mean(pred[n] != y)),
            "abstain_rate_by_class": [float(1 - a[y == k].mean()) for k in range(3)]}}
        log(f"[selective] {n}: AURC(error)={aurc:.3f} coverage={a.mean():.3f} "
            f"bacc_accepted={sel[n]['operating_point']['balanced_accuracy_accepted']:.3f} "
            f"err_accepted={sel[n]['operating_point']['error_rate_accepted']:.3f} "
            f"err_all={sel[n]['operating_point']['error_rate_all']:.3f} "
            f"abstain_by_class={np.round(sel[n]['operating_point']['abstain_rate_by_class'], 3).tolist()}")
    pd.DataFrame(cr_rows).to_csv(os.path.join(RES, "coverage_risk.csv"), index=False)
    sel["rf_spec"]["snr_gate_abstain_rate_clean"] = float(1 - qual_ok.mean())
    sel["rf_spec"]["abstain_reasons"] = {k: int(v) for k, v in zip(*np.unique(reason, return_counts=True))}
    log(f"[selective] rf_spec SNR-gate abstain on clean windows = {1 - qual_ok.mean():.3f}; reasons={sel['rf_spec']['abstain_reasons']}")
    summary["selective"] = sel

    # ---------- degradation stress test (semi-synthetic: real test windows + added noise)
    rng = np.random.default_rng(123)
    deg_rows = []
    levels = [("bersih", None), ("snr_10dB", 10.0), ("snr_0dB", 0.0), ("snr_-10dB", -10.0), ("sensor_lepas", "detached")]
    for u, (m, gate) in fold_models.items():
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
                acc_mask, rs = gate.decide(Xd, P)
                pr = P.argmax(1)
                for i in range(len(Xd)):
                    deg_rows.append({"unit": u, "recording": r, "state": st, "level": lname, "window": i,
                                     "pred": int(pr[i]), "correct": bool(pr[i] == st), "accept": bool(acc_mask[i]),
                                     "quality_ok": bool(gate.quality_ok(Xd.iloc[[i]])[0]), "reason": rs[i],
                                     "snr_db": float(Xd["shaft_snr_db"].iloc[i])})
    D = pd.DataFrame(deg_rows)
    D.to_csv(os.path.join(RES, "degradation_windows.csv"), index=False)
    agg = []
    for lname, _ in levels:
        d = D[D.level == lname]
        a = d[d.accept]
        agg.append({"level": lname, "n": len(d), "accuracy_no_abstain": d.correct.mean(),
                    "snr_gate_abstain_rate": 1 - d.quality_ok.mean(), "total_abstain_rate": 1 - d.accept.mean(),
                    "accuracy_on_accepted": a.correct.mean() if len(a) else np.nan,
                    "median_snr_db": d.snr_db.median()})
        log(f"[degrade] {lname:12s} acc_no_abstain={agg[-1]['accuracy_no_abstain']:.3f} "
            f"snr_gate_abstain={agg[-1]['snr_gate_abstain_rate']:.3f} total_abstain={agg[-1]['total_abstain_rate']:.3f} "
            f"acc_accepted={agg[-1]['accuracy_on_accepted']:.3f} medianSNR={agg[-1]['median_snr_db']:.1f}")
    pd.DataFrame(agg).to_csv(os.path.join(RES, "degradation_summary.csv"), index=False)
    summary["degradation"] = agg

    # ---------- per-unit deviation mode (own healthy baseline, no cross-unit training)
    from sklearn.metrics import roc_auc_score
    dev_rows = []
    for u in np.unique(units):
        Fu = F[F.unit == u]
        H = Fu[Fu.state == 0].sort_values("window")
        ref, hold = H[H.window < 5], H[H.window >= 5]
        ub = UnitBaseline().fit(ref)
        for part, dfp in (("sehat_holdout", hold), ("waspada", Fu[Fu.state == 1]), ("rusak", Fu[Fu.state == 2])):
            s, s_rms = ub.score(dfp), ub.rms_only(dfp)
            for i in range(len(dfp)):
                dev_rows.append({"unit": int(u), "part": part, "score": float(s[i]), "score_rms_only": float(s_rms[i])})
    DV = pd.DataFrame(dev_rows)
    DV.to_csv(os.path.join(RES, "deviation_scores.csv"), index=False)
    dev_sum = {}
    for col in ("score", "score_rms_only"):
        res = {}
        for tgt in ("waspada", "rusak"):
            d = DV[DV.part.isin(["sehat_holdout", tgt])]
            res[f"auc_pooled_sehat_vs_{tgt}"] = float(roc_auc_score(d.part == tgt, d[col]))
            per = []
            for u in np.unique(DV.unit):
                du = d[d.unit == u]
                per.append(roc_auc_score(du.part == tgt, du[col]))
            res[f"auc_per_unit_median_{tgt}"] = float(np.median(per))
            res[f"units_auc_ge_0.9_{tgt}"] = int(np.sum(np.array(per) >= 0.9))
        med = DV.groupby(["unit", "part"])[col].median().unstack()
        res["units_order_rusak_gt_waspada_gt_sehat"] = int(((med.rusak > med.waspada) & (med.waspada > med.sehat_holdout)).sum())
        res["units_waspada_gt_sehat"] = int((med.waspada > med.sehat_holdout).sum())
        res["n_units"] = int(len(med))
        dev_sum[col] = res
        log(f"[deviation] {col}: {res}")
    summary["deviation_mode"] = dev_sum

    # ---------- plots
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        C = pd.DataFrame(cr_rows)
        fig, ax = plt.subplots(figsize=(6, 4))
        for n, lab in (("rf_stat", "RF fitur statistik (baseline c)"), ("rf_spec", "RF fitur spektral (usulan)")):
            c = C[C.model == n]
            ax.plot(c.coverage, c.error_rate, label=f"{lab}, AURC={sel[n]['aurc_error']:.3f}")
            op = sel[n]["operating_point"]
            ax.scatter([op["coverage"]], [op["error_rate_accepted"]], marker="o")
        ax.set_xlabel("cakupan (fraksi jendela yang dijawab)")
        ax.set_ylabel("tingkat galat pada yang dijawab")
        ax.set_title("Cakupan vs risiko, leave-one-bearing-out (Ottawa)")
        ax.grid(alpha=.3); ax.legend(fontsize=8)
        fig.tight_layout(); fig.savefig(os.path.join(RES, "coverage_risk.png"), dpi=130)
    except Exception as e:  # plotting is optional
        log(f"[plot] skipped: {e}")

    summary["runtime_s"] = time.time() - t0
    with open(os.path.join(RES, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, default=float)
    log(f"[done] {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
