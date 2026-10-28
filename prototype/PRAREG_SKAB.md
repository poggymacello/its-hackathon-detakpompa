# PRAREG-SKAB v1: eksplorasi terencana "residual hidraulik" di data lab pompa SKAB

**Ditulis:** 28 Okt 2026, ±22:55 WIB, **sebelum** data SKAB diunduh atau dibuka. Yang sudah dibaca: README repo (`https://github.com/waico/SKAB`), `data/README.md`, gambar `docs/pictures/testbed.png`, `core/utils.py` (cara memuat CSV: `sep=";"`, indeks `datetime`), README notebook, dan metadata pohon repo dari GitHub API (nama berkas + ukuran byte). **Tidak ada** isi CSV yang dibuka. Tidak ada paper posisi SKAB yang sudah terbit (README: "currently submitted for publication"); laju sampel 1 Hz hanya dari sumber sekunder (blog + `11_RISET_KELEMAHAN.md` [cuplikan]).

**Status terhadap PRAREG-TKT4 v2 (`PRAREG_TKT4.md`, SHA-256 `406e8025…abac`):** dokumen ini **bukan** addendum PRAREG v2 dan **tidak** menggantikan P1/P2.
- P1 (H-AI1) butuh ≥ 8 unit fisik; P2 (H-AI2) butuh ≥ 3 unit fisik. SKAB hanya punya **1 testbed** (1 pompa). Uji konfirmatori P1/P2 **tidak bisa dijalankan** di SKAB → menurut PRAREG v2 §7 statusnya **TIDAK KONKLUSIF / belum teruji** dan tetap begitu apa pun hasil dokumen ini.
- Model terkunci PRAREG v2 (`proposed_rf`, fitur spektral getaran) juga tidak bisa dijalankan: SKAB hanya menyimpan RMS akselerometer pada ±1 Hz, bukan sinyal getaran mentah.
- Hasil di sini adalah **eksplorasi terencana** dengan keluarga uji sendiri. Hasil ini tidak boleh dipakai untuk menyatakan "PRAREG v2 lulus".

## 1. Pertanyaan

Inti AI yang dianjurkan `11_RISET_KELEMAHAN.md` §2–§3: throttling katup menggeser titik kerja **sepanjang** kurva pompa; fault menggeser **kurvanya** (atau, untuk fault mekanik, menaikkan getaran pada titik kerja yang sama). Model "perilaku normal bersyarat titik kerja" seharusnya memberi residual kecil saat throttling dan residual besar saat fault, sedangkan ambang per sensor bereaksi pada keduanya.

- **H1 (throttling vs fault pompa).** Skor residual model R membedakan kejadian *penutupan katup* (throttling = perubahan titik kerja, **bukan** fault pompa) dari kejadian *fault pompa* (imbalance rotor, kavitasi) lebih baik daripada **setiap** baseline ambang sederhana B1–B3.
- **H2 (deteksi anomali umum).** Skor R mendeteksi titik anomali (label SKAB apa adanya) lebih baik daripada **setiap** baseline B1–B3.

Catatan fisika yang ditulis **sebelum** melihat data: `valve1` = katup di **inlet** pompa. Menutup katup isap menurunkan tekanan isap (NPSH tersedia turun), sehingga tekanan buang ikut turun dan bisa memicu kavitasi. Jadi `valve1` **bukan** throttling murni sepanjang kurva. Throttling murni adalah `valve2` (katup **outlet**). Kami tetap memakai `valve1 ∪ valve2` sebagai kelas throttling primer sesuai pertanyaan pengguna dan `11_RISET` §7.2, dan melaporkan `valve2` saja sebagai sekunder S1. Prediksi kami sebelum data: R lebih mungkin berhasil pada `valve2` daripada `valve1`.

## 2. Data, unit, split

- **Dataset:** SKAB v0.9, `https://github.com/waico/SKAB` (GPL-3.0), folder `data/`: `anomaly-free/anomaly-free.csv`, `valve1/0..15.csv` (16), `valve2/0..3.csv` (4), `other/1..14.csv` (14). Total 34 berkas eksperimen + 1 berkas bebas anomali.
- **Unit analisis = berkas eksperimen (run).** ID = `<folder>/<nama>` (mis. `valve1/3`). `anomaly-free` **selalu** di sisi latih, tidak pernah diuji.
- **Split: leave-one-experiment-out (LOEO), 34 fold.** Untuk berkas uji *f*: data latih = `anomaly-free.csv` + baris `anomaly == 0` dari 33 berkas lain. Tidak ada baris *f* di data latih. `detakpompa.splits.assert_no_leakage` dipanggil tiap fold atas ID eksperimen. Tidak ada tuning di data uji: semua hiperparameter di bawah tetap; ambang τ dari data latih.
- **Kolom** (README): `Accelerometer1RMS`, `Accelerometer2RMS` (g), `Current` (A), `Pressure` (bar, setelah pompa), `Temperature` (°C, badan motor), `Thermocouple` (°C, fluida), `Voltage` (V), `RateRMS` (L/min), `anomaly`, `changepoint`. Turunan: **`P_app = Voltage × Current`** (VA, daya semu; cos φ tidak ada).
- Berkas dibaca dengan `pd.read_csv(sep=";", index_col="datetime", parse_dates=True)`. Bila `anomaly-free.csv` tidak punya kolom `anomaly`, semua barisnya dianggap normal. Baris dengan NaN di kolom yang dipakai dibuang (jumlah dicatat di log).
- **Kejadian (event)** = semua baris `anomaly == 1` dalam satu berkas (README: satu anomali per berkas; bila ada beberapa segmen, gabungannya dianggap satu kejadian). Berkas tanpa baris anomali dikeluarkan dari analisis kejadian dan dicatat.

