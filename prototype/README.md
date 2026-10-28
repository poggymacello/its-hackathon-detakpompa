# DetakPompa: purwarupa TKT 3 (triase kondisi motor/pompa + abstain berbasis SNR)

**Posisi:** alat **triase**, yaitu menentukan pompa mana yang perlu dicek atau diaudit duluan, berdasarkan getaran. Alat ini **tidak mengukur efisiensi**: efisiensi pompa butuh debit, head, dan daya listrik. Kalau sinyalnya jelek atau modelnya ragu, alat ini menjawab **TIDAK TAHU** dan memberi langkah berikutnya.

**Status jujur:** TKT 3. Konsep sudah dibuktikan di data nyata publik, yaitu rig bantalan Ottawa. Data itu **bukan pompa** dan **tidak berisi arus motor**. Yang terbukti bekerja adalah gerbang kualitas sinyal (DSP); model ML **belum** terbukti lebih baik dari ambang RMS dengan gerbang yang sama (lihat "Eksperimen tambahan" dan "Triase armada"). Rincian ada di `../05_BUKTI_TKT.md` (§2b–§2d, prareg di §3).

**Tambahan 28 Okt malam (data lab pompa SKAB, pihak lain, 1 testbed):** model residual hidraulik **GAGAL** di kedua hipotesis yang diprareg (`PRAREG_SKAB.md`): tidak lebih baik dari ambang arus sederhana untuk memisahkan penutupan katup dari fault pompa, dan tidak lebih baik dari ambang getaran / z-maks untuk deteksi anomali umum. Lihat bagian "Uji data lab pompa SKAB" di bawah.

## Cara menjalankan (Windows, dari folder `prototype\`)
```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install numpy scipy pandas scikit-learn matplotlib pytest h5py
# 1) data: 60 file MAT Ottawa (289 MB) ke data\ottawa_uored_vafcls\mat\  (lihat DATA.md untuk URL + SHA-256)
# 2) evaluasi penuh (±4-5 menit): menulis results\*
.venv\Scripts\python.exe -I run_eval.py
# 3) demo satu rekaman
.venv\Scripts\python.exe -I -X utf8 demo.py data\ottawa_uored_vafcls\mat\I_3_1.mat
.venv\Scripts\python.exe -I -X utf8 demo.py data\ottawa_uored_vafcls\mat\I_3_1.mat --baseline data\ottawa_uored_vafcls\mat\H_3_0.mat
.venv\Scripts\python.exe -I -X utf8 demo.py rekaman_saya.csv --fs 25600      # CSV 1 kolom / NPY juga bisa
# 4) triase armada: folder (atau --daftar file.lst) -> tabel AUDIT DULU / PANTAU / UKUR ULANG / AMAN
.venv\Scripts\python.exe -I -X utf8 triase.py data\ottawa_uored_vafcls\mat --out results\triase\armada_60
.venv\Scripts\python.exe -I -X utf8 triase.py --daftar results\triase\armada_22.lst --out results\triase\armada_22 [--model rms]
.venv\Scripts\python.exe -I run_triase_eval.py        # presisi top-3, usulan vs RMS + gerbang (±4 menit)
.venv\Scripts\python.exe -I run_triase_eval.py --prevalensi   # hanya skenario 22 pompa, 3 dan 5 bermasalah (±30 detik)
# 5) eksplorasi SKAB (data lab pompa, prareg PRAREG_SKAB.md): data ke data\skab\ (lihat DATA.md), ±4 menit
.venv\Scripts\python.exe -I run_skab.py
.venv\Scripts\python.exe -I -X utf8 scripts\skab_posthoc.py     # diagnostik POST-HOC (tidak diprareg)
# 6) tes
.venv\Scripts\python.exe -I -m pytest -q tests
```
Versi yang dipakai: Python 3.11.9, numpy 2.4.6, scipy 1.17.1, scikit-learn 1.9.1, pandas 3.1.0, matplotlib 3.11.2, h5py 3.16.0.

