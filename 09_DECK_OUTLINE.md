# 09_DECK_OUTLINE: deck Demo Day DetakPompa (10 slide, ±5 menit)
### Agen A9 "Penulis Pitch" · 28 Okt 2026 · dasar: `07-MEGA-PROMPT-ITS-HACKATHON-28okt2026.md` §B Fase 7, `08_PENDAFTARAN.md`

**Aturan deck:**
- Satu slide = satu pesan. Judul slide **adalah** pesannya.
- Setiap angka di slide diberi rujukan kecil di pojok bawah (`[S6]`, nama file hasil, dst.).
- **Slide 3 tidak boleh berisi kutipan apa pun sampai wawancara asli selesai.** Persona simulasi di `03b` §2.9 dan `06` §6 dilarang muncul di slide, naskah, atau video.
- Angka hemat energi hanya muncul di slide 8, berlabel **[SKENARIO]**.
- Visual yang belum ada ditandai `[ISI: buat dari ...]`. Figur jadi saat ini: `prototype\results\coverage_risk.png`, `prototype\results\rmsgate_coverage_risk.png`, dan `prototype\results\skab\ruang_Q_p_P.png` (SKAB, wajib dengan caption perancu sesi).
- Naskah ±30 detik ≈ 65–80 kata diucapkan santai. Total ±5 menit + demo langsung.

**Judul deck (sampul):** DetakPompa: memilih 3 dari 22 pompa PDAM yang diukur debitnya duluan. Subjudul: "Antrean audit untuk 22 pompa IPA Ngagel I dari rekaman getaran singkat per pompa." Sama dengan judul di `08_PENDAFTARAN.md`. Judul lama "triase … yang tahu kapan harus diam" **tidak dipakai lagi**: fitur yang dijualnya (gerbang SNR) bisa dipasang di model apa pun.

---

## Slide 1. Hook (20 detik)
**Judul-pesan:** 22 pompa, 12 terukur, 5 di bawah 55 %. Sepuluh sisanya tidak terlihat.

**Isi:**
- IPA Ngagel I, Surabaya: 8 pompa air baku + 14 pompa distribusi [S6]
- Audit energi manual mengukur 12 [S6]
- 5 dari 12 itu bekerja di bawah ±55 %. Terendah 49,77 % [S6]
- Satu baris di bawah: "DetakPompa memilih pompa mana yang diukur duluan."

**Visual:** 22 ikon pompa dalam dua baris (8 dan 14). 12 berwarna (5 merah, 7 abu), 10 kosong dengan tanda tanya. `[ISI: buat ikon di Canva/PowerPoint dari angka S6]`

**Naskah (±20 detik):**
> "Di IPA Ngagel I, Surabaya, ada dua puluh dua pompa. Waktu ITS dan PDAM mengaudit energinya, yang sempat diukur hanya dua belas, karena debitnya harus diukur manual dengan flowmeter portabel. Dari dua belas itu, lima bekerja di bawah lima puluh lima persen. Yang paling rendah empat puluh sembilan koma tujuh tujuh. Sepuluh pompa sisanya? Tidak masuk audit itu. DetakPompa membantu memilih pompa mana yang diukur duluan."

---

## Slide 2. Energy gap
**Judul-pesan:** Di angka bulanan IPA, PDAM tampak efisien. Pompa yang menurun tersembunyi di dalamnya.

**Isi (kiri: biaya, kanan: kenapa tersembunyi):**
- Biaya energi PDAM Surya Sembada **Rp147,65 miliar (2021)**, **24,37 %** biaya operasional [S6]
- Biaya energi **Rp409/m³**, rata-rata nasional Rp356,34/m³ [S6]
- SEC IPA Ngagel I **0,27–0,29 kWh/m³**, sudah di bawah patokan 0,4 [S6]. Karena itu satu pompa yang menurun hampir tidak menggerakkan angka bulanan.
- Pompa aus memang memakan energi lebih: satu kasus lapangan, efisiensi turun **65,2 % → 53,6 %** [S10]
- Kotak kecil "yang tidak kami klaim": angka "motor = 45 % listrik dunia" [S3] hanya konteks; potensi hemat 20–30 % di sumber itu berasal dari efisiensi sistem motor, bukan dari deteksi kerusakan (`03b` §2.3).

