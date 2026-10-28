# 05_BUKTI_TKT: DetakPompa
### Agen A6 "Arsitek-Builder" · 28 Okt 2026 · kode: `prototype\` · dasar: `04_KEPUTUSAN.md`, `03_RISET.md`

**Klaim jujur hari ini: TKT 3 untuk rangkaian triase getaran (gerbang kualitas sinyal + model + antrean) di data publik bantalan, bukan di pompa.** Model ML di dalamnya **belum** terbukti lebih baik dari ambang RMS yang diberi gerbang sinyal yang sama (§2b); klaim AI kami adalah hipotesis dengan kriteria lulus/gagal tertulis dan dibekukan dengan SHA-256 sebelum ada data baru (§3, `prototype\PRAREG_TKT4.md` v2). Domain pompa (arus motor dan data PDAM) belum diuji. TKT FaceVitals tidak diwariskan.

Posisi produk: **triase**, yaitu menentukan pompa mana yang dicek atau diaudit duluan. Alat ini **tidak mengukur efisiensi**, karena efisiensi butuh debit + head + daya. Tidak ada angka efisiensi atau kWh yang dihasilkan model.

## 1. Bukti per tingkat
| TKT | Syarat (ringkas) | Bukti | File |
|---|---|---|---|
| 2 | Konsep dan aplikasi dirumuskan | Ide, kasus PDAM, dan sumber energi | `04_KEPUTUSAN.md`, `03_RISET.md` §1 (S6, S10, S14) |
| 2→3 | Komponen inti bekerja di sinyal uji | DSP FaceVitals (pelacak Viterbi, SNR) diadaptasi ke pita mesin. Tes di sinyal sintetis lulus: frekuensi poros terlacak, derau ditolak, kliping ditolak | `prototype/detakpompa/spectral.py`, `tests/test_features.py`, `tests/test_abstain.py`, `results/pytest_output.txt` (54 passed sejak 28 Okt ±23:15, setelah 12 tes SKAB; sebelumnya 42, 40, 31, lalu 23) |
| **3** | Proof of concept di **data nyata**, dengan metrik vs baseline dan tanpa kebocoran | Leave-one-bearing-out 20 fold pada Ottawa UORED-VAFCLS (CC BY 4.0). Ada 3 baseline, CI bootstrap per unit, kurva cakupan-risiko, dan uji degradasi | `prototype/results/run_eval_log.txt`, `metrics_summary.csv`, `paired_bootstrap.csv`, `coverage_risk.csv/.png`, `degradation_summary.csv`, `summary.json` |
| 3 (demo) | Keluaran yang bisa dibaca pengguna | `demo.py` menghasilkan status SEHAT/WASPADA/RUSAK/TIDAK TAHU, alasan, langkah berikutnya, dan catatan energi berlabel skenario. Unit dari rekaman input dikeluarkan dari data latih | `prototype/results/demo/*.txt` (7 contoh, termasuk yang salah dan yang abstain) |
| 3 (triase armada) | Keluaran yang sesuai produk: urutan pompa | `triase.py` menghasilkan antrean AUDIT DULU / PANTAU / UKUR ULANG / AMAN untuk satu folder rekaman; rekaman yang ditolak gerbang sinyal tidak diberi prioritas. Presisi top-3 leave-one-bearing-out setara dengan RMS + gerbang (§2c) | `prototype/results/triase/` |
| 3 (anti-bocor) | Unit train ∩ test = ∅ | `assert_no_leakage` dijalankan di setiap fold, plus 4 tes split | `prototype/detakpompa/splits.py`, `tests/test_split.py` |
| 4 | Validasi komponen di **lab** | **Belum.** Uji di data lab pompa milik pihak lain (SKAB, 1 testbed) sudah dijalankan untuk fungsi "pisahkan katup vs fault": **GAGAL** (§2e). Rekaman lab sendiri belum ada | §2e, §3 |
| 5 | Validasi di **lingkungan pengguna** | **Belum** | §3 |

## 2. Hasil metrik (hanya dari run nyata, 28 Okt 2026)
Sumber: `prototype/results/run_eval_log.txt` dan `metrics_summary.csv`. Ada 600 jendela 1 s (200 per kelas), dari 60 rekaman dan 20 bearing. Peluang acak untuk balanced accuracy = 0,333.

| Model | Balanced acc. [CI95 bootstrap per unit] | Macro-F1 |
|---|---|---|
| (a) Ambang RMS | **0,640** [0,558-0,727] | 0,600 |
| (b) Envelope + kurtosis (aturan klasik) | 0,432 [0,357-0,510] | 0,423 |
| (c) RF fitur statistik | 0,553 [0,465-0,645] | 0,541 |
| **Usulan: RF fitur spektral + pelacak FaceVitals** | 0,608 [0,532-0,687] | 0,596 |

