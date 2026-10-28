import os
import re

import numpy as np
import pytest

import demo
from conftest import DATA, FEATURES
from detakpompa.report import energy_note

needs_feat = pytest.mark.skipif(not os.path.exists(FEATURES), reason="run run_eval.py first")


def test_energy_note_is_labelled_scenario_and_sourced():
    txt = "\n".join(energy_note())
    assert "SKENARIO, BUKAN PENGUKURAN" in txt
    assert "S6" in txt and "S10" in txt
    assert "TIDAK mengukur efisiensi" in txt
    # only sourced percentages (+ the two arithmetic ones derived from S10) may appear
    pcts = set(re.findall(r"(\d+[.,]?\d*) %", txt))
    assert pcts <= {"24.37", "49.77", "65.2", "53.6", "5.6", "11.0"}, pcts


@needs_feat
def test_demo_noise_file_says_tidak_tahu(tmp_path):
    p = tmp_path / "lepas.npy"
    np.save(p, np.random.default_rng(0).normal(size=10 * 42000))
    r = demo.analyse(str(p))
    assert r["status"] == -1 and r["abstain_reason"] == "sinyal"
    assert "Ukur ulang 30 detik" in r["next_step"]
    assert "LANGKAH BERIKUTNYA" in demo.format_report(r)


@needs_feat
def test_demo_short_file(tmp_path):
    p = tmp_path / "pendek.npy"
    np.save(p, np.zeros(1000))
    r = demo.analyse(str(p))
    assert r["status"] == -1 and r["abstain_reason"] == "pendek"


@needs_feat
@pytest.mark.skipif(not os.path.isdir(DATA), reason="dataset not downloaded")
def test_demo_excludes_own_unit(monkeypatch):
    seen = {}
    real = demo.fit_model

    def spy(F):
        seen["units"] = set(F["unit"])
        return real(F)

    monkeypatch.setattr(demo, "fit_model", spy)
    r = demo.analyse(os.path.join(DATA, "I_3_1.mat"))
    assert 3 not in seen["units"] and len(seen["units"]) == 19
    assert r["unit_note"] and r["status"] in (-1, 0, 1, 2)
    txt = demo.format_report(r)
    assert "LAPORAN KESEHATAN POMPA" in txt and "SKENARIO, BUKAN PENGUKURAN" in txt