## Isi
| Path | Fungsi |
|---|---|
| `detakpompa/io.py` | Loader Ottawa (`<F>_<bearing>_<state>.mat`), CSV, dan NPY. Memotong rekaman jadi jendela 1 s yang tidak tumpang tindih |
| `detakpompa/spectral.py` | DSP yang **diadaptasi dari FaceVitals**: `psd`, `spectral_snr`, `peak_frequency`, `viterbi_track` |
| `detakpompa/features.py` | Fitur statistik (baseline c), envelope + kurtosis (baseline b), fitur spektral (usulan), dan indeks kualitas sinyal |
| `detakpompa/splits.py` | Leave-one-unit-out, grouped k-fold, dan `assert_no_leakage` |
| `detakpompa/models.py` | Aturan ambang RMS, aturan envelope/kurtosis, RF statistik, RF spektral, dan `AbstainGate` |
| `detakpompa/deviation.py` | Mode "deviasi dari baseline unit sendiri" |
| `detakpompa/report.py` | Teks laporan, langkah berikutnya untuk TIDAK TAHU, dan catatan energi (skenario bersumber) |
| `run_eval.py` | Evaluasi penuh. Semua hasil masuk ke `results/` |
| `run_eval_rms_gate.py` | Eksperimen tambahan: pembanding ambang RMS + gerbang SNR yang sama, plus model gabungan (±10 menit). Hasil masuk ke `results/rmsgate_*`. Opsi `--plot-only` menggambar ulang figur dari CSV |
| `detakpompa/triage.py` | Keputusan tingkat rekaman (usulan dan RMS + gerbang yang sama), antrean armada AUDIT DULU / PANTAU / UKUR ULANG / AMAN, metrik top-k. Dipakai bersama oleh `demo.py`, `triase.py`, `run_triase_eval.py` |
| `demo.py` | Laporan kesehatan satu rekaman. Contoh keluaran ada di `results/demo/` |
| `triase.py` | Triase armada: folder/daftar rekaman → satu tabel antrean dengan alasan dan langkah berikutnya. Model per rekaman dilatih tanpa bearing-nya. Contoh di `results/triase/armada_22/`, `armada_60/` |
| `run_triase_eval.py` | Evaluasi presisi top-3 armada, leave-one-bearing-out, usulan vs RMS + gerbang. Hasil di `results/triase/eval_*` |
| `scripts/survey_data.py`, `scripts/make_demo_inputs.py` | Survei data dan pembuat input demo yang didegradasi |
| `detakpompa/hydraulic.py` | **Baru (SKAB).** Pemuat SKAB, split leave-one-experiment-out, model residual hidraulik (P_app ~ f(Q, p), p ~ f(Q), getaran ~ f(Q, p); Ridge polinomial derajat 2 atau GBM), baseline z per sensor, AUROC berbobot + bootstrap berpasangan, Holm. Tidak mengubah modul lama |
| `run_skab.py`, `scripts/skab_posthoc.py` | Run SKAB persis `PRAREG_SKAB.md` → `results/skab/`; diagnostik post-hoc (perancu sesi, besar perubahan titik kerja, resolusi tekanan) |
| `tests/` | 54 tes pytest (1 di antaranya butuh data SKAB): 12 untuk SKAB (`tests/test_skab.py`: eksperimen uji tidak pernah ada di data latih, uji kebocoran, AUROC berbobot = sklearn, hash prareg utuh, dll.), 8 untuk pembanding RMS + gerbang (`tests/test_rms_gate.py`), 9 untuk perbaikan prioritas dan triase armada (`tests/test_triage.py`), 2 untuk skenario prevalensi (`tests/test_triase_prevalence.py`). Output: `results/pytest_output.txt` |

## Desain evaluasi (anti-bocor)
- **Unit = satu bearing** (20 unit). Tiap unit punya 3 rekaman 10 s: sehat (`H_k_0`), fault berkembang (`X_k_1`), dan rusak (`X_k_2`). Label tugas: **sehat / waspada / rusak** (0/1/2). Ada 600 jendela, masing-masing 200 per kelas.
- **Split: leave-one-bearing-out (20 fold).** Ketiga rekaman satu bearing, beserta semua jendelanya, selalu berada di sisi uji yang sama. `assert_no_leakage` dipanggil di setiap fold dan dites (`tests/test_split.py`: train ∩ test = ∅ untuk unit dan rekaman). Ini mengikuti kritik kebocoran data di 03_RISET.md S14.
- **Tidak ada penyetelan di data uji.**
  - Ambang aturan dipilih di unit latih.
  - Hiperparameter RF tetap (`RF_PARAMS`), tidak di-*tune*.
  - Ambang SNR bersifat CFAR: kuantil 99 % dari SNR yang sama pada derau putih murni, sehingga tidak melihat label maupun data uji.
  - Ambang keyakinan diambil dari CV grouped 5-fold **di dalam** unit latih, dengan target cakupan 90 %.
- **Keputusan desain yang dibuat setelah melihat data** (ditulis supaya transparan):
  - Pita poros dilebarkan ke 15-35 Hz karena bearing 16-19 berputar di ~19,5 Hz.
  - SNR gerbang diganti dari rasio pita ala FaceVitals menjadi **prominensi garis lokal**, karena rasio pita justru *naik* saat derau ditambahkan (garis 60/120 Hz mendominasi pita).
  - Keduanya diputuskan dari inspeksi spektrum dan derau sintetis, bukan dari skor klasifikasi uji. `spectral_snr` FaceVitals tetap dipakai sebagai fitur model (`shaft_snr_fv_db`).
- **Baseline** (wajib menurut 04_KEPUTUSAN.md):
  - (a) ambang RMS 2 tingkat;
  - (b) aturan klasik "terburuk dari" kurtosis dan prominensi puncak spektrum envelope (demodulasi 2-10 kHz). Aturan ini *tanpa geometri bearing*, karena geometri belum diverifikasi;
  - (c) random forest 10 fitur statistik.
- **Usulan:** RF dengan pengaturan sama ditambah fitur spektral, yaitu energi pita, centroid/spread/flatness/entropy, frekuensi poros terlacak (Viterbi FaceVitals), SNR garis poros, harmonik 1x/2x/3x, dan fitur envelope. Ditambah **abstain dua tahap**: (1) gerbang sinyal (SNR garis poros < 11,52 dB, sinyal terpotong, atau sinyal datar); (2) gerbang ragu (probabilitas maksimum < τ dari CV dalam).

## Hasil (angka apa adanya dari `results/run_eval_log.txt`, `results/metrics_summary.csv`)
Tingkat jendela, n = 600. Peluang acak = 0,333. CI 95 % memakai bootstrap per unit (2000 kali, `metrics.unit_bootstrap`).