- **Usulan TIDAK mengalahkan ambang RMS:** selisih −0,030 [−0,145; +0,067]. Usulan juga belum terbukti lebih baik dari RF statistik: +0,057 [−0,028; +0,138]. Usulan hanya lebih baik dari aturan envelope/kurtosis: +0,179 [+0,083; +0,292]. Sumber: `results/paired_bootstrap.csv`.
- Sehat vs "perlu dicek" (waspada+rusak), dihitung dari matriks kebingungan di log:
  - usulan: sehat dikenali 186/200, fault ditandai 352/400;
  - RMS: 182/200 dan 362/400.
- Yang paling lemah: membedakan waspada dari rusak (F1 waspada usulan 0,429, RMS 0,288).
- **Abstain:**
  - AURC galat usulan 0,235 vs RF statistik 0,305.
  - Di titik operasi (τ dari CV dalam), cakupan 0,873 dan galat pada yang dijawab 0,344 (tanpa abstain 0,392).
  - Sumber: `results/coverage_risk.csv`, `results/summary.json`.
- **Uji degradasi semi-sintetis** (`results/degradation_summary.csv`), yaitu jendela uji asli ditambah derau. Persentase yang ditolak gerbang SNR:
  - data bersih 4,5 %;
  - SNR 10 dB: 54,0 %;
  - SNR 0 dB: 87,3 %;
  - SNR −10 dB: 97,2 %;
  - sensor lepas (derau murni): 98,8 %.
  - Tanpa abstain, akurasi pada sensor lepas adalah 0,370, dan model tetap menjawab "rusak" dengan yakin.
- **Mode deviasi dari baseline unit sendiri** (`results/deviation_scores.csv`): AUC 1,0 di 20/20 unit, tetapi **RMS saja juga 1,0**. Hasil ini dianggap **tidak informatif**, karena jendela sehat uji berasal dari sesi yang sama dengan baseline. Pengukuran alarm palsu baru mungkin kalau ada beberapa rekaman sehat dari sesi berbeda.

**Kalimat lama (DICABUT 28 Okt, jangan dipakai; pengganti di §2d):**
> ~~"Di data bantalan publik dengan split per-bearing, AI kami belum lebih akurat dari ambang RMS. Kelebihannya: AI kami tahu kapan harus diam. Derau dan sensor lepas ditolak, bukan ditebak."~~

Jangan menulis "akurasi 9x %".

> **Koreksi 28 Okt (lihat §2b):** frasa "AI kami tahu kapan harus diam" terlalu memuji AI. Penolakan derau dan sensor lepas adalah jasa **gerbang SNR (DSP)**, dan gerbang itu bekerja sama baiknya di depan ambang RMS. Kalimat pengganti ada di §2b.

## 2b. Eksperimen tambahan: ambang RMS + gerbang SNR yang sama (28 Okt 2026)
Pertanyaan juri yang diantisipasi: *"Kalau ambang RMS + gerbang SNR yang sama sudah cukup, AI kalian menambah apa?"*

Protokolnya sama persis dengan evaluasi utama: leave-one-bearing-out 20 fold, bootstrap per unit 2000×, gerbang SNR identik (11,52 dB CFAR), τ dari CV dalam, dan tanpa penyetelan di data uji. Skor keyakinan RMS ditetapkan **sebelum** run: jarak log10 ke ambang terdekat. Hasil run lama berhasil direproduksi identik. Kode dan hasil:
- kode: `prototype/run_eval_rms_gate.py`, `detakpompa/models.py` (`RMSGateBaseline`, `rule_margin`, `RFPlusRuleFeature`);
- hasil: `prototype/results/rmsgate_log.txt`, `rmsgate_metrics.csv`, `rmsgate_paired_bootstrap.csv`, `rmsgate_coverage_risk.png/.csv`, `rmsgate_degradation_summary.csv`, `rmsgate_per_class_disagreement.csv`;
- tes: `results/pytest_output.txt` (31 passed saat itu; 40 setelah §2c; 42 setelah skenario prevalensi).

| Perbandingan (usulan − RMS+gerbang) | Usulan | RMS + gerbang | Selisih [CI95 per unit] |
|---|---|---|---|
| Balanced acc. pada jendela yang sama (lolos gerbang, cakupan 0,955) | 0,605 | **0,639** | −0,034 [−0,155; +0,071] |
| Macro-F1, himpunan sama | 0,595 | 0,602 | −0,008 [−0,150; +0,122] |
| AURC galat + gerbang (makin kecil makin baik) | **0,229** | 0,291 | −0,062 [−0,195; +0,076] |
| Balanced acc. di titik operasi dua tahap | 0,640 (cakupan 0,873) | **0,671** (cakupan 0,850) | −0,031 [−0,152; +0,079] |
| Recall waspada | **0,415** | 0,213 | +0,202 [−0,056; +0,453] |
| Recall rusak | 0,470 | **0,795** | −0,324 [−0,562; −0,089] (p Holm 0,198) |
| Recall sehat | 0,930 | 0,910 | +0,020 [−0,010; +0,075] |