**Visual:** dua angka besar di kiri (Rp147,65 M · 24,37 %). Di kanan, satu batang SEC IPA 0,27 di bawah garis 0,4, dengan lima titik merah pompa (U6 baku 54,26 %, U6 distribusi 51,76 %, T1 49,77 %, S1 51,18 %, S2 52,60 % [S6]) "di balik" batang itu. `[ISI: buat dari 07_BISNIS_DAMPAK.md §3.2]`

**Naskah (±30 detik):**
> "PDAM Surabaya membayar seratus empat puluh tujuh miliar rupiah untuk energi pada 2021, hampir seperempat biaya operasionalnya. Tapi kalau Direksi melihat angka bulanan IPA, semuanya tampak baik: nol koma dua tujuh kilowatt-jam per kubik, di bawah patokan nol koma empat. Masalahnya, satu pompa yang menurun tidak menggerakkan angka itu. Di Ngagel I ada lima pompa di bawah lima puluh lima persen. Celah energinya adalah waktu antara pompa mulai menurun dan pompa itu akhirnya diaudit."

---

## Slide 3. Pengguna + bukti wawancara
**Judul-pesan:** [ISI: judul dari temuan wawancara asli, mis. "Kepala IPA memilih pompa untuk rekondisi dari ..."]. Kalau wawancara belum ada: "Penggunanya jelas. Validasinya sedang berjalan, dan kami tunjukkan apa adanya."

**Isi:**
- **Siapa pakai** (dari `06_VALIDASI_PENGGUNA.md` §1.1): operator rumah pompa (pemakai harian), teknisi pemeliharaan, kepala IPA/unit produksi (memilih pompa untuk rekondisi), manajer energi. **Pembeli:** Direksi lewat RKAP.
- **Fakta yang sudah ada di rumah pompa** [S6]: power meter Schneider PM2100 di tiap panel; debit diukur dengan flowmeter ultrasonik portabel; aturan praktik η ≥ 60 % → rawat rutin, ≤ 50 % → perbaikan total.
- **Bukti wawancara:** [ISI: hasil wawancara — jumlah responden dan peran (kode R1–R6 + pakar), tanggal]
- **Papan skor hipotesis** (dari `06` §7.2): H1 akses [ISI: L/G], H3 rasa sakit [ISI: L/G], H6 abstain dihargai [ISI: L/G]
- **Komitmen nyata yang didapat:** [ISI: perkenalan / kunjungan / data / surat, atau "belum ada"]
- **Yang berubah karena wawancara:** [ISI: satu perubahan produk yang lahir dari wawancara asli]

**Visual:** tabel papan skor hipotesis (L/G per responden). `[ISI: isi dari 06_VALIDASI_PENGGUNA.md §7.2 setelah wawancara]`. **Jangan** memakai foto orang atau rumah pompa tanpa izin tertulis.

**Naskah (±30 detik):**
> "[ISI: naskah dari hasil wawancara asli. Kerangka: 'Kami berbicara dengan [jumlah] orang: [peran]. [Temuan paling mengejutkan, dengan kata-kata mereka hanya kalau mereka mengizinkan dikutip tanpa nama]. Hipotesis yang gagal: [..]. Karena itu kami mengubah [..].']"
>
> *Kalau wawancara belum terlaksana sebelum Demo Day, pakai versi ini:* "Pengguna kami adalah kepala IPA yang setiap tahun harus memilih pompa mana yang direkondisi dengan anggaran terbatas, dan teknisi yang harus membuktikannya. Wawancara kami dengan PDAM sedang berjalan. Kami belum mau mengutip siapa pun sebelum kami punya jawaban asli. Yang sudah kami siapkan: delapan hipotesis dengan kriteria gagal yang jelas, termasuk aturan kapan ide ini kami hentikan."

---

## Slide 4. Demo
**Judul-pesan:** Tiga rekaman, tiga jawaban, termasuk "tidak tahu".