| Model | Balanced acc. [CI95] | Macro-F1 | F1 sehat / waspada / rusak |
|---|---|---|---|
| (a) Ambang RMS | **0,640** [0,558-0,727] | 0,600 | 0,867 / 0,288 / 0,645 |
| (b) Envelope + kurtosis | 0,432 [0,357-0,510] | 0,423 | 0,569 / 0,251 / 0,448 |
| (c) RF fitur statistik | 0,553 [0,465-0,645] | 0,541 | 0,819 / 0,319 / 0,486 |
| **Usulan: RF fitur spektral** | 0,608 [0,532-0,687] | 0,596 | 0,857 / 0,429 / 0,502 |

Selisih berpasangan usulan − baseline (balanced accuracy, `results/paired_bootstrap.csv`):
- vs RMS: **−0,030** [−0,145; +0,067] → **tidak mengalahkan ambang RMS**.
- vs RF statistik: +0,057 [−0,028; +0,138] → tidak signifikan.
- vs envelope/kurtosis: +0,179 [+0,083; +0,292] → lebih baik.

Tingkat rekaman (n = 60): RMS 0,633, envelope 0,433, RF statistik 0,533, usulan 0,617.

**Abstain (cakupan vs risiko, `results/coverage_risk.csv`, `coverage_risk.png`):**
- AURC galat: usulan 0,235, RF statistik 0,305.
- Titik operasi usulan: cakupan 0,873; galat pada yang dijawab 0,344 (galat tanpa abstain 0,392); balanced accuracy pada yang dijawab 0,640.
- Gerbang sinyal menolak 4,5 % jendela bersih. Semuanya berasal dari rekaman fault (C_16_1, C_16_2, C_17_2, O_7_1, O_7_2), karena garis poros tenggelam oleh fault.
- *(Dikoreksi 28 Okt; versi lama menulis "aturan RMS tidak punya skor keyakinan", dan itu salah.)* Jarak ke ambang terdekat adalah skor keyakinan yang sah untuk RMS. Dengan skor margin yang didefinisikan sebelumnya, AURC RMS adalah 0,306, atau 0,291 dengan gerbang. Selisihnya dengan usulan tidak signifikan (lihat "Eksperimen tambahan").

**Uji degradasi semi-sintetis** (`results/degradation_summary.csv`; jendela uji asli ditambah derau putih):

| Kondisi | Akurasi tanpa abstain | Abstain gerbang SNR | Akurasi pada yang dijawab |
|---|---|---|---|
| Bersih | 0,608 | 0,045 | 0,656 |
| SNR 10 dB | 0,517 | 0,540 | 0,632 |
| SNR 0 dB | 0,503 | 0,873 | 0,486 |
| SNR −10 dB | 0,325 | 0,972 | 0,235 |
| Sensor lepas (derau murni) | 0,370 | 0,988 | (n kecil) |

Tanpa abstain, model tetap menjawab dengan yakin pada derau murni. Contohnya `results/demo/laporan_sensor_lepas.txt`: probabilitas "rusak" 0,74 untuk derau murni, yang lalu ditolak gerbang.

**Mode deviasi dari baseline unit sendiri** (`results/deviation_scores.csv`): AUC sehat vs waspada = 1,0 dan sehat vs rusak = 1,0 di 20/20 unit. **Skor RMS saja juga 1,0.** Artinya pemisahan ini **tidak informatif**: jendela "sehat" uji diambil dari rekaman yang sama dengan baseline, sedangkan rekaman fault adalah sesi lain. Setiap perubahan sesi atau pemasangan sensor mungkin sudah cukup untuk memisahkan. Urutan rusak > waspada > sehat benar di 14/20 unit (RMS saja: 12/20). Untuk mengukur alarm palsu, dibutuhkan beberapa rekaman sehat dari sesi berbeda.

## Keterbatasan (wajib dibaca)
1. **Bukan pompa, bukan arus motor.** Ottawa adalah rig bantalan. Cerita "arus + getaran pompa" belum diuji (dataset pompa 4TU tidak bisa diakses; lihat DATA.md). Data pompa lab SKAB (1 testbed, 1 Hz, RMS getaran saja) sudah dipakai untuk model residual hidraulik, dengan hasil GAGAL (bagian "Uji data lab pompa SKAB"); model getaran terkunci PRAREG v2 tidak bisa dijalankan di SKAB.
2. **Usulan tidak mengalahkan ambang RMS + gerbang SNR yang sama**, baik dalam akurasi, AURC, maupun presisi top-3. Penolakan derau adalah jasa gerbang SNR (DSP), bukan AI. Recall *waspada* usulan lebih tinggi (0,415 vs 0,213, belum signifikan), tetapi itu beda **label tahap**, bukan deteksi lebih dini: jendela waspada yang ditandai "perlu cek" 156/188 = 0,830 (usulan) vs 158/188 = 0,840 (RMS). RMS lebih baik di *rusak*. Klaim AI = hipotesis, dengan kriteria lulus/gagal yang dibekukan sebelum ada data baru di `PRAREG_TKT4.md` v2 (SHA-256 di `PRAREG_TKT4.sha256`).
3. **Sampel kecil:** 20 unit, 60 rekaman. CI lebar.
4. **Kemungkinan perancu sesi:** kanal suhu dan offset DC berbeda antar-sesi sehat dan fault. Model tidak memakai keduanya, tetapi perbedaan sesi lain (pemasangan sensor) bisa ikut terbaca. Data ini tidak bisa memisahkan efek tersebut.
5. **Abstain bisa mengenai pompa yang benar-benar rusak** (C_16_2 → TIDAK TAHU). Di OOF, 69 dari 76 jendela TIDAK TAHU (91 %) berasal dari jendela waspada/rusak. Karena itu TIDAK TAHU masuk antrean **UKUR ULANG** dan **tidak boleh** dianggap "aman".
6. Contoh demo I_3_1 (label: waspada) dilaporkan **RUSAK**, dan O_8_2 (label: rusak) dilaporkan TIDAK TAHU. Contoh ini sengaja tidak dipilih yang bagus saja.

