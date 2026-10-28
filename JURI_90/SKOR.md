# JURI_90 / SKOR: DetakPompa (Seno Hackathon ITS 2026), putaran 2
### Agen A10 "Panel Juri" · 28 Okt 2026 (±21:20–22:00) · protokol `03-MEGA-PROMPT-JURI-90.md` · rubrik **asumsi** `07-MEGA-PROMPT-ITS-HACKATHON-28okt2026.md` §C (panitia belum merilis rubrik)

**Yang dinilai (versi terbaru):** `08_PENDAFTARAN.md`, `09_DECK_OUTLINE.md`, `10_QNA.md`, `05_BUKTI_TKT.md` (termasuk §2b–§2d dan PRAREG-TKT4), `07_BISNIS_DAMPAK.md`, `06_VALIDASI_PENGGUNA.md` (§6 persona **simulasi, bukan bukti**, tidak dihitung), `04_KEPUTUSAN.md`, `prototype\` (README, `detakpompa\`, `triase.py`, `demo.py`, `results\` termasuk `rmsgate_*` dan `triase\`). Pembanding: `JURI_90\SKOR_AWAL.md` (putaran 1: **46,9**, veto aktif).

Penilaian dilakukan independen terhadap keadaan file saat ini. Panel tidak mengubah file proyek mana pun selain berkas ini.

---

## 0. Verifikasi yang dijalankan sendiri oleh panel

| Cek | Hasil |
|---|---|
| `prototype\.venv\Scripts\python.exe -m pytest -q` (dari folder `prototype\`) | **40 passed** (121 s). Cocok dengan `results\pytest_output.txt` (40 passed) dan klaim "40/40" di 05/08/09 |
| Angka §2b di 05/08/09/10 vs `rmsgate_metrics.csv`, `rmsgate_paired_bootstrap.csv`, `rmsgate_log.txt`, `rmsgate_summary.json`, `rmsgate_degradation_summary.csv` | **Semua cocok**: 0,605 vs 0,639, −0,034 [−0,155; +0,071]; mF1 0,595 vs 0,602; AURC bergerbang 0,229 vs 0,291, −0,062 [−0,195; +0,076]; titik operasi 0,640 (cak. 0,873) vs 0,671 (cak. 0,850); recall waspada 0,415 vs 0,213, +0,202 [−0,056; +0,453], p 0,122; recall rusak 0,470 vs 0,795, −0,324 [−0,562; −0,089], p Holm 0,198; 22 uji, tidak ada yang signifikan setelah Holm; 98,8 %; lolos gerbang keyakinan 88,5–96,5 % ("88–97 %"); reproduksi run lama identik (`[repro]` True) |
| Angka §2c vs `triase\eval_log.txt`, `eval_summary.json` | **Cocok**: presisi@3 0,971 vs 0,952, +0,019 [−0,333; +0,333], seri 0,87; dijawab 53/60 vs 50/60; UKUR ULANG 7/40 vs 9/40; AMAN 3/40 vs 4/40; presisi "rusak"@3 seluruh armada 0,33 vs 0,67 |
| Klaim Q27 "3 teratas AUDIT DULU adalah bantalan rusak; sensor lepas dan derau −10 dB masuk UKUR ULANG" | **Benar** (`triase\armada_22\antrean_usulan.txt`: B_13_2, I_1_2, B_15_2, ketiganya label rusak; `sensor_lepas` dan `I_3_1_derau_-10dB` di UKUR ULANG, tanpa prioritas) |
| `results\demo\laporan_sensor_lepas.txt` | Prioritas "-", antrean UKUR ULANG, probabilitas ditandai "TIDAK DIPAKAI". Bug putaran 1 (0,87) **tertutup** |
| Fakta OOF "69/76 TIDAK TAHU dari jendela fault" | Konsisten dengan putaran 1 (dihitung panel saat itu) |
| Angka putaran 1 yang tidak berubah (0,640/0,608/0,553/0,432; S6; 07) | Tidak berubah, tetap cocok |

**Tidak ditemukan angka yang dikarang atau salah salin.** Dua catatan verifiabilitas:
- `run_eval_rms_gate.py` bertanggal 20:47:41, setelah `rmsgate_metrics.csv` (20:43:42). Kemungkinan besar hanya penambahan `--plot-only` (PNG bertanggal 20:47). Tetapi klaim "protokol ditulis sebelum run dan tidak diubah sesudahnya" **tidak bisa diverifikasi**, karena seluruh pekerjaan prototipe belum di-commit (repo hanya punya commit awal 24 Okt). PRAREG-TKT4 juga masih berisi `[ISI: hash commit]`.
- `CARA_KIRIM.md` masih menulis "hasil yang diharapkan: 23 passed … klaim 23/23 tes". Ini sudah usang (sekarang 40).

### Eksperimen tambahan panel (hanya membaca file hasil; skrip di scratchpad)

**(E1) "Deteksi dini" yang dijual dari recall waspada.** Dihitung dari matriks kebingungan jendela yang lolos gerbang (`rmsgate_metrics.csv`, baris `lolos_gerbang_sinyal_sama`):

| Jendela lolos gerbang | Usulan | RMS + gerbang |
|---|---|---|
| Jendela **waspada** yang ditandai "perlu cek" (waspada **atau** rusak) | 156/188 = **0,830** | 158/188 = **0,840** |
| Jendela rusak yang ditandai "perlu cek" | 169/185 = 0,914 | 177/185 = 0,957 |
| Jendela sehat yang ditandai (alarm palsu) | 14/200 = 7,0 % | 18/200 = 9,0 % |

**Artinya:** keunggulan "recall waspada 0,415 vs 0,213" **bukan** deteksi yang lebih dini. Kedua model sama-sama menandai ±83–84 % jendela tahap awal untuk dicek. Bedanya hanya **label tahapnya**: RMS menyebut tahap awal "rusak", usulan menyebutnya "waspada", dan akibatnya usulan juga menurunkan banyak jendela rusak menjadi "waspada". Ini pergeseran batas waspada/rusak, bukan kemampuan melihat lebih awal. README sendiri mengakui hal ini ("untuk triase, ini merugikan"), tetapi 09 slide 5 ("Recall waspada (deteksi dini)"; naskah "AI kami lebih sering menangkap tahap awal"), 10 Q20 ("tahap waspada, yaitu deteksi dini"), dan 05 §2d masih memakai bingkai "deteksi dini". **Ini overclaim tersisa.**

**(E2) Presisi@3 pada prevalensi realistis.** Skrip: `C:\Users\POGGY\AppData\Local\Temp\claude\C--Users-POGGY--claude-spares-spare-xjE250\c0f1913a-f688-4e27-af57-a6dab34be300\scratchpad\j4_prevalence.py`, membaca `results\triase\eval_recording_decisions.csv` (keputusan LOBO tingkat rekaman milik tim), 5000 armada × 22 "pompa" dengan jumlah pompa bermasalah tetap.

| Pompa bermasalah dari 22 (dasar acak) | Presisi@3 usulan | Presisi@3 RMS + gerbang | Armada dengan ≥1 pompa sehat di AUDIT DULU (usulan / RMS) |
|---|---|---|---|
| 2 (0,091) | 0,640 | 0,610 | 0,66 / 0,67 |
| 3 (0,136) | 0,703 | 0,679 | 0,62 / 0,63 |
| 5 (0,227) | 0,787 | 0,757 | 0,51 / 0,55 |
| 8 (0,364) | 0,887 | 0,840 | 0,30 / 0,40 |
| *tim: 2/3 bermasalah (0,667)* | *0,971* | *0,952* | — |

**Artinya:** angka 0,971 adalah hasil armada simulasi tim yang **dua pertiganya rusak** (dasar acak 0,667). Di IPA nyata, mayoritas pompa sehat. Pada 3–5 pompa bermasalah dari 22, presisi@3 turun ke ±0,70–0,79, dan masih setara antara usulan dan RMS. Dua model itu salah menandai **rekaman sehat yang sama** (H_13_0), jadi angka di prevalensi rendah praktis ditentukan oleh satu rekaman. Kesimpulan "setara" tetap berlaku. Yang perlu diubah adalah cara angka 0,971 disajikan: tanpa menyebut prevalensinya, angka itu menyesatkan.

---

## 1. Rubrik (asumsi, §C)

| Kriteria | Bobot | Sumber turunan |
|---|---|---|
| Masalah nyata & energy gap terkuantifikasi | 20 | "Define the Energy Gap", "masalah nyata" |
| AI di inti + kualitas purwarupa & bukti TKT | 25 | "AI Driven", syarat TKT 3–6 |
| Inovasi & keunikan vs solusi yang ada | 15 | "Innovative" |
| Dampak lokal & efisiensi terukur | 15 | "Local", "efficiency gains" |
| Kelayakan model bisnis | 10 | "business model viability", business matching |
| Validasi pengguna & co-design | 10 | "co-design", tahap validasi pengguna |
| Presentasi & demo | 5 | Demo Day |

**Fatal flaw (veto J4, skor maksimal 80):** klaim TKT tanpa bukti · angka tanpa sumber · AI yang tidak perlu · hasil wawancara karangan · melanggar orisinalitas aset lomba lain.

---

## 2. Skor per juri × kriteria: awal (putaran 1) → akhir (putaran 2)

### J1: profesor energi/AI (CityU School of Energy & Environment / Tsinghua)
| Kriteria | Awal | Akhir | Alasan | Apa yang membuat ini 10/10 |
|---|---|---|---|---|
| Masalah & energy gap | 7 | **7** | Tidak berubah. Angka S6 per pompa kuat; interval audit dan kWh per bulan keterlambatan masih `[ISI]`. | Interval audit nyata dari PDAM atau penulis S6. |
| AI inti + purwarupa + TKT | 5 | **5,5** | Kualitas evaluasi sekarang di atas standar banyak paper: pembanding adil (gerbang identik, skor margin yang ditetapkan sebelum run), 22 uji dengan Holm, reproduksi identik, prareg dengan pengaman dan aturan "tidak konklusif". Tapi hasilnya justru mengunci kesimpulan: **tidak ada metrik di mana ML lebih baik dari RMS + gerbang**. Endpoint utama prareg (recall waspada 3-kelas) mengukur pelabelan tahap, bukan nilai triase (E1), dan tidak menguji alasan AI yang dipakai di Q20 (memisahkan katup/permintaan dari keausan). | Endpoint prareg yang sesuai produk dan sesuai alasan AI-nya, dibekukan dengan hash, lalu lulus di data pompa. |
| Inovasi | 5 | **5** | Antrean triase k = 3 adalah pembingkaian produk, bukan kebaruan metode. Gerbang CFAR dan prediksi selektif tetap standar. | Ide teknis yang tidak dimiliki vendor dan tervalidasi terhadap audit Q–H. |
| Dampak lokal & efisiensi | 5 | **5** | Tidak berubah: 0 kWh terukur, rantai ①→②→③ jujur. | ΔkW dan ΔkWh/m³ diukur sendiri. |
| Bisnis | 5 | **5** | Tidak berubah. | Harga jangkar dari biaya audit energi nyata. |
| Validasi & co-design | 2 | **2** | Nol wawancara. Materi siap. | ≥5 wawancara + pakar S6, papan skor H1/H3/H6. |
| Presentasi & demo | 6 | **6,5** | Slide 5 sekarang jujur dan satu pesan ("Gerbang sinyal kami terbukti. AI kami belum"). Deck, figur, dan video belum ada. | Deck jadi, 4–5 figur yang terbaca dalam 5 detik. |
| **Skor berbobot J1** | **51,5** | **53,0** | | |

### J2: praktisi industri pompa/energi Indonesia
| Kriteria | Awal | Akhir | Alasan | Apa yang membuat ini 10/10 |
|---|---|---|---|---|
| Masalah & energy gap | 7 | **7** | Tidak berubah. Status rekondisi 5 pompa S6 sejak 2024 belum diketahui. | Konfirmasi PDAM soal kondisi pompa hari ini. |
| AI inti + purwarupa + TKT | 4 | **5** | Naik karena bentuk produk sekarang ada: `triase.py` mengeluarkan daftar AUDIT DULU / PANTAU / UKUR ULANG / AMAN, dan bug prioritas sensor lepas sudah ditutup dengan 9 tes. Tetap: masukannya file .mat 42 kHz, belum ada pembacaan PM2100, model belum cocok dengan sensor BOM (ADXL343 3,2 kHz; a6 belum dikerjakan), dan belum ada pompa. | Rekaman pompa sentrifugal dengan sensor di BOM, plus mode A yang membaca PM2100/Modbus. |
| Inovasi | 5 | **5** | "Lapisan di atas meter Schneider" masih rencana. | Purwarupa yang membaca data panel yang sudah ada. |
| Dampak lokal & efisiensi | 5 | **5** | Biaya salah alarm dan biaya kunjungan ukur belum dikurangkan. Presisi@3 di prevalensi realistis hanya ±0,7–0,8 (E2), jadi biaya kunjungan yang sia-sia lebih besar dari yang tersirat dari 0,971. | Nilai neto per IPA setelah biaya kunjungan. |
| Bisnis | 5 | **5** | Tidak berubah. | Mitra pemasang/servis lokal. |
| Validasi & co-design | 2 | **2** | Belum ada operator yang melihat laporan. | Satu ronde nyata dengan operator. |
| Presentasi & demo | 6 | **6,5** | Daftar armada mudah dibaca kepala IPA. Laporan satu rekaman masih panjang (mode operator belum dibuat; std/rms masih ganda). | Laporan 5 baris untuk operator, lembar mingguan untuk kepala IPA. |
| **Skor berbobot J2** | **49,0** | **51,75** | | |

### J3: investor (InvestHK / Kerogen CelerateX)
| Kriteria | Awal | Akhir | Alasan | Apa yang membuat ini 10/10 |
|---|---|---|---|---|
| Masalah & energy gap | 7 | **7** | Tidak berubah. | Satu kejadian biaya nyata akibat triase yang terlambat. |
| AI inti + purwarupa + TKT | 4 | **4,5** | Demo produk lebih lengkap. Tapi uji tambahan memperkuat bahwa produk yang terbukti adalah "gerbang DSP + ambang RMS + antrean". Bagi investor, itu sebenarnya produk yang lebih murah dan lebih mudah dipelihara, tetapi itu bukan "AI Driven". | Bukti bahwa model memberi nilai yang tidak bisa diberikan aturan. |
| Inovasi | 5 | **5** | Tidak ada parit, dan AI juga bukan pembeda. | Akses data eksklusif lewat kerja sama riset. |
| Dampak lokal & efisiensi | 5 | **5** | Tidak berubah. | Studi kasus terukur. |
| Bisnis | 4 | **4** | Pra-pendapatan, tanpa LOI, harga [ASUMSI]. | Satu pembayar Fase 1. |
| Validasi & co-design | 2 | **2** | Nol. | Komitmen nyata dari PDAM. |
| Presentasi & demo | 6 | **6** | Narasi kejujurannya kuat. Tapi versi 150 kata (yang paling mungkin dibaca reviewer seleksi) menyebut AI hanya dengan kalimat "belum lebih baik dari ambang RMS" dan "masih hipotesis", tanpa satu kalimat tentang apa yang dikerjakan komponen AI. Di lomba AI, abstrak itu mengundang vonis "bukan purwarupa AI". | Abstrak yang jujur **dan** menjelaskan peran komponen AI beserta cara mengujinya. |
| **Skor berbobot J3** | **48,0** | **49,25** | | |

### J4: reviewer skeptis (veto)
| Kriteria | Awal | Akhir | Alasan | Apa yang membuat ini 10/10 |
|---|---|---|---|---|
| Masalah & energy gap | 6 | **6** | "10 pompa tidak terlihat" masih bisa punya alasan lain (cadangan/mati saat audit). | Penjelasan PDAM. |
| AI inti + purwarupa + TKT | 3 | **4** | Naik: semua kalimat terlarang dari putaran 1 sudah dihapus dan diganti, baseline (d) RMS + gerbang + margin ada di file, prareg tertulis. Tetap rendah karena: (1) AI tidak diperlukan menurut semua metrik; (2) bingkai "deteksi dini" masih menjual pergeseran label sebagai kemampuan (E1); (3) presisi@3 0,971 disajikan tanpa prevalensi 2/3 (E2); (4) prareg belum dibekukan (tanpa hash commit), dan "protokol ditulis sebelum run" tidak bisa diverifikasi tanpa riwayat git. | Prareg di-commit dengan hash, endpoint sesuai produk, dan AI menang di uji yang ditentukan sebelum datanya ada. |
| Inovasi | 4 | **4** | Judul masih "triase … yang tahu kapan harus diam". Secara harfiah benar (subjeknya sistem, bukan AI), tetapi fitur unggulan di judul adalah `if snr < τ` yang menurut berkas tim sendiri bisa dipasang di model apa pun. | Judul yang memakai sudut unik (Ngagel I, 12/22, ronde operator). |
| Dampak lokal & efisiensi | 4 | **4** | 0 kWh terukur. | Satu ΔkW terukur sendiri. |
| Bisnis | 4 | **4** | Semua harga [ASUMSI]. | Satu harga pembanding nyata. |
| Validasi & co-design | 1 | **1** | Tidak ada data pengguna. Tidak ada yang dikarang (dicek ulang: tidak ada kutipan persona di 08/09/10). | Wawancara asli dengan persetujuan. |
| Presentasi & demo | 5 | **5** | Masih banyak `[ISI]`, slide 3 kosong, video belum ada. Versi "150 kata" sebenarnya 164 kata dan versi "300 kata" 329 kata: berisiko kalau form punya batas keras. `CARA_KIRIM.md` masih "23 passed". | Semua `[ISI]` terisi dari data asli, panjang teks sesuai batas. |
| **Skor berbobot J4** | **39,0** | **41,5** | | |

### Rekap
| Kriteria (bobot) | J1 | J2 | J3 | J4 | Rata-rata akhir | Poin berbobot akhir | Poin awal |
|---|---|---|---|---|---|---|---|
| Masalah & energy gap (20) | 7 | 7 | 7 | 6 | 6,75 | 13,50 | 13,50 |
| AI inti + purwarupa + TKT (25) | 5,5 | 5 | 4,5 | 4 | 4,75 | 11,88 | 10,00 |
| Inovasi (15) | 5 | 5 | 5 | 4 | 4,75 | 7,13 | 7,13 |
| Dampak lokal & efisiensi (15) | 5 | 5 | 5 | 4 | 4,75 | 7,13 | 7,13 |
| Bisnis (10) | 5 | 5 | 4 | 4 | 4,50 | 4,50 | 4,50 |
| Validasi & co-design (10) | 2 | 2 | 2 | 1 | 1,75 | 1,75 | 1,75 |
| Presentasi & demo (5) | 6,5 | 6,5 | 6 | 5 | 6,00 | 3,00 | 2,88 |
| **Total** | 53,0 | 51,75 | 49,25 | 41,5 | | **48,9 / 100** | **46,9** |

**Skor akhir putaran 2: 48,9 / 100** (naik +2,0 dari 46,9). **Veto J4: tetap AKTIF** (batas atas 80; belum mengikat skor sekarang, tetapi mengikat plafon).

Kenaikannya lebih kecil dari estimasi putaran 1 untuk a1–a3 (±+5). Sebabnya: pekerjaan a3 (presisi top-3) memang dikerjakan dengan baik, tetapi hasilnya **menambah** bukti bahwa AI tidak diperlukan pada tugas yang dijual. Kejujuran menutup overclaim, tetapi tidak menambah poin di kriteria "AI di inti".

---

## 3. Fatal flaw dan status veto

### Keputusan kunci: apakah FF1 "AI yang tidak perlu" masih aktif?

**Keputusan J4: MASIH AKTIF.** Veto tetap. Tingkat keparahannya turun: dari "AI tidak perlu **dan** diklaim perlu" (dua masalah) menjadi "AI belum terbukti perlu, dan tim mengakuinya" (satu masalah). Alasannya:

1. **Flaw ini sifat karya, bukan sifat kalimat.** Fatal flaw di §C berbunyi "AI yang tidak perlu", bukan "klaim AI yang berlebihan". Mengakui kelemahan menutup overclaim (FF1b), dan itu sudah dilakukan dengan baik. Tetapi pengakuan itu sekaligus menjadi bukti flaw-nya. Di semua metrik yang diuji tim sendiri (akurasi, AURC, presisi@3, tanda "perlu cek" per kelas), RMS + gerbang yang sama setara atau lebih baik. Rencana cadangan tim sendiri adalah "cabut kata AI dan jual gerbang sinyal + ambang RMS + antrean". Komponen yang tim rencanakan untuk dibuang kalau gagal tidak bisa disebut "di inti".
2. **Prareg adalah rencana, bukan bukti.** PRAREG-TKT4 ditulis dengan baik: satu uji utama, pengaman rusak dan alarm palsu, aturan tidak konklusif, larangan mengubah fitur atau ambang. Ini menaikkan kredibilitas (J1 +0,5, J4 +1). Tapi lomba menilai purwarupa yang **ada**, dan purwarupa yang ada tidak membutuhkan AI-nya.
3. **Prareg yang sekarang pun belum bisa menutup FF1 walaupun lulus.** Endpoint utamanya (recall waspada 3-kelas) bisa naik hanya dengan menggeser batas waspada/rusak, tanpa menandai satu pompa pun lebih awal (E1: 0,830 vs 0,840 "perlu cek"). Endpoint itu juga tidak menguji alasan AI yang dipakai di Q20 dan 07 R3, yaitu memisahkan perubahan karena katup/permintaan dari keausan dengan beberapa masukan. Prareg juga belum dibekukan (`[ISI: hash commit]`).
4. **Syarat lomba "purwarupa AI TKT 3–6".** Secara formal, panel menilai syarat kelayakan **kemungkinan besar terpenuhi**: ada model ML yang berjalan end-to-end di data nyata, dengan evaluasi tanpa kebocoran. Tidak ada aturan yang mewajibkan AI mengalahkan baseline. Risikonya ada di **penilaian**, bukan di kelayakan. Reviewer seleksi yang membaca versi 150 kata bisa menyimpulkan "tim ini sendiri bilang AI-nya tidak perlu". Itu bukan alasan menyembunyikan hasil. Itu alasan menulis dengan jelas apa yang dikerjakan komponen AI dan bagaimana ia akan diuji.
5. **Veto tidak mengikat skor sekarang (48,9 < 80).** Yang dibatasi adalah plafon: tanpa bukti AI diperlukan, karya ini tidak bisa melewati 80 walaupun semua aksi manusia selesai.

**Cara mencabut veto (salah satu, dengan bukti):**
- (i) **Ubah prareg sebelum ada data pompa**, lalu bekukan dengan commit lokal dan isi hash-nya. Endpoint utama harus sesuai produk dan sesuai alasan AI-nya, misalnya: di rekaman pompa lab dengan kondisi **throttling katup sebagai perancu**, model (getaran + kW, tekanan kalau ada) vs RMS + gerbang **dan** vs ambang kW sederhana, pada tugas biner "perlu cek" di alarm palsu tetap (atau presisi@3 pada prevalensi ≤ 25 %). Batas bawah CI 95 % > 0. Recall waspada jadi metrik sekunder. Lalu **lulus** di data itu (aksi b4).
- (ii) Paderborn (a5) dengan pergeseran kondisi operasi + arus motor, prareg dulu, uji di bantalan rusak *nyata*. Kalau lulus, J4 mencabut veto **bersyarat** (domainnya tetap bantalan, bukan pompa).
- (iii) Kalau keduanya gagal: AI tidak bisa diklaim di inti. Di lomba ini, itu berarti DetakPompa tidak layak dipitch sebagai karya utama di Demo Day (lihat §8).

### Tabel fatal flaw
| # | Fatal flaw | Status awal | Status akhir | Bukti | Cara menutup |
|---|---|---|---|---|---|
| FF1 | **AI yang tidak perlu** | AKTIF → veto | **AKTIF → veto** (keparahan turun) | §2b–§2d tim sendiri; E1; E2; presisi@3 setara; Holm: tidak ada yang signifikan | §3 (i)/(ii) di atas; aksi b4 |
| FF1b | Overclaim turunan ("RMS tidak punya skor keyakinan", "nilai tambah AI di abstain", "AI kami tahu kapan harus diam", sensor lepas 0,87) | AKTIF | **TERTUTUP** | Kalimat dihapus di 05/08/09/10/README (dicek dengan grep); bug prioritas diperbaiki + tes; checklist di 09 melarang kalimat lama | Jaga saat memotong teks untuk form |
| FF1c | **Overclaim baru/tersisa:** "recall waspada = deteksi dini"; presisi@3 0,971 tanpa prevalensi | — | **AKTIF**, bisa ditutup agen dalam <1 jam | E1 (0,830 vs 0,840), E2 (0,70–0,79 di 3–5/22) | Gap a1, a3 |
| FF2 | Klaim TKT tanpa bukti | Tidak aktif, risiko sedang | **Tidak aktif**, risiko sedang | 05 sekarang menulis "TKT 3 untuk rangkaian triase getaran … di data publik bantalan, bukan di pompa". Fungsi "baseline pompa sendiri" (mode deviasi) masih TKT 2 tetapi tidak ditulis eksplisit sebagai TKT 2 | Tambahkan satu kalimat eksplisit di 08 §3 |
| FF3 | Angka tanpa sumber | Tidak aktif | **Tidak aktif** | Diverifikasi §0 | Jaga label [ASUMSI]/[SKENARIO] |
| FF4 | Wawancara karangan | Tidak aktif | **Tidak aktif** | Tidak ada kutipan persona di 08/09/10 | Risiko terbesar saat mengisi `[ISI]` di menit terakhir |
| FF5 | Orisinalitas aset | Menunggu konfirmasi | **Menunggu konfirmasi** | FaceVitals diberi atribusi; Ottawa CC BY 4.0 | `AKSI_MANUSIA.md` #3 |
| — | Diskualifikasi formal | Risiko tinggi | **Risiko tinggi** | Deadline dan isi form belum diketahui; bentrok 1 Nov dengan IBSC; teks melebihi label panjangnya | `AKSI_MANUSIA.md` #1 hari ini |

---

## 4. Daftar perubahan yang dinilai (putaran 1 → 2)

| Gap putaran 1 | Status | Dinilai |
|---|---|---|
| a1 Baseline (d) RMS + gerbang + margin, CI AURC, ganti kalimat overclaim, Q26 | **Selesai** (`run_eval_rms_gate.py`, `RMSGateBaseline`, `rule_margin`, `rmsgate_*`, 8 tes; 05 §2b/§2d, 08, 09, 10, README) | Menutup FF1b. Model gabungan RF + aturan RMS diuji dan dilaporkan nol hasil. Koreksi Holm 22 uji. Ini kerja yang benar |
| a2 Tanpa prioritas untuk rekaman yang gagal gerbang | **Selesai** (`detakpompa\triage.py`, `report.py`, `tests\test_triage.py`; laporan demo dibuat ulang) | Ditutup. Prioritas "sementara" untuk ragu adalah kompromi yang masuk akal |
| a3 `triase.py` + presisi top-3 | **Selesai** (`triase.py`, `run_triase_eval.py`, `results\triase\`) | Dikerjakan, tetapi prevalensi armadanya 2/3 (E2) |
| PRAREG-TKT4 (baru, tidak diminta di putaran 1) | **Ditulis**, belum dibekukan | Positif untuk kredibilitas; endpoint perlu diubah (§3) |
| Tes 23 → 40 | **Selesai**, diverifikasi | — |
| Q27 sensor lepas | **Selesai** | — |
| a4 Metrik biner sehat vs perlu cek | Tidak dikerjakan | E1 panel sebagian menggantikannya |
| a5 Paderborn prareg | Tidak dikerjakan (Q19: sengaja tidak pakai Paderborn karena non-komersial) | Alasannya sah untuk produk, tetapi tidak untuk uji riset/lomba |
| a6 Decimasi ke 3,2 kHz | Tidak dikerjakan | — |
| a7 Figur + deck | Tidak dikerjakan (`results\fig\` tidak ada) | — |
| a8 Mode operator | Tidak dikerjakan | — |
| a9 Klaim "AI" di judul/hook | **Sebagian**: "AI kami" dihapus, judul "yang tahu kapan harus diam" tetap | §5 |
| a10 Uji stres mikrofon/kecepatan | Tidak dikerjakan | — |
| a11 Q28, Q29 | Q26, Q27 ada; Q28, Q29 belum | — |
| `07_BISNIS_DAMPAK.md` | Tidak diperbarui sejak putaran 1. Rantai ① masih bertuliskan "AI mendeteksi" | Kecil, tapi tidak konsisten dengan §2d |

---

## 5. Uji anti-generik (putaran 2)

| Pertanyaan | Jawaban panel |
|---|---|
| Apakah 50 tim lain bisa mengirim hal yang hampir sama? | **Teknisnya ya, berkasnya tidak.** "RF + fitur getaran di dataset bantalan publik" tetap salah satu proyek paling umum. Yang tidak bisa disalin: (1) angka audit Ngagel I 12/22 dan 49,77 % dengan jalur kontak ITS–PDAM; (2) budaya evaluasi: pembanding adil yang menang tetap ditebalkan, Holm, prareg dengan aturan gagal. Ini jarang sekali di hackathon; (3) posisi "triase, bukan pengukur efisiensi", plus antrean UKUR ULANG yang terpisah |
| Judul memakai sudut unik? | **Belum.** "Triase pompa air PDAM yang tahu kapan harus diam": fitur di judul adalah gerbang DSP yang menurut 05 §2b bisa dipasang di model apa pun. Tidak bohong, tapi generik dan menjual bagian yang paling mudah ditiru. Saran: **"DetakPompa: memilih 3 dari 22 pompa PDAM yang diukur duluan"** atau **"Sepuluh pompa yang tidak sempat diaudit: triase getaran untuk IPA Ngagel I"** |
| Kata kosong? | Bersih. "Deteksi dini" (E1) adalah satu-satunya istilah yang menjanjikan lebih dari buktinya |
| Setiap angka bersumber? | Ya (§0). Angka 0,971 bersumber tetapi butuh konteks prevalensi |
| Pemenang tahun lalu? | Tidak ada data publik. Tidak bisa dibandingkan |

**Vonis: LULUS SEBAGIAN** (sama dengan putaran 1). Masalah, konteks, dan budaya evaluasinya unik. Metode dan judulnya generik.

---

## 6. Sisa gap (diurutkan menurut kenaikan skor ÷ usaha)

### (a) Bisa ditutup agen sekarang, tanpa mengarang

| # | Gap | Kenaikan (poin total) | Usaha | Instruksi spesifik |
|---|---|---|---|---|
| **a1** | FF1c: bingkai "deteksi dini" | +0,5 (J1/J4 AI +0,5) + mencegah Q&A runtuh | 20 menit | Di 09 slide 5 ganti label "Recall waspada (deteksi dini)" → "Recall waspada (label tahap)" dan tambahkan baris "Tahap awal yang ditandai perlu cek: 0,830 vs 0,840". Ganti naskah "AI kami lebih sering menangkap tahap awal" → "keduanya menandai tahap awal sama seringnya; AI lebih sering memberi label 'waspada', RMS menyebutnya 'rusak'". Sesuaikan 10 Q20, 05 §2d butir 2, 08 §2. Tambahkan Q30: "Recall waspada 0,415 itu deteksi dini?" (jawab dengan E1) |
| **a2** | Prareg belum dibekukan dan endpoint tidak sesuai (§3) | +0,5–1 (J1 +0,5, J4 +0,5) | 1 jam | Ubah PRAREG-TKT4 **sebelum** ada data pompa: endpoint utama biner "perlu cek" pada alarm palsu tetap (atau presisi@3 pada prevalensi ≤ 25 %), dengan **throttling sebagai kondisi perancu yang harus dianggap "sehat-beban-berubah"**; pembanding RMS + gerbang **dan** ambang kW. Recall waspada jadi sekunder. Lalu commit lokal seluruh `prototype\` + 05 (pesan diakhiri `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`) dan isi `[ISI: hash commit]`. Commit itu juga membuat klaim "protokol ditulis sebelum run" bisa diverifikasi ke depannya |
| **a3** | Presisi@3 tanpa prevalensi (E2) | +0,5 (J4/J2) | 1 jam | Di `run_triase_eval.py`, tambahkan skenario armada 22 pompa dengan 3 dan 5 pompa bermasalah, dan laporkan dasar acaknya. Di 05 §2c, 08 §3, 09 slide 5, 10 Q11/Q20, tulis 0,971 selalu bersama "(armada 2/3 bermasalah; pada 5 dari 22: ±0,79 vs ±0,76)". Sebutkan bahwa kedua model salah menandai rekaman sehat yang sama (H_13_0) |
| **a4** | Judul/hook generik | +0,5 (J4 inovasi +0,5; J3 presentasi) | 15 menit | Ganti judul di 08 (tiga versi) dan 09 dengan sudut unik (§5) |
| **a5** | Abstrak 150 kata tidak menjelaskan komponen AI | +0,5 (J3 presentasi/AI) | 30 menit | Tetap jujur, tapi tambahkan satu kalimat "apa yang dikerjakan AI": RF fitur spektral menilai kondisi dan memberi skor prioritas, gerbang SNR menolak sinyal jelek, antrean memilih 3 pompa. Lalu satu kalimat hasil ("setara dengan ambang RMS + gerbang yang sama"), lalu satu kalimat uji ("akan diuji di pompa lab dengan kriteria lulus yang sudah dibekukan"). Pangkas ke ≤150 dan ≤300 kata (sekarang 164 dan 329) |
| a6 | Ketidakcocokan sensor BOM (3,2 kHz) | +1 | 1–2 jam | Seperti putaran 1 a6, dengan pembanding RMS + gerbang |
| a7 | Figur + deck | +1–1,5 | 2–3 jam | Seperti putaran 1 a7. Tambahkan figur E1 (batang "ditandai perlu cek" per kelas, dua model) |
| a8 | Mode operator | +0,5–1 | 1–2 jam | Seperti putaran 1 a8. Sembunyikan "frekuensi poros terlacak" bila sinyal ditolak (sensor lepas sekarang mencetak "34,13 Hz (~2048 rpm)" dari derau murni) |
| a9 | Metrik biner (AUROC, sens./spes.) | +0,5 | 30 menit | Tulis sebagai eksploratif. Angka E1 bisa langsung dipakai |
| a10 | Paderborn dengan prareg | +0 s.d. +6 (veto bisa dicabut bersyarat) | 1–2 hari + **izin unduh dari user** | Seperti putaran 1 a5. CC BY-NC 4.0 boleh untuk riset/lomba bila dideklarasikan. Ubah Q19 supaya tidak terkesan menghindari uji |
| a11 | Uji stres mikrofon / pergeseran kecepatan | +0–1 | 1–2 jam | Seperti putaran 1 a10 (eksploratif) |
| a12 | Kepatuhan kecil | +0,25, mencegah risiko | 15 menit | `CARA_KIRIM.md` "23 passed" → 40; 08 §2 urutan "0,971 vs 0,952" ditulis eksplisit "(usulan 0,971; RMS 0,952)"; 07 rantai ① "AI mendeteksi" → "alat menandai"; Q28 dan Q29 dari putaran 1 |

**Total realistis (a) tanpa a10:** ±+6,5 → **±55**. Dengan a10 positif: ±+5 → **±60**, dan veto bisa dicabut bersyarat.

### (b) Hanya bisa ditutup manusia

| # | Aksi | Siapa | Kenaikan (estimasi) | Catatan |
|---|---|---|---|---|
| b1 | Login portal: **deadline WIB, field form, batas karakter**. Selesaikan bentrok 1 Nov dengan IBSC | Aziz | 0 poin, tapi **syarat ikut** | Hari ini. Batas karakter menentukan versi 150/300 mana yang dipakai |
| b2 | ≥5 wawancara PDAM/operator + 1 pakar (penulis S6) dengan skrip `06` §3 + pertanyaan juri tamu (§9) | Uqi, Pio | **+6–8** | Minimal 2 sebelum daftar kalau bisa. Tunjukkan `antrean_usulan.txt`, bukan laporan satu rekaman |
| b3 | Izin tertulis pilot (PDAM via DIKST/penulis S6, atau Sarpras ITB) | Aziz, Pio | **+3–5** | Tanpa hadiah/uang. Jangan lampirkan apa pun yang menyerupai LOI |
| b4 | **TKT 4 lab** dengan prareg yang sudah diubah dan dibekukan (a2): pompa sentrifugal + akselerometer BOM + clamp + power meter + flowmeter/manometer; sehat / imbalance / misalignment / **throttling**; ≥5 sesi × 30 s | Poggy | **+9–11 kalau AI lulus** (veto dicabut). **+4 kalau gagal** (TKT 4 sah, veto tetap → batas 80, dan "AI di inti" turun lagi) | Satu-satunya jalan nyata untuk menutup FF1 di domain pompa |
| b5 | Data PDAM: log PM2100/ampere per shift, catatan perawatan, status rekondisi 5 pompa S6 | Aziz (lewat penulis S6) | **+4–6** | On-prem |
| b6 | Video demo ≤2 menit (versi setelah a1–a5), data tim, foto, dosen pembimbing, latihan Q&A (Q20, Q26, Q30) | Poggy, semua | +1 | — |
| b7 | Konfirmasi izin FaceVitals dan tidak ada pengiriman ganda | Poggy, Aziz | 0, mencegah FF5 | — |
| b8 | Coba ulang dataset pompa 4TU dari jaringan lain | siapa saja | +0–2 | Cek lisensi dan ukuran dulu, dan minta izin unduh |
| b9 | Izinkan agen mengunduh subset Paderborn (a10) | user | memungkinkan +0–6 | Catat nama berkas, sumber, ukuran sebelum unduh |

---

## 7. Plafon

| Keadaan | Skor | Catatan |
|---|---|---|
| Putaran 1 | 46,9 | Veto aktif |
| **Sekarang (putaran 2)** | **48,9** | Veto aktif (FF1). FF1b tertutup, FF1c terbuka |
| **Plafon sekarang** (semua aksi agen a1–a9, a11, a12) | **±55** | FF1c tertutup, FF1 tetap. Validasi tetap ±2 |
| Plafon sekarang + a10 Paderborn positif | ±60 | Veto dicabut bersyarat. Hasil tidak dijamin |
| + b2 wawancara | ±62 (±67) | |
| + b3 izin pilot | ±66 (±71) | |
| + b4 TKT 4 lab, AI lulus prareg | ±76 (±81) | Kalau AI **gagal**: +4 dan veto tetap → batas keras 80, realistis ±70 |
| + b5 data PDAM | ±81 (±85) | |
| + b6 video/deck/latihan | **±82 (±86)** | |
| **Plafon setelah aksi manusia** | **±82–86 kalau AI lulus; maksimal 80 (realistis ±70–74) kalau tidak** | Skor 90 tetap butuh TKT 5 (presisi top-3 terukur di pompa PDAM pada prevalensi nyata, AI > RMS + gerbang). Kecil kemungkinan selesai sebelum Demo Day Jan 2027 |
| **Realistis saat berkas dikirim** (agen a1–a5, a12 + b1 + 1–2 wawancara + video) | **±56–59** | Ini angka yang dibaca reviewer seleksi 15 tim |

---

## 8. Rekomendasi jujur untuk tim

**Rekomendasi panel: DAFTAR dengan DetakPompa, dengan syarat.** Pivot ke LautHemat tidak disarankan. "Tidak ikut" hanya kalau syarat minimum di bawah tidak bisa dipenuhi.

**Alasan memilih DetakPompa:**
- Purwarupanya memenuhi syarat formal "purwarupa AI TKT 3": ada model ML yang berjalan end-to-end di data nyata, dengan evaluasi tanpa kebocoran, 40 tes, dan demo yang bisa diulang. Kejujurannya jauh di atas rata-rata.
- Masalahnya lokal, bersumber, dan cocok dengan mitra energi lomba ini (S6: Rp147,65 M, 12/22, 49,77 %).
- Kelemahan terbesarnya (AI belum diperlukan) **sudah diketahui, tertulis, dan punya uji yang bisa memutuskannya**. Itu lebih baik daripada kelemahan yang belum diketahui.

**Syarat daftar (semua wajib):**
1. b1 selesai: deadline WIB dan isi form diketahui, ada pengirim yang tidak bentrok dengan IBSC.
2. Agen mengerjakan a1 (deteksi dini), a3 (prevalensi), a4 (judul), a5 (abstrak + batas kata), dan a12 **sebelum** teks disalin ke form. Kalau a2 juga sempat, commit lokal dan isi hash prareg.
3. Video demo direkam dari versi setelah perbaikan. Sensor lepas harus tampil tanpa prioritas dan tanpa rpm palsu.
4. Validasi pengguna ditulis jujur: hasil wawancara asli, atau "dijadwalkan". **Jangan** memakai persona.
5. Izin FaceVitals dikonfirmasi (b7).

**Syarat lanjut setelah lolos 15 besar:** b4 dengan prareg yang sudah diubah adalah titik keputusan. Kalau AI **gagal** prareg, jangan pitch DetakPompa sebagai "karya AI" di Demo Day. Pilihannya: (a) pitch jujur sebagai "triase DSP + aturan" dan terima bahwa skor kriteria AI rendah, atau (b) pindahkan peran AI ke tempat yang memang memerlukannya, yaitu model baseline per pompa dari kW–tekanan–debit dengan data PDAM (b5), dengan prareg baru.

**Kenapa tidak pivot ke LautHemat sekarang:**
- Komponen AI-nya **belum ada sama sekali**. `01_INVENTARIS_ASET.md` C: "Komponen AI: belum ada. Quantile mapping adalah statistik, bukan ML". Untuk TKT 3, model prakiraan harus dibangun dari nol (estimasi 3–5 hari) dan harus mengalahkan persistensi/klimatologi. Itu FF1 yang sama, dalam bentuk lain, dengan waktu lebih sedikit.
- Energy gap-nya bersumber dari organisasi advokasi (S5), kaitan prakiraan → BBM butuh data trip/tangkapan yang belum ada, akses nelayan dari Bandung sulit, dan pesaingnya pemerintah (PPDPI).
- **Pivot hanya masuk akal kalau:** deadline ≥ 7 Nov, **dan** Poggy punya ≥3 hari penuh untuk membangun prakiraan vs persistensi dengan LOYO dan prareg, **dan** aturan berhenti DetakPompa terpicu (H1 akses dan H3 rasa sakit sama-sama gagal setelah 5 wawancara).

**Tidak ikut, kalau:** deadline ternyata 1 Nov **dan** tidak ada anggota yang bisa login, mengisi `[ISI]` tim, dan mengirim tanpa mengorbankan IBSC. Mengirim berkas berisi `[ISI]`, atau mengisinya dengan tebakan, lebih buruk daripada tidak ikut: itu memicu FF4 atau diskualifikasi formal.

---

## 9. Juri tamu (non-skor): operator / manajer pompa PDAM

> **SIMULASI PERSONA, BUKAN BUKTI.** Disusun panel dari fakta S6 (`06` §0 F4–F8) dan dari membaca keluaran asli `results\triase\armada_22\antrean_usulan.txt` dan `results\demo\*.txt` versi terbaru. **Tidak boleh dikutip** di berkas, deck, atau video. Semua butir adalah **pertanyaan untuk wawancara asli (b2)**, bukan temuan.

**Persona:** operator shift rumah pompa distribusi (±10 tahun) dan kepala unit produksi. Mereka melihat daftar armada 22 "pompa" dan laporan sensor lepas.

**Yang membaik sejak putaran 1 (menurut persona):**
- Daftar armada adalah bentuk yang benar untuk kepala IPA: tiga nama di atas, antrean ukur ulang terpisah, dan langkah per baris.
- Sensor lepas tidak lagi menyalip pompa rusak, dan antrean UKUR ULANG punya instruksi pemasangan yang bisa langsung dikerjakan.
- Kalimat "TIDAK TAHU bukan berarti aman" di setiap laporan mudah dimengerti.

**Yang masih membuat tidak dipakai:**
1. **"RUSAK tapi PANTAU?"** Di daftar contoh ada empat pompa berstatus RUSAK di antrean PANTAU karena "di luar kapasitas audit". Kepala IPA akan membaca ini sebagai "rusak dibiarkan". Perlu kata lain (mis. "antre audit minggu depan") atau tampilan yang memisahkan status dari antrean.
2. **"Empat belas dari dua puluh pompa saya bermasalah?"** Armada contoh terlalu sakit untuk IPA nyata. Persona akan bertanya bagaimana daftar ini terlihat kalau hanya 2–3 pompa yang menurun, dan berapa kali minggu itu tim flowmeter didatangkan ke pompa sehat (E2: pada 3/22, ±6 dari 10 armada simulasi punya ≥1 pompa sehat di AUDIT DULU).
3. **Kapasitas k = 3 per ronde: dari mana?** Berapa pompa yang benar-benar bisa diukur flowmeter portabel per minggu oleh tim PDAM? Itu harus ditanyakan, bukan diasumsikan.
4. **Angka prioritas 0,85 / 0,78 dan "label asli … tidak dipakai model"** tidak berarti bagi operator. Baris label asli cocok untuk demo juri, tapi harus hilang di versi lapangan.
5. **Laporan sensor lepas masih mencetak "frekuensi poros terlacak 34,13 Hz (~2048 rpm)"** dari derau murni. Operator yang mencocokkan rpm dengan pelat nama bisa tertipu.
6. **Baseline per pompa masih belum jelas sumbernya** ("bandingkan dengan rekaman baseline unit ini (mode --baseline)"). Siapa yang merekam baseline, kapan (setelah overhaul?), dan disimpan per nomor pompa di mana?
7. **Masih file .mat 42 kHz.** Belum ada jawaban untuk "alat apa yang saya bawa saat ronde, ditempel di mana, 30 detik per pompa".

**Pertanyaan tambahan untuk wawancara asli (lanjutan daftar putaran 1):**
1. Berapa pompa yang bisa diukur debit + head-nya oleh tim PDAM dalam seminggu (nilai k yang realistis)?
2. Dari 22 pompa, berapa yang menurut Anda sedang bermasalah saat ini (prevalensi)?
3. Kalau daftar ini salah mengirim tim ke satu pompa sehat per bulan, apakah daftar masih dipakai?
4. Apakah label "waspada" vs "rusak" mengubah tindakan Anda, atau yang penting hanya "cek / tidak cek"? (Ini langsung menentukan apakah endpoint prareg recall waspada relevan, lihat §3.)
5. Apakah perubahan karena pengaturan katup atau permintaan zona sering membuat angka ampere/kW panel "terlihat aneh"? (Ini menguji alasan AI di Q20.)

---

*Skrip panel (hanya membaca hasil tim, tidak mengubah file proyek):* `C:\Users\POGGY\AppData\Local\Temp\claude\C--Users-POGGY--claude-spares-spare-xjE250\c0f1913a-f688-4e27-af57-a6dab34be300\scratchpad\j4_prevalence.py`. E1 dihitung langsung dari matriks kebingungan di `prototype\results\rmsgate_metrics.csv`.
