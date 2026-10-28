# JURI_90 / SKOR_P3: DetakPompa (Seno Hackathon ITS 2026), putaran 3
### Agen A10 "Panel Juri" · 28 Okt 2026 (±23:20–00:00 WIB) · protokol `03-MEGA-PROMPT-JURI-90.md` · rubrik **asumsi** `07-MEGA-PROMPT-ITS-HACKATHON-28okt2026.md` §C (panitia belum merilis rubrik)

**Yang dinilai (keadaan terkini):** `08_PENDAFTARAN.md`, `09_DECK_OUTLINE.md`, `10_QNA.md`, `05_BUKTI_TKT.md` (termasuk §2e SKAB), `07_BISNIS_DAMPAK.md`, `06_VALIDASI_PENGGUNA.md` (persona = **simulasi, bukan bukti**, tidak dihitung), `11_RISET_KELEMAHAN.md`, `04_KEPUTUSAN.md`, `prototype\` (README, DATA, PRAREG_TKT4 + PRAREG_SKAB + `.sha256`, `SKAB_KODE_PRADATA.sha256`, `detakpompa\hydraulic.py`, `run_skab.py`, `results\skab\`, `results\triase\eval_prevalensi_*`). Pembanding: `SKOR_AWAL.md` (putaran 1: **46,9**) dan `SKOR.md` (putaran 2: **48,9**, veto aktif).

Penilaian dibuat independen terhadap file saat ini. Panel tidak mengubah file proyek mana pun selain berkas ini.

---

## 0. Verifikasi yang dijalankan sendiri oleh panel

### 0.1 Tes
| Cek | Hasil |
|---|---|
| `prototype\.venv\Scripts\python.exe -m pytest -q` (dari `prototype\`) | **54 passed** (152,8 s). Cocok dengan `results\pytest_output.txt` (54 passed, 23:12) dan README ("54 tes") |
| Angka tes di materi kirim | **Tidak cocok.** 08 §3 dan §4 butir 8, 08 L7, 09 slide 9, dan `CARA_KIRIM.md` masih menulis **42**. 05 §1 sudah 54 |

### 0.2 Hash dan urutan waktu
| Berkas | SHA-256 tersimpan | SHA-256 dihitung panel | Status |
|---|---|---|---|
| `PRAREG_TKT4.md` | `406e8025…abac` | `406e8025…abac` | **Cocok** |
| `PRAREG_SKAB.md` | `c29805a2…014e` | `c29805a2…014e` | **Cocok** |
| Manifes kode PRAREG_TKT4 §2 (15 berkas: 11 `detakpompa\*.py` + `run_eval.py`, `run_eval_rms_gate.py`, `triase.py`, `demo.py`) | di dalam prareg | dihitung satu per satu | **15/15 cocok**. Kode terkunci belum berubah sejak 21:39 |
| `run_skab.py`, `tests\test_skab.py` vs `SKAB_KODE_PRADATA.sha256` | `defd052e…`, `54f3207d…` | sama | **Cocok** |
| `detakpompa\hydraulic.py` vs pra-data | `23ea488e…` | `104779ea…` (= `kode_saat_run.sha256`) | **Berbeda, dan dideklarasikan** sebagai deviasi D1 (rename kolom `Volume Flow RateRMS` → `RateRMS`). Baris rename ada di kode (baris 103–105). **Klaim bahwa D1 hanya satu baris tidak bisa diverifikasi**, karena salinan pra-data tidak disimpan |

**Urutan waktu (mtime sistem berkas):** `PRAREG_SKAB.md` 22:54:13 → `.sha256` 22:54:19 → `SKAB_KODE_PRADATA.sha256` 23:01:26 → `data\skab\.git` (clone) 23:01:46 → `manifest_skab_csv.sha256` 23:01:54 → `points_oof.csv` 23:04 → log 23:06 → post-hoc 23:07. **Urutannya konsisten dengan klaim "dibekukan sebelum unduh".**

**Catatan J4.** Hash lokal hanya membuktikan *integritas* berkas, bukan *waktu*. Hash dan mtime berada di disk yang sama dan bisa ditulis ulang. Folder masih tidak terlacak git, dan belum ada stempel waktu eksternal (commit, email ke mentor, OpenTimestamps). Bagi juri luar, "dibekukan sebelum data" masih klaim yang dibuktikan sendiri, walaupun konsisten. Ini tetap jauh lebih baik dari putaran 2 (saat itu `[ISI: hash commit]`).

### 0.3 Angka di dokumen vs file hasil
| Klaim | Sumber | Status |
|---|---|---|
| Presisi@3 pada prevalensi realistis (08 §2/§3, 09 slide 5, 10 Q20, 05 §2d): 3/22 → 0,707 vs 0,682, +0,022 [−0,333; +0,333]; 5/22 → 0,791 vs 0,765, +0,026 [−0,333; +0,500]; dasar acak 0,136 / 0,227; H_13_0 ditandai keduanya; ±5–6 dari 10 armada punya ≥1 sehat di AUDIT DULU | `triase\eval_prevalensi_log.txt` (any_sehat_in_audit 0,609 / 0,496) | **Cocok**. Sejalan dengan E2 panel putaran 2 (0,703 / 0,787) |
| 0,830 vs 0,840 "tahap awal ditandai perlu cek" (08, 09, 10 Q30, 05 §2b) | `rmsgate_metrics.csv`, E1 panel | **Cocok** |
| SKAB H1: R 1,000; B1 0,571; **B2 1,000**; B3 0,571; Δ vs B2 0,000 [0; 0]; p_H1 = 1,000 → GAGAL | `run_skab_log.txt`, `primary.csv`, `auc_per_method.csv` | **Cocok** |
| SKAB H2: 0,532 vs 0,573 / 0,502 / 0,581; p_H2 = 0,912 → GAGAL | sama | **Cocok** (0,9116) |
| Di τ: R = B1, bal. acc 0,857 [0,714; 1,000], 5/7 fault, 0/20 katup | `S7_balanced_acc_event.csv` / log | **Cocok** |
| GBM: AUROC titik 0,867 (signifikan) tetapi menandai 18/20 katup | log S5, S7 `flag_rate_T` 0,900 | **Cocok**. Dilaporkan sebagai sekunder, tidak dijual sebagai keberhasilan |
| Pemusatan ulang: R_rc 0,629 vs B1_rc 0,563 / B2_rc 0,507 (signifikan) vs B3_rc 0,582 (tidak) | log S10 | **Cocok** |
| Post-hoc: run katup Q ≈ 32 L/min, fault ≈ 125 L/min, penutupan katup −6 % Q, P_app < 1 %, tekanan 10 nilai unik | `posthoc_log.txt`, `DEVIASI.md` | **Cocok**, dan dikonfirmasi ulang dari CSV mentah (E3) |

**Tidak ditemukan angka karangan atau salah salin.** Masalahnya ada pada **kelengkapan**: 08/09 tidak memuat SKAB sama sekali (§3, FF1d).

### 0.4 Eksperimen tambahan panel

**(E3) Konfirmasi independen perancu sesi SKAB.** Skrip: `C:\Users\POGGY\AppData\Local\Temp\claude\C--Users-POGGY--claude-spares-spare-xjE250\c0f1913a-f688-4e27-af57-a6dab34be300\scratchpad\p3_skab_check.py`. Skrip ini membaca 35 CSV SKAB mentah dengan `python -I` dan tidak memakai kode tim.

| Kelompok | Q normal (L/min) | Q kejadian | Arus normal (A) | Arus kejadian | Acc1 RMS normal | Acc1 RMS kejadian |
|---|---|---|---|---|---|---|
| F (imbalance + kavitasi, 7) | 127,0 | 126,0 | 2,555 | 2,563 | 0,221 | **0,564** |
| T (katup, 20) | **32,0** | 30,0 | **0,985** | 0,988 | 0,028 | 0,028 |
| anomaly-free | 125,7 | — | 2,542 | — | 0,213 | — |

- AUROC F vs T dari **median arus di baris normal saja = 1,000**. Dari median Q di baris normal saja juga 1,000. Pemisahan "katup vs fault" di H1 sudah ada sebelum anomali terjadi. Ini perancu sesi, persis seperti diagnosis tim.
- AUROC dari **perubahan** arus dalam satu run (|kejadian − normal|) = 0,357. Arus tidak bereaksi pada kedua jenis kejadian. Yang berubah hanya getaran pada fault, sedangkan penutupan katup praktis tidak mengubah apa pun.
- **Arti:** H1 di SKAB **tidak informatif**. Semua metode yang memakai level atau perubahan getaran akan menang di sana. Data itu tidak bisa membuktikan, dan juga tidak bisa membantah, bahwa model residual memisahkan throttling dari aus. Status "GAGAL" tetap benar menurut aturan prareg. Tafsiran tim ("data tidak bisa menguji klaim dengan tajam") juga benar dan tidak berlebihan.

---

## 1. Rubrik (asumsi, §C)
| Kriteria | Bobot |
|---|---|
| Masalah nyata & energy gap terkuantifikasi | 20 |
| AI di inti + kualitas purwarupa & bukti TKT | 25 |
| Inovasi & keunikan vs solusi yang ada | 15 |
| Dampak lokal & efisiensi terukur | 15 |
| Kelayakan model bisnis | 10 |
| Validasi pengguna & co-design | 10 |
| Presentasi & demo | 5 |

**Fatal flaw (veto J4, skor maksimal 80):** klaim TKT tanpa bukti · angka tanpa sumber · AI yang tidak perlu · hasil wawancara karangan · melanggar orisinalitas aset lomba lain. Protokol §2 J4 juga mencari *cherry-picking*.

---

## 2. Skor per juri × kriteria: putaran 2 → putaran 3

### J1: profesor energi/AI (CityU SEE / Tsinghua)
| Kriteria | P2 | **P3** | Alasan | Apa yang membuat ini 10/10 |
|---|---|---|---|---|
| Masalah & energy gap | 7 | **7** | Tidak berubah di materi kirim. Hanson 2002 (kW bisa *naik* setelah rekondisi; KPI harus kWh/m³) adalah koreksi penting, tetapi baru ada di 11, belum masuk 07/08/10. | Interval audit nyata, ditambah KPI kWh/m³ per stasiun yang dipakai konsisten. |
| AI inti + purwarupa + TKT | 5,5 | **6** | Naik karena disiplin metode. PRAREG v2 sekarang menguji alasan AI langsung (P1 unit baru, P2 throttling vs fault) dengan pengaman G1–G3. Prareg dan 15 berkas kode dikunci hash (diverifikasi). Uji SKAB diprareg sebelum unduh, memakai IUT (harus mengalahkan *setiap* baseline), deviasi dicatat, post-hoc ditandai. Perancunya didiagnosis sendiri dan dikonfirmasi panel (E3). Ini setingkat replikasi yang baik. Tidak naik lebih jauh karena: AI tetap tidak terbukti diperlukan; desain H1 tidak mengantisipasi efek plafon (AUROC baseline 1,0); dan P1/P2 masih belum teruji. | P1 atau P2 lulus di ≥ 3–8 unit fisik. |
| Inovasi | 5 | **5** | Residual QP/QH sudah prior art (paten ABB US9027398B2, kelompok LUT, Kallesøe 2006), dan diakui. Penerapannya ke PM2100 + tekanan header PDAM masuk akal, tetapi belum dibangun dan uji pertamanya tidak informatif. | Residual kurva per pompa yang *dipelajari* dari data PDAM, tervalidasi terhadap audit S6. |
| Dampak lokal & efisiensi | 5 | **5** | 0 kWh terukur. | ΔkWh/m³ terukur sendiri. |
| Bisnis | 5 | **5** | Tidak berubah. | — |
| Validasi & co-design | 2 | **2** | Nol wawancara. | ≥5 wawancara + pakar S6. |
| Presentasi & demo | 6,5 | **6,5** | Judul baru bagus. Tetapi 08/09 tidak sinkron dengan 05 (SKAB hilang, 42 vs 54 tes), dan belum ada figur maupun deck. | Deck jadi, ditambah satu figur SKAB "ruang Q–P" yang jujur. |
| **Berbobot J1** | **53,0** | **54,25** | | |

### J2: praktisi industri pompa/energi Indonesia
| Kriteria | P2 | **P3** | Alasan | Apa yang membuat ini 10/10 |
|---|---|---|---|---|
| Masalah & energy gap | 7 | **7** | Hanson dan Wellington Water (8 %, 34 pompa) relevan untuk praktisi, tetapi belum dipakai di 07/08. | Status rekondisi 5 pompa S6 dari PDAM. |
| AI inti + purwarupa + TKT | 5 | **5,5** | Pertama kali menyentuh data pompa nyata dengan arus, tegangan, debit, dan tekanan pada ±1 Hz. Ini analog data panel PM2100. Pemuat dan pipeline LOEO-nya jalan. Tim juga sekarang tahu persis apa yang dibutuhkan rig (throttling bertingkat, sesi diacak, beberapa unit). Tetap: belum ada pompa sendiri, belum ada pembaca PM2100, dan sensor BOM 3,2 kHz belum cocok (a6). | Rig sendiri dengan throttling bertingkat + power meter + flowmeter. |
| Inovasi | 5 | **5** | Arah "baca data panel yang sudah ada" benar, tetapi produk di 08 masih dijual sebagai triase getaran. | Mode A (PM2100) berjalan pada log nyata. |
| Dampak lokal & efisiensi | 5 | **5** | Biaya kunjungan sia-sia belum dikurangkan (±5–6 dari 10 armada mengirim tim ke ≥1 pompa sehat). | Nilai neto per IPA. |
| Bisnis | 5 | **5** | — | — |
| Validasi & co-design | 2 | **2** | — | — |
| Presentasi & demo | 6,5 | **6,5** | Laporan sensor lepas **masih** mencetak "frekuensi poros terlacak 34,13 Hz (~2048 rpm)" dari derau (gap a8 putaran 2 belum dikerjakan). | Mode operator 5 baris. |
| **Berbobot J2** | **51,75** | **53,0** | | |

### J3: investor (InvestHK / Kerogen CelerateX)
| Kriteria | P2 | **P3** | Alasan | Apa yang membuat ini 10/10 |
|---|---|---|---|---|
| Masalah & energy gap | 7 | **7** | — | — |
| AI inti + purwarupa + TKT | 4,5 | **4,5** | Disiplinnya sinyal kualitas tim yang kuat. Tetapi tesis "AI-driven" sekarang dua kali tidak terbukti (bantalan, lalu data lab pompa). Investor melihat produk yang terbukti adalah DSP + ambang + antrean. Itu bisa dijual, tetapi bukan AI. | AI menang di uji yang diprareg. |
| Inovasi | 5 | **5** | — | — |
| Dampak lokal & efisiensi | 5 | **5** | — | — |
| Bisnis | 4 | **4** | Pra-pendapatan, harga [ASUMSI]. Wellington Water (payback < 3 bulan) bisa jadi jangkar harga yang jujur, tetapi belum dipakai. | Satu pembayar Fase 1. |
| Validasi & co-design | 2 | **2** | — | — |
| Presentasi & demo | 6 | **6,5** | Judul "memilih 3 dari 22 pompa PDAM yang diukur debitnya duluan" sekarang tajam dan lokal. Abstrak 150 kata masih belum menjelaskan *apa yang dikerjakan* komponen AI. Panjangnya 165 kata (±154 tanpa judul), dan versi 300 kata **355** kata, lebih panjang dari putaran 2 (329). | Abstrak ≤ batas form yang menyebut peran AI dan hasil ujinya. |
| **Berbobot J3** | **49,25** | **49,5** | | |

### J4: reviewer skeptis (veto)
| Kriteria | P2 | **P3** | Alasan | Apa yang membuat ini 10/10 |
|---|---|---|---|---|
| Masalah & energy gap | 6 | **6,5** | Q28 sekarang menjawab "10 pompa tidak diaudit" dengan jujur ("kami belum tahu; argumen melemah kalau itu cadangan"). Kalimat di 08 §3.1 tepat ("audit yang dilaporkan tidak menjangkaunya"). | Penjelasan dari PDAM/penulis S6. |
| AI inti + purwarupa + TKT | 4 | **4,5** | +1: FF1c tertutup (deteksi dini dicabut di semua materi, dicek dengan grep; 0,971 selalu dengan prevalensi). +0,5: prareg dan manifes dikunci hash, SKAB diprareg dan dilaporkan GAGAL. −1: **materi kirim (08/09) menghilangkan uji pompa yang gagal.** 08 masih menulis "Data ini belum dari pompa" dan "Klaim AI kami adalah hipotesis untuk uji pompa lab". 10 Q25 menulis "Tidak ada data pompa", padahal Q31 dan 05 §2e melaporkan uji di data lab pompa. Tidak ada tanda kesengajaan (08/09 bertanggal 22:47, run SKAB 23:02), tetapi reviewer yang hanya membaca 08 akan mengira hipotesis throttling belum pernah diuji. | 08/09/10 konsisten dengan 05 §2e, dan prareg di-commit dengan stempel waktu eksternal. |
| Inovasi | 4 | **4,5** | Judul generik diganti sudut unik (a4 putaran 2). Metodenya tetap umum. | — |
| Dampak lokal & efisiensi | 4 | **4** | 0 kWh. 09 slide 8 masih "① **AI** menandai", padahal 07 sudah "Alat menandai". | ΔkW terukur sendiri. |
| Bisnis | 4 | **4** | — | — |
| Validasi & co-design | 1 | **1** | Tidak ada data pengguna, dan tidak ada yang dikarang (dicek: tidak ada kutipan persona di 08/09/10). | Wawancara asli. |
| Presentasi & demo | 5 | **5** | Masih banyak `[ISI]`, video belum ada. Teks melebihi label panjangnya (165/355). Angka tes usang di 4 tempat. 10 menulis "30 pertanyaan" padahal isinya 31. Slide 9 menulis "tambah fitur arus (MCSA)" tanpa menyebut bahwa menurut PRAREG v2 itu model baru yang butuh prareg baru. | Semua sinkron, sesuai batas. |
| **Berbobot J4** | **41,5** | **44,5** | | |

### Rekap
| Kriteria (bobot) | J1 | J2 | J3 | J4 | Rata-rata P3 | Poin P3 | Poin P2 |
|---|---|---|---|---|---|---|---|
| Masalah (20) | 7 | 7 | 7 | 6,5 | 6,875 | 13,75 | 13,50 |
| AI + purwarupa + TKT (25) | 6 | 5,5 | 4,5 | 4,5 | 5,125 | 12,81 | 11,88 |
| Inovasi (15) | 5 | 5 | 5 | 4,5 | 4,875 | 7,31 | 7,13 |
| Dampak (15) | 5 | 5 | 5 | 4 | 4,75 | 7,13 | 7,13 |
| Bisnis (10) | 5 | 5 | 4 | 4 | 4,50 | 4,50 | 4,50 |
| Validasi (10) | 2 | 2 | 2 | 1 | 1,75 | 1,75 | 1,75 |
| Presentasi (5) | 6,5 | 6,5 | 6,5 | 5 | 6,125 | 3,06 | 3,00 |
| **Total** | 54,25 | 53,0 | 49,5 | 44,5 | | **50,3 / 100** | **48,9** |

**Skor akhir putaran 3: 50,3 / 100** (+1,4 dari 48,9; +3,4 dari 46,9). **Veto J4: tetap AKTIF.**

---

## 3. Fatal flaw dan status veto

### Pertanyaan kunci 1: apakah veto "AI tidak perlu" masih aktif?
**Ya, masih aktif. Buktinya malah bertambah, walaupun bukti yang baru lemah.**
1. Di Ottawa, tidak ada metrik di mana RF lebih baik dari RMS + gerbang (tidak berubah).
2. Alasan AI yang paling kuat (memisahkan throttling dari aus) sekarang punya **satu uji yang diprareg, dan hasilnya GAGAL**. E3 menunjukkan uji itu tidak informatif (plafon dan perancu sesi), jadi uji itu **tidak membantah** alasan AI. Tetapi juga tidak memberi satu pun bukti untuknya. Veto dicabut oleh bukti bahwa AI diperlukan, bukan oleh tidak adanya bukti sebaliknya.
3. P1/P2 PRAREG v2 masih TIDAK KONKLUSIF (SKAB hanya 1 testbed dan model getaran terkunci tidak bisa dijalankan pada RMS 1 Hz). Tim menulis ini dengan benar.
4. Veto tidak mengikat skor sekarang (50,3 < 80). Yang dibatasi adalah plafon.

### Pertanyaan kunci 2: apakah ada klaim TKT 4 yang sah?
**Tidak ada, dan tim juga tidak mengklaimnya.** 05 §1 menulis TKT 4 "Belum" dan menegaskan fungsi katup vs fault "tidak naik ke TKT 4". Alasannya: (a) komponen yang diuji **gagal** menunjukkan keunggulan; (b) datanya milik pihak lain dan dari 1 testbed; (c) yang diuji model residual baru, bukan rangkaian DetakPompa yang terintegrasi. Satu-satunya hal positif dari SKAB: deteksi fault berbasis ambang (R = B1) menandai 5/7 fault dengan 0/20 alarm palsu katup pada τ. Itu jasa ambang getaran, bukan AI, dan juga bukan TKT 4 untuk sistem. **Klaim TKT 3 (bantalan, data publik) tetap sah.** FF2 tidak aktif.

### Pertanyaan kunci 3: apakah 08/09 memasukkan SKAB secara jujur?
**Tidak dimasukkan sama sekali.** Ini kelalaian karena urutan kerja, bukan penyembunyian yang disengaja: 08/09/07/CARA_KIRIM bertanggal 22:47, prareg SKAB 22:54, run 23:02–23:07, lalu 05/10/README/DATA diperbarui 23:14–23:16. Kegagalannya tercatat lengkap di 05 §2e, 10 Q31, dan README, sesuai aturan `PRAREG_SKAB.md` §7 (yang hanya mewajibkan README/05).

Tetapi **kalau 08 dikirim apa adanya, hasilnya adalah pelaporan selektif**: teks pendaftaran yang dibaca reviewer seleksi menyiratkan bahwa uji di data pompa belum pernah dilakukan, padahal sudah dan gagal. Ini juga bertentangan dengan narasi resmi tim sendiri ("Semua angka … dilaporkan apa adanya"). Panel mencatatnya sebagai **FF1d (AKTIF, bisa ditutup agen ±30 menit)**. Kalau tidak ditutup sebelum kirim, J4 akan menilainya cherry-picking dan menurunkan kriteria AI ke 3,5.

Kalimat yang harus diganti:
- 08 §1: "Data ini belum dari pompa" → "Uji pertama di data lab pompa publik (SKAB, 1 testbed) dengan prareg terkunci: gagal, tidak lebih baik dari ambang arus; datanya juga tidak cukup tajam untuk menguji klaim itu."
- 08 §2 dan §3 "Batas klaim": tambahkan satu baris SKAB (H1/H2 GAGAL, AUROC, perancu sesi).
- 09 slide 5 (baris bawah) atau slide 9 (TKT 4): satu baris SKAB.
- 10 Q25: "Tidak ada data pompa" → "Belum ada pompa sendiri; satu uji di data lab pompa publik gagal".

### Pertanyaan kunci 4: apakah disiplin prareg + kegagalan yang dilaporkan menaikkan skor?
**Ya, tetapi sedikit: ±+0,6 dari total +1,4.**
| Sumber kenaikan P2 → P3 | Poin total |
|---|---|
| Disiplin prareg v2 (hash + manifes) + SKAB diprareg dan dilaporkan gagal (J1 AI +0,5; J2 AI +0,5) | **+0,63** |
| FF1c ditutup (deteksi dini, prevalensi), dikurangi kelalaian SKAB di 08/09 (J4 AI netto +0,5) | +0,31 |
| Judul unik (J4 inovasi, J3 presentasi) | +0,25 |
| Q28 jujur (J4 masalah) | +0,25 |
| **Total** | **+1,44** |

**Kenapa kecil:** rubrik memberi 25 % bobot pada "AI di inti". Disiplin metode menaikkan *kepercayaan* pada angka, tetapi angkanya sendiri berkata AI tidak diperlukan. Kejujuran menutup flaw jenis klaim (FF1b, FF1c), tetapi tidak menutup flaw jenis karya (FF1). **Nilai terbesar disiplin ini ada di plafon, bukan di skor:** kalau b4 kelak lulus, prareg yang terkunci sebelum data adalah satu-satunya hal yang membuat J4 mau mencabut veto. Tanpa prareg, hasil lulus pun akan dicurigai. Kalau 08/09 sudah memuat SKAB, J4 AI naik +0,5 lagi (+0,31 total).

### Tabel fatal flaw
| # | Fatal flaw | P2 | **P3** | Bukti | Cara menutup |
|---|---|---|---|---|---|
| FF1 | AI yang tidak perlu | AKTIF → veto | **AKTIF → veto** | Ottawa setara; SKAB H1/H2 GAGAL (tidak informatif, E3); P1/P2 belum teruji | b4 (rig, P2), a10 (Paderborn, P1 dengan izin user), b5 (data PDAM, prareg baru) |
| FF1b | Overclaim lama | TERTUTUP | **TERTUTUP** | grep bersih | — |
| FF1c | "Deteksi dini"; 0,971 tanpa prevalensi | AKTIF | **TERTUTUP** | 08/09/10/05 diperbaiki; angka cocok `eval_prevalensi_log.txt` | Jaga saat memotong teks |
| **FF1d** | **Uji pompa yang gagal tidak ada di 08/09; Q25 bertentangan dengan Q31** | — | **AKTIF (ringan, agen ±30 menit)** | §3 pertanyaan 3 | Gap a1 |
| FF2 | Klaim TKT tanpa bukti | Tidak aktif | **Tidak aktif** | TKT 3 sah; TKT 4 tidak diklaim | Jangan menulis "TKT 4 lab" untuk SKAB |
| FF3 | Angka tanpa sumber | Tidak aktif | **Tidak aktif** | §0.3 | — |
| FF4 | Wawancara karangan | Tidak aktif | **Tidak aktif** | Tidak ada kutipan persona | Risiko menit terakhir |
| FF5 | Orisinalitas aset | Menunggu | **Menunggu** | FaceVitals; Ottawa CC BY; SKAB GPL-3.0 dipakai sebagai data saja, `data\` di-gitignore | AKSI_MANUSIA #3/#4d. Kalau repo dibuka (L2), pastikan `data\skab\` tidak ikut |
| — | Diskualifikasi formal | Tinggi | **Tinggi** | Deadline/form belum diketahui; teks 165/355 kata | b1 |

---

## 4. Daftar perubahan yang dinilai (P2 → P3)
| Gap P2 | Status | Penilaian panel |
|---|---|---|
| a1 deteksi dini | **Selesai** | Q30 baru, slide 5 berlabel "label tahap" |
| a2 prareg dibekukan + endpoint diganti | **Selesai** (hash + manifes, tanpa git) | Endpoint sekarang sesuai produk. Manifes 15/15 cocok |
| a3 prevalensi | **Selesai** | Angka cocok, H_13_0 disebut |
| a4 judul | **Selesai** | — |
| a5 abstrak + batas kata | **Sebagian**: peran AI masih samar; panjang 165/355 | — |
| a6 decimasi 3,2 kHz | Tidak | — |
| a7 figur + deck | Tidak (`results\fig\` tidak ada). Ada dua PNG SKAB baru | — |
| a8 mode operator / rpm palsu | **Tidak**: sensor lepas masih "~2048 rpm" | — |
| a10 Paderborn | Tidak (izin user belum ada); diganti SKAB | SKAB tidak bisa menguji P1 |
| a12 kepatuhan kecil | **Sebagian**: CARA_KIRIM 23 → 42 (sekarang usang lagi, harus 54); 07 ① sudah "Alat menandai", 09 slide 8 belum; Q28/Q29 ada | — |
| Baru: 11_RISET_KELEMAHAN | Literatur kuat dan diberi label jujur ([dibuka]/[cuplikan]/klaim vendor) | Hanson dan Wellington belum dibawa ke 07/08/10 |
| Baru: SKAB | Prareg sebelum unduh, 12 tes, deviasi D1, post-hoc ditandai | Contoh disiplin terbaik di berkas ini |

---

## 5. Uji anti-generik (P3)
| Pertanyaan | Jawaban |
|---|---|
| 50 tim lain bisa mengirim hal yang hampir sama? | **Berkasnya tidak.** Judul sekarang memakai sudut unik (3 dari 22 pompa Ngagel I). Budaya evaluasinya hampir tidak ada di hackathon: prareg dikunci hash sebelum mengunduh data, IUT melawan setiap baseline, kegagalan dilaporkan, perancu didiagnosis. **Metodenya tetap umum** (RF fitur getaran; residual QP/QH = prior art ABB/LUT) |
| Judul/hook unik? | **Ya** (lulus, naik dari P2) |
| Kata kosong? | Bersih. "Deteksi dini" sudah hilang |
| Setiap angka bersumber? | Ya (§0.3) |
| Pemenang tahun lalu? | Tidak ada data publik |

**Vonis: LULUS untuk masalah, konteks, judul, dan budaya evaluasi; GAGAL untuk keunikan metode AI.** Hasilnya membaik dari "lulus sebagian".

---

## 6. Sisa gap

### (a) Bisa ditutup agen sekarang, tanpa mengarang
| # | Gap | Kenaikan | Usaha | Instruksi |
|---|---|---|---|---|
| **a1** | FF1d: SKAB di 08/09/10 Q25 | +0,3 (J4 AI +0,5) dan mencegah −1,25 | 30 menit | Lihat kalimat pengganti di §3 pertanyaan 3. Satu kalimat di versi 150 kata, dua kalimat di 300 kata, satu baris di tabel 08 §3 dan "Batas klaim", satu baris di 09 slide 5/9. Jangan menulis "TKT 4" |
| **a2** | Panjang teks + angka usang | +0,2 dan mencegah diskualifikasi | 30 menit | Versi 150 ≤ 150 kata termasuk judul, versi 300 ≤ 300. 42 → 54 di 08 (3 tempat), 09 slide 9, CARA_KIRIM. 10 "30 pertanyaan" → 31. 09 slide 8 "① AI menandai" → "① Alat menandai" |
| **a3** | Stempel waktu prareg | +0,25 (J4) | 10 menit | Commit lokal `git add -f ITSHackathon2026/prototype/PRAREG_* … SKAB_KODE_PRADATA.sha256 results/skab/*.sha256` (tanpa `data\`), pesan diakhiri `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Ini hanya mengunci mulai saat ini. Stempel eksternal adalah b8. Mulai sekarang, simpan salinan kode pra-data untuk deviasi |
| **a4** | KPI Hanson ke 07/08/10 | +0,3 (J1/J2 masalah +0,5) | 30 menit | 07 §3–§4 dan 10: "setelah rekondisi kW bisa naik karena debit naik; KPI = kWh/m³ per stasiun pada permintaan yang sama [Hanson 2002]". Wellington Water dipakai hanya sebagai bukti bahwa program pemantauan efisiensi bisa balik modal, berlabel non-peer-review |
| **a5** | Abstrak: apa yang dikerjakan AI | +0,15 (J3) | 20 menit | Satu kalimat: "RF dengan fitur spektral memberi skor kondisi untuk mengurutkan pompa; hasilnya setara ambang RMS; uji katup vs aus di data lab pompa SKAB gagal; syarat lulus berikutnya sudah dibekukan" |
| a6 | rpm palsu di laporan sensor lepas + mode operator | +0,3–0,5 | 1–2 jam | Sembunyikan frekuensi poros bila gerbang menolak |
| a7 | Figur + deck | +1–1,5 | 2–3 jam | Figur E1 (perlu cek per kelas), presisi@3 vs prevalensi, SKAB `ruang_Q_p_P.png` dengan caption perancu |
| a8 | Decimasi 3,2 kHz (sensor BOM) | +0,5–1 | 1–2 jam | Dengan pembanding RMS + gerbang |
| a9 | Addendum P1 untuk Paderborn, ditulis **sebelum** unduh | 0 sekarang; prasyarat a10 | 1 jam | Ikuti PRAREG v2 §9. Paderborn punya ≥ 8 bantalan fisik, jadi P1 bisa diuji |
| a10 | Paderborn P1 (perlu izin user, catat nama berkas/ukuran/lisensi CC BY-NC) | +0 s.d. +6 (veto dicabut **bersyarat**, domain bantalan) | 1–2 hari | Peluang lulus panel: rendah–sedang (RF ≈ RMS di Ottawa) |

**Total realistis (a) tanpa a10: ±+4,5 → ±55.** Dengan a10 lulus: ±60–61.

### (b) Hanya bisa ditutup manusia
| # | Aksi | Siapa | Kenaikan | Catatan |
|---|---|---|---|---|
| b1 | Login portal: deadline WIB, field, batas karakter; selesaikan bentrok IBSC 1 Nov | Aziz | 0, tapi **syarat ikut** | Hari ini |
| b2 | ≥ 5 wawancara + 1 pakar S6 (skrip `06` + pertanyaan §9) | Uqi, Pio | **+6–8** | Minimal 2 sebelum daftar |
| b3 | Izin tertulis pilot | Aziz, Pio | +3–5 | Tanpa hadiah atau uang |
| b4 | Rig TKT 4: pompa + akselerometer BOM + clamp + power meter + flowmeter/manometer; **throttling bertingkat yang benar-benar menggeser titik kerja (≥ 20–30 % Q)**; sesi diacak (pelajaran SKAB); ≥ 3 unit untuk P2 | Poggy | **+9–11 kalau AI lulus** (veto dicabut); **+4 kalau gagal** | Setelah SKAB, peluang P2 lulus menurut panel ±20–30 % |
| b5 | Data PDAM: log PM2100, tekanan header, status rekondisi 5 pompa S6 | Aziz lewat penulis S6 | +4–6 | Di sini AI paling mungkin diperlukan (kurva per pompa yang dipelajari). Butuh prareg baru |
| b6 | Video ≤ 2 menit, data tim, latihan Q20/Q25/Q30/Q31 | semua | +1 | Rekam setelah a1–a2 dan a6 |
| b7 | Izin FaceVitals; tidak ada pengiriman ganda | Poggy, Aziz | 0, mencegah FF5 | — |
| b8 | Stempel waktu eksternal prareg: kirim SHA-256 PRAREG_TKT4/SKAB ke mentor/dosen lewat email, atau push ke repo privat | Poggy | +0,25 | Agen tidak boleh mengirim |
| b9 | Izin unduh Paderborn (a10) / coba 4TU NLN-EMP dari jaringan lain | user | memungkinkan +0–6 | 4TU punya debit, tekanan, V/I, dan restriksi outlet, jadi uji SKAB yang lebih tajam |

---

## 7. Plafon
| Keadaan | Skor | Catatan |
|---|---|---|
| P1 / P2 | 46,9 / 48,9 | Veto aktif |
| **Sekarang (P3)** | **50,3** | Veto aktif; FF1c tertutup; FF1d terbuka |
| **Plafon sekarang** (agen a1–a8) | **±55** | FF1 tetap |
| + a10 Paderborn lulus | ±60–61 | Veto dicabut bersyarat (domain bantalan) |
| + b2 wawancara | ±62 (±67) | |
| + b3 izin pilot | ±66 (±71) | |
| + b4 rig, AI lulus P2 | ±76 (±81) | Kalau gagal: +4, batas keras 80, realistis ±70 |
| + b5 data PDAM | ±81 (±85) | |
| + b6 | **±82 (±86)** | |
| **Plafon setelah aksi manusia** | **±82–86 kalau AI lulus prareg; ≤ 80 (realistis ±70–74) kalau tidak** | Setelah SKAB, panel menilai jalur "tidak lulus" lebih mungkin. **Ekspektasi tertimbang ±74**. Skor 90 butuh TKT 5 dengan AI > RMS + gerbang di pompa PDAM; tidak realistis sebelum Demo Day Jan 2027 |
| **Realistis saat berkas dikirim** (a1–a5 + b1 + 1–2 wawancara + video) | **±57–60** | Angka yang dibaca reviewer seleksi 15 tim |

---

## 8. Rekomendasi final

**DAFTAR dengan DetakPompa, dengan syarat.** Rekomendasinya tidak berubah dari P2. Ada satu syarat baru yang wajib.

**Kenapa tetap daftar:** syarat formal "purwarupa AI TKT 3–6" kemungkinan besar terpenuhi (ML berjalan end-to-end di data nyata, tanpa kebocoran, 54 tes). Masalahnya lokal dan bersumber. Program ini pra-inkubasi dengan validasi pengguna, sehingga tim yang tahu persis apa yang belum terbukti dan punya prareg untuk mengujinya adalah profil yang dicari. Tidak ada aturan yang mewajibkan AI mengalahkan baseline.

**Syarat daftar (semua wajib):**
1. b1 selesai (deadline, form, batas karakter, pengirim yang tidak bentrok dengan IBSC).
2. **Baru:** a1 (SKAB masuk 08/09, Q25 diperbaiki) dan a2 (panjang teks, 54 tes) **sebelum** teks disalin ke form. Mengirim 08 versi sekarang = pelaporan selektif.
3. Tidak ada klaim TKT 4, dan tidak ada kalimat "AI membedakan katup vs aus" sebagai hasil.
4. Validasi pengguna: hasil wawancara asli, atau "dijadwalkan". Persona dilarang.
5. Izin FaceVitals (b7). Repo publik tanpa `data\skab\` (GPL-3.0).
6. Video direkam setelah perbaikan rpm palsu (a6), atau rpm dipotong dari video.

**Titik keputusan setelah 15 besar:**
- Kalau b4 (P2) **lulus**: pitch sebagai karya AI, dengan prareg sebagai bukti.
- Kalau b4 **gagal** atau tidak sempat: jangan pitch "AI-driven" di Demo Day. Pilihannya (a) pitch jujur sebagai "triase DSP + ambang + antrean, AI sebagai hipotesis yang sudah diuji dua kali" dan terima skor kriteria AI rendah; atau (b) pindahkan peran AI ke kurva kinerja per pompa yang **dipelajari** dari log PM2100 + tekanan header PDAM (b5), dengan prareg baru. Panel menilai (b) satu-satunya jalur yang realistis menutup FF1 di domain PDAM.

**Tidak ikut, kalau:** deadline 1 Nov dan tidak ada yang bisa login, mengisi `[ISI]`, dan menjalankan a1–a2 tanpa mengorbankan IBSC.

---

## 9. Juri tamu (non-skor): operator dan kepala unit produksi PDAM

> **SIMULASI PERSONA, BUKAN BUKTI.** Disusun panel dari fakta S6 (`06` §0), hasil SKAB, dan keluaran asli `results\triase\armada_22\antrean_usulan.txt` dan `results\demo\laporan_sensor_lepas.txt`. **Tidak boleh dikutip** di berkas, deck, atau video. Semua butir adalah **pertanyaan untuk wawancara asli (b2)**.

**Yang menurut persona membaik:** judul sekarang berbicara dalam bahasa kepala IPA ("3 dari 22 pompa diukur debitnya duluan"). Pengakuan bahwa presisi turun ke ±7 dari 10 kalau hanya 3 pompa yang bermasalah terasa jujur.

**Reaksi terhadap arah "residual hidraulik" (11, SKAB):**
1. "Di rumah pompa kami, katup outlet diatur operator per shift mengikuti tekanan zona. Perubahannya bisa jauh lebih besar dari 6 %. Kalau rig Anda hanya menutup katup sedikit, Anda belum menguji keadaan kami." (Ini sejalan dengan E3: uji butuh throttling bertingkat yang besar.)
2. "Tekanan apa yang Anda pakai? Kami punya manometer analog per pompa dan mungkin tekanan header di SCADA. Resolusinya bisa sekasar SKAB."
3. "PM2100 mencatat kW, tetapi apakah lognya disimpan, dan per berapa menit? Siapa yang boleh mengekspornya?"
4. "Kalau pompa direkondisi lalu kW-nya naik, Direksi akan mengira rekondisi gagal." (Hanson 2002. Persona akan meminta KPI kWh/m³ per zona.)
5. "Pompa kami jalan DOL, bukan VFD. Metode QP dari paten ABB butuh kecepatan dan torsi dari VFD. Apa gantinya?"

**Yang masih membuat tidak dipakai (sisa P2):** "RUSAK tapi PANTAU"; laporan sensor lepas masih mencetak ~2048 rpm dari derau; asal rekaman baseline per pompa belum jelas; perangkat ronde belum ada.

**Pertanyaan tambahan untuk wawancara asli:**
1. Seberapa besar dan seberapa sering bukaan katup outlet diubah per hari?
2. Apakah ada tekanan header atau tekanan per pompa yang tercatat otomatis, dan berapa resolusinya?
3. Apakah log PM2100 disimpan? Interval berapa, dan berapa lama mundur ke belakang?
4. Pompa DOL atau VFD? Ada flowmeter induk per stasiun atau zona?
5. Apakah satu dari lima pompa S6 sudah direkondisi sejak 2024? Kalau ya, apakah ada log kW sebelum dan sesudahnya pada tekanan header yang sama?

---

*Skrip panel (hanya membaca, tidak mengubah file proyek):* `C:\Users\POGGY\AppData\Local\Temp\claude\C--Users-POGGY--claude-spares-spare-xjE250\c0f1913a-f688-4e27-af57-a6dab34be300\scratchpad\p3_skab_check.py` (E3). Hash dihitung dengan `sha256sum` dari `prototype\`. Tes dijalankan ulang: 54 passed.
