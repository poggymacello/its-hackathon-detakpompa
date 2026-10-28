import os

import numpy as np
import pytest

from conftest import DATA
from detakpompa.io import list_dataset, load_recording, parse_name, windows


def test_parse_name():
    i = parse_name("some/dir/I_3_1.mat")
    assert (i.unit, i.state, i.ftype) == (3, 1, "I")
    assert parse_name("H_17_0").state == 0
    assert parse_name("random_file.csv") is None


def test_windows_do_not_overlap():
    x = np.arange(42000 * 3 + 100, dtype=float)
    ws = windows(x, 42000, 1.0)
    assert len(ws) == 3
    assert ws[0][-1] + 1 == ws[1][0]          # contiguous, disjoint
    assert sum(len(w) for w in ws) == 3 * 42000


def test_csv_roundtrip(tmp_path):
    x = np.sin(np.linspace(0, 100, 5000))
    p = tmp_path / "rek.csv"
    np.savetxt(p, np.c_[x, x * 0], delimiter=",")
    y, fs = load_recording(str(p), fs=1000)
    assert fs == 1000 and np.allclose(x, y)


@pytest.mark.skipif(not os.path.isdir(DATA), reason="dataset not downloaded")
def test_ottawa_files():
    items = list_dataset(DATA)
    assert len(items) == 60
    units = {i.unit for _, i in items}
    assert units == set(range(1, 21))
    # every bearing has exactly one healthy, one developing and one faulty recording
    for u in units:
        assert sorted(i.state for _, i in items if i.unit == u) == [0, 1, 2]
    x, fs = load_recording(items[0][0])
    assert fs == 42000 and len(x) == 420000