- **RMS + gerbang SNR setara dengan usulan dalam akurasi, bahkan sedikit lebih baik.** Tidak ada selisih yang signifikan setelah koreksi Holm atas 22 uji.
- **Usulan unggul di kelas waspada, RMS unggul di kelas rusak.**
  - Recall rusak adalah satu-satunya CI yang tidak memuat 0 sebelum koreksi, dan arahnya menguntungkan RMS.
  - Untuk sehat vs perlu-dicek, keduanya setara.
- **Derau dan sensor lepas:**
  - Gerbang SNR menolak 98,8 % derau murni, sama untuk kedua model.
  - Gerbang keyakinan model saja, baik RF maupun RMS, meloloskan 88-97 % jendela derau. Penolakan itu datang dari DSP, bukan dari AI.
  - Akurasi RMS 0,640 pada "sensor lepas" adalah artefak simulasi: derau dibuat dengan RMS yang sama dengan sinyal asli.
- **Keunggulan AURC usulan** (tidak signifikan) berasal dari ujung atas peringkat keyakinan.
  - 60 jendela paling yakin dari usulan semuanya benar.
  - 10 % jendela paling yakin menurut RMS memuat 16 jendela waspada yang dijawab "rusak".
- **Model gabungan (keputusan aturan RMS sebagai fitur RF; RMS mentah memang sudah menjadi fitur) tidak membawa perbaikan yang terbukti:**
  - balanced acc. 0,623 (+0,015 [−0,007; +0,037] terhadap usulan);
  - AURC 0,227;
  - eksperimen ini diperlakukan sebagai eksplorasi.

**Kalimat pengganti untuk proposal/QnA:**
> "Di data bantalan publik dengan split per-bearing, ambang RMS yang diberi gerbang SNR kami sama akuratnya dengan model AI kami. Penolakan derau dan sensor lepas berasal dari gerbang SNR, yang bisa dipasang di depan model apa pun. Kedua model menandai tahap awal untuk dicek sama seringnya (jendela waspada yang ditandai perlu cek: 0,830 vs 0,840). AI lebih sering memberi label 'waspada' (recall 0,42 vs 0,21), sedangkan RMS menyebut tahap yang sama 'rusak'; itu beda label, bukan deteksi lebih dini. Sebagai gantinya, AI lebih sering menurunkan bantalan rusak menjadi waspada. Urutan keyakinan AI sedikit lebih baik di ujung atas, belum signifikan dengan 20 bearing."

**Recall waspada bukan deteksi dini** (dihitung dari matriks kebingungan `results/rmsgate_metrics.csv`, baris `lolos_gerbang_sinyal_sama`; angka sama dengan eksperimen E1 panel juri):

| Jendela lolos gerbang | Usulan | RMS + gerbang |
|---|---|---|
| Jendela waspada yang ditandai "perlu cek" (waspada atau rusak) | 156/188 = 0,830 | 158/188 = 0,840 |
| Jendela rusak yang ditandai "perlu cek" | 169/185 = 0,914 | 177/185 = 0,957 |
| Jendela sehat yang ditandai (alarm palsu) | 14/200 = 7,0 % | 18/200 = 9,0 % |

Selisih recall waspada (0,415 vs 0,213) adalah pergeseran batas waspada/rusak. Kedua model sama-sama menandai ±83–84 % jendela tahap awal untuk dicek.

## 2c. Perbaikan prioritas + triase armada (28 Okt 2026, malam)
**Bug yang diperbaiki.** Sebelumnya, rekaman yang ditolak gerbang sinyal tetap dicetak dengan skor prioritas: sensor lepas **0,87**, derau −10 dB **0,83**, C_16_2 **0,75**. Kalau laporan itu diurutkan, sensor lepas berada di atas pompa yang benar-benar rusak (I_3_1, 0,88, nyaris sama). Sekarang:
- TIDAK TAHU karena sinyal (SNR rendah, sensor lepas, terpotong/datar) atau rekaman terlalu pendek **tidak diberi prioritas sama sekali** dan masuk antrean **UKUR ULANG** dengan langkah berikutnya.
- TIDAK TAHU karena model ragu menampilkan prioritas **SEMENTARA** (O_8_2: 0,48), juga masuk UKUR ULANG, dan tidak ikut urutan audit.
- Kode: `prototype/detakpompa/triage.py` (dipakai bersama oleh `demo.py`, `triase.py`, `run_triase_eval.py`), `detakpompa/report.py`. Tes: `tests/test_triage.py`. Laporan demo dibuat ulang (`results/demo/*.txt`); selain baris prioritas/antrean, isinya identik dengan versi sebelumnya.
- Fakta dari OOF (`results/oof_predictions.csv`): 76 jendela TIDAK TAHU, **69 (91 %)** dari jendela waspada/rusak (27 karena sinyal, semuanya fault; 49 karena ragu, 86 % fault). Karena itu aturan produk: **TIDAK TAHU = ukur ulang, bukan aman.**