## Atribusi
- **FaceVitals** (© Poggy Macello + Aziz, keduanya anggota tim). `detakpompa/spectral.py` mengadaptasi `psd`, `spectral_snr`, `peak_frequency` dari `FaceVitals2027-SPCup_GAJADI-DAFTAR/facevitals/signal/quality.py` dan `viterbi_track` dari `facevitals/vitals/hr.py`. Perubahannya: pita mesin, satuan Hz, dan lebar jendela SNR yang bisa diatur. Ide abstain berbasis SNR juga berasal dari FaceVitals (prediksi selektif). Folder FaceVitals tidak diubah. Ini **bukan** warisan TKT: status TKT 4 FaceVitals hanya berlaku untuk HR video wajah.
- **Dataset:** Sehri, M., & Dumond, P. (2023). *UORED-VAFCLS* (v5), Mendeley Data, doi:10.17632/y2px5tg92h.5, **CC BY 4.0**. Perubahan yang kami lakukan dijelaskan di `DATA.md`.
- Angka energi di laporan demo berasal dari 03_RISET.md **S6** (Indra dkk., JIST 2024) dan **S10** (Nelik, Pumps & Systems 2016), dengan label "skenario, bukan pengukuran".

## Eksperimen tambahan (28 Okt 2026): pembanding "ambang RMS + gerbang SNR yang sama"
Pertanyaan juri yang dijawab: *"Gerbang SNR itu aturan DSP. Kalau ambang RMS + gerbang SNR yang sama sudah cukup, AI kalian menambah apa?"*

### Protokol (ditulis SEBELUM pembanding ini dijalankan; tidak diubah sesudahnya)
- Skrip: `run_eval_rms_gate.py` (tidak menimpa hasil lama; semua file baru berawalan `rmsgate_`). Data, fitur (`results/features.csv`), split leave-one-bearing-out 20 fold, `assert_no_leakage`, hiperparameter RF, dan bootstrap per unit (2000×, seed 0, draw unit yang sama) **identik** dengan `run_eval.py`.
- **Model pembanding `rms_gate`** (`detakpompa/models.py: RMSGateBaseline`): aturan ambang RMS 2 tingkat yang sama (`ThresholdRule("rms")`, ambang dari unit latih) + **gerbang sinyal yang identik** (`AbstainGate.quality_ok`: SNR garis poros ≥ 11,52 dB CFAR, kliping, sinyal datar).
- **Skor keyakinan RMS (didefinisikan sebelum melihat hasil):** `rule_margin` = jarak skor RMS ke ambang **terdekat**, dalam satuan log10 (dekade), karena RMS besaran skala positif sehingga yang bermakna adalah rasio terhadap ambang. 0 = tepat di ambang (paling ragu). Gerbang ragu tahap 2 untuk RMS memakai resep yang sama dengan RF: τ = kuantil 10 % dari margin hasil CV grouped 5-fold **di dalam** unit latih (target cakupan 90 %).
- Untuk kurva cakupan-risiko versi "bergerbang", jendela yang ditolak gerbang sinyal diurutkan paling bawah (diabstain lebih dulu) untuk kedua model (`metrics.gated_score`). Seri (ties) skor diputus dengan permutasi acak tetap (`metrics._order`), bukan urutan baris.
- **Perbandingan utama (ditetapkan sebelumnya):**
  - U1: usulan vs `rms_gate` pada **himpunan jendela yang sama** = yang lolos gerbang sinyal (gerbangnya identik, jadi cakupannya identik): balanced accuracy dan macro-F1, selisih berpasangan bootstrap per unit.
  - U2: AURC galat versi bergerbang, usulan vs `rms_gate`, berpasangan.
- **Sekunder:** titik operasi dua tahap masing-masing; cakupan yang disamakan (= cakupan titik operasi usulan, ambil top-k menurut skor masing-masing); per kelas (recall/F1 sehat, waspada, rusak); uji degradasi (derau dan "sensor lepas") dengan derau yang **sama persis** (rng seed 123, urutan sama dengan `run_eval.py`).
- **Eksperimen kedua (gabungan):** `RFPlusRuleFeature` = RF usulan + 1 fitur keputusan aturan RMS (0/1/2), out-of-fold di dalam unit latih. Catatan: fitur `rms` mentah **sudah** termasuk dalam fitur usulan (`SPEC_COLS` ⊃ `STAT_COLS`). Dilaporkan sebagai eksperimen kedua; risiko *multiple comparison* dicatat dan p-value bootstrap dikoreksi Holm di seluruh keluarga uji berpasangan.

### Hasil (run 28 Okt 2026, `results/rmsgate_log.txt`; 608 s)
**Cek reproduksi:** prediksi, probabilitas, dan keputusan abstain usulan, serta prediksi aturan RMS, **identik** dengan hasil `run_eval.py` (`oof_predictions.csv`, `degradation_windows.csv`; lihat baris `[repro]`). Angka di bawah bisa langsung dibandingkan dengan tabel di atas.

**U1: pada himpunan jendela yang sama.** Himpunan ini berisi jendela yang lolos gerbang sinyal, yang identik untuk kedua model, sehingga cakupan keduanya 0,955 (`results/rmsgate_metrics.csv`, `rmsgate_paired_bootstrap.csv`):