**Isi:**
- Demo langsung `demo.py` (atau video cadangan) pada tiga rekaman dari bantalan yang **dikeluarkan dari data latih**:
  1. `H_3_0` → **SEHAT**, prioritas cek 0,02 (`prototype\results\demo\laporan_H_3_0.txt`)
  2. `I_3_1` → **RUSAK**, prioritas 0,88. Label aslinya "waspada": tingkatnya salah, tetapi pompa ini tetap masuk daftar cek (`laporan_I_3_1.txt`)
  3. `sensor_lepas.npy` (derau murni) → **TIDAK TAHU**, antrean **UKUR ULANG**, **tanpa prioritas**: "garis putaran poros tidak terlihat". Langkah berikut: pasang ulang sensor di bearing housing, ukur ulang 30 detik. Tanpa gerbang SNR, model sendiri akan menjawab "rusak" 0,74 (`laporan_sensor_lepas.txt`)
- Penutup demo (±15 detik): `triase.py` pada armada contoh 22 rekaman → satu tabel AUDIT DULU (3) / PANTAU / UKUR ULANG / AMAN (`prototype\results\triase\armada_22\antrean_usulan.txt`). Label: bearing Ottawa sebagai pengganti pompa.
- Setiap laporan memuat catatan energi berlabel **[SKENARIO, BUKAN PENGUKURAN]** dan batas klaim.

**Visual:** layar terminal dengan tiga laporan berdampingan, kata STATUS diperbesar. `[ISI: screenshot dari prototype\results\demo\*.txt]` · Video cadangan: `[ISI: link video demo ≤2 menit]`

**Naskah (±30 detik, di luar waktu demo):**
> "Ini tiga rekaman dari bantalan yang tidak pernah dilihat model saat latihan. Yang pertama sehat, dan alat bilang sehat. Yang kedua sedang berkembang rusak; alat bilang rusak. Tingkatnya kurang tepat, tapi pompanya tetap masuk daftar cek. Yang ketiga adalah sensor yang lepas, isinya derau. Model kami sebenarnya yakin tujuh puluh empat persen itu 'rusak'. Gerbang sinyal, aturan DSP yang juga bisa dipasang di depan RMS, menahannya. Alat menjawab 'tidak tahu, pasang ulang sensornya', memasukkannya ke antrean ukur ulang, dan tidak memberinya nomor urut. Jadi sensor lepas tidak pernah menyalip pompa yang benar-benar rusak."

---

## Slide 5. Hasil vs baseline
**Judul-pesan:** Gerbang sinyal kami terbukti. AI kami belum: dengan gerbang yang sama, ambang RMS sama baiknya.

**Isi:**
- Desain uji: leave-one-bearing-out 20 fold, 600 jendela, data Ottawa CC BY [S13]; tidak ada bantalan yang sama di data latih dan uji (`prototype\tests\test_split.py`)
- Tabel, semua model di belakang **gerbang SNR yang sama**, jendela yang sama (cakupan 0,955), CI95 bootstrap per unit (`prototype\results\rmsgate_metrics.csv`, `rmsgate_paired_bootstrap.csv`, `triase\eval_log.txt`):

| | **Ambang RMS + gerbang** | Usulan (RF spektral) + gerbang | Selisih usulan − RMS |
|---|---|---|---|
| Akurasi seimbang | **0,639** | 0,605 | −0,034 [−0,155; +0,071] |
| Presisi 3 pompa teratas, armada simulasi 2/3 bermasalah (dasar acak 0,667) | 0,952 | 0,971 | +0,019 [−0,333; +0,333] |
| Presisi 3 pompa teratas, 22 pompa, 5 bermasalah (dasar acak 0,227) | 0,765 | 0,791 | +0,026 [−0,333; +0,500] |
| Presisi 3 pompa teratas, 22 pompa, 3 bermasalah (dasar acak 0,136) | 0,682 | 0,707 | +0,022 [−0,333; +0,333] |
| Recall rusak | **0,795** | 0,470 | −0,324 [−0,562; −0,089] |
| Recall waspada (label tahap) | 0,213 | **0,415** | +0,202 [−0,056; +0,453] |
| Tahap awal (waspada) yang ditandai perlu cek | **0,840** | 0,830 | — |