**Triase armada** (`prototype/triase.py`, contoh di `prototype/results/triase/armada_22/` dan `armada_60/`). Satu rekaman = satu "pompa"; keluaran satu tabel antrean AUDIT DULU (maks. k = 3) / PANTAU / UKUR ULANG / AMAN, dengan alasan dan langkah berikutnya. Setiap rekaman dinilai model yang dilatih **tanpa** bearing-nya. Data: bearing Ottawa sebagai pengganti pompa.

**Presisi top-3** (`prototype/run_triase_eval.py`; protokol ditulis di docstring sebelum run pertama; hasil `results/triase/eval_log.txt`, `eval_summary.json`, `eval_fleet_sim.csv`). Leave-one-bearing-out, keputusan tingkat rekaman, k = 3 tetap (KPI Lean Canvas). 2000 armada simulasi: 20 bearing diambil dengan pengembalian, satu rekaman acak per bearing. Dasar acak "perlu cek" = 0,667.

| Metrik (armada simulasi, rata-rata [2,5–97,5 %]) | Usulan | RMS + gerbang SNR | Selisih |
|---|---|---|---|
| **Presisi@3 "perlu cek" (waspada/rusak)** | 0,971 [0,667; 1,000] | 0,952 [0,667; 1,000] | +0,019 [−0,333; +0,333]; seri di 87 % armada |
| Presisi@3 "rusak" saja | 0,453 [0; 1] | 0,412 [0; 1] | +0,042 [−0,667; +0,667] |
| Pompa sehat di AUDIT DULU (per armada) | 0,087 | 0,145 | −0,058 [−1; +1] |
| Pompa perlu-cek yang masuk UKUR ULANG | 0,176 | 0,222 | −0,046 [−0,308; +0,214] |
| Pompa perlu-cek yang lolos ke AMAN (terlewat) | 0,074 | 0,101 | −0,027 [−0,182; +0,111] |

- **Konteks prevalensi:** angka 0,971 vs 0,952 berasal dari armada simulasi yang **dua pertiganya bermasalah** (dasar acak 0,667). IPA nyata kebanyakan pompanya sehat, jadi angka itu tidak boleh dikutip tanpa skenario di bawah.
- **Setara.** Dalam tugas yang sebenarnya dijual (3 pompa teratas), usulan dan RMS + gerbang memberi presisi yang sama, dan selisihnya tidak bisa dibedakan dari nol. Ini **bukan** bukti bahwa AI diperlukan.

**Skenario prevalensi realistis** (`run_triase_eval.py --prevalensi`, addendum protokol di docstring; hasil `results/triase/eval_prevalensi_log.txt`, `eval_prevalensi_summary.json`, `eval_prevalensi.csv`). Keputusan LOUO tingkat rekaman yang sama, k = 3, tanpa penyetelan. 5000 armada × 22 pompa per skenario, jumlah pompa bermasalah tetap; slot sehat dan slot bermasalah masing-masing diambil per bearing dengan pengembalian (seed 0).

| Armada 22 pompa, rata-rata [2,5–97,5 %] | Dasar acak | Presisi@3 usulan | Presisi@3 RMS + gerbang | Selisih | Armada dengan ≥1 pompa sehat di AUDIT DULU (usulan / RMS) |
|---|---|---|---|---|---|
| 3 bermasalah | 0,136 | 0,707 [0; 1] | 0,682 [0; 1] | +0,022 [−0,333; +0,333]; seri 83 % | 0,61 / 0,62 |
| 5 bermasalah | 0,227 | 0,791 [0,333; 1] | 0,765 [0,333; 1] | +0,026 [−0,333; +0,500]; seri 81 % | 0,50 / 0,53 |
| *rujukan: armada 20 bearing di atas* | *0,667* | *0,971* | *0,952* | *+0,019 [−0,333; +0,333]* | — |