| | Balanced acc. | Macro-F1 | Recall sehat / waspada / rusak |
|---|---|---|---|
| `rms_gate` (ambang RMS + gerbang SNR) | **0,639** | **0,602** | 0,910 / 0,213 / **0,795** |
| Usulan (RF spektral + gerbang SNR) | 0,605 | 0,595 | 0,930 / **0,415** / 0,470 |
| Selisih usulan − rms_gate [CI95 bootstrap per unit] | −0,034 [−0,155; +0,071] | −0,008 [−0,150; +0,122] | |

→ **Dalam akurasi, ambang RMS + gerbang SNR yang sama setara dengan usulan, bahkan sedikit lebih baik.** Selisihnya tidak signifikan ke arah mana pun.

**U2: cakupan vs risiko.** Metriknya AURC galat; makin kecil makin baik (`results/rmsgate_coverage_risk.png/.csv`):

| | AURC tanpa gerbang | AURC + gerbang SNR |
|---|---|---|
| Ambang RMS (skor = margin log10) | 0,306 | 0,291 |
| Usulan (skor = probabilitas maks.) | 0,235 | 0,229 |
| Selisih usulan − RMS (bergerbang) | | −0,062 [−0,195; +0,076], **tidak signifikan** |

Kurva menunjukkan asal selisih AURC itu:
- Di cakupan ≤ ~0,3, jawaban paling yakin dari usulan hampir tanpa galat. Ke-60 jendela teratas semuanya sehat dan semuanya benar.
- Sebaliknya, 10 % jendela yang "paling yakin" menurut RMS memuat 16 jendela waspada yang dijawab "rusak" (unit 16-17, RMS sangat tinggi).
- Di cakupan praktis (≥ 0,5), galat RMS sama dengan usulan atau lebih rendah.

**Sekunder** (semua angka = selisih usulan − RMS, dengan CI95 bootstrap per unit):
- **Tanpa abstain (600 jendela):** balanced acc. −0,032 [−0,145; +0,067], sama dengan hasil lama.
- **Titik operasi dua tahap** masing-masing model (τ dari CV dalam):
  - usulan: cakupan 0,873, balanced acc. 0,640, macro-F1 0,633;
  - RMS: cakupan 0,850, balanced acc. **0,671**, macro-F1 0,616;
  - selisih balanced acc. −0,031 [−0,152; +0,079].
- **Cakupan disamakan 0,873** (top-k menurut skor bergerbang masing-masing):
  - balanced acc. 0,634 vs **0,664** (−0,029 [−0,164; +0,069]);
  - macro-F1 **0,628** vs 0,607 (+0,021 [−0,149; +0,146]).

**Per kelas (jendela yang lolos gerbang): di sinilah perbedaannya** (`results/rmsgate_per_class_disagreement.csv`, `rmsgate_per_unit.csv`):
- **Waspada: usulan lebih baik.** Recall 0,415 vs 0,213 (+0,202 [−0,056; +0,453]). Usulan benar sendirian di 56 jendela, RMS benar sendirian di 18.
- **Rusak: RMS jauh lebih baik.** Recall 0,470 vs 0,795, selisih **−0,324 [−0,562; −0,089]**. Ini satu-satunya CI yang tidak memuat 0: p = 0,009 sebelum koreksi, **p Holm = 0,198** setelah koreksi untuk 22 uji. RMS benar sendirian di 69 jendela, usulan di 9.
- **Sehat: praktis sama** (recall 0,930 vs 0,910). Untuk triase "perlu dicek atau tidak", keduanya setara.
- **Per unit:** usulan lebih akurat di 8 unit, RMS di 5, seri di 7.
- **Bacaan:** usulan lebih sering menyebut "waspada", tetapi akibatnya banyak jendela rusak ikut disebut waspada. Untuk triase, ini merugikan. Pompa rusak memang tetap tertandai "perlu dicek", tetapi prioritasnya turun.

**Sensor lepas dan derau.** Derau yang dipakai sama persis dengan uji lama (`results/rmsgate_degradation_summary.csv`).

| Kondisi | Abstain gerbang SNR (sama untuk keduanya) | Akurasi tanpa abstain: usulan / RMS | Lolos gerbang keyakinan saja (tanpa SNR): usulan / RMS |
|---|---|---|---|
| Bersih | 0,045 | 0,608 / 0,640 | 0,918 / 0,895 |
| SNR 10 dB | 0,540 | 0,517 / 0,643 | 0,917 / 0,888 |
| SNR 0 dB | 0,873 | 0,503 / 0,578 | 0,945 / 0,962 |
| SNR −10 dB | 0,972 | 0,325 / 0,402 | 0,965 / 0,915 |
| Sensor lepas (derau murni) | 0,988 | 0,370 / 0,640 | 0,913 / 0,885 |

- **Penolakan derau sepenuhnya berasal dari gerbang SNR (DSP), bukan dari AI.**
  - Gerbang keyakinan, baik milik RF maupun RMS, meloloskan 88-97 % jendela derau.
  - Gerbang SNR yang sama menolak 98,8 % derau murni, entah dipasang di depan RMS atau di depan usulan.
- **Akurasi RMS 0,640 pada "sensor lepas" adalah artefak simulasi.**
  - Derau disimulasikan dengan simpangan baku yang sama dengan sinyal asli (rasio RMS derau/bersih = 1,01). Akibatnya aturan RMS memberi jawaban yang persis sama seperti pada mesin.
  - Artinya RMS **buta** terhadap isi sinyal. Karena itulah gerbang dibutuhkan, tetapi gerbang itu sendiri bukan AI.
