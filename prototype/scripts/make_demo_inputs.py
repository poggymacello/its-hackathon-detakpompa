"""Make two degraded demo inputs from a real Ottawa recording (semi-synthetic, for the demo only).

  results/demo_inputs/I_3_1_derau_-10dB.npy   real I_3_1 accelerometer + white noise at -10 dB
  results/demo_inputs/sensor_lepas.npy         pure white noise (sensor not coupled to the machine)

File names intentionally do not match the dataset pattern, so demo.py treats them as unknown units
(it then trains on all 20 bearings; the underlying I_3_1 signal IS in that training set, which
does not matter here because the point of these inputs is the SNR abstain, not accuracy).
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402

from detakpompa.io import load_recording  # noqa: E402

out = os.path.join(HERE, "results", "demo_inputs")
os.makedirs(out, exist_ok=True)
x, fs = load_recording(os.path.join(HERE, "data", "ottawa_uored_vafcls", "mat", "I_3_1.mat"))
x = x - x.mean()
rng = np.random.default_rng(42)
np.save(os.path.join(out, "I_3_1_derau_-10dB.npy"), (x + rng.normal(0, x.std() * 10 ** 0.5, len(x))).astype(np.float32))
np.save(os.path.join(out, "sensor_lepas.npy"), rng.normal(0, x.std(), len(x)).astype(np.float32))
print("written to", out)
