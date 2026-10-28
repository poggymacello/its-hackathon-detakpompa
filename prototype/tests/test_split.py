import os

import numpy as np
import pandas as pd
import pytest

from conftest import FEATURES
from detakpompa.splits import assert_no_leakage, grouped_kfold, leave_one_unit_out


def _toy():
    units = np.repeat(np.arange(1, 21), 30)
    recs = np.array([f"r{u}_{k // 10}" for u, k in zip(units, np.tile(np.arange(30), 20))])
    return units, recs


def test_louo_units_disjoint():
    units, recs = _toy()
    seen = []
    for u, tr, te in leave_one_unit_out(units):
        assert set(units[tr]).isdisjoint(set(units[te]))      # train intersect test = empty
        assert set(recs[tr]).isdisjoint(set(recs[te]))
        assert set(units[te]) == {u}
        assert len(tr) + len(te) == len(units)
        seen.append(u)
    assert sorted(seen) == list(range(1, 21))


def test_grouped_kfold_disjoint_and_complete():
    units, _ = _toy()
    test_units = []
    for tu, tr, te in grouped_kfold(units, k=5):
        assert set(units[tr]).isdisjoint(set(units[te]))
        test_units.extend(tu.tolist())
    assert sorted(test_units) == list(range(1, 21))


def test_assert_no_leakage_raises():
    units = np.array([1, 1, 2, 2])
    with pytest.raises(AssertionError):
        assert_no_leakage(units, [0, 2], [1, 3])


@pytest.mark.skipif(not os.path.exists(FEATURES), reason="run run_eval.py first")
def test_real_feature_table_split():
    F = pd.read_csv(FEATURES)
    units, recs = F["unit"].to_numpy(), F["recording"].to_numpy()
    # each recording belongs to exactly one unit -> a unit split implies a recording split
    assert (F.groupby("recording")["unit"].nunique() == 1).all()
    for u, tr, te in leave_one_unit_out(units):
        assert_no_leakage(units, tr, te, recs)
        assert set(units[tr]) & set(units[te]) == set()