- **Pada derau sedang (10 dB, sebelum gerbang), RMS lebih tahan** (0,643) daripada usulan (0,517). Fitur spektral usulan lebih rusak oleh derau.

**Eksperimen kedua: model gabungan `rf_spec_plus_rmsrule`.** RMS mentah sudah menjadi fitur usulan, jadi model gabungan ini hanya menambahkan keputusan aturan RMS sebagai fitur.
- Balanced acc. 0,623: +0,015 [−0,007; +0,037] terhadap usulan dan −0,017 [−0,130; +0,083] terhadap RMS.
- AURC bergerbang 0,227: −0,002 [−0,010; +0,006] terhadap usulan.
- Recall rusak naik sedikit (0,545 vs 0,505).
- **Tidak ada perbaikan yang terbukti.** Model ini dirancang sebelum dijalankan, tetapi diperlakukan sebagai eksperimen kedua yang eksploratif.

**Multiple comparison.** Ada 22 uji berpasangan dalam satu keluarga: 3 utama, 13 sekunder, dan 6 eksperimen 2. Setelah koreksi Holm, **tidak ada satu pun yang signifikan**. p Holm terkecil adalah 0,198, yaitu recall rusak, dan arahnya menguntungkan RMS. Lihat kolom `p_holm_all` di `rmsgate_paired_bootstrap.csv`.

### Jawaban jujur untuk juri
> "Di data ini, ambang RMS ditambah gerbang SNR kami **sama baiknya** dengan AI kami dalam akurasi. Selisihnya −0,03 dan tidak signifikan, dan RMS bahkan lebih baik mengenali bantalan rusak. Penolakan derau dan sensor lepas berasal dari gerbang SNR, yaitu bagian DSP. Gerbang itu bisa dipasang di depan model apa pun, termasuk RMS. Kedua model menandai tahap awal untuk dicek sama seringnya (0,830 vs 0,840); AI hanya lebih sering memberi label **waspada** (recall 0,42 vs 0,21), dan itu bukan deteksi lebih dini. Yang mungkin ditambahkan AI, dan belum terbukti signifikan, adalah peringkat keyakinan yang lebih tepat di ujung atas. Jawaban AI yang paling yakin hampir tanpa galat, sedangkan RMS bisa yakin tetapi salah pada kasus waspada beramplitudo tinggi. Dengan 20 bearing, kami belum bisa mengklaim lebih dari itu."

## Perbaikan prioritas + triase armada (28 Okt 2026, malam)
### Bug prioritas (diperbaiki)
Sebelumnya laporan rekaman yang ditolak gerbang sinyal tetap mencetak "Prioritas cek": sensor lepas 0,87, derau −10 dB 0,83, C_16_2 0,75. Di daftar urutan, sensor lepas bisa menyalip pompa yang benar-benar rusak. Sekarang (`detakpompa/triage.py: decide_proposal`, `report.py: priority_text`):
- TIDAK TAHU karena **sinyal** (SNR rendah, sensor lepas, terpotong/datar) atau rekaman **pendek**: `priority = None`, laporan menulis "Prioritas cek: - (tidak diurutkan; masuk antrean UKUR ULANG ...)", probabilitas diberi tanda "TIDAK DIPAKAI".
- TIDAK TAHU karena **ragu**: hanya prioritas **SEMENTARA** (O_8_2: 0,48), antrean UKUR ULANG, tidak ikut urutan audit.
- Laporan demo dibuat ulang; selain baris prioritas/antrean/catatan, isinya identik dengan versi sebelumnya. Tes: `tests/test_triage.py` (`test_signal_gated_decision_has_no_priority`, `test_gated_never_outranks_assessed_pump`, `test_report_gated_prints_no_priority_number`, `test_demo_noise_gets_no_priority_and_ukur_ulang`, dll.).

### Triase armada (`triase.py`)
Masukan: folder atau daftar rekaman, satu rekaman = satu "pompa". Keluaran: `antrean_<model>.csv/.txt` dengan empat antrean:
- **AUDIT DULU:** k = 3 prioritas tertinggi di antara rekaman yang dijawab WASPADA/RUSAK (kapasitas audit per ronde, KPI Lean Canvas);
- **PANTAU:** WASPADA/RUSAK di luar kapasitas;
- **UKUR ULANG:** semua TIDAK TAHU, tidak pernah masuk AUDIT DULU;
- **AMAN:** dijawab SEHAT.

Anti-bocor: berkas yang namanya diawali pola Ottawa (`I_3_1.mat`, juga `I_3_1_derau_-10dB.npy`) dinilai model yang dilatih **tanpa** bearing itu (satu model per bearing). Contoh: `results/triase/armada_22/` (20 bearing, satu rekaman acak per bearing dengan `default_rng(2026)`, ditambah input derau −10 dB dan sensor lepas; daftar di `results/triase/armada_22.lst`) dan `results/triase/armada_60/` (seluruh folder data). Masing-masing untuk `--model usulan` dan `--model rms`. Hasil `armada_60` cocok persis dengan tabel antrean di `eval_whole_fleet_queues_*.csv`.

### Presisi top-3 (`run_triase_eval.py`; protokol di docstring, ditulis sebelum run pertama)
Leave-one-bearing-out, keputusan tingkat rekaman, gerbang SNR identik (11,52 dB), τ dari CV dalam (cakupan 90 %), k = 3 tetap. 2000 armada simulasi, masing-masing 20 bearing diambil dengan pengembalian dan satu rekaman acak per bearing (seed 0). Dasar acak "perlu cek" = 0,667. Hasil di `results/triase/eval_log.txt`, `eval_summary.json`, `eval_fleet_sim.csv`, `eval_recording_decisions.csv`, `eval_whole_fleet*.csv`.

