# Deviasi dan catatan proses: run SKAB (PRAREG_SKAB.md, SHA-256 `c29805a2…014e`)

## Urutan kejadian (WIB, 28 Okt 2026)
| Waktu | Kejadian |
|---|---|
| 22:54:19 | `PRAREG_SKAB.md` dibekukan (`PRAREG_SKAB.sha256`). Belum ada data SKAB di disk. |
| ±22:55–23:01 | `detakpompa/hydraulic.py`, `run_skab.py`, `tests/test_skab.py` ditulis dan diuji **hanya pada data sintetis** di scratchpad (bukan SKAB). |
| 23:01:26 | Hash kode pra-data dicatat di `prototype/SKAB_KODE_PRADATA.sha256`. |
| ±23:01 | `git clone --depth 1 https://github.com/waico/SKAB.git data/skab` (commit `b2c0d46c2971dcbfe71e26087b6d231998bb91c2`, 11 Agu 2024). Manifes SHA-256 35 CSV: `manifest_skab_csv.sha256`. |
| ±23:02 | Run #1 **gagal saat memuat data** (`KeyError: ['RateRMS'] not in index`) sebelum fold pertama. Tidak ada angka yang dihasilkan atau dilihat. Hanya baris header CSV yang diperiksa. |
| 23:02–23:06 | Run #2 (setelah D1) = **satu-satunya run analisis**. Hasil: `run_skab_log.txt`, `summary.json`. |
| 23:07 | Diagnostik **post-hoc** (`scripts/skab_posthoc.py`, tidak diprareg) dijalankan atas `points_oof.csv`. |

## D1: nama kolom laju alir (format saja)
- Prareg memakai nama kolom dari README SKAB: `RateRMS`. Header CSV yang sebenarnya: `Volume Flow RateRMS` (35/35 berkas).
- Perubahan: satu baris `rename` di `hydraulic.load_skab`. Tidak ada perubahan model, skor, ambang, kelas, atau endpoint.
- Hash `detakpompa/hydraulic.py`: pra-data `23ea488e…0095` → sesudah D1 `104779ea…9684`. `run_skab.py` dan `tests/test_skab.py` tidak berubah (`defd052e…`, `54f3207d…`).

## Bukan deviasi (sudah diatur prareg §2)
- `anomaly-free.csv` tidak punya kolom `anomaly` → semua barisnya dianggap normal.
- Tidak ada NaN; tidak ada baris yang dibuang. Semua 20 kejadian T dan 7 kejadian F punya label anomali → bukan TIDAK KONKLUSIF.

## Sifat data yang melemahkan asumsi prareg (dicatat, BUKAN diubah)
Ditemukan setelah run (post-hoc, `posthoc_log.txt`):
1. **Tekanan terkuantisasi kasar:** hanya 10 nilai unik di 37.401 baris uji, langkah ±0,328 bar, 55 % baris bernilai 0,055 bar. Model `p ~ f(Q)` (kurva tekanan–debit) praktis tidak punya informasi. Komponen "hidraulik" R pada dasarnya hanya `P_app ~ f(Q)`.
2. **Eksperimen katup direkam di rezim lain:** semua berkas `valve1`/`valve2` berjalan di Q ≈ 32 L/min dan P_app ≈ 226 VA **sepanjang berkas**, termasuk bagian normalnya. Berkas fault (`other/5–9`, `12–13`) berjalan di Q ≈ 125 L/min, P_app ≈ 580 VA. Penutupan katup sendiri hanya menurunkan Q ±6 % (32 → 30 L/min) dan P_app < 1 %.
3. Akibatnya, **skor pada baris NORMAL saja** sudah memisahkan berkas fault dari berkas katup dengan sempurna (AUROC 1,000 untuk R dan B2). AUROC per kejadian di H1 sebagian besar mengukur "sesi/rezim rekaman mana", bukan "throttling atau fault". Ini perancu sesi, mirip catatan Ottawa (README Keterbatasan 4).
4. Throttling di SKAB terlalu kecil untuk menguji klaim "alarm palsu ambang saat titik kerja berubah": tidak ada satu pun metode ambang (B1–B3) yang menandai kejadian katup pada τ (laju tanda 0/20), jadi tidak ada alarm palsu yang bisa dikurangi R.