**Kelas untuk H1 (ditetapkan sekarang dari `data/README.md`):**
| Kelas | Berkas | n kejadian | Arti |
|---|---|---|---|
| T (throttling, "tidak perlu cek pompa") | `valve1/0..15`, `valve2/0..3` | 20 | katup inlet/outlet ditutup |
| F (fault pompa, "perlu cek") | `other/5..9` (imbalance rotor, 5 profil), `other/12..13` (kavitasi) | 7 | fault pompa |
| X (proses/sistem, tidak masuk H1 primer) | `other/1..4` (bocor/tambah fluida), `other/10..11` (tambah volume air), `other/14` (air panas) | 7 | perubahan sistem, bukan fault pompa, bukan throttling murni |

## 3. Metode (semuanya dilatih ulang per fold hanya di data latih fold itu)

**Model usulan R ("R-fis2", residual hidraulik + getaran bersyarat titik kerja).** Titik kerja: `Q = RateRMS`, `p = Pressure`. Empat regresi, masing-masing `StandardScaler → PolynomialFeatures(degree=2, include_bias=False) → Ridge(alpha=1.0)` (bentuk kurva pompa kuadratik):
1. `P_app ~ poly2(Q, p)` (daya harapan pada titik kerja yang sama),
2. `p ~ poly2(Q)` (kurva tekanan–debit pompa),
3. `Accelerometer1RMS ~ poly2(Q, p)`,
4. `Accelerometer2RMS ~ poly2(Q, p)`.

Residual distandarkan: `z_k = (y_k − ŷ_k) / s_k`, `s_k = 1,4826 · MAD` residual latih (bila 0, pakai simpangan baku; batas bawah 1e-9). **Skor titik** `S_R = sqrt(mean_k z_k²)`. Tanpa klipping input (kurva fisika diekstrapolasi apa adanya).

**Baseline ambang sederhana** (z robust per sensor, median/MAD dari baris normal latih yang sama):
- **B1 getaran:** `max(|z_Acc1|, |z_Acc2|)` (analog RMS getaran).
- **B2 arus:** `|z_Current|`.
- **B3 z-maks per sensor:** `max |z|` atas 8 sensor mentah (Acc1, Acc2, Current, Pressure, Temperature, Thermocouple, Voltage, RateRMS).

**Sama untuk semua metode:** skor titik dihaluskan dengan rata-rata bergulir kausal 5 sampel di dalam berkas (`min_periods=1`). **Ambang τ_m** = kuantil 0,99 skor halus pada baris normal latih fold itu. **Skor kejadian** = median skor halus atas baris kejadian. Keputusan kejadian "perlu cek" = skor kejadian > τ_m.

## 4. Endpoint primer (keluarga primer, m = 2, Holm, α satu sisi 0,025)

| # | Endpoint | Himpunan | Metrik |
|---|---|---|---|
| **H1** | throttling vs fault | 27 kejadian: F (positif, 7) vs T (negatif, 20), skor kejadian OOF | AUROC per kejadian |
| **H2** | deteksi anomali umum | semua baris 34 berkas uji, OOF, label `anomaly` | AUROC titik (pooled) |