- Pada 3–5 pompa bermasalah dari 22, presisi@3 turun ke ±0,7–0,8 dan tetap **setara** antara usulan dan RMS.
- **Kedua model salah menandai rekaman sehat yang sama, dan hanya itu:** dari 20 rekaman sehat, usulan dan RMS + gerbang sama-sama menandai `H_13_0` (RUSAK dengan prioritas) dan tidak menandai rekaman sehat lain. Karena itu pompa sehat di AUDIT DULU pada prevalensi rendah praktis ditentukan oleh satu rekaman (apakah `H_13_0` terambil ke armada). Dengan 20 rekaman sehat, angka alarm palsu ini sangat kasar.
- Tangkapan@3 (pompa bermasalah di AUDIT DULU ÷ min(3, jumlah bermasalah)): 3/22 usulan 0,603 vs RMS 0,546; 5/22 0,774 vs 0,729; CI selisih memuat 0. Rekaman bermasalah yang masuk peringkat audit sama sekali: usulan 30/40, RMS 27/40 (sisanya UKUR ULANG atau AMAN).
- Eksploratif, sama seperti angka 0,971: 20 bearing, data sudah pernah dilihat. Hasil panel juri (E2, skrip terpisah) mirip: 0,703/0,679 dan 0,787/0,757.
- Sekunder, seluruh 60 rekaman sebagai satu armada (`eval_whole_fleet.csv`): presisi@3/@5/@10 usulan 1,00/1,00/1,00, RMS 1,00/1,00/0,90. Presisi "rusak"@3: usulan 0,33, RMS 0,67. Pompa perlu-cek yang masuk UKUR ULANG: usulan 7/40, RMS 9/40; yang lolos ke AMAN: usulan 3/40, RMS 4/40.
- Tingkat rekaman: usulan menjawab 53/60 (TIDAK TAHU: 2 sinyal, 5 ragu), RMS 50/60 (2 sinyal, 8 ragu).
- Semua ini eksploratif: 20 bearing, data sudah pernah dilihat, interval tidak dikoreksi untuk uji berganda.

## 2d. Narasi resmi soal AI (berlaku untuk 08, 09, 10)
1. **Gerbang SNR (DSP, warisan FaceVitals) adalah komponen yang terbukti mencegah jawaban palsu saat sensor lepas.** Gerbang ini menolak 98,8 % jendela derau murni, sama untuk usulan maupun RMS. Gerbang keyakinan model saja meloloskan 88–97 % jendela derau (§2b).
2. **Model ML saat ini belum terbukti lebih baik dari ambang RMS + gerbang yang sama di data rig bantalan.** Akurasi setara (−0,034 [−0,155; +0,071]), AURC tidak berbeda signifikan (−0,062 [−0,195; +0,076]), presisi top-3 setara (0,971 vs 0,952, +0,019 [−0,333; +0,333], di armada simulasi 2/3 bermasalah; pada 3 dari 22 bermasalah 0,707 vs 0,682, pada 5 dari 22 0,791 vs 0,765, keduanya salah menandai rekaman sehat yang sama, `H_13_0`). RMS lebih baik mengenali "rusak" (recall 0,795 vs 0,470). Recall **waspada** 0,415 vs 0,213 (+0,202 [−0,056; +0,453], p = 0,122 sebelum koreksi, p Holm = 1,0) adalah perbedaan **label tahap**, bukan deteksi dini: jendela waspada yang ditandai perlu cek 0,830 (usulan) vs 0,840 (RMS) (§2b). **Tidak ada metrik di mana AI terbukti lebih baik.**
3. **Karena itu klaim AI kami adalah hipotesis** yang akan diuji dengan prareg yang sudah dibekukan sebelum ada data baru (`prototype\PRAREG_TKT4.md` v2, ringkasan di §3): endpoint primer adalah akurasi di unit fisik yang tidak pernah dilihat dan kemampuan membedakan throttling dari fault, keduanya AI vs RMS + gerbang. Kalau gagal, klaim AI dicabut dan produk dijual sebagai gerbang sinyal + ambang RMS + antrean triase.

Kalimat yang **tidak boleh** dipakai lagi: "RMS tidak punya skor keyakinan", "nilai tambah AI ada di abstain", "AI kami tahu kapan harus diam".

## 2e. Uji data lab pompa SKAB (28 Okt 2026, ±23:00 WIB)
**Apa yang diuji.** Inti AI yang dianjurkan `11_RISET_KELEMAHAN.md` §2–§3: model **residual hidraulik**, yaitu perilaku normal bersyarat titik kerja (daya semu V·I harapan pada debit + tekanan yang sama, kurva tekanan–debit, getaran harapan pada titik kerja yang sama), dilatih **hanya** pada data normal. Klaimnya: penutupan katup menggeser titik kerja *sepanjang* kurva (residual kecil), fault menggeser kurva atau menaikkan getaran pada titik kerja yang sama (residual besar), sedangkan ambang per sensor bereaksi pada keduanya.

