"""Quick survey of the Ottawa MAT files (run from prototype/: .venv python -I scripts/survey_data.py)."""
import glob, os, sys
import numpy as np, scipy.io as sio
from scipy.stats import kurtosis
root = sys.argv[1] if len(sys.argv) > 1 else "data/ottawa_uored_vafcls/mat"
rows = []
for p in sorted(glob.glob(os.path.join(root, "*.mat"))):
    n = os.path.splitext(os.path.basename(p))[0]
    m = sio.loadmat(p); a = m[n]
    acc = a[:, 0] - a[:, 0].mean()
    f = np.fft.rfftfreq(len(acc), 1/42000); P = np.abs(np.fft.rfft(acc * np.hanning(len(acc))))**2
    band = (f > 20) & (f < 40); fs_peak = f[band][np.argmax(P[band])]
    print(f"{n:8s} c2r0={a[0,2]:7.0f} c3r0={a[0,3]:5.0f} nz2={np.count_nonzero(a[:,2])} nz3={np.count_nonzero(a[:,3])} "
          f"accDC={a[:,0].mean():8.2f} accSTD={acc.std():7.2f} kurt={kurtosis(acc):6.2f} micSTD={a[:,1].std():.4f} "
          f"c4med={np.median(a[:,4]):7.2f} peak20-40={fs_peak:6.2f}")