**Uji.** Untuk tiap baseline B_j: Δ_j = AUROC(R) − AUROC(B_j). Bootstrap berpasangan, B = 10.000, seed 0. H1: ambil ulang kejadian dengan pengembalian **di dalam tiap kelas** (stratifikasi F/T). H2: ambil ulang **berkas eksperimen** (34) dengan pengembalian, semua baris berkas terambil ikut. p satu sisi_j = (1 + #{Δ*_j ≤ 0}) / (B + 1). CI 95 % persentil dua sisi. Karena H_k menuntut R mengalahkan **setiap** baseline (uji intersection–union), **p_Hk = max_j p_j**. Holm m = 2: p terkecil < 0,0125, berikutnya < 0,025.

## 5. Pengaman (wajib agar LULUS)
- **G-H1:** recall kejadian F pada τ_R (skor kejadian > τ_R) ≥ 0,5 (≥ 4 dari 7). Mencegah AUROC tinggi dari model yang tidak pernah menandai fault.
- **G-H2:** laju alarm palsu titik (baris normal berkas uji yang melewati τ) R ≤ FAR B3 + 0,05 (estimasi titik).

**H_k LULUS** bila ditolak Holm **dan** pengamannya terpenuhi. **GAGAL** bila tidak. **TIDAK KONKLUSIF** bila: < 10 kejadian T atau < 5 kejadian F punya label anomali; uji kebocoran gagal; atau suatu metode tidak bisa dihitung tanpa mengubah definisi di atas.

## 6. Sekunder (semua dilaporkan; tidak mengubah status primer)
Tiap baris: Δ AUROC R − B_j (j = 1..3) dengan CI 95 %, bootstrap B = 2.000, seed 0, skema ambil ulang sama dengan primer. Semua p sekunder (dua sisi) dikoreksi Holm bersama, α = 0,05.
- **S1** H1 dengan T = `valve2` saja (throttling outlet murni, 4 kejadian).
- **S2** H1 dengan T = `valve1` saja (16).
- **S3** H1 dengan F' = F ∪ X (14 kejadian) vs T.
- **S4** varian **R-sehat**: data latih R juga memuat baris anomali dari berkas `valve1/valve2` **latih** sebagai "pompa sehat" (konvensi label PRAREG v2: titik operasi berubah = sehat). Baseline tetap seperti primer. Endpoint H1.
- **S5** varian **R-GBM**: tiap regresi diganti `HistGradientBoostingRegressor(max_iter=200, learning_rate=0.1, random_state=0)`. Endpoint H1 dan H2.
- **S6** skor **hidraulik saja** `sqrt(mean(z_P², z_p²))`. Endpoint H1.
- **S7** balanced accuracy per kejadian pada τ (himpunan H1), tiap metode (dilaporkan nilai + CI, tanpa uji).
- **S8** F1, FAR, MAR titik pada τ (himpunan H2), tiap metode (nilai saja).
- **S9** H2 tanpa berkas `valve1/valve2` (14 berkas).
- **S10** **pemusatan ulang per run tanpa label**: untuk tiap berkas uji, tiap komponen z (residual R atau z sensor baseline) dikurangi median-nya di 120 baris pertama berkas itu, lalu skor dihitung ulang (τ dihitung dengan cara yang sama di baris normal latih yang juga dipusatkan per berkas). Endpoint H1 dan H2.

**Deskriptif (tanpa uji):** median z per target R untuk tiap kelas (T-valve1, T-valve2, imbalance, kavitasi, X), untuk memeriksa apakah throttling benar bergerak "sepanjang kurva" (z_P, z_p ≈ 0). Figur ruang Q–p dan Q–P_app: titik normal, throttling, fault, dan kurva model.

Perbandingan dengan leaderboard SKAB **tidak** apel-ke-apel: leaderboard melatih tiap berkas pada 400 baris pertama berkas itu sendiri; kami LOEO tanpa data berkas uji.

## 7. Aturan pelaporan
- Satu run analisis. Semua angka primer dan sekunder dilaporkan, termasuk yang merugikan R.
- Keputusan yang terpaksa diubah setelah melihat data (format kolom, kolom hilang, berkas rusak) dicatat sebagai **deviasi** di `results\skab\DEVIASI.md` dengan alasan; perubahan yang menyentuh model, skor, ambang, kelas, atau endpoint **dilarang**; bila tak terhindarkan, hasil primer dilaporkan TIDAK KONKLUSIF.
- **Bila H1 GAGAL:** di README/05 tertulis "GAGAL: di SKAB, residual hidraulik tidak terbukti lebih baik dari ambang sederhana untuk memisahkan throttling dari fault", dengan angka + CI. Klaim "AI memisahkan katup vs aus" tetap **hipotesis** dan tidak boleh dipakai di materi lomba sebagai hasil.
- **Bila H1 LULUS:** klaim yang boleh: "Pada data lab pompa nyata milik pihak lain (SKAB, 1 testbed, 1 Hz), model residual hidraulik yang dilatih hanya pada data normal memisahkan penutupan katup dari imbalance/kavitasi lebih baik dari ambang getaran, arus, dan z-maks (AUROC … [CI])." Ini validasi **komponen** di lingkungan lab (pendukung TKT 4 untuk fungsi itu), **bukan** integrasi sistem DetakPompa dan **bukan** P1/P2 PRAREG v2.
- H2 dilaporkan dengan cara yang sama, terpisah dari H1.

## 8. Pembekuan
SHA-256 berkas ini disimpan di `prototype\PRAREG_SKAB.sha256` dengan timestamp, sebelum `git clone`/unduh SKAB. Kode (`detakpompa\hydraulic.py`, `run_skab.py`) ditulis setelah pembekuan dan harus mengikuti dokumen ini persis.