**Data.** SKAB v0.9 (Katser & Kozitsin 2020, Kaggle DOI 10.34740/KAGGLE/DSV/1693952, https://github.com/waico/SKAB, **GPL-3.0**): **1 testbed** pompa air Skoltech, 1 Hz, arus, tegangan, tekanan setelah pompa, laju alir, RMS dua akselerometer, dua suhu. 34 eksperimen berlabel per titik + 1 berkas bebas anomali. Rincian, SHA-256, dan lisensi: `prototype\DATA.md` §4.

**Prareg.** `prototype\PRAREG_SKAB.md`, SHA-256 `c29805a228ddc8e7c2d9cfca2527085585626efc2a90c8c96b10131823cb014e`, dibekukan 28 Okt 2026 22:54:19 WIB **sebelum** data diunduh (`PRAREG_SKAB.sha256`); hash kode pra-data di `prototype\SKAB_KODE_PRADATA.sha256`. **Bukan** P1/P2 PRAREG-TKT4 v2: SKAB hanya 1 testbed (P1 butuh ≥ 8 unit fisik, P2 ≥ 3), dan model getaran terkunci tidak bisa dijalankan pada RMS 1 Hz. Status PRAREG v2 tetap **belum teruji / TIDAK KONKLUSIF**.

**Desain.** Unit = berkas eksperimen; leave-one-experiment-out (34 fold); berkas bebas anomali selalu di data latih; `assert_no_leakage` tiap fold (tes: `tests\test_skab.py`). H1: kejadian penutupan katup (`valve1` inlet 16 + `valve2` outlet 4 = 20) vs fault pompa (imbalance 5 + kavitasi 2 = 7), AUROC per kejadian. H2: deteksi anomali umum, AUROC per titik di 34 berkas. Baseline: B1 RMS getaran, B2 ambang arus, B3 z-maks per sensor. Bootstrap berpasangan 10.000×, Holm m = 2, α satu sisi 0,025; model harus mengalahkan **setiap** baseline. Satu deviasi format (nama kolom laju alir), `prototype\results\skab\DEVIASI.md`.

**Hasil primer** (`prototype\results\skab\run_skab_log.txt`, `primary.csv`, `auc_per_method.csv`, `summary.json`):

| | Residual R | B1 getaran | B2 arus | B3 z-maks | Status |
|---|---|---|---|---|---|
| **H1** AUROC kejadian, fault vs katup [CI95] | 1,000 [1,000; 1,000] | 0,571 [0,143; 0,857] | **1,000** [1,000; 1,000] | 0,571 [0,143; 0,857] | **GAGAL** |
| Δ R − baseline [CI95] | | +0,429 [+0,143; +0,857] | **0,000** [0; 0] | +0,429 [+0,143; +0,857] | p_H1 = 1,000 |
| **H2** AUROC titik [CI95] | 0,532 [0,488; 0,590] | 0,573 [0,481; 0,673] | 0,502 [0,480; 0,521] | 0,581 [0,493; 0,679] | **GAGAL** |
| Δ R − baseline [CI95] | | −0,041 [−0,109; +0,033] | +0,031 [−0,020; +0,092] | −0,049 [−0,113; +0,022] | p_H2 = 0,912 |

Pada ambang τ (kuantil 0,99 normal latih), R dan ambang getaran B1 **identik**: balanced accuracy per kejadian 0,857 [0,714; 1,000], 5/7 fault ditandai, 0/20 penutupan katup ditandai. Sekunder (`secondary.csv`, Holm): varian GBM mendeteksi anomali umum jauh lebih baik (AUROC titik 0,867 vs ≤ 0,581, signifikan) tetapi menandai 18/20 penutupan katup, jadi bukan pemisah katup vs fault. Pemusatan ulang per run tanpa label: R 0,629 vs B1 0,563 dan B2 0,507 (signifikan), vs B3 0,582 (tidak signifikan setelah Holm).

**Diagnostik post-hoc (tidak diprareg, `prototype\scripts\skab_posthoc.py`, `results\skab\posthoc_*`):**
1. **Perancu sesi/rezim.** Semua eksperimen katup direkam di Q ≈ 32 L/min dan P_app ≈ 226 VA sepanjang berkas, termasuk bagian normalnya; eksperimen imbalance/kavitasi di Q ≈ 125 L/min dan P_app ≈ 580 VA. Skor pada **baris normal saja** sudah memisahkan kedua kelompok berkas (AUROC 1,000 untuk R dan B2). AUROC 1,0 di H1 terutama mengukur *sesi rekaman*, bukan jenis anomali.
2. **Throttling SKAB kecil:** penutupan katup menurunkan Q ±6 % dan P_app < 1 %. Tidak ada ambang yang memberi alarm palsu pada kejadian katup, jadi tidak ada alarm palsu yang bisa dikurangi.
3. **Tekanan terkuantisasi** (10 nilai, langkah ±0,33 bar): kurva tekanan–debit tidak terukur; residual "hidraulik" tinggal daya ~ debit.
4. Deskriptif yang konsisten dengan teori, tetapi lemah karena butir 2: residual daya pada baris penutupan katup ≈ 0 (z_P 0,00 dan −0,01), sama dengan baris normal.

**Arti untuk klaim TKT (jujur).**
- Hasil ini adalah **uji komponen pada data lab pompa nyata milik pihak lain** (1 testbed), bukan rekaman lab sendiri dan **bukan integrasi sistem DetakPompa**.
- Untuk fungsi "memisahkan throttling dari fault", komponen residual hidraulik **GAGAL** menunjukkan keunggulan atas ambang sederhana. Ambang arus saja sudah memisahkan kedua kelompok, dan pemisahan itu sebagian besar datang dari perbedaan sesi rekaman. **Fungsi ini tidak naik ke TKT 4.** Klaim "AI membedakan katup vs aus" tetap **hipotesis**. Klaim itu tidak boleh muncul sebagai hasil di materi lomba, sesuai aturan pelaporan `PRAREG_SKAB.md` §7.
- Yang boleh dikatakan: "Kami sudah menjalankan model residual hidraulik di data lab pompa publik SKAB dengan prareg yang dibekukan sebelum data dibuka. Hasilnya GAGAL: tidak lebih baik dari ambang arus atau getaran. Data itu juga tidak bisa menguji klaim dengan tajam, karena throttling-nya kecil, tekanannya kasar, dan eksperimen katup direkam di rezim berbeda. Uji yang sah butuh rekaman sendiri dengan bukaan katup bertingkat dan fault di pompa yang sama, dalam sesi yang diacak (§3, TKT 4 butir 3)."
- **Keterbatasan:** 1 testbed; 1 Hz; getaran hanya RMS; label per titik dibuat penyusun SKAB; daya = V·I tanpa cos φ; hanya 7 kejadian fault. Lisensi GPL-3.0: kami hanya **memakai** data dan tidak menyalin kode SKAB. Data tidak didistribusikan ulang (`data\` di-gitignore). Kalau kelak data atau kode SKAB ikut didistribusikan bersama kode tim, bagian itu tunduk pada GPL-3.0.

## 3. Yang DIBUTUHKAN untuk naik tingkat
### PRAREG-TKT4 v2: syarat klaim AI (dibekukan 28 Okt 2026 21:41 WIB, sebelum ada data baru apa pun)
Teks lengkap dan mengikat: **`prototype\PRAREG_TKT4.md`**. SHA-256 `406e80259a32cc39b2c2aca394e0b1eb76f249a73b0822872d1db521d953abac`, disimpan bersama timestamp di `prototype\PRAREG_TKT4.sha256`. Folder ini tidak terlacak git (`.gitignore` berisi `*/`), jadi pengunci kodenya adalah manifes SHA-256 15 berkas kode di dalam prareg itu, bukan hash commit. Ringkasan (kalau berbeda, berkas prareg yang berlaku):
- **Model dan pembanding dikunci = versi purwarupa sekarang:** RF `SPEC_COLS` + `RF_PARAMS` (300 pohon, `min_samples_leaf=2`, `class_weight="balanced"`, `random_state=0`), gerbang SNR CFAR (pfa 0,01, dihitung ulang untuk laju sampel baru tanpa label), τ dari CV dalam (cakupan 0,9), k = 3. Pembanding: `RMSGateBaseline` / `RMSRecordingTriage` dengan gerbang identik. Penyesuaian yang diizinkan hanya `SHAFT_BAND` dari pelat nama, laju sampel, pembaca format berkas baru, dan skrip evaluasi; semuanya dicatat di addendum sebelum label dibuka.
- **Endpoint primer** (Holm atas m = 1 atau 2 uji, satu sisi α = 0,025; lulus bila batas bawah CI selisih > 0):
  - **P1 (H-AI1):** balanced accuracy 3-kelas pada **unit fisik yang tidak pernah dilihat** (leave-one-physical-unit-out, ≥ 8 unit), usulan − RMS + gerbang, bootstrap per unit 10.000×.
  - **P2 (H-AI2, bila data punya throttling/perubahan titik operasi):** balanced accuracy keputusan "perlu cek" pada {titik operasi berubah, mekanis sehat} ∪ {fault}, yaitu kemampuan membedakan throttling dari fault, usulan − RMS + gerbang (≥ 3 unit fisik).
- **Pengaman wajib:** tidak kehilangan fault (batas bawah CI selisih "fault ditandai perlu cek" > −0,10), tidak menambah alarm palsu (≤ RMS + 0,05), presisi@3 pada 3/22 dan 5/22 bermasalah ≥ RMS − 0,05.
- **Sekunder** (≤ 10 uji, Holm, dilaporkan semua): macro-F1, recall per kelas (recall waspada ditandai sebagai **label tahap, bukan deteksi dini**), jendela waspada yang ditandai perlu cek, AURC, titik operasi dua tahap, presisi@3 prevalensi realistis, ambang kW (bila ada data daya), aturan envelope + kurtosis.
- **Aturan berhenti:** satu analisis konfirmasi per dataset, tanpa intip di tengah, tanpa menambah data setelah melihat hasil. TIDAK KONKLUSIF bila unit/sesi kurang, gerbang menolak > 30 % jendela sehat, atau kode terkunci tidak bisa dijalankan tanpa perubahan terlarang.
- **Kalau gagal:** kata "AI" dicabut dari klaim inti; produk = gerbang sinyal + ambang RMS + antrean; semua angka dilaporkan apa adanya; metrik sekunder tidak boleh dipakai sebagai hiburan.

**PRAREG-TKT4 v1 (DICABUT 28 Okt 2026 malam, tidak pernah dijalankan pada data apa pun).** Endpoint utamanya, recall waspada 3-kelas dengan split per sesi, bisa naik hanya dengan menggeser batas waspada/rusak tanpa menandai pompa lebih awal (§2b: 0,830 vs 0,840), dan tidak menguji alasan AI dipakai. Jangan dikutip lagi.

**TKT 4: validasi di lab, dengan rekaman sendiri**
1. Satu motor + pompa sentrifugal di lab (ITS/ITB) `[ISI: akses lab]`.
2. Akselerometer di bearing housing pompa dan motor, clamp arus 1 fasa (atau 3 fasa), serta **power meter** (kW). Untuk kinerja hidrolik: flowmeter portable dan manometer isap/tekan.
3. Kondisi yang diinduksi, mengikuti desain S8: sehat; tidak seimbang (massa di kopling/impeller); misalignment; katup throttling (titik kerja bergeser). Setiap kondisi direkam ≥5 kali × 30 s, **dari sesi berbeda** (lepas-pasang sensor), supaya alarm palsu mode deviasi bisa diukur. Untuk P1 prareg v2 dibutuhkan ≥ 8 unit fisik (pompa atau bantalan yang dapat ditukar); dengan satu pompa, P1 = TIDAK KONKLUSIF dan hanya P2 (≥ 3 unit) yang bisa diuji.
4. Ukur **ΔkW dan ΔkWh/m³** per kondisi dengan power meter + flowmeter. Ini satu-satunya cara memperoleh angka energi milik sendiri.
5. Jalankan evaluasi dengan split per **unit fisik**, model dan pembanding terkunci, endpoint dan kriteria lulus/gagal **persis** seperti `prototype\PRAREG_TKT4.md` v2. Fitur arus (MCSA: sideband slip, garis 2×f_line) atau kW sebagai masukan model = model baru, jadi hanya boleh lewat prareg baru; di v2 kW hanya dipakai sebagai pembanding sekunder (ambang kW).

**TKT 5: lingkungan pengguna**
1. Izin direksi PDAM Surya Sembada lewat penulis S6 (ITS) untuk ≥3 pompa di IPA Ngagel. Lihat `AKSI_MANUSIA.md`.
2. Rekaman berkala selama ≥4 minggu, ditambah data kWh/m³ PDAM dan catatan perawatan atau rekondisi sebagai label.
3. Ukur bersama operator: apakah urutan triase sesuai dengan pompa yang hasil auditnya terburuk (misalnya pompa T1 49,77 % di S6)?

## 4. Data dan atribusi
- Dataset: Ottawa UORED-VAFCLS v5, CC BY 4.0 (`prototype/DATA.md`). Dataset pompa 4TU tidak dapat diakses (koneksi gagal), sehingga tidak dipakai.
- Dataset lab pompa: SKAB v0.9 (Katser & Kozitsin 2020, Kaggle DOI 10.34740/KAGGLE/DSV/1693952), **GPL-3.0**, hanya dipakai sebagai data (`prototype/DATA.md` §4, hasil §2e).
- Kode DSP diadaptasi dari FaceVitals (Poggy + Aziz), dengan atribusi di `prototype/README.md` dan `detakpompa/spectral.py`.
- Angka energi di demo hanya dari S6 dan S10, dengan label "skenario, bukan pengukuran".