| Armada simulasi, rata-rata [2,5–97,5 %] | Usulan | RMS + gerbang | Selisih usulan − RMS |
|---|---|---|---|
| **Presisi@3 "perlu cek"** | 0,971 [0,667; 1,000] | 0,952 [0,667; 1,000] | +0,019 [−0,333; +0,333], seri di 87 % armada |
| Presisi@3 "rusak" | 0,453 [0; 1] | 0,412 [0; 1] | +0,042 [−0,667; +0,667] |
| Pompa sehat di AUDIT DULU | 0,087 | 0,145 | −0,058 [−1; +1] |
| Perlu-cek yang masuk UKUR ULANG | 0,176 | 0,222 | −0,046 [−0,308; +0,214] |
| Perlu-cek yang lolos ke AMAN | 0,074 | 0,101 | −0,027 [−0,182; +0,111] |

- **Setara.** Untuk tugas yang dijual (3 pompa teratas), keduanya hampir selalu benar, dan selisihnya tidak bisa dibedakan dari nol.
- Seluruh 60 rekaman sebagai satu armada: presisi@3/@5/@10 usulan 1,00/1,00/1,00, RMS 1,00/1,00/0,90. Presisi "rusak"@3: usulan 0,33, RMS 0,67.
- Tingkat rekaman: usulan menjawab 53/60 (TIDAK TAHU: 2 sinyal, 5 ragu), RMS 50/60 (2 sinyal, 8 ragu).
- Eksploratif: 20 bearing, data sudah pernah dilihat. Bearing Ottawa sebagai pengganti pompa.
- **Konteks prevalensi:** armada di atas dua pertiganya bermasalah (dasar acak 0,667), jadi 0,971 tidak boleh dikutip sendirian.

**Skenario prevalensi realistis** (`run_triase_eval.py --prevalensi`; addendum protokol di docstring; keputusan LOUO yang sama, k = 3, tanpa penyetelan; 5000 armada × 22 pompa per skenario, seed 0; hasil `results/triase/eval_prevalensi_log.txt`, `eval_prevalensi_summary.json`, `eval_prevalensi.csv`):

| Armada 22 pompa | Dasar acak | Presisi@3 usulan | Presisi@3 RMS + gerbang | Selisih [2,5–97,5 %] | ≥1 pompa sehat di AUDIT DULU (usulan / RMS) |
|---|---|---|---|---|---|
| 3 bermasalah | 0,136 | 0,707 | 0,682 | +0,022 [−0,333; +0,333], seri 83 % | 0,61 / 0,62 |
| 5 bermasalah | 0,227 | 0,791 | 0,765 | +0,026 [−0,333; +0,500], seri 81 % | 0,50 / 0,53 |

Kedua model salah menandai rekaman sehat yang sama, `H_13_0`, dan tidak ada rekaman sehat lain yang ditandai. Pompa sehat di AUDIT DULU pada prevalensi rendah praktis ditentukan oleh satu rekaman itu. Tes: `tests/test_triase_prevalence.py`.

## Uji data lab pompa SKAB (28 Okt 2026, ±23:00 WIB)
**Pertanyaan.** Apakah model "residual hidraulik" (perilaku normal bersyarat titik kerja: daya semu V·I harapan pada debit + tekanan yang sama, kurva tekanan–debit, getaran harapan pada titik kerja yang sama) memisahkan **penutupan katup** (throttling, bukan fault pompa) dari **fault pompa** (imbalance rotor, kavitasi) lebih baik dari ambang sederhana? Ini alasan AI yang dianjurkan `../11_RISET_KELEMAHAN.md` §2–§3.

**Prareg:** `PRAREG_SKAB.md`, SHA-256 `c29805a228ddc8e7c2d9cfca2527085585626efc2a90c8c96b10131823cb014e`, dibekukan 28 Okt 2026 22:54:19 WIB **sebelum** SKAB diunduh (`PRAREG_SKAB.sha256`). Kode ditulis dan di-hash sebelum unduhan juga (`SKAB_KODE_PRADATA.sha256`). Ini **eksplorasi terencana**, bukan P1/P2 PRAREG-TKT4 v2: SKAB hanya punya 1 testbed (P1 butuh ≥ 8 unit, P2 ≥ 3), dan model getaran terkunci tidak bisa jalan pada RMS 1 Hz. Status PRAREG v2 tetap **belum teruji**.

**Desain.** 34 berkas eksperimen = 34 unit; leave-one-experiment-out; `anomaly-free.csv` selalu di sisi latih; model dilatih **hanya** pada baris normal berkas latih; `assert_no_leakage` tiap fold. Kelas H1: T = `valve1` (16) + `valve2` (4) = 20 kejadian; F = imbalance `other/5–9` + kavitasi `other/12–13` = 7 kejadian. Baseline: B1 RMS getaran (z maks dua akselerometer), B2 ambang arus (|z|), B3 z-maks 8 sensor. Ambang τ = kuantil 0,99 skor normal latih. Bootstrap berpasangan 10.000×, Holm m = 2, α satu sisi 0,025; R harus mengalahkan **setiap** baseline (p = maks atas tiga). Satu deviasi format (nama kolom `Volume Flow RateRMS`), lihat `results/skab/DEVIASI.md`.

