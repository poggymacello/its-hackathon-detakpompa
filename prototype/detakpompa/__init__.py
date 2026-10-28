"""DetakPompa: triase kondisi motor/pompa dari getaran dengan abstain berbasis SNR.

Purwarupa TKT 3 (proof of concept di data publik nyata, Ottawa UORED-VAFCLS).
Bagian DSP spektral diadaptasi dari FaceVitals (Poggy + Aziz), lihat detakpompa/spectral.py.
"""

FS_OTTAWA = 42000
STATES = ("sehat", "waspada", "rusak")  # healthy / developing fault / faulty