- Setelah koreksi Holm atas 22 uji, **tidak ada selisih yang signifikan** ke arah mana pun (`rmsgate_paired_bootstrap.csv`, kolom `p_holm_all`).
- Presisi 3 teratas turun dari 0,97 ke ±0,7–0,8 bila hanya 3–5 dari 22 pompa bermasalah, sama untuk kedua model. Keduanya salah menandai rekaman sehat yang sama (H_13_0) (`triase\eval_prevalensi_log.txt`).
- Recall waspada adalah beda label, bukan deteksi lebih dini: kedua model menandai ±83–84 % jendela tahap awal untuk dicek; RMS menyebutnya "rusak", AI "waspada" (`rmsgate_metrics.csv`).
- Gerbang SNR (DSP, warisan FaceVitals) menolak **98,8 %** jendela sensor lepas, untuk RMS maupun AI. Gerbang keyakinan model saja meloloskan 88–97 % (`rmsgate_degradation_summary.csv`).
- Baris bawah slide: "Klaim AI = hipotesis. Syarat lulus dibekukan sebelum ada data baru (SHA-256): di unit fisik yang belum pernah dilihat, AI harus lebih akurat dari RMS + gerbang, dan lebih mampu membedakan throttling katup dari kerusakan; batas bawah CI 95 % > 0." (`prototype\PRAREG_TKT4.md` v2, `05_BUKTI_TKT.md` §3)
- Kotak kecil **"Uji di data pompa: GAGAL"**: data lab pompa publik SKAB (pihak lain, 1 testbed), prareg dikunci hash sebelum data diunduh. Katup vs fault (H1): model residual 1,000 = ambang arus 1,000 → gagal. Anomali umum (H2): 0,532 vs 0,581 → gagal. Post-hoc: eksperimen katup dan fault direkam di rezim debit berbeda (±32 vs ±125 L/min), jadi data ini tidak bisa menguji klaim dengan tajam (`prototype\results\skab\summary.json`, `posthoc_log.txt`, `05_BUKTI_TKT.md` §2e). **Jangan** ditulis sebagai TKT 4.
- Catatan kaki: banyak studi CWRU melaporkan hampir 100 %; 40 dari 41 studi CWRU memakai split yang rentan bocor [S14]

**Visual:** kiri: tabel di atas, kolom RMS **ditebalkan** (kami sengaja menyorot pembanding yang menang). Kanan: `prototype\results\rmsgate_coverage_risk.png` (kurva bergerbang keduanya; di cakupan ≥ 0,5 galat RMS sama atau lebih rendah). `[ISI: buat batang recall waspada/rusak dari rmsgate_metrics.csv]`. Untuk kotak SKAB: `prototype\results\skab\ruang_Q_p_P.png` kecil, caption "Uji diprareg GAGAL; katup dan fault direkam di rezim berbeda".

**Naskah (±30 detik):**
> "Kami menguji dengan cara yang paling tidak menguntungkan diri sendiri: tiap bantalan diuji tanpa pernah dilihat saat latihan, dan pembandingnya ambang RMS yang kami beri gerbang sinyal yang sama. Hasilnya: setara. Untuk memilih tiga pompa teratas, keduanya sama tepatnya: hampir selalu benar kalau dua pertiga armada rusak, sekitar tujuh atau delapan dari sepuluh kalau hanya tiga sampai lima dari dua puluh dua yang bermasalah. RMS lebih jeli melihat yang sudah rusak. Keduanya menandai tahap awal untuk dicek sama seringnya; AI hanya lebih sering menamainya 'waspada'. Yang terbukti bekerja adalah gerbang sinyalnya. Jadi AI kami kami sebut hipotesis, dan syarat lulusnya sudah kami bekukan sebelum ada data baru. Kami juga sudah mencobanya sekali di data lab pompa milik pihak lain, dengan aturan yang dikunci sebelum datanya dibuka. Hasilnya gagal, dan kami tunjukkan di sini."

---

## Slide 6. Pembanding
**Judul-pesan:** Vendor besar menjual alarm kerusakan. Kami menjual urutan pompa yang perlu diukur, dan kami kalah di banyak hal lain.

**Isi:** tabel ringkas dari `07_BISNIS_DAMPAK.md` §6:

