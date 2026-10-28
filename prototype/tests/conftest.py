import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
DATA = os.path.join(ROOT, "data", "ottawa_uored_vafcls", "mat")
FEATURES = os.path.join(ROOT, "results", "features.csv")