**Hasil primer** (`results/skab/run_skab_log.txt`, `primary.csv`, `auc_per_method.csv`, `summary.json`):

| | R (residual) | B1 getaran | B2 arus | B3 z-maks | Status |
|---|---|---|---|---|---|
| **H1** AUROC per kejadian, F vs T (7 vs 20) [CI95] | 1,000 [1,000; 1,000] | 0,571 [0,143; 0,857] | **1,000** [1,000; 1,000] | 0,571 [0,143; 0,857] | **GAGAL** |
| Δ R − baseline [CI95], p satu sisi | | +0,429 [+0,143; +0,857], 0,020 | **0,000** [0; 0], 1,000 | +0,429 [+0,143; +0,857], 0,020 | p_H1 = 1,000 |
| **H2** AUROC titik, semua 34 berkas (13.067 anomali / 24.334 normal) [CI95] | 0,532 [0,488; 0,590] | 0,573 [0,481; 0,673] | 0,502 [0,480; 0,521] | 0,581 [0,493; 0,679] | **GAGAL** |
| Δ R − baseline [CI95], p satu sisi | | −0,041 [−0,109; +0,033], 0,848 | +0,031 [−0,020; +0,092], 0,127 | −0,049 [−0,113; +0,022], 0,912 | p_H2 = 0,912 |

Pengaman terpenuhi (recall kejadian fault pada τ 5/7 = 0,714; FAR titik R 0,024 vs B3 0,018), tetapi tidak ada hipotesis yang ditolak Holm. Pada ambang τ, R dan B1 sama persis: balanced accuracy per kejadian 0,857 [0,714; 1,000], 5/7 fault ditandai, 0/20 penutupan katup ditandai (`S7_balanced_acc_event.csv`).

**Sekunder (dilaporkan semua, `secondary.csv`; tidak mengubah status).**
- S1/S2 (T = `valve2` saja / `valve1` saja): pola sama dengan H1 (seri dengan B2, tidak signifikan setelah Holm).
- S3 (F ∪ proses vs T, 14 vs 20): R 1,000 vs B1/B3 0,286 (Holm signifikan), vs B2 0,714 (p dua sisi 0,016, tidak signifikan setelah Holm).
- S5 R-GBM: H2 AUROC 0,867 vs 0,573 / 0,502 / 0,581 (Holm signifikan terhadap ketiganya), **tetapi** pada τ varian ini menandai 18/20 penutupan katup (balanced accuracy H1 0,407). Ini detektor anomali umum, kebalikan dari tujuan H1.
- S10 (pemusatan ulang per run tanpa label): H2 R 0,629 vs B1 0,563 / B2 0,507 (Holm signifikan) / B3 0,582 (+0,047 [+0,002; +0,098], p 0,043, tidak signifikan setelah Holm); H1 semua metode ≈ 1,0.
- Deskriptif (`deskriptif_median_z.csv`): pada baris penutupan katup, residual daya z_P = 0,00 (`valve1`) dan −0,01 (`valve2`), sama dengan baris normal. Residual getaran imbalance 203 / 125 dan kavitasi 24 / 10 (satuan simpangan robust).

**Diagnostik POST-HOC** (`scripts/skab_posthoc.py`, `results/skab/posthoc_*.csv`; tidak diprareg, ditulis setelah melihat hasil):
1. **Perancu sesi/rezim.** Semua berkas katup berjalan di Q ≈ 32 L/min, P_app ≈ 226 VA **di sepanjang berkas**, termasuk bagian normalnya. Berkas fault berjalan di Q ≈ 125 L/min, P_app ≈ 580 VA. Skor median pada **baris normal saja** sudah memisahkan berkas fault dari berkas katup dengan AUROC 1,000 (R dan B2). Jadi AUROC 1,0 di H1 sebagian besar mengukur sesi rekaman, bukan jenis anomali.
2. **Throttling di SKAB kecil:** penutupan katup menurunkan Q ±6 % (32 → 30 L/min) dan P_app < 1 %. Tidak ada metode ambang yang memberi alarm palsu pada kejadian katup, jadi tidak ada alarm palsu yang bisa dikurangi model residual.
3. **Tekanan terkuantisasi:** 10 nilai unik, langkah ±0,33 bar, 55 % baris bernilai 0,055 bar. Kurva tekanan–debit praktis tidak terukur; komponen "hidraulik" R tinggal P_app ~ f(Q).

**Artinya.** Di data lab pompa nyata ini, model residual hidraulik **tidak terbukti** lebih baik dari ambang arus sederhana untuk memisahkan katup dari fault, dan tidak lebih baik dari ambang getaran untuk deteksi anomali umum. Mekanismenya (titik katup tetap di manifold normal daya–debit) konsisten dengan teori, tetapi SKAB tidak bisa mengujinya secara tajam karena throttling-nya kecil, tekanan kasar, dan rezim rekaman berbeda antarjenis eksperimen. Klaim "AI memisahkan katup vs aus" tetap **hipotesis**.

**Keterbatasan.** 1 testbed (bukan unit fisik berbeda); 1 Hz, getaran hanya RMS; label per titik buatan penyusun SKAB; daya = V·I (tanpa cos φ); n kejadian kecil (7 fault). Lisensi data GPL-3.0: kami hanya **memakai** data (tidak menyalin kode SKAB; tidak ada berkas SKAB di repo tim karena `data/` di-gitignore). Bila suatu saat data atau kode SKAB didistribusikan ulang bersama kode kami, syarat GPL-3.0 berlaku.
