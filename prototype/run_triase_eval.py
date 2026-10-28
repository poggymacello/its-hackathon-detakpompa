"""Fleet-triage evaluation: top-k precision of the queue table, proposal vs RMS rule + same SNR gate.

Run from prototype/ (after run_eval.py, which caches results/features.csv):
    .venv\\Scripts\\python.exe -I run_triase_eval.py

PROTOCOL (written before the first run of this script; not changed afterwards)
- Unit = one Ottawa bearing (20). "Pump" = one recording (10 s). Labels: 0 sehat, 1 waspada, 2 rusak.
- Leave-one-unit-out (20 folds, assert_no_leakage): for held-out bearing u, both decision makers are
  fitted on the 19 other bearings only, exactly as triase.py does for a file of bearing u:
    usulan   = detakpompa.triage.fit_proposal + decide_proposal (same code as demo.py / triase.py)
    rms_gate = detakpompa.triage.RMSRecordingTriage (RMS rule, same signal gate, rule_margin tau)
  The 3 recordings of u are then decided at recording level. Nothing is tuned on test units:
  RF hyper-parameters fixed, SNR threshold CFAR (no labels), tau from inner grouped 5-fold.
- Queues: detakpompa.triage.assign_queues with audit capacity k = 3 (Lean Canvas KPI "presisi top-3";
  fixed in advance, not chosen from results). TIDAK TAHU never enters AUDIT DULU.
- PRIMARY metric: precision@3 = share of the AUDIT DULU list (<= 3 pumps) whose true label is
  "perlu cek" (waspada or rusak). Fleet simulation: 2000 fleets (seed 0); each fleet = 20 bearings
  drawn WITH replacement (per-unit bootstrap) and one of the bearing's 3 recordings drawn uniformly.
  Expected base rate of "perlu cek" in a fleet = 2/3. Reported: mean and 2.5-97.5 % percentile
  interval for each model, and the paired difference usulan - rms_gate on the same fleets.
- SECONDARY: precision@3 for "rusak" only; number of healthy pumps in AUDIT DULU; share of
  perlu-cek pumps that land in UKUR ULANG and in AMAN (missed); and the whole data set as one
  fleet of 60 recordings at k = 3, 5, 10 (no interval). All exploratory: 20 bearings, data seen.
Writes results/triase/eval_*.csv, eval_summary.json, eval_log.txt.

ADDENDUM 28 Okt 2026 ~21:45 WIB: realistic-prevalence scenario (`--prevalensi`). Written before this
scenario was run by the team; motivated by panel critique JURI_90/SKOR.md E2 (the primary fleets above
are 2/3 "perlu cek", but in a real IPA most pumps are healthy). No model, gate, tau or k is changed:
it re-uses the SAME leave-one-unit-out recording decisions (eval_recording_decisions.csv, written by
the primary run) and the same assign_queues/topk_metrics.
- Fleet = 22 pumps with a FIXED number of problem pumps n_bad in {3, 5} (base rate 3/22 = 0.136,
  5/22 = 0.227). Each healthy slot: a bearing drawn with replacement among bearings that have a
  healthy recording, then one of its healthy recordings uniformly; each problem slot: a bearing drawn
  with replacement, then one of its waspada/rusak recordings uniformly (per-unit bootstrap, as above).
- 5000 fleets per scenario (seed 0). Reported per model: precision@3 "perlu cek" (mean and 2.5-97.5 %
  interval over fleets with a non-empty AUDIT DULU list), share of fleets with >= 1 healthy pump in
  AUDIT DULU, catch@3 = problem pumps in AUDIT DULU / min(3, n_bad), share of fleets with an empty
  AUDIT DULU list; paired difference usulan - rms_gate on the same fleets. Also listed: which healthy
  recordings each model flags (WASPADA/RUSAK with a priority) in the LOUO decisions.
- Exploratory, like everything in this file: 20 bearings (20 healthy recordings), data seen.
Writes results/triase/eval_prevalensi.csv, eval_prevalensi_summary.json, eval_prevalensi_log.txt.
Run only the scenario (needs eval_recording_decisions.csv):  python -I run_triase_eval.py --prevalensi
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

from detakpompa import FS_OTTAWA  # noqa: E402
from detakpompa.models import AbstainGate  # noqa: E402
from detakpompa.pipeline import snr_cfar_threshold  # noqa: E402
from detakpompa.splits import assert_no_leakage, leave_one_unit_out  # noqa: E402
from detakpompa.triage import (QUEUES, RMSRecordingTriage, assign_queues, decide_proposal,  # noqa: E402
                               fit_proposal, topk_metrics)

OUT = os.path.join(HERE, "results", "triase")
MODELS = ("usulan", "rms_gate")
K, N_FLEET, N_SIM, SEED = 3, 20, 2000, 0
PREV_N_PUMPS, PREV_N_BAD, PREV_N_SIM = 22, (3, 5), 5000


def loo_recording_decisions(F: pd.DataFrame, snr_min: float, log=print) -> pd.DataFrame:
    gate = AbstainGate(snr_min=snr_min)
    units, rec = F["unit"].to_numpy(), F["recording"].to_numpy()
    rows = []
    for u, tr, te in leave_one_unit_out(units):
        assert_no_leakage(units, tr, te, rec)
        Ftr, Fte = F.iloc[tr].reset_index(drop=True), F.iloc[te].reset_index(drop=True)
        model, tau = fit_proposal(Ftr)
        rms = RMSRecordingTriage().fit(Ftr)
        for name in pd.unique(Fte["recording"]):
            X = Fte[Fte["recording"] == name].reset_index(drop=True)
            ok = gate.quality_ok(X)
            dp = decide_proposal(ok, model.predict_proba(X), tau)
            dr = rms.decide(X, ok)
            rows.append({"recording": name, "unit": int(u), "state": int(X["state"].iloc[0]),
                         "n_ok": int(ok.sum()), "n_windows": int(len(ok)),
                         "usulan_status": dp["status"], "usulan_reason": dp["abstain_reason"],
                         "usulan_priority": dp["priority"], "usulan_conf": dp["conf"], "usulan_tau": tau,
                         "rms_gate_status": dr["status"], "rms_gate_reason": dr["abstain_reason"],
                         "rms_gate_priority": dr["priority"], "rms_gate_conf": dr["conf"], "rms_gate_tau": rms.tau,
                         "rms_median": dr["rms_median"]})
        log(f"[fold] unit {u:2d}: tau usulan {tau:.3f}, tau rms {rms.tau:.3f}")
    return pd.DataFrame(rows)


def fleet_rows(D: pd.DataFrame, idx, model: str):
    out = []
    for i, j in enumerate(idx):
        r = D.iloc[j]
        pr = r[f"{model}_priority"]
        out.append({"name": f"{r['recording']}#{i}", "status": int(r[f"{model}_status"]),
                    "priority": None if pd.isna(pr) else float(pr)})
    return out


def labels_for(D, idx):
    return {f"{D.iloc[j]['recording']}#{i}": int(D.iloc[j]["state"]) for i, j in enumerate(idx)}


def simulate(D: pd.DataFrame, n_sim=N_SIM, k=K, seed=SEED):
    rng = np.random.default_rng(seed)
    uniq = np.unique(D["unit"])
    by_u = {u: np.flatnonzero(D["unit"].to_numpy() == u) for u in uniq}
    res = []
    for s in range(n_sim):
        draw = rng.choice(uniq, N_FLEET, replace=True)
        idx = [int(rng.choice(by_u[u])) for u in draw]
        lab = labels_for(D, idx)
        row = {"sim": s, "base_rate_perlu_cek": float(np.mean([v >= 1 for v in lab.values()]))}
        for m in MODELS:
            met = topk_metrics(assign_queues(fleet_rows(D, idx, m), k=k), lab, k=k)
            row.update({f"{m}_{key}": v for key, v in met.items()})
        res.append(row)
    return pd.DataFrame(res)


def summarise(S: pd.DataFrame):
    keys = ("prec_perlu_cek", "prec_rusak", "n_sehat_in_audit", "fault_to_ukur_ulang", "fault_to_aman", "n_audit")
    out = {}
    for key in keys:
        for m in MODELS:
            v = S[f"{m}_{key}"].to_numpy(float)
            v = v[~np.isnan(v)]
            out[f"{m}_{key}"] = {"mean": float(v.mean()), "lo": float(np.percentile(v, 2.5)),
                                 "hi": float(np.percentile(v, 97.5)), "n": int(len(v))}
        d = (S[f"usulan_{key}"] - S[f"rms_gate_{key}"]).to_numpy(float)
        d = d[~np.isnan(d)]
        out[f"diff_{key}"] = {"mean": float(d.mean()), "lo": float(np.percentile(d, 2.5)),
                              "hi": float(np.percentile(d, 97.5)), "share_le_0": float(np.mean(d <= 0)),
                              "share_eq_0": float(np.mean(d == 0)), "n": int(len(d))}
    out["base_rate_perlu_cek"] = float(S["base_rate_perlu_cek"].mean())
    return out


def whole_fleet(D: pd.DataFrame):
    rows, tables = [], {}
    idx = list(range(len(D)))
    lab = labels_for(D, idx)
    for m in MODELS:
        for k in (3, 5, 10):
            q = assign_queues(fleet_rows(D, idx, m), k=k)
            rows.append({"model": m, "k": k, **topk_metrics(q, lab, k=k)})
        q = assign_queues(fleet_rows(D, idx, m), k=K)
        t = pd.crosstab(pd.Series([r["queue"] for r in q], name="antrean"),
                        pd.Series([("sehat", "waspada", "rusak")[lab[r["name"]]] for r in q], name="label_asli"))
        tables[m] = t.reindex(index=list(QUEUES), columns=["sehat", "waspada", "rusak"], fill_value=0)
    return pd.DataFrame(rows), tables


def _flagged(D: pd.DataFrame, m: str) -> pd.Series:
    """Recording enters the audit ranking (WASPADA/RUSAK with a priority), as in assign_queues."""
    return D[f"{m}_status"].isin([1, 2]) & D[f"{m}_priority"].notna()


def simulate_prevalence(D: pd.DataFrame, n_bad: int, n_pumps: int = PREV_N_PUMPS, n_sim: int = PREV_N_SIM,
                        k: int = K, seed: int = SEED) -> pd.DataFrame:
    """Fleets of n_pumps with exactly n_bad problem pumps (state >= 1); see ADDENDUM in the docstring."""
    rng = np.random.default_rng(seed)
    st, un = D["state"].to_numpy(), D["unit"].to_numpy()
    by_h = {u: np.flatnonzero((un == u) & (st == 0)) for u in np.unique(un[st == 0])}
    by_f = {u: np.flatnonzero((un == u) & (st >= 1)) for u in np.unique(un[st >= 1])}
    uh, uf = np.array(sorted(by_h)), np.array(sorted(by_f))
    res = []
    for s in range(n_sim):
        idx = [int(rng.choice(by_h[u])) for u in rng.choice(uh, n_pumps - n_bad, replace=True)]
        idx += [int(rng.choice(by_f[u])) for u in rng.choice(uf, n_bad, replace=True)]
        lab = labels_for(D, idx)
        row = {"sim": s, "n_bad": n_bad, "base_rate_perlu_cek": n_bad / n_pumps}
        for m in MODELS:
            q = assign_queues(fleet_rows(D, idx, m), k=k)
            met = topk_metrics(q, lab, k=k)
            audit = [r for r in q if r["queue"] == QUEUES[0]][:k]
            n_hit = sum(lab[r["name"]] >= 1 for r in audit)
            row.update({f"{m}_{key}": v for key, v in met.items()})
            row[f"{m}_catch_at_k"] = n_hit / min(k, n_bad)
            row[f"{m}_any_sehat_in_audit"] = float(met["n_sehat_in_audit"] > 0)
            row[f"{m}_audit_empty"] = float(met["n_audit"] == 0)
        res.append(row)
    return pd.DataFrame(res)


def summarise_prevalence(S: pd.DataFrame) -> dict:
    out = {"n_bad": int(S["n_bad"].iloc[0]), "base_rate_perlu_cek": float(S["base_rate_perlu_cek"].iloc[0]),
           "n_fleets": int(len(S))}
    for key in ("prec_perlu_cek", "prec_rusak", "catch_at_k", "any_sehat_in_audit", "n_sehat_in_audit",
                "audit_empty", "n_audit"):
        for m in MODELS:
            v = S[f"{m}_{key}"].to_numpy(float)
            v = v[~np.isnan(v)]
            out[f"{m}_{key}"] = {"mean": float(v.mean()), "lo": float(np.percentile(v, 2.5)),
                                 "hi": float(np.percentile(v, 97.5)), "n": int(len(v))}
        d = (S[f"usulan_{key}"] - S[f"rms_gate_{key}"]).to_numpy(float)
        d = d[~np.isnan(d)]
        out[f"diff_{key}"] = {"mean": float(d.mean()), "lo": float(np.percentile(d, 2.5)),
                              "hi": float(np.percentile(d, 97.5)), "share_eq_0": float(np.mean(d == 0)),
                              "share_gt_0": float(np.mean(d > 0)), "share_lt_0": float(np.mean(d < 0)),
                              "n": int(len(d))}
    return out


def run_prevalence(D: pd.DataFrame, log=print) -> dict:
    H = D[D["state"] == 0]
    flagged = {m: sorted(H.loc[_flagged(H, m), "recording"]) for m in MODELS}
    both = sorted(set(flagged["usulan"]) & set(flagged["rms_gate"]))
    log(f"PREVALENSI REALISTIS: armada {PREV_N_PUMPS} pompa, {PREV_N_SIM} armada per skenario (seed {SEED}), "
        f"keputusan LOUO yang sama (eval_recording_decisions.csv), k = {K}")
    log(f"  rekaman sehat yang ditandai (WASPADA/RUSAK + prioritas), dari {len(H)}: "
        f"usulan {flagged['usulan']}, rms_gate {flagged['rms_gate']}; ditandai keduanya: {both}")
    for m in MODELS:
        F = D[D["state"] >= 1]
        log(f"  rekaman perlu-cek yang masuk peringkat audit, {m}: {int(_flagged(F, m).sum())}/{len(F)}")
    summ = {"protocol": (f"{PREV_N_SIM} fleets x {PREV_N_PUMPS} pumps, fixed n_bad in {list(PREV_N_BAD)}; per-unit "
                         f"bootstrap of healthy and problem slots; same LOUO recording decisions; k={K}; seed {SEED}"),
            "healthy_flagged": flagged, "healthy_flagged_by_both": both, "scenarios": {}}
    sims = []
    for nb in PREV_N_BAD:
        S = simulate_prevalence(D, nb)
        sims.append(S)
        s = summarise_prevalence(S)
        summ["scenarios"][str(nb)] = s
        log("")
        log(f"  {nb}/{PREV_N_PUMPS} pompa bermasalah (dasar acak {s['base_rate_perlu_cek']:.3f})")
        for key in ("prec_perlu_cek", "prec_rusak", "catch_at_k", "any_sehat_in_audit", "audit_empty"):
            a, b, d = s[f"usulan_{key}"], s[f"rms_gate_{key}"], s[f"diff_{key}"]
            log(f"    {key:20s} usulan {a['mean']:.3f} [{a['lo']:.3f}; {a['hi']:.3f}]  rms_gate {b['mean']:.3f} "
                f"[{b['lo']:.3f}; {b['hi']:.3f}]  selisih {d['mean']:+.3f} [{d['lo']:+.3f}; {d['hi']:+.3f}] "
                f"(seri {d['share_eq_0']:.2f}; selisih > 0 di {d['share_gt_0']:.2f}, < 0 di {d['share_lt_0']:.2f} armada)")
    pd.concat(sims, ignore_index=True).to_csv(os.path.join(OUT, "eval_prevalensi.csv"), index=False)
    with open(os.path.join(OUT, "eval_prevalensi_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summ, fh, indent=2)
    return summ


def main_prevalence():
    t0 = time.time()
    lines = []

    def log(s=""):
        print(s)
        lines.append(str(s))

    D = pd.read_csv(os.path.join(OUT, "eval_recording_decisions.csv"))
    run_prevalence(D, log)
    log("")
    log(f"runtime {time.time() - t0:.0f} s")
    with open(os.path.join(OUT, "eval_prevalensi_log.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    lines = []

    def log(s=""):
        print(s)
        lines.append(str(s))

    F = pd.read_csv(os.path.join(HERE, "results", "features.csv"))
    snr_min = snr_cfar_threshold(float(FS_OTTAWA))
    log(f"features: {len(F)} windows, {F['recording'].nunique()} recordings, {F['unit'].nunique()} units; "
        f"SNR gate {snr_min:.2f} dB; k = {K}; fleets {N_SIM} x {N_FLEET} bearings (seed {SEED})")
    D = loo_recording_decisions(F, snr_min, log)
    D.to_csv(os.path.join(OUT, "eval_recording_decisions.csv"), index=False)
    for m in MODELS:
        st = D[f"{m}_status"]
        log(f"[rekaman] {m}: dijawab {int((st >= 0).sum())}/60, TIDAK TAHU sinyal "
            f"{int((D[f'{m}_reason'] == 'sinyal').sum())}, ragu {int((D[f'{m}_reason'] == 'ragu').sum())}; "
            f"status benar pada yang dijawab {int((st[st >= 0] == D['state'][st >= 0]).sum())}/{int((st >= 0).sum())}")
    S = simulate(D)
    S.to_csv(os.path.join(OUT, "eval_fleet_sim.csv"), index=False)
    summ = summarise(S)
    W, tables = whole_fleet(D)
    W.to_csv(os.path.join(OUT, "eval_whole_fleet.csv"), index=False)
    log("")
    log(f"PRIMER presisi@{K} (perlu cek) di {N_SIM} armada simulasi; dasar acak = {summ['base_rate_perlu_cek']:.3f}")
    for key in ("prec_perlu_cek", "prec_rusak", "n_sehat_in_audit", "fault_to_ukur_ulang", "fault_to_aman", "n_audit"):
        a, b, d = summ[f"usulan_{key}"], summ[f"rms_gate_{key}"], summ[f"diff_{key}"]
        log(f"  {key:20s} usulan {a['mean']:.3f} [{a['lo']:.3f}; {a['hi']:.3f}]  rms_gate {b['mean']:.3f} "
            f"[{b['lo']:.3f}; {b['hi']:.3f}]  selisih {d['mean']:+.3f} [{d['lo']:+.3f}; {d['hi']:+.3f}] "
            f"(seri {d['share_eq_0']:.2f})")
    log("")
    log("SEKUNDER: seluruh 60 rekaman sebagai satu armada")
    log(W.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    for m, t in tables.items():
        log(f"\nantrean x label asli, {m}, k = {K} (60 rekaman):")
        log(t.to_string())
        t.to_csv(os.path.join(OUT, f"eval_whole_fleet_queues_{m}.csv"))
    summ["runtime_s"] = time.time() - t0
    summ["protocol"] = (f"LOUO 20 folds; recording-level; k={K}; {N_SIM} fleets of {N_FLEET} bearings drawn with "
                        f"replacement, one random recording each (seed {SEED}); identical SNR gate {snr_min:.2f} dB")
    with open(os.path.join(OUT, "eval_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summ, fh, indent=2)
    log(f"\nruntime {summ['runtime_s']:.0f} s")
    with open(os.path.join(OUT, "eval_log.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    if "--prevalensi" in sys.argv[1:]:
        main_prevalence()
    else:
        main()
        main_prevalence()