| | DetakPompa | Schneider (sudah mitra PDAM [S7]; PM2100 di panel [S6]) | Schaeffler OPTIME [S16] | Include Technology Indonesia, startup ITS [S17] | Augury |
|---|---|---|---|---|---|
| Fokus | Triase: pompa mana diukur duluan | Meter energi, *smart water* | Getaran nirkabel: imbalance, misalignment | IoT, deteksi kegagalan, PdM | Getaran/suhu/magnetik + AI |
| Abstain + langkah berikut | Ya | [ISI] | Tidak disebut di [S16] | Tidak diverifikasi | Tidak diverifikasi |
| Pakai meter panel yang ada | Rencana (mode A) | Ya, milik mereka | Tidak | [ISI] | Tidak |
| Harga | [ASUMSI] Rp300 rb/pompa/bulan | [ISI] | [ISI] | [ISI] | Estimasi US$50–200/mesin/bulan [B6] |

- **Di mana kami kalah:** perangkat bersertifikat industri, garansi, jaringan layanan, rekam jejak. Schneider sudah ada di dalam PDAM. Include ada di kampus yang sama.
- **Posisi:** lapisan analitik yang **membaca** meter Schneider, bukan pengganti.

**Visual:** tabel di atas; kolom DetakPompa diberi latar tipis. Sumber di kaki slide.

**Naskah (±30 detik):**
> "Kami bukan yang pertama memantau mesin dengan AI. Schaeffler punya OPTIME, dan di ITS sendiri ada Include Technology yang mengerjakan predictive maintenance. Schneider bahkan sudah bermitra dengan PDAM dan meternya terpasang di setiap panel. Dalam perangkat keras, garansi, dan layanan, kami kalah. Yang kami tawarkan lebih sempit: membaca data yang sudah ada, mengurutkan pompa yang perlu diukur debitnya, dan berani bilang 'tidak tahu'. Kami ingin jadi lapisan di atas meter Schneider, bukan pesaingnya."

---

## Slide 7. Bisnis
**Judul-pesan:** Mulai dari pilot riset tanpa pembelian, lalu jasa triase berbatas waktu, baru langganan.

**Isi** (`07_BISNIS_DAMPAK.md` §2–§3):
- **Fase 0 (Nov 2026 – ±Mar 2027):** pilot riset ITS–PDAM di 1–2 pompa yang kondisinya sudah diketahui dari audit [S6]. Pendapatan 0. Tanpa uang/hadiah untuk staf PDAM.
- **Fase 1:** kampanye triase 3 bulan per IPA, [ASUMSI] Rp30 juta.
- **Fase 2:** langganan [ASUMSI] Rp300.000/pompa/bulan → 22 pompa = Rp79,2 juta/tahun.
- Capex satu IPA ±Rp40,2 juta (komponen bersumber [B1]–[B3]; lebih dari separuh masih [ASUMSI]).
- **Titik impas:** 76.464 kWh/tahun per IPA = satu pompa ±24,5 kW direkondisi ±4,3 bulan lebih awal.
- Pasar lanjutan: 38 Perumda air minum di Jawa Timur [B7]. Jumlah pompa per Perumda [ISI].

**Visual:** tiga anak tangga (Fase 0 → 1 → 2) dengan syarat naik di setiap anak tangga: izin tertulis → presisi top-3 terukur → neto positif diukur PDAM.

**Naskah (±30 detik):**
> "PDAM adalah BUMD. Pembelian lewat RKAP tahunan dan pengadaan, jadi kami tidak mulai dengan menjual. Langkah pertama adalah pilot riset bersama ITS, tanpa pembelian. Kalau urutan pompa kami terbukti tepat ketika dicek dengan flowmeter PDAM sendiri, baru kami tawarkan kampanye triase tiga bulan per IPA, lalu langganan. Harga yang kami tulis masih asumsi. Titik impasnya bisa dicek siapa pun: satu pompa yang menurun dua puluh empat kilowatt direkondisi empat bulan lebih awal dalam setahun."

---

## Slide 8. Dampak
**Judul-pesan:** Pilot kami menghemat nol kWh. Penghematan datang dari rekondisi PDAM; kami membuatnya datang lebih awal.

**Isi:**
- Tiga mata rantai yang dipisah (`07_BISNIS_DAMPAK.md` §0): ① Alat menandai → ② audit mengukur Q dan H → ③ PDAM merekondisi. DetakPompa hanya mengklaim ①.
- **[SKENARIO, BUKAN PENGUKURAN]** per IPA, atribusi DetakPompa (`07` §3.4, §4.2):

| Skenario | kWh/tahun | Rp/tahun | tCO₂e/tahun |
|---|---|---|---|
| Pilot Fase 0 | 0 | 0 | 0 |
| Konservatif | 12.352 | 12,8 juta | 10,7 |
| Moderat | 171.766 | 177,9 juta | 149 |

