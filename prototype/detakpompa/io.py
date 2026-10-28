"""Loader for Ottawa UORED-VAFCLS v5 raw files (and generic CSV/NPY vibration recordings).

File naming in the dataset: <F>_<bearing>_<state>.mat with F in {H, I, O, B, C}
(healthy, inner race, outer race, ball, cage), bearing 1..20, state 0 = healthy,
1 = developing fault, 2 = faulty. Bearings 1-5 inner, 6-10 outer, 11-15 ball, 16-20 cage;
each bearing also has its own healthy file H_<bearing>_0.

Columns (from the dataset authors' code, github.com/Mert-Sehri/1_Bearing_Spectrogram_Dataset_Creation):
0 = accelerometer, 1 = microphone. Columns 2-3 hold a single metadata value in row 0;
column 4 looks like a temperature channel and is NOT used (it rises with fault state and would
act as a shortcut; see README "Keterbatasan").
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass

import numpy as np

from . import FS_OTTAWA

NAME_RE = re.compile(r"^(?P<ftype>[HIOBC])_(?P<unit>\d+)_(?P<state>[012])$")
FAULT_NAMES = {"H": "healthy", "I": "inner", "O": "outer", "B": "ball", "C": "cage"}


@dataclass(frozen=True)
class RecordingInfo:
    name: str
    unit: int      # bearing id = the "unit" used for grouped splitting
    state: int     # 0 sehat, 1 waspada (developing), 2 rusak (faulty)
    ftype: str     # H/I/O/B/C


def parse_name(path_or_name: str) -> RecordingInfo | None:
    name = os.path.splitext(os.path.basename(path_or_name))[0]
    m = NAME_RE.match(name)
    if not m:
        return None
    return RecordingInfo(name, int(m["unit"]), int(m["state"]), m["ftype"])


def load_recording(path: str, channel: int = 0, fs: float | None = None):
    """Return (signal, fs). Supports Ottawa .mat/.csv, a 1-column .csv/.txt, or .npy."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".mat":
        import scipy.io as sio
        m = sio.loadmat(path)
        keys = [k for k in m if not k.startswith("__")]
        arr = np.asarray(m[keys[0]], float)
        x = arr[:, channel] if arr.ndim == 2 else arr.ravel()
        return x, float(fs or FS_OTTAWA)
    if ext in (".csv", ".txt"):
        arr = np.loadtxt(path, delimiter="," if ext == ".csv" else None, ndmin=2)
        x = arr[:, channel] if arr.shape[1] > channel else arr[:, 0]
        return x.astype(float), float(fs or FS_OTTAWA)
    if ext == ".npy":
        return np.load(path, allow_pickle=False).astype(float).ravel(), float(fs or FS_OTTAWA)
    raise ValueError(f"unsupported file type: {ext}")


def windows(x: np.ndarray, fs: float, win_s: float = 1.0):
    """Non-overlapping windows (so no sample is shared between two windows)."""
    n = int(round(win_s * fs))
    k = len(x) // n
    return [x[i * n:(i + 1) * n] for i in range(k)]


def list_dataset(root: str):
    out = []
    for fn in sorted(os.listdir(root)):
        if fn.lower().endswith(".mat"):
            info = parse_name(fn)
            if info is not None:
                out.append((os.path.join(root, fn), info))
    return out
