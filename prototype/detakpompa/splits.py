"""Leakage-free splits: every fold holds out ALL windows of one (or more) physical units.

A "unit" is one bearing of the Ottawa rig (bearing id 1..20). The healthy, developing and
faulty recordings of a bearing, and every window cut from them, always land on the same side.
"""

from __future__ import annotations

import numpy as np


def leave_one_unit_out(units: np.ndarray):
    units = np.asarray(units)
    for u in np.unique(units):
        test = np.flatnonzero(units == u)
        train = np.flatnonzero(units != u)
        yield u, train, test


def grouped_kfold(units: np.ndarray, k: int = 5, seed: int = 0):
    """Group k-fold over units with a fixed shuffled unit order."""
    units = np.asarray(units)
    uniq = np.unique(units)
    rng = np.random.default_rng(seed)
    order = rng.permutation(uniq)
    for i in range(k):
        test_units = order[i::k]
        test = np.flatnonzero(np.isin(units, test_units))
        train = np.flatnonzero(~np.isin(units, test_units))
        yield test_units, train, test


def assert_no_leakage(units: np.ndarray, train_idx, test_idx, recordings: np.ndarray | None = None):
    units = np.asarray(units)
    inter = set(units[train_idx]) & set(units[test_idx])
    if inter:
        raise AssertionError(f"unit leakage between train and test: {sorted(inter)}")
    if recordings is not None:
        recordings = np.asarray(recordings)
        r = set(recordings[train_idx]) & set(recordings[test_idx])
        if r:
            raise AssertionError(f"recording leakage: {sorted(r)[:5]}")