- Tarif Rp1.035,78/kWh [S19]; faktor emisi Jamali 0,87 tCO₂/MWh, nilai 2019 [S21]. Jumlah kejadian, waktu lebih awal, dan utilisasi adalah [ASUMSI].
- Pembanding skala: listrik IPA Ngagel I 14.738.920 kWh (2021) [S6]. Skenario moderat ≈ 1,2 % darinya.
- Nilai rekondisi 5 pompa yang sudah ditemukan audit S6 (536.681–858.690 kWh/tahun) adalah milik PDAM, **bukan** klaim kami.

**Visual:** rantai ①→②→③ dengan kotak "klaim kami" hanya di ①. Di bawahnya tabel skenario, dengan label [SKENARIO] besar.

**Naskah (±30 detik):**
> "Kami ingin jujur soal dampak. Pilot kami tidak menghemat satu kilowatt-jam pun. Penghematan terjadi kalau PDAM mengukur pompa yang kami tandai, lalu merekondisinya. Yang bisa kami klaim hanya bagian 'lebih awal'. Dalam skenario moderat, itu sekitar seratus tujuh puluh ribu kilowatt-jam per tahun untuk satu IPA, sekitar satu persen listriknya. Angkanya kecil, dan memang sengaja kecil supaya bisa dipertahankan. Angka sungguhannya akan kami ukur bersama PDAM."

---

## Slide 9. Roadmap TKT 3 → 4 → 5
**Judul-pesan:** Hari ini TKT 3 di data bantalan publik. Uji pertama di data pompa lab pihak lain gagal. Yang memisahkan kami dari TKT 4 adalah rig pompa sendiri dengan throttling bertingkat.

**Isi** (`05_BUKTI_TKT.md` §1, §3):

