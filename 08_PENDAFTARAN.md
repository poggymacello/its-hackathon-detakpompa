# 08_PENDAFTARAN: paket pendaftaran DetakPompa
### Agen A9 "Penulis Pitch" · 28 Okt 2026 · tim: Aziz (PIC), Uqi, Pio, Poggy

**Dasar:** `00_INFO.md`, `03_RISET.md` (S-nomor), `03b_ADVOKAT_SETAN.md`, `04_KEPUTUSAN.md` (termasuk revisi posisi "triase"), `05_BUKTI_TKT.md`, `06_VALIDASI_PENGGUNA.md`, `07_BISNIS_DAMPAK.md`, `prototype\README.md`, `prototype\results\*`.

**Aturan yang dipakai di file ini:**
- Setiap angka punya rujukan: file hasil di `prototype\results\`, `[Sx]` dari `03_RISET.md` §0, atau `[Bx]` dari `07_BISNIS_DAMPAK.md` §10.
- Angka hemat energi selalu diberi label **[SKENARIO]**. Belum ada satu kWh pun yang diukur tim.
- Belum ada wawancara pengguna. Tidak ada kutipan pengguna di file ini, dan persona simulasi (`03b` §2.9, `06` §6) **tidak** dipakai.
- Format form resmi belum diketahui karena ada di balik login (`00_INFO.md`). Karena itu disiapkan tiga panjang: 150 kata, 300 kata, 1 halaman. Pilih yang sesuai batas karakter form.
- Semua `[ISI: ...]` wajib diisi manusia sebelum dikirim. Kalau tidak bisa diisi, hapus kalimatnya. Jangan diganti tebakan.

---

## 1. Versi 150 kata

> **DetakPompa: memilih 3 dari 22 pompa PDAM yang diukur debitnya duluan**
>
> Biaya energi PDAM Surya Sembada Surabaya Rp147,65 miliar (2021), 24,37 % biaya operasional. Di IPA Ngagel I, audit manual hanya mengukur 12 dari 22 pompa; lima bekerja di bawah ±55 % [S6]. DetakPompa mengurutkan pompa yang paling patut diukur debitnya lebih dulu, tanpa mengukur efisiensi. Random forest dengan fitur spektral getaran memberi skor kondisi untuk antrean. Kalau sinyal jelek, jawabannya TIDAK TAHU plus langkah berikutnya. Bukti TKT 3 (leave-one-bearing-out, 20 bantalan publik Ottawa): akurasi seimbang 0,608, tidak lebih baik dari ambang RMS (0,640). Gerbang sinyal DSP, bukan AI, menolak 98,8 % rekaman sensor lepas. Uji pemisahan katup-ditutup vs pompa-rusak di data lab pompa publik SKAB (prareg terkunci sebelum data dibuka) gagal: tidak lebih baik dari ambang arus, dan datanya kurang tajam untuk menguji klaim itu. Uji berikutnya: rig pompa sendiri dengan throttling bertingkat; syarat lulusnya sudah dibekukan.

*(≤150 kata termasuk judul; hitungan skrip di §8. Sumber angka: [S6]; `prototype\results\metrics_summary.csv`; `prototype\results\degradation_summary.csv`; `prototype\results\skab\summary.json`.)*

---

## 2. Versi 300 kata

> **DetakPompa: memilih 3 dari 22 pompa PDAM yang diukur debitnya duluan**
>
> **Masalah.** Biaya energi PDAM Surya Sembada Surabaya Rp147,65 miliar (2021), 24,37 % biaya operasional [S6]. SEC IPA Ngagel I 0,27–0,29 kWh/m³ tampak sehat, tetapi masalahnya tersembunyi per pompa: audit manual hanya mengukur 12 dari 22 pompa karena debit diukur dengan flowmeter portabel, dan 5 dari 12 itu bekerja di bawah ±55 % (terendah 49,77 %) [S6].
>
> **Solusi.** DetakPompa adalah alat triase. Random forest dengan fitur spektral getaran memberi skor kondisi untuk mengurutkan pompa yang paling patut diukur debitnya atau direkondisi lebih dulu. Tahap berikutnya: membaca power meter yang sudah terpasang di tiap panel [S6]. Alat ini tidak mengukur efisiensi. Kalau sinyal jelek atau model ragu, jawabannya TIDAK TAHU dengan langkah berikutnya.
>
> **Bukti TKT 3.** Leave-one-bearing-out (20 fold) pada data bantalan publik Ottawa (CC BY 4.0), tiga baseline, selang kepercayaan bootstrap. Akurasi seimbang kami 0,608 [0,532–0,687]; ambang RMS 0,640 [0,558–0,727]. Dengan gerbang sinyal yang sama, keduanya setara (−0,034 [−0,155; +0,071]); presisi 3 pompa teratas usulan 0,791, RMS 0,765, bila 5 dari 22 bermasalah. Penolakan 98,8 % rekaman sensor lepas adalah jasa gerbang DSP, bukan AI. Data ini bantalan, bukan pompa.
>
> **Uji di data pompa.** Kami lalu menguji pemisahan "katup ditutup vs pompa rusak" di data lab pompa publik SKAB (1 testbed), dengan prareg terkunci hash sebelum data diunduh. Hasilnya gagal: model residual kami tidak lebih baik dari ambang arus. Data itu juga kurang tajam: eksperimen katup dan kerusakan direkam di sesi berbeda. Uji berikutnya: rig pompa sendiri dengan throttling bertingkat dan sesi diacak; syarat lulusnya sudah dibekukan.
>
> **Pengguna dan jalur.** Pilot riset ITS–PDAM lewat penulis paper audit Ngagel I [S6], bukan pembelian. Wawancara pengguna: [ISI: jumlah dan peran responden].
>
> **Dampak [SKENARIO].** Titik impas langganan satu IPA = 76.464 kWh/tahun (`07_BISNIS_DAMPAK.md` §3.4).
>
> **Tim:** [ISI: 4 nama, prodi, kampus].

*(≤300 kata termasuk judul; hitungan skrip di §8. Sumber: [S6], `prototype\results\metrics_summary.csv`, `rmsgate_paired_bootstrap.csv`, `degradation_summary.csv`, `triase\eval_prevalensi_log.txt`, `prototype\PRAREG_SKAB.md`, `prototype\results\skab\summary.json`, `posthoc_log.txt`, `07_BISNIS_DAMPAK.md` §3.4.)*

---

## 3. Versi 1 halaman

### DetakPompa: memilih 3 dari 22 pompa PDAM yang diukur debitnya duluan
*Antrean audit untuk 22 pompa IPA Ngagel I dari rekaman getaran singkat per pompa. Tahap berikutnya: membaca power meter yang sudah terpasang di tiap panel [S6].*
**Sektor:** energi–air (utilitas air minum) · **Lokasi masalah:** Surabaya, Jawa Timur · **TKT saat daftar:** 3 (bukti di bawah)

**1. Masalah dan energy gap (bersumber)**
- Biaya energi PDAM Surya Sembada **Rp147.654.439.569 (2021)**, **24,37 %** dari biaya operasional. Listrik unit produksi = 76 % energi PDAM. Biaya energi **Rp409/m³**, di atas rata-rata nasional Rp356,34/m³ [S6].
- IPA Ngagel I punya **8 pompa air baku + 14 pompa distribusi**. Audit energi manual (ITS + PDAM) hanya mengukur **5 dari 8** dan **7 dari 14**, karena debit diukur dengan flowmeter ultrasonik portabel [S6].
- Dari 12 pompa yang terukur, **5 bekerja di bawah ±55 %**. Terendah: pompa distribusi T1, **49,77 %** [S6].
- Di level IPA, masalah ini tidak terlihat: SEC Ngagel I **0,27 kWh/m³ (2021)** dan **0,29 (2022)**, sudah di bawah patokan 0,4 [S6]. Pompa yang menurun tersembunyi di angka bulanan.
- Keausan memang menaikkan energi: pada satu kasus lapangan, celah wear-ring yang terbuka menurunkan efisiensi pompa dari **65,2 % ke 53,6 %** [S10].
- **Energy gap yang kami sasar:** waktu antara pompa mulai menurun dan pompa itu diaudit. Untuk 10 dari 22 pompa Ngagel I, audit yang dilaporkan di [S6] tidak menjangkaunya sama sekali.

**2. Solusi: triase, bukan pengukur efisiensi**
- DetakPompa membaca getaran pompa, menilai kondisinya terhadap pola sehat, lalu memberi **skor prioritas cek** (0 = sehat … 1 = rusak) untuk mengurutkan pompa yang perlu diukur debit dan head-nya, atau direkondisi, lebih dulu. Keluarannya satu tabel antrean armada: **AUDIT DULU** (maks. 3 pompa), **PANTAU**, **UKUR ULANG**, **AMAN** (`prototype\triase.py`).
- **Kami tidak mengklaim mengukur efisiensi.** Efisiensi pompa butuh debit (Q), head (H), dan daya: Ph = 0,163 × Q × H, η = Ph/Pi [S6]. Getaran saja tidak cukup.
- **Abstain dua tahap.** (1) Gerbang sinyal: garis putaran poros harus terlihat di atas derau, dan sinyal tidak boleh terpotong atau datar. (2) Gerbang ragu: probabilitas tertinggi harus melewati ambang yang dipilih dari validasi silang di data latih. Kalau salah satu gagal, keluarannya **TIDAK TAHU** dengan langkah berikutnya (pasang ulang sensor, ukur ulang 30 detik, atau ukur debit manual), dan pompa masuk antrean **UKUR ULANG**. Rekaman yang ditolak gerbang sinyal **tidak diberi prioritas**, jadi sensor lepas tidak pernah mendahului pompa yang benar-benar rusak. Tahap (1) adalah aturan DSP dan terbukti bekerja; tahap (2) bisa dipasang di model apa pun, termasuk ambang RMS.
- Tahap berikutnya: membaca **power meter Schneider PM2100 yang sudah terpasang di tiap panel** Ngagel I [S6], supaya PDAM tidak perlu alat arus baru. Data tetap on-prem, tanpa koneksi ke SCADA.

**3. TKT 3 dan buktinya**

| Klaim | Angka | File bukti |
|---|---|---|
| Proof of concept di data nyata, tanpa kebocoran | Leave-one-bearing-out, 20 fold, 600 jendela 1 s dari 60 rekaman Ottawa UORED-VAFCLS (CC BY 4.0) [S13]. Train ∩ test = ∅ dicek di tiap fold | `prototype\detakpompa\splits.py`, `prototype\tests\test_split.py`, `prototype\results\folds.csv` |
| Akurasi vs 3 baseline (peluang acak 0,333) | Ambang RMS **0,640** [0,558–0,727] · usulan **0,608** [0,532–0,687] · RF fitur statistik 0,553 [0,465–0,645] · aturan envelope + kurtosis 0,432 [0,357–0,510] | `prototype\results\metrics_summary.csv` |
| Selisih berpasangan | Usulan − RMS = **−0,030** [−0,145; +0,067]: **tidak mengalahkan RMS**. Usulan − envelope = +0,179 [+0,083; +0,292] | `prototype\results\paired_bootstrap.csv` |
| Pembanding adil: RMS + gerbang SNR yang sama | Pada jendela yang sama: usulan 0,605 vs RMS + gerbang **0,639**, selisih −0,034 [−0,155; +0,071]. AURC galat (skor keyakinan RMS = jarak log ke ambang, ditetapkan sebelum run) 0,229 vs 0,291, selisih −0,062 [−0,195; +0,076]: **tidak signifikan**. Recall waspada 0,415 vs 0,213 (+0,202 [−0,056; +0,453]) adalah beda **label tahap**, bukan deteksi dini: jendela waspada yang ditandai perlu cek 0,830 vs 0,840. Recall rusak 0,470 vs **0,795**. Setelah koreksi Holm (22 uji) tidak ada yang signifikan | `prototype\results\rmsgate_metrics.csv`, `rmsgate_paired_bootstrap.csv`, `rmsgate_coverage_risk.png` |
| Triase armada: presisi 3 teratas | 2000 armada simulasi × 20 bearing, leave-one-bearing-out, **2/3 pompa bermasalah** (dasar acak 0,667): presisi@3 "perlu cek" usulan 0,971 vs RMS + gerbang 0,952, selisih +0,019 [−0,333; +0,333], seri di 87 % armada. Prevalensi realistis, armada 22 pompa: **3 bermasalah** (dasar acak 0,136) 0,707 vs 0,682, +0,022 [−0,333; +0,333]; **5 bermasalah** (0,227) 0,791 vs 0,765, +0,026 [−0,333; +0,500]. Kedua model salah menandai rekaman sehat yang sama (H_13_0), sehingga ±5–6 dari 10 armada punya ≥1 pompa sehat di AUDIT DULU. **Setara** di semua skenario | `prototype\results\triase\eval_log.txt`, `eval_summary.json`, `eval_prevalensi_log.txt` |
| Tahan sensor lepas (jasa gerbang DSP) | Gerbang SNR menolak **98,8 %** jendela derau murni ("sensor lepas") dan 4,5 % jendela bersih, sama untuk usulan maupun RMS. Gerbang keyakinan model saja meloloskan 88–97 % jendela derau. Tanpa gerbang SNR, model tetap menjawab "rusak" dengan yakin | `prototype\results\degradation_summary.csv`, `prototype\results\demo\laporan_sensor_lepas.txt` |
| Uji di data lab pompa milik pihak lain: memisahkan penutupan katup dari fault pompa | SKAB v0.9 (1 testbed Skoltech, 1 Hz, arus/tegangan/debit/tekanan/RMS getaran; GPL-3.0, hanya dipakai sebagai data). Prareg `prototype\PRAREG_SKAB.md` dikunci SHA-256 **sebelum** data diunduh; leave-one-experiment-out 34 fold; model harus mengalahkan **setiap** baseline. **H1** (20 kejadian katup vs 7 fault, AUROC): residual 1,000 vs ambang arus **1,000**, selisih 0,000 → **GAGAL**. **H2** (anomali umum, AUROC titik): 0,532 vs 0,573 / 0,502 / 0,581 → **GAGAL** (p = 0,912). Post-hoc (tidak diprareg): eksperimen katup direkam di Q ≈ 32 L/min, fault di ≈ 125 L/min, jadi H1 terutama mengukur sesi rekaman; penutupan katup hanya menurunkan Q ±6 %. Artinya: klaim "AI memisahkan throttling dari aus" **tetap hipotesis**, tidak terbukti dan juga tidak terbantah. Ini **bukan** TKT 4 | `prototype\results\skab\summary.json`, `run_skab_log.txt`, `posthoc_log.txt`, `DEVIASI.md`; `05_BUKTI_TKT.md` §2e |
| Kode teruji | **54/54 tes lulus** (12 di antaranya untuk SKAB) | `prototype\results\pytest_output.txt` |

**Kenapa kami menulis "tidak lebih akurat dari RMS".** Banyak studi di dataset bantalan CWRU melaporkan akurasi mendekati 100 %. Rosa dkk. menyebut hasil itu terlalu optimistis karena pembagian datanya bocor, dan contoh Hendriks dkk. yang mereka kutip turun dari 95 % ke 53 % setelah split diperketat. Tinjauan yang dikutip Vieira dkk. [S14] menemukan **40 dari 41** studi CWRU memakai desain yang rentan bias ini (`03b_ADVOKAT_SETAN.md` §2.1). Kami membagi data per bantalan, memasang tiga baseline, dan melaporkan selang kepercayaan. Hasilnya: AI kami belum lebih baik dari ambang sederhana yang diberi gerbang sinyal yang sama. Karena itu kami membekukan lebih dulu, sebelum ada data baru, syarat yang harus dipenuhi AI (`prototype\PRAREG_TKT4.md` v2, SHA-256 di `PRAREG_TKT4.sha256`): di unit fisik yang tidak pernah dilihat, AI harus mengalahkan RMS + gerbang dalam akurasi seimbang, dan, bila data punya throttling katup, dalam membedakan throttling dari kerusakan; batas bawah CI 95 % selisih > 0 setelah koreksi Holm, tanpa kehilangan pompa rusak dan tanpa menambah alarm palsu. Kalau gagal, klaim AI dicabut (`05_BUKTI_TKT.md` §3). Disiplin yang sama kami pakai di data lab pompa SKAB: prareg dikunci sebelum data diunduh, dan hasilnya kami laporkan walaupun gagal. Angka yang lebih kecil dan jujur lebih berguna bagi PDAM daripada 99 % yang tidak akan bertahan di rumah pompa.

**Batas klaim.** Data Ottawa adalah rig bantalan, **bukan pompa**, dan **tidak berisi arus motor**. Sampel kecil (20 unit). Membedakan "waspada" dari "rusak" masih lemah (F1 waspada 0,429). Abstain kadang mengenai rekaman yang benar-benar rusak (C_16_2 → TIDAK TAHU), jadi TIDAK TAHU berarti "ukur ulang", bukan "aman": 69 dari 76 jendela TIDAK TAHU (91 %) di uji berasal dari bantalan berkembang/rusak (`prototype\README.md`, Keterbatasan). Satu-satunya uji di data pompa (SKAB, data lab pihak lain, 1 testbed) **gagal** untuk hipotesis yang diprareg (H1 dan H2), dan datanya tidak cukup tajam untuk klaim katup vs aus (perancu sesi, throttling kecil, tekanan terkuantisasi). Uji berikutnya yang sah: rig pompa sendiri dengan bukaan katup bertingkat (≥ 20–30 % Q) dan fault di pompa yang sama, sesi diacak, ≥ 3 unit (`05_BUKTI_TKT.md` §3). TKT 4 (validasi di lab) dan TKT 5 (lingkungan pengguna) **belum**.

**4. Pengguna dan jalur pilot**
- **Pengguna utama:** kepala IPA/unit produksi (memilih pompa mana yang direkondisi), teknisi pemeliharaan, dan operator rumah pompa di PDAM Surya Sembada. **Pembeli:** Direksi lewat RKAP tahunan (Board Manual PDAM, `06_VALIDASI_PENGGUNA.md` §0).
- **Jalur pilot:** kerja sama riset ITS–PDAM lewat penulis paper audit Ngagel I [S6] (penulis dari ITS dan PDAM), di 1–2 pompa yang kondisinya sudah diketahui dari audit itu sebagai *ground truth*. Bukan pembelian. Tidak ada uang atau hadiah untuk staf PDAM (Board Manual memuat pengendalian gratifikasi).
- **Lokasi cadangan untuk TKT 4:** pompa gedung di Sarpras ITB `[ISI: status izin]`.
- **Validasi pengguna sejauh ini:** [ISI: hasil wawancara — jumlah responden, peran, hipotesis yang lulus/gagal dari `06_VALIDASI_PENGGUNA.md` §7.2]. Kalau belum ada, tulis: "Wawancara dijadwalkan; skrip, form persetujuan, dan kriteria lulus/gagal sudah disiapkan (`06_VALIDASI_PENGGUNA.md` §2–§4)."

**5. Dampak [SKENARIO, bukan pengukuran]** (hitungan di `07_BISNIS_DAMPAK.md` §3–§4)
- **Pilot riset sendiri menghemat 0 kWh.** Pilot hanya membuktikan ketepatan urutan triase.
- Hemat terjadi **hanya kalau PDAM mengaudit lalu merekondisi** pompa yang ditandai. Contoh skala: lima pompa buruk yang sudah ditemukan audit S6, bila dinaikkan ke efisiensi 60 %, bernilai 122,53 kW atau 536.681–858.690 kWh/tahun (asumsi utilisasi 50–80 %). Nilai ini milik audit dan rekondisi PDAM, **bukan** klaim DetakPompa.
- Yang bisa diatribusikan ke DetakPompa adalah kWh yang dihemat **lebih awal**. Untuk satu IPA: skenario konservatif 12.352 kWh/tahun (Rp12,8 juta; 10,7 tCO₂e), skenario moderat 171.766 kWh/tahun (Rp177,9 juta; 149 tCO₂e). Tarif Rp1.035,78/kWh [S19], faktor emisi Jamali 0,87 tCO₂/MWh (nilai 2019) [S21]. Semua parameter kejadian dan waktu adalah [ASUMSI].
- **KPI harus kWh/m³, bukan kW.** Setelah rekondisi, kW pompa bisa *naik* karena debitnya naik: di 63 uji pompa irigasi, daya input naik di 58 % instalasi walaupun efisiensi rata-rata naik 33 %, dan energi baru turun (−22 %) bila volume air tetap [Hanson 2002, peer-reviewed; `11_RISET_KELEMAHAN.md` L6.4]. Jadi yang diukur adalah kWh/m³ per stasiun pada permintaan atau tekanan header yang sama.
- **Titik impas:** langganan untuk 22 pompa baru layak kalau dalam setahun DetakPompa membuat satu pompa yang menurun ±24,5 kW direkondisi ±4,3 bulan lebih awal (76.464 kWh/tahun).

**6. Model bisnis (ringkas)** (`07_BISNIS_DAMPAK.md` §2–§3)
Fase 0 pilot riset tanpa pembelian → Fase 1 kampanye triase 3 bulan per IPA ([ASUMSI] Rp30 juta) → Fase 2 langganan ([ASUMSI] Rp300.000/pompa/bulan). Capex satu IPA ±Rp40,2 juta, lebih dari separuhnya masih [ASUMSI]. Pasar lanjutan: 38 Perumda air minum di Jawa Timur [B7].

**7. Tim**

| Nama panggilan | Nama lengkap | Prodi | Kampus | Peran |
|---|---|---|---|---|
| Aziz | [ISI: nama lengkap] | [ISI: prodi] | [ISI: kampus] | PIC, review, pengirim berkas; pemilik bersama kode DSP FaceVitals |
| Poggy | [ISI: nama lengkap] | [ISI: prodi] | [ISI: kampus] | [ISI: peran, mis. pembangun purwarupa dan penulis]; pemilik bersama kode DSP FaceVitals |
| Uqi | [ISI: nama lengkap] | [ISI: prodi] | [ISI: kampus] | [ISI: peran, mis. validasi pengguna] |
| Pio | [ISI: nama lengkap] | [ISI: prodi] | [ISI: kampus] | [ISI: peran, mis. validasi pengguna dan jalur pilot] |
| Dosen pembimbing | [ISI: nama, kalau ada] | [ISI] | [ISI] | [ISI] |

---

## 4. Deskripsi purwarupa (untuk kolom "deskripsi purwarupa" atau lampiran)

**Apa yang jalan hari ini** (`prototype\`, Python 3.11, dijalankan di laptop tanpa GPU):
1. **Masukan:** satu rekaman getaran (file MAT Ottawa, CSV satu kolom, atau NPY) dengan laju sampel yang diketahui. Rekaman dipotong menjadi jendela 1 detik (`detakpompa\io.py`).
2. **Pengolahan sinyal:** spektrum daya, pelacakan frekuensi putaran poros dengan algoritma Viterbi, dan SNR garis poros. Bagian ini diadaptasi dari kode FaceVitals milik dua anggota tim (Poggy dan Aziz), dari pita detak jantung ke pita mesin (`detakpompa\spectral.py`). Status TKT FaceVitals **tidak** diwariskan.
3. **Model:** random forest dengan fitur spektral (energi pita, centroid/flatness/entropy, frekuensi poros terlacak, harmonik 1×/2×/3×, fitur envelope). Hiperparameter tetap, tidak disetel di data uji (`detakpompa\features.py`, `detakpompa\models.py`).
4. **Abstain dua tahap:** gerbang sinyal (ambang SNR 11,52 dB dari kuantil 99 % derau putih, tanpa melihat label) dan gerbang ragu (ambang keyakinan dari validasi silang di data latih) (`detakpompa\models.py`, `AbstainGate`).
5. **Keluaran** (`demo.py`, `detakpompa\report.py`): status SEHAT / WASPADA / RUSAK / TIDAK TAHU, antrean, skor prioritas cek (tidak ada untuk rekaman yang ditolak gerbang sinyal), alasan, kualitas sinyal, langkah berikutnya, dan catatan energi berlabel **[SKENARIO, BUKAN PENGUKURAN]**. Mode opsional `--baseline` membandingkan rekaman dengan rekaman sehat unit yang sama.
6. **Triase armada** (`triase.py`): folder rekaman beberapa pompa → satu tabel antrean AUDIT DULU / PANTAU / UKUR ULANG / AMAN dengan alasan dan langkah berikutnya. Contoh: `prototype\results\triase\armada_22\antrean_usulan.txt`.
7. **Evaluasi** (`run_eval.py`, `run_eval_rms_gate.py`, `run_triase_eval.py`): leave-one-bearing-out 20 fold, tiga baseline + RMS dengan gerbang yang sama, bootstrap per unit, kurva cakupan-risiko, uji degradasi derau, dan presisi top-3 armada. Semua hasil ditulis ke `prototype\results\`.
8. **Tes:** 54 tes pytest, termasuk tes anti-bocor, tes bahwa catatan energi selalu berlabel skenario, dan 12 tes untuk uji SKAB (`prototype\results\pytest_output.txt`; 1 tes butuh data SKAB dan dilewati bila data belum diunduh).
9. **Uji data lab pompa** (`run_skab.py`, `detakpompa\hydraulic.py`): model residual hidraulik (perilaku normal bersyarat titik kerja) vs tiga baseline di SKAB, sesuai `PRAREG_SKAB.md`. Hasil: GAGAL (§3 tabel; `05_BUKTI_TKT.md` §2e).

**Contoh keluaran nyata** (tidak dipilih yang bagus saja; `prototype\results\demo\`):

| File | Label asli | Keluaran | Catatan |
|---|---|---|---|
| `laporan_H_3_0.txt` | sehat | **SEHAT** (prioritas 0,02) | Benar |
| `laporan_I_3_1.txt` | waspada | **RUSAK** (prioritas 0,88) | Tingkatnya salah, tetapi pompa tetap masuk daftar cek |
| `laporan_O_8_2.txt` | rusak | **TIDAK TAHU** (model ragu, probabilitas tertinggi 0,36), antrean UKUR ULANG, prioritas sementara 0,48 | Langkah berikut: ukur ulang, bandingkan dengan baseline, lalu cek debit |
| `laporan_C_16_2.txt` | rusak | **TIDAK TAHU** (garis poros tenggelam, SNR 0,2 dB), antrean UKUR ULANG | Contoh abstain yang mengenai pompa rusak. Karena itu TIDAK TAHU = "ukur ulang", bukan "aman" |
| `laporan_I_3_1_derau_-10dB.txt` | waspada + derau | **TIDAK TAHU** (SNR 4,7 dB) | Derau ditolak |
| `laporan_sensor_lepas.txt` | derau murni | **TIDAK TAHU**, antrean UKUR ULANG, **tanpa prioritas** (model sendiri memberi "rusak" 0,74) | Tanpa gerbang SNR, alat akan salah alarm. Penolakan ini jasa gerbang DSP |
| `laporan_I_3_1_vs_baseline_H_3_0.txt` | waspada vs sehat unit sama | RUSAK + skor deviasi 11,41 | Mode deviasi belum tervalidasi (lihat `05_BUKTI_TKT.md` §2) |

**Yang belum ada (ditulis supaya juri tidak perlu menebak):** pompa sendiri (satu-satunya data pompa adalah data lab SKAB milik pihak lain, dan ujinya gagal), arus motor di data getaran yang dipakai model, rekaman lab sendiri, pembacaan power meter panel, antarmuka web/ponsel, perangkat sensor terpasang, dan uji di lokasi pengguna.

**Atribusi data:** Sehri, M., & Dumond, P. (2023). *UORED-VAFCLS* (v5). Mendeley Data. doi:10.17632/y2px5tg92h.5, CC BY 4.0. Perubahan: dipotong jendela 1 s, high-pass 10 Hz, ekstraksi fitur, derau sintetis untuk uji degradasi (`prototype\DATA.md`).

---

## 5. Daftar lampiran

| # | Lampiran | Sumber / status | Siapa |
|---|---|---|---|
| L1 | Link video demo ≤2 menit: `demo.py` dijalankan langsung pada H_3_0 (SEHAT), I_3_1 (RUSAK), dan `sensor_lepas.npy` (TIDAK TAHU, UKUR ULANG), lalu `triase.py` pada armada contoh 22 rekaman | [ISI: link video] (belum direkam; `AKSI_MANUSIA.md` #5) | Poggy |
| L2 | Link repositori kode (tanpa folder `data\`, karena data Ottawa diunduh ulang lewat `DATA.md`) | [ISI: link repo, kalau form meminta dan tim setuju repo dibuka] | Poggy (unggah), Aziz (setuju) |
| L3 | Gambar kurva cakupan-risiko | `prototype\results\coverage_risk.png` (sudah ada) | — |
| L3b | Gambar SKAB ruang Q–P, dengan caption: "Uji diprareg GAGAL. Eksperimen katup dan fault direkam di rezim berbeda, jadi data ini tidak bisa menguji pemisahan katup vs aus dengan tajam." | `prototype\results\skab\ruang_Q_p_P.png` (sudah ada) | — |
| L4 | Screenshot tabel hasil vs baseline | [ISI: screenshot dari `prototype\README.md` bagian Hasil, atau tabel yang dibuat dari `metrics_summary.csv`] | Poggy |
| L5 | Screenshot tiga laporan demo (SEHAT, RUSAK, TIDAK TAHU) | [ISI: screenshot terminal dari `prototype\results\demo\laporan_H_3_0.txt`, `laporan_I_3_1.txt`, `laporan_sensor_lepas.txt`] | Poggy |
| L6 | Screenshot uji degradasi (persentase abstain per tingkat derau) | [ISI: screenshot tabel dari `prototype\README.md` atau `degradation_summary.csv`] | Poggy |
| L7 | Screenshot 54 tes lulus | [ISI: screenshot dari `prototype\results\pytest_output.txt`] | Poggy |
| L8 | Ringkasan bukti TKT (PDF dari `05_BUKTI_TKT.md`) | [ISI: konversi ke PDF kalau form meminta dokumen] | Pio |
| L9 | Surat/izin mitra pilot | **Belum ada.** Jangan lampirkan apa pun yang menyerupai surat minat. [ISI: lampirkan hanya kalau sudah ada surat asli] | Aziz |

---

## 6. Cek sebelum menyalin ke form
- [ ] Tidak ada kalimat "akurasi 9x %" atau "lebih akurat dari metode klasik".
- [ ] Tidak ada klaim "mengukur efisiensi", "menghemat X kWh", atau "TKT 4/5".
- [ ] Hasil SKAB ikut tertulis sebagai **GAGAL** di versi yang dikirim (150/300/1 halaman). Tidak ada kalimat "AI membedakan katup vs aus" sebagai hasil, dan SKAB tidak disebut "TKT 4".
- [ ] Panjang teks dihitung ulang setelah setiap edit (§8). Angka tes = 54.
- [ ] Tidak ada kutipan dari persona simulasi (`03b` §2.9, `06` §6). Bagian validasi pengguna hanya berisi hasil wawancara asli atau kalimat "dijadwalkan".
- [ ] Setiap angka energi berlabel [SKENARIO] atau bersumber [S6]/[S10]/[S19]/[S21].
- [ ] Include (startup ITS) dan OPTIME disebut di bagian pembanding, kalau form punya kolom itu (`09_DECK_OUTLINE.md` slide 6). Tidak ada klaim "pertama".
- [ ] Semua `[ISI]` sudah terisi atau kalimatnya dihapus.
- [ ] Atribusi dataset Ottawa (CC BY 4.0) dan asal kode FaceVitals tercantum.

## 7. Sumber yang dirujuk
| ID | Isi | Tempat |
|---|---|---|
| S6 | Indra dkk., *JIST* 5(2), Feb 2024: efisiensi pompa IPA Ngagel I, PDAM Surya Sembada | `03_RISET.md` §0; detail tabel di `06_VALIDASI_PENGGUNA.md` §0 dan `07_BISNIS_DAMPAK.md` §3.2 |
| S10 | Nelik, *Pumps & Systems*, 3 Okt 2016: pompa aus 65,2 % → 53,6 % | `03_RISET.md` §0 |
| S13 | Ottawa UORED-VAFCLS v5, CC BY 4.0 | `03_RISET.md` §0, `prototype\DATA.md` |
| S14 | Vieira dkk., arXiv 2509.22267: kebocoran data di benchmark bantalan; 40/41 studi CWRU rentan | `03_RISET.md` §0, `03b_ADVOKAT_SETAN.md` §2.1 |
| Rosa dkk. | arXiv 2407.14625: split CWRU umum bocor, akurasi "nearly 100%"; contoh Hendriks 95 % → 53 % | `03b_ADVOKAT_SETAN.md` §2.1, §7.1 |
| S19 | Permen ESDM 7/2024, tarif Rp1.035,78/kWh LWBP B-3/I-3 | `03_RISET.md` §0 |
| S21 | Faktor emisi Jamali 0,87 tCO₂/MWh (nilai 2019) | `03_RISET.md` §0 |
| B7 | Rakerda Perpamsi Jatim: 38 Perumda | `07_BISNIS_DAMPAK.md` §10 |

## 8. Hitungan kata (28 Okt 2026, skrip)
Dihitung dengan memisah teks kutipan §1 dan §2 per spasi, **termasuk judul**, penanda `**` dibuang. Simbol yang berdiri sendiri (`%`, `vs`, `[S6]`) ikut dihitung sebagai kata, jadi hitungan form biasanya sama atau lebih kecil.

| Versi | Batas | Hitungan |
|---|---|---|
| §1 | 150 | **148** |
| §2 | 300 | **297** |

Kalau form menghitung karakter, hitung ulang di form. Kalau terlalu panjang, potong kalimat dampak atau pengguna dulu, **jangan** kalimat SKAB atau kalimat RMS.
