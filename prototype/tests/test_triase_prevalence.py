"""Realistic-prevalence fleet scenario in run_triase_eval.py (addendum 28 Okt 2026)."""

import numpy as np
import pandas as pd

import run_triase_eval as rte


def _toy_decisions():
    rows = []
    for u in range(1, 7):
        for state in (0, 1, 2):
            sick = state >= 1
            rows.append({"recording": f"X_{u}_{state}", "unit": u, "state": state,
                         "usulan_status": state, "usulan_priority": (0.1 * state + 0.01 * u) if sick else 0.0,
                         "rms_gate_status": state if u != 6 else -1,
                         "rms_gate_priority": (0.2 * state) if (sick and u != 6) else None})
    return pd.DataFrame(rows)


def test_prevalence_fleet_has_fixed_number_of_problem_pumps():
    D = _toy_decisions()
    S = rte.simulate_prevalence(D, n_bad=3, n_pumps=22, n_sim=50, k=3, seed=0)
    assert len(S) == 50
    assert np.allclose(S["base_rate_perlu_cek"], 3 / 22)
    # toy usulan never flags a healthy pump and always flags every problem pump -> perfect top-3
    assert np.allclose(S["usulan_prec_perlu_cek"], 1.0)
    assert np.allclose(S["usulan_catch_at_k"], 1.0)
    assert (S["usulan_n_sehat_in_audit"] == 0).all()
    summ = rte.summarise_prevalence(S)
    assert summ["n_bad"] == 3 and summ["n_fleets"] == 50
    assert summ["usulan_prec_perlu_cek"]["mean"] == 1.0


def test_flagged_requires_priority():
    D = _toy_decisions()
    f = rte._flagged(D, "rms_gate")
    assert not f[(D["unit"] == 6)].any()          # TIDAK TAHU (status -1, no priority) never ranked
    assert f[(D["unit"] == 1) & (D["state"] == 2)].all()