| TKT | Status | Bukti / syarat |
|---|---|---|
| **3** | **Selesai (28 Okt 2026)** | Leave-one-bearing-out Ottawa, 3 baseline + RMS dengan gerbang yang sama, abstain, triase armada, 54/54 tes (`prototype\results\`) |
| 4 | **Belum.** Uji pertama di data lab pompa pihak lain (SKAB, 1 testbed, prareg terkunci): **GAGAL**, dan data itu tidak tajam (perancu sesi, throttling ±6 % Q). Target rig sendiri: [ISI: tanggal] | Motor + pompa sentrifugal lab `[ISI: akses lab]`; akselerometer, clamp arus, power meter, flowmeter, manometer; kondisi sehat / tidak seimbang / misalignment / **throttling bertingkat yang menggeser titik kerja ≥ 20–30 % Q**, ≥5 × 30 s, **sesi diacak** (pelajaran SKAB), ≥ 3 unit; ukur ΔkW dan ΔkWh/m³; bandingkan lagi dengan RMS + gerbang yang sama. Fitur arus (MCSA) = model baru, jadi butuh prareg baru sebelum data (PRAREG v2) |
| 5 | Belum. Target: [ISI: tanggal] | Izin PDAM untuk ≥3 pompa IPA Ngagel; rekaman ≥4 minggu + kWh/m³ + catatan perawatan; cek apakah urutan triase cocok dengan pompa yang hasil auditnya terburuk |

- Aturan berhenti: kalau akses PDAM (H1) dan rasa sakit (H3) sama-sama gagal setelah 5 wawancara, DetakPompa turun ke cadangan (`06` §2).

**Visual:** garis waktu tiga titik, titik TKT 3 terisi, titik 4 dan 5 kosong dengan daftar syarat di bawahnya.

**Naskah (±30 detik):**
> "Status kami TKT 3: konsep terbukti di data nyata, tapi data bantalan publik, bukan pompa, dan belum ada arus motor. Kami sudah mencoba sekali di data lab pompa publik dengan aturan yang dikunci lebih dulu, dan hasilnya gagal: tidak lebih baik dari ambang arus, dan datanya terlalu tumpul untuk menguji klaim kami. Untuk TKT 4 kami butuh pompa lab sendiri, power meter, dan flowmeter, lalu menginduksi kerusakan dan throttling katup bertingkat dalam sesi yang diacak. Di situ kami juga akan menguji ulang: kalau ambang RMS ditambah gerbang yang sama tetap setara AI kami, yang kami kirim ke PDAM adalah yang lebih sederhana. TKT 5 baru dimulai setelah ada izin tertulis dari PDAM."

---

## Slide 10. Tim
**Judul-pesan:** Empat orang yang membangun purwarupa ini dan sedang mengetuk pintu PDAM.

**Isi:**

| Nama | Prodi, kampus | Peran |
|---|---|---|
| [ISI: nama lengkap Aziz] | [ISI: prodi, kampus] | PIC; pemilik bersama kode DSP FaceVitals |
| [ISI: nama lengkap Poggy] | [ISI: prodi, kampus] | [ISI: peran, mis. purwarupa dan evaluasi]; pemilik bersama kode DSP FaceVitals |
| [ISI: nama lengkap Uqi] | [ISI: prodi, kampus] | [ISI: peran, mis. validasi pengguna] |
| [ISI: nama lengkap Pio] | [ISI: prodi, kampus] | [ISI: peran, mis. validasi pengguna, jalur pilot] |

- **Permintaan kami di Demo Day:** (1) perkenalan ke unit produksi PDAM Surya Sembada lewat jalur resmi ITS; (2) akses satu pompa lab untuk TKT 4; (3) mentoring soal pengadaan BUMD. Bukan dana.

**Visual:** foto tim `[ISI: foto tim, dengan izin semua anggota]`, satu baris per orang.

**Naskah (±30 detik):**
> "Kami [ISI: empat mahasiswa dari ...]. Kode pengolahan sinyal ini berasal dari proyek pengukur detak jantung dari video wajah yang dua dari kami bangun, lalu kami ubah untuk mendengar detak mesin. Yang kami minta hari ini bukan dana. Kami minta perkenalan ke unit produksi PDAM lewat jalur ITS, akses ke satu pompa lab, dan masukan soal pengadaan BUMD. Kalau urutan pompa kami salah, kami ingin tahu secepatnya, dari flowmeter PDAM sendiri."

---

## Ringkasan waktu
| Slide | Detik |
|---|---|
| 1 Hook | 20 |
| 2 Energy gap | 30 |
| 3 Pengguna | 30 |
| 4 Demo (naskah) + demo langsung | 30 + [ISI: durasi demo yang diizinkan panitia] |
| 5 Hasil vs baseline | 30 |
| 6 Pembanding | 30 |
| 7 Bisnis | 30 |
| 8 Dampak | 30 |
| 9 Roadmap | 30 |
| 10 Tim | 30 |
| **Total naskah** | **±4 menit 50 detik** |

Batas waktu pitch resmi: `[ISI: dari panitia]`. Kalau hanya 3 menit, gabungkan slide 6+7 dan 8+9, dan potong naskah slide 3.

## Cek sebelum Demo Day
- [ ] Slide 3 berisi hasil wawancara asli, atau versi "sedang berjalan". Tidak ada persona simulasi.
- [ ] Kolom RMS + gerbang di slide 5 tetap ditebalkan. Jangan menghapus baseline yang menang.
- [ ] Tidak ada kalimat "RMS tidak punya skor keyakinan", "nilai tambah AI ada di abstain", atau "AI kami tahu kapan harus diam" di slide, naskah, maupun video.
- [ ] Tidak ada "deteksi dini" atau "AI menangkap tahap awal". Angka 0,971 selalu disebut bersama "armada 2/3 bermasalah" dan angka 3/22–5/22.
- [ ] Label [SKENARIO] terlihat dari kursi belakang di slide 8.
- [ ] Demo langsung sudah dicoba di laptop presentasi; video cadangan siap offline.
- [ ] Semua `[ISI]` terisi atau dihapus.
- [ ] Jawaban Q&A di `10_QNA.md` sudah dilatih, terutama Q20 ("AI kalah dari RMS"), Q21, Q25, Q26, dan Q31 (SKAB gagal).
- [ ] Hasil SKAB muncul di slide 5 (kotak) dan slide 9 sebagai **GAGAL**. Tidak ada "TKT 4" untuk SKAB, dan tidak ada "AI membedakan katup vs aus" sebagai hasil.
- [ ] Angka tes = 54 (`prototype\results\pytest_output.txt`).
