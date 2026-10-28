# 03b_ADVOKAT_SETAN: alasan top 3 bisa KALAH
### Agen A5 "Advokat Setan" (reviewer skeptis, pemegang veto J4) · 28 Okt 2026 · Seno Hackathon ITS 2026

**Dasar:** `07-MEGA-PROMPT-ITS-HACKATHON-28okt2026.md` (§A, §C), `03-MEGA-PROMPT-JURI-90.md`, `01_INVENTARIS_ASET.md`, `02_BRAINSTORM.md`, ditambah pengecekan langsung kode di repo dan pencarian web (§7).

**Aturan baca:**
- Tugas dokumen ini mencari alasan ide **kalah**. Kelebihannya sudah ditulis di `02_BRAINSTORM.md` dan tidak diulang di sini.
- **Persona = [SIMULASI PERSONA, bukan data wawancara].** Persona dipakai untuk menebak keberatan, bukan sebagai bukti. Jangan dikutip di berkas pendaftaran.
- Setiap klaim eksternal diberi status: **[dibuka]** berarti halaman/PDF benar-benar dibuka dan teksnya dibaca; **[cuplikan]** berarti hanya dari ringkasan hasil pencarian, belum diverifikasi, dan **tidak boleh dikutip sebagai fakta** sebelum dibuka.
- Angka yang tidak ketemu ditulis `[ISI: …]`.

---

## 0. Vonis ringkas

| Ide | Vonis | Alasan kalah utama (1 kalimat) | Pertanyaan juri paling mematikan |
|---|---|---|---|
| **E5 DetakMesin** | **LANJUT DENGAN SYARAT (berat)** | Dataset CWRU sudah jenuh dan rawan bocor, kode FaceVitals yang bisa dipakai ulang hanya DSP buku teks, dan rantai "deteksi fault → hemat kWh" tidak didukung bukti yang konsisten. | "Akurasi Anda pakai split apa, dan mana bukti fault yang Anda deteksi menaikkan kWh?" |
| **E2 TagihanJujur** | **BUNUH** | Bank Indonesia sudah menyediakan Kalkulator Hijau **gratis** untuk UMKM, lengkap dengan Scope 2 listrik PLN dan faktor emisi nasional. Perhitungannya cuma kWh × faktor, jadi AI tidak perlu dan tidak ada mekanisme hemat energi. | "BI sudah memberi ini gratis. Kenapa ada yang mau membayar Anda?" |
| **E15 TagihanIndustri** | **BUNUH sebagai ide berdiri sendiri** (boleh jadi fitur) | Denda kVARh bisa dicek dengan satu rasio kVARh/kWh. LLM di sini hanya OCR mahal, dan dampaknya lebih ke rupiah daripada kWh. | "Rumus ini muat di satu sel Excel. AI-nya di mana?" |
| **E3 JadwalDingin** | **LANJUT DENGAN SYARAT** | Skripsi Teknik Elektro **UKWMS Surabaya (2026)** sudah memutus daya ruang kelas berdasarkan jadwal dan melaporkan hemat 34,09 % **tanpa AI**. Sudut "jadwal = sensor" tidak baru, bahkan di kota tuan rumah. | "Pemutusan berbasis jadwal sudah hemat 34 % tanpa AI. Berapa kWh tambahan dari AI Anda?" |
| *(di luar top 3)* **E1 LautHemat** | Naikkan jadi **penantang/cadangan** | Klaim TKT-nya paling bisa dipertahankan karena aset dan AI barunya ada di domain yang sama (§5). | — |

**Temuan paling penting untuk orkestrator:**
1. **Tidak ada satu pun aset yang sudah punya AI TKT ≥3 di domain energi.** Semua top 3 memulai komponen AI energinya dari TKT 1–2 (§1).
2. Angka andalan E5 (IEA 4E: motor 45 % listrik dunia, potensi 20–30 %) berasal dari dokumen tentang **standar efisiensi (MEPS)**, bukan predictive maintenance. Kalau dipakai untuk membenarkan deteksi fault, juri energi akan menganggapnya salah atribusi (§2.3).

---

## 1. Masalah lintas ide: klaim TKT dari aset yang dipivot

Syarat lomba (dicek ulang di https://hackathon-its.id/ **[dibuka]**): purwarupa AI atau desain awal berbasis AI harus sudah di **TKT 3–6** saat daftar. Situs tidak memuat tenggat, rubrik, maupun aturan orisinalitas.

| Aset | TKT terverifikasi (`01_INVENTARIS_ASET.md`) | Berlaku untuk | TKT jujur untuk ide energi **hari ini** | Alasan |
|---|---|---|---|---|
| FaceVitals | 4 | HR dari video wajah | **E5: 1–2** | Dicek langsung di kode. Metode inti (`facevitals/signal/methods.py`: GREEN/CHROM/POS/PBV) adalah proyeksi kanal **RGB kulit** dan tidak berlaku untuk getaran. Pita frekuensi `band=(0.7, 3.0)` Hz tertanam di `methods.py`, `quality.py`, dan `vitals/hr.py`. Bagian yang bisa dipakai ulang (`viterbi_track`, `spectral_snr`, `psd`, `bandpass`) adalah DSP umum; seluruh `signal/` + `hr.py` hanya 784 baris. **Belum pernah dijalankan pada satu pun sinyal getaran/arus.** |
| Kendali | 4 (sistem) / 3 (LLM, stub) | Invoice treasury EN/ID | **E2/E15: 2** · **E3: 1** | `kendali/invoices.py::read_text` hanya membaca **PDF ber-teks (pypdf) atau file teks**. **Tidak ada OCR gambar**, jadi "foto struk" adalah komponen baru. LLM asli belum pernah diukur (`LLM_SCORECARD.md`: "No real model has been run yet"). Kolom invoice (vendor, total, tanggal, alamat bayar) berbeda dari kolom tagihan PLN (ID pelanggan, golongan, daya, kWh LWBP/WBP, kVARh). Untuk E3, mesin kebijakan Kendali hanya bersinggungan secara konsep. |

**Konsekuensi:**
- Menulis "TKT 4" di berkas E5/E2/E3 karena asetnya TKT 4 = **fatal flaw J4** ("klaim TKT tanpa bukti", plafon 80).
- Formulasi yang jujur: "Komponen X (DSP/ekstraksi) TKT 4 di domain asal. Komponen AI untuk kasus pakai ini mencapai TKT 3 pada [tanggal], dengan bukti [file hasil]."
- Klaim TKT 3 itu baru sah setelah eksperimennya **benar-benar dijalankan** sebelum daftar.

---

## 2. E5 DetakMesin

### 2.1 Generik?
- **CWRU adalah dataset paling jenuh di bidang ini.**
  - Rosa, Braga & Silva menyebutnya "standard reference for testing new algorithms" (https://arxiv.org/html/2407.14625v1 **[dibuka]**).
  - Makalah yang sama menyebut split umum CWRU **bocor** dan menghasilkan hasil "overoptimistic … nearly 100% accuracy". Mereka mengutip Hendriks dkk.: CNN yang mencapai 95 % saat dibagi per beban turun ke **53 %** saat dibagi per ukuran fault.
  - Vieira dkk. 2025 (https://arxiv.org/html/2509.22267v1 **[dibuka]**) mengutip tinjauan yang menemukan **40 dari 41** studi CWRU memakai desain yang rentan bias kemiripan ini.
  - Jumlah total paper CWRU: **tidak ketemu angka bersumber** `[ISI]`. Patokan Smith & Randall, *MSSP* 64–65 (2015), hanya diketahui dari **[cuplikan]**.
  - **Artinya:** juri J1 yang paham bidang ini akan langsung bertanya soal split. Angka 99 % di CWRU justru jadi tanda bahaya.
- **Produk komersial sudah ada, termasuk di Indonesia:**
  - **ABB Ability Smart Sensor** menempel di rangka motor, membaca getaran + suhu, dan diklaim memangkas energi "hingga 10 %" **[cuplikan]**; halaman ABB timeout saat dibuka. Ini klaim vendor.
  - **Groundup.ai** memasarkan pemantauan getaran/akustik/arus motor untuk pabrik Indonesia (https://groundup.ai/resources/blog/iot-predictive-maintenance-indonesia-plants **[dibuka]**; pelanggan Indonesia tidak disebut).
  - **Nanoprecise** dan **TMEIC TMASMS** (pengiriman pertama 25 unit ke pabrik kertas Indonesia) **[cuplikan]**.
  - **Artinya:** "sensor murah + AI untuk motor" bukan celah pasar. Satu-satunya pembeda adalah cerita asal-usul rPPG, dan itu cerita tim, bukan nilai bagi pengguna.

### 2.2 AI tidak perlu?
- Untuk bantalan, analisis envelope + frekuensi karakteristik (BPFO/BPFI dari geometri) adalah metode klasik. Ambang tingkat getaran juga sudah distandarkan `[ISI: cek nomor standar ISO yang berlaku]`. Kalau model AI tidak mengalahkan **baseline envelope-FFT dengan split yang tidak bocor**, J4 akan menyebut AI-nya tempelan.
- Pelacak Viterbi + abstain SNR dari FaceVitals berguna untuk **melacak satu frekuensi dominan** seperti kecepatan poros. Klasifikasi jenis fault tidak membutuhkannya. Jadi kontribusi aset ke inti AI kecil.

### 2.3 Klaim energi masuk akal?
**Ini titik terlemah E5.**
- **S4 (IEA 4E) salah dipakai.**
  - PDF-nya sudah diekstrak dan dicari (https://www.iea-4e.org/wp-content/uploads/2020/12/PGmdu_oct2016.pdf **[dibuka]**). Kalimat sumbernya: motor menyumbang "45 % of the world's total electricity consumption" dan "new and existing technologies offer the potential to reduce … by 20 % to 30 %".
  - Dokumen itu membahas **MEPS / unit penggerak motor** (efisiensi motor, pompa, kipas, sistem). Kata "maintenance" dan "misalign" **tidak muncul** di teksnya.
  - **Jangan** menautkan 20–30 % ke deteksi fault.
- **Bukti fault → kWh tidak konsisten:**
  - Tesis S. Jesse, Univ. Tennessee 2001, *The effects of shaft misalignment on efficiency and bearing load of electric motors* (https://trace.tennessee.edu/utk_gradthes/9649 **[dibuka]**): **"no significant correlation between misalignment and efficiency"** selama kopling dalam rentang rekomendasi pabrikan.
  - Studi motor DC 250 kW di pabrik baja melaporkan hingga 13 % **[cuplikan, halaman 403]**, tetapi hanya satu motor di satu pabrik. Angka 9–17 % dari Ludeca/Reliabilityweb adalah materi vendor alignment **[cuplikan]**.
- **Tuas hemat energi motor yang nyata adalah ukuran motor dan pengendalian kecepatan.**
  - Fact sheet DOE *Determining Electric Motor Load and Efficiency* (https://www.energy.gov/sites/prod/files/2014/04/f15/10097517.pdf **[dibuka]**): efisiensi motor "tends to decrease dramatically below about 50% load".
  - Fact sheet yang sama juga menulis "The slip method is generally not recommended for determining motor loads in the field". Metode yang disarankan adalah ukur kW input atau arus.
  - **Artinya:** pivot "pelacak frekuensi untuk estimasi slip → beban" yang terdengar pas dengan aset FaceVitals justru tidak dianjurkan DOE. Clamp meter/power meter sudah cukup tanpa AI.
- **Kesimpulan:** dengan data yang ada, E5 adalah **predictive maintenance (downtime/biaya)**, bukan efisiensi energi. Kritik J2 di brainstorm ("ini PdM, bukan energi") **benar** dan belum terjawab.

### 2.4 Data tersedia & legal?
- **Paderborn:** lisensi CC BY-NC 4.0 **[cuplikan]**; halaman resmi 404 saat dibuka. Non-komersial, jadi boleh untuk purwarupa tetapi **tidak boleh dijual** tanpa izin. Ini penting untuk juri investor.
- **CWRU:** **lisensi/terms of use tidak ditemukan** `[ISI: cek halaman Bearing Data Center CWRU]`.
- **Data motor lokal:** tidak ada. Rekaman lab ITB butuh izin lab dan alat (akselerometer + DAQ + power meter) `[ISI: ketersediaan]`.

### 2.5 Siapa bayar?
- Pembayar "pabrik" masuk akal untuk downtime, tetapi harus bersaing dengan vendor di §2.1 yang sudah punya perangkat keras, sertifikasi, dan layanan.
- PDAM membayar kWh/m³, tetapi keputusan pembelian ada di direksi/BUMD, dengan siklus anggaran tahunan `[ISI: validasi]`.

### 2.6 Risiko klaim TKT
- Lihat §1: **TKT hari ini 1–2.**
- TKT 3 jujur = pipeline getaran berjalan di CWRU/Paderborn **dengan split tanpa bocor (per bearing/ukuran fault)** + baseline envelope-FFT + angka di file hasil.
- TKT 4 butuh minimal satu rekaman motor nyata. TKT 5 butuh motor di lingkungan pengguna (pabrik/PDAM).

### 2.7 Risiko orisinalitas
**Rendah.** SP Cup tidak didaftar; pemilik FaceVitals adalah Poggy + Aziz, keduanya ada di tim (`01_INVENTARIS_ASET.md`).

### 2.8 Bisa dibangun jujur sebelum ~1 Nov?
- **TKT 3 di dataset publik: mungkin** (2 hari kerja fokus), dengan catatan hasil jujur dengan split ketat bisa jauh dari 99 % (pembanding: 53 % pada contoh Hendriks).
- **Bukti kWh: tidak mungkin sebelum 1 Nov.** Butuh motor + power meter + fault terinduksi.
- Bentrok IBSC 1 Nov (`02_BRAINSTORM.md`).

### 2.9 Persona pengguna
- **[SIMULASI PERSONA, bukan data wawancara] Kepala maintenance pabrik pakan, SIER Rungkut:** "Sensor getaran sudah pernah ditawarkan vendor, lengkap dengan dasbor. Masalah saya bukan kurang alarm. Masalah saya izin downtime untuk ganti bearing. Hemat listrik? Tagihan listrik dihitung per pabrik, jadi saya tidak bisa melihat efek satu motor. Kalau Anda bilang motor 3 boros 5 %, buktikan pakai kWh meter, bukan grafik."
- **[SIMULASI PERSONA, bukan data wawancara] Operator rumah pompa PDAM:** "Pompa kami jalan 24 jam. Saya tidak boleh menempel alat di aset tanpa surat dari direksi, dan data SCADA tidak boleh keluar. Yang dihitung atasan saya kWh per meter kubik, bukan 'kondisi bearing'. Kalau alat Anda tidak bicara kWh/m³, tidak akan dibaca."

### 2.10 Vonis: **LANJUT DENGAN SYARAT (berat)**
Syarat (semua wajib; kalau syarat 3 gagal sebelum Demo Day, turunkan E5 ke cadangan):
1. **Hapus** S4 sebagai pembenaran hemat energi PdM. Pakai S4 hanya sebagai konteks ("motor = 45 % listrik dunia"), dan tulis terang bahwa 20–30 % berasal dari langkah efisiensi sistem, bukan dari deteksi fault.
2. **Split tanpa bocor** (per ukuran fault/bearing, mengikuti Hendriks/Rosa dkk.) + baseline envelope-FFT. Laporkan angka apa adanya.
3. **Satu eksperimen kWh nyata:** motor lab dengan power meter, induksi unbalance/misalignment, ukur kW sebelum/sesudah. Ini bukti yang membedakan E5 dari ±50 tim lain, dan juga satu-satunya jalan ke TKT 4. `[ISI: akses lab mesin listrik ITB/ITS]`
4. **Geser KPI** ke metrik energi yang langsung diukur pengguna, mis. kWh/m³ pompa (PDAM). Ganti cerita "detak motor" menjadi "detak yang dihubungkan ke kWh".
5. Klaim di berkas: "DSP TKT 4 (domain HR); komponen AI getaran TKT 3 di data publik". Bukan TKT 4.

### 2.11 Pertanyaan juri paling mematikan + jawaban jujur terbaik
> **J1:** "Akurasi Anda di CWRU memakai split apa? Kalau per ukuran fault, berapa? Lalu tunjukkan bukti bahwa fault yang Anda deteksi menaikkan kWh."

**Jawaban jujur:** "Kami sengaja tidak memakai split per beban karena literatur menunjukkan split itu bocor. Dengan split per ukuran fault, akurasi kami [ISI: angka dari eksperimen] terhadap baseline envelope-FFT [ISI]. Untuk energi, literaturnya tidak konsisten. Tesis Tennessee tidak menemukan korelasi signifikan selama misalignment masih dalam toleransi. Karena itu kami mengukurnya sendiri di motor lab: [ISI: ΔkW terukur] atau, kalau belum, 'belum terukur, itu target TKT 4 kami bulan November'."

---

## 3. E2 TagihanJujur (+ E15 TagihanIndustri)

### 3.1 Generik? **Ya, dan pesaingnya gratis dari bank sentral.**
- **Kalkulator Hijau, Bank Indonesia + Kemenko Marves.** FAQ resmi (https://www.bi.go.id/id/fungsi-utama/stabilitas-sistem-keuangan/Keuangan-Hijau/Documents/FAQ_Kalkulator_Hijau.pdf **[dibuka, teks diekstrak]**):
  - alat penghitung emisi GRK berbasis smartphone yang "gratis";
  - pengguna "perbankan dan pelaku usaha termasuk UMKM";
  - "Scope 2: Emisi dari pemakaian listrik yang berasal dari Perusahaan Listrik Negara (PLN)", memakai faktor emisi nasional;
  - bisa dipakai sejak **2 Oktober 2024**;
  - manfaat yang disebut termasuk akses pendanaan hijau, yaitu persis pembayar yang diandalkan E2.
- **Panduan UKMIndonesia.id** (25 Agu 2026, https://ukmindonesia.id/baca-deskripsi-posts/tagihan-listrik-dan-gas-membengkak-ini-cara-umkm-menghitung-jejak-emisi-dan-energi-bisnisnya **[dibuka]**) sudah mengarahkan UMKM ke Jejakkarbonku.id, GHG Emissions Calculator, dan Kalkulator Hijau. Input Scope 2 cukup kWh tahunan dari tagihan.
- **PLN Mobile** punya fitur Catat Meter/SwaCAM: foto stand meter → estimasi tagihan (https://listrikindonesia.com/detail/8775/layanan-baca-meter-mandiri-di-pln-mobile-bantu-pelanggan-pantau-penggunaan-listrik **[dibuka]**, artikel 2021). Jadi "foto → angka listrik" juga sudah dimiliki PLN.
- **Ekstraksi tagihan utilitas** sudah jadi produk global. Arcadia melakukan OCR + ekstraksi kolom (pemasok, ID akun, periode, konsumsi, satuan) dan mencantumkan **bahasa Indonesia** di "provider coverage extension (without OCR)" (https://docs.arcadia.com/docs/uploaded-bills-processing **[dibuka]**). Klippa, Affinda, dan LlamaParse juga memasarkan OCR tagihan **[cuplikan]**.

### 3.2 AI tidak perlu? **Ya.**
- Struk token prabayar dan tagihan pascabayar sudah mencetak kWh. Emisi = kWh × faktor (S2), yaitu satu perkalian. Panel juri internal Kendali sendiri sudah mencatat risiko "AI hanya hiasan".
- Klaim di persona brainstorm, *"freezer Anda boros cukup dari foto struk"*, **mustahil secara teknis**. Satu angka total bulanan tidak bisa dipecah per alat; itu butuh NILM (E10) dan sensor. Kalau klaim ini masuk berkas, J4 akan memveto.
- Tambahan untuk prabayar: **pembelian token ≠ konsumsi** pada periode yang sama, sehingga deret kWh dari struk pun bias.

### 3.3 Klaim energi masuk akal? **Tidak ada mekanisme.**
Hasilnya laporan dan "kesadaran". Tidak ada aktuator, tidak ada rekomendasi yang bisa diturunkan dari data tagihan selain "pemakaian naik/turun". Checklist panitia "Define the Energy Gap" dan "efficiency gains" tidak terpenuhi.

### 3.4 Data & legal
- Tagihan berisi nama, ID pelanggan, dan alamat, sehingga terkena aturan data pribadi `[ISI: pasal UU PDP yang relevan + URL]`. Butuh persetujuan tertulis untuk 20–30 tagihan uji.
- Untuk E15 (pelanggan besar), PLN sudah memasang AMR pada hampir 250 ribu pelanggan, dan tambah daya di atas 33 kVA langsung memakai AMR (Republika, 10 Sep 2020, https://ekonomi.republika.co.id/berita/qgfgad370/250-ribu-meteran-listrik-sudah-terdigitalisasi **[dibuka]**). Data beban segmen ini sudah tercatat di PLN. Nilai tambah membaca PDF tagihannya kecil.

### 3.5 Siapa bayar?
- **UMKM:** alternatif gratis sudah tersedia (BI).
- **Bank hijau:** sudah punya Kalkulator Hijau dan pedoman OJK `[cuplikan: Buku 3 Metode Perhitungan Emisi Karbon CRMS OJK 2024]`.
- **Pembeli ekspor yang meminta data pemasok:** `[ISI]`, belum ada bukti.
- **E15:** vendor kapasitor bank/ESCO (lead generation) adalah pembayar paling jelas di antara semua opsi. Tetapi persona brainstorm sendiri menyebut vendor kapasitor "sudah sering datang menawarkan hal yang sama".

### 3.6 E15: denda kVARh
- Aturan: biaya kVARh dikenakan bila faktor daya rata-rata bulanan < 0,85; di Kepmen 1772/2001 berarti kVARh > 0,62 × kWh **[cuplikan]**, dirujuk ke Kepmen ESDM 1616/2003 dan Permen ESDM 7/2024.
- Halaman Permen ESDM 7/2024 di pasal.id **[dibuka]** mengonfirmasi judulnya ("Tarif Tenaga Listrik Yang Disediakan Oleh PT PLN"), tetapi **pasal kVARh tidak tampil** di teks ekstraksi `[ISI: buka lampiran resmi di JDIH ESDM/BPK]`.
- Logika deteksinya `kVARh_tercatat > 0,62 × kWh`, cukup satu sel Excel. Sizing kapasitor juga rumus baku. **AI tidak dibutuhkan.**
- Dampak: perbaikan faktor daya terutama menghapus **denda rupiah**. Penurunan kWh hanya dari rugi jaringan di sisi pelanggan `[ISI: angka bersumber]`. J1 akan memisahkan rupiah dari kWh.

### 3.7 Risiko TKT & orisinalitas
- TKT tagihan hari ini **2** (§1). OCR foto belum ada. LLM asli belum pernah diukur.
- **Kendali sedang di FinTechathon** (pengumuman finalis ≤31 Okt, final 20–23 Nov).
  - IP tetap milik peserta, dan tidak ditemukan larangan pakai ulang (`01_INVENTARIS_ASET.md`).
  - Situs ITS tidak menyebut aturan orisinalitas **[dibuka]**.
  - Risikonya **reputasi + waktu**: tim yang sama, dua final yang berdekatan, dan juri yang bisa melihat repo/Devpost lomba lain. Wajib diungkapkan.

### 3.8 Bisa dibangun jujur sebelum deadline?
Secara teknis bisa: ekstraksi + aturan dalam 1–2 hari setelah ada 20–30 tagihan dengan izin dan API key LLM. Tetapi yang terbangun adalah **produk yang sudah ada gratis**, sehingga cepat dibangun tidak menolong.

### 3.9 Persona pengguna
- **[SIMULASI PERSONA, bukan data wawancara] Pemilik usaha keripik, Sidoarjo (E2):** "Struk token saya sudah ada angka kWh-nya, dan di PLN Mobile juga ada. Kalau bank minta laporan emisi, saya diarahkan ke aplikasi BI yang gratis. Aplikasi Anda bilang listrik saya naik? Saya sudah tahu dari dompet. Yang saya mau itu caranya turun, dan foto struk tidak bisa memberi tahu itu."
- **[SIMULASI PERSONA, bukan data wawancara] Chief engineer hotel, Surabaya (E15):** "Faktor daya kami dijaga kapasitor bank, dan vendornya audit gratis setiap tahun. Tagihan dipegang bagian keuangan dan berisi data pelanggan, jadi saya tidak akan mengunggahnya ke aplikasi mahasiswa tanpa persetujuan GM. Kalau dendanya memang ada, saya cukup lihat satu baris di tagihan."

### 3.10 Vonis
- **E2: BUNUH.** Pesaing gratis dari regulator, AI tidak perlu, dan tidak ada mekanisme hemat.
- **E15: BUNUH sebagai ide berdiri sendiri.** Boleh disimpan sebagai **fitur pelengkap** (mis. modul "cek denda" di ide gedung/E3), tanpa diklaim sebagai inti AI.
- **Satu-satunya cara E2 hidup lagi** (tidak disarankan, hanya dicatat): pivot ke "verifikasi dokumen emisi UMKM untuk bank" dengan bukti bahwa input manual Kalkulator Hijau menjadi hambatan nyata `[ISI: wawancara bank/UMKM]`. Itu tetap bukan energy gap.

### 3.11 Pertanyaan juri paling mematikan + jawaban jujur terbaik
> **J3:** "Bank Indonesia sudah memberi Kalkulator Hijau gratis untuk UMKM, dengan Scope 2 PLN dan faktor emisi nasional. Kenapa ada yang mau membayar Anda, dan berapa kWh yang dihemat?"

**Jawaban jujur:** "Untuk menghitung emisi, tidak ada alasan membayar kami. Kalkulator BI sudah cukup. Nilai tambah kami hanya mengurangi input manual dan memeriksa konsistensi dokumen, dan kami belum punya bukti ada yang mau membayar untuk itu [ISI]. Kami juga belum bisa menunjukkan kWh yang dihemat, karena alat kami tidak mengubah pemakaian." Jawaban sejujur ini sekaligus menunjukkan kenapa ide ini dibunuh.

---

## 4. E3 JadwalDingin

### 4.1 Generik? **Ya, dan contohnya ada di Surabaya.**
- **S-CLASS**, skripsi Teknik Elektro **Universitas Katolik Widya Mandala Surabaya**, 2026 (V. H. Budiarto; https://repositori.ukwms.ac.id/47418/10/ABSTRAK.pdf **[dibuka, abstrak diekstrak]**):
  - ESP32-S3 + Home Assistant + IR blaster, memutus daya otomatis saat jadwal peminjaman berakhir;
  - "Implementasi pemutusan daya berbasis jadwal terbukti menghemat energi sebesar 34,09%" (paired t-test p = 0,0252);
  - override suhu AC 24 °C;
  - **tanpa AI.**
- **Politeknik Negeri Medan / Universitas Medan Area, 2025** (Saleh & Azmi, *Jurnal Mahajana Informasi* 10(2), https://e-journal.sari-mutiara.ac.id/index.php/7/article/view/6313 **[dibuka]**): penjadwalan ESP32 di ruang kuliah, 20,5 → 18,5 kWh/hari (**9,8 %**).
- **SRT Labs (AS, vendor):** audit jadwal kuliah satu semester di 4 gedung. Ruang kosong **81 %** dari jam yang dikondisikan; penyetelan BAS dari kelas pertama sampai kelas terakhir menghemat rata-rata **72,48 % waktu** (https://srtlabs.com/2023/07/03/academic-schedule-review-for-energy-savings-potential/ **[dibuka]**; studi kasus vendor).
- Studi Korea (pemutusan pendinginan ruang kosong, 30–60 %) dan Brunel/Fukuoka **[cuplikan]**.
- **Artinya:** "jadwal kuliah = sensor okupansi gratis" adalah **ide yang sudah dipublikasikan**. Juri ITS bisa saja mengenal karya dari kampus tetangga.

### 4.2 AI tidak perlu? **Untuk inti yang diusulkan, ya.**
- Jadwal → ON/OFF adalah aturan, dan S-CLASS membuktikannya tanpa AI.
- "Ekstraksi jadwal dari PDF berantakan" adalah **masalah buatan**. Kampus menyimpan jadwal di sistem informasi akademik dalam bentuk basis data `[ISI: konfirmasi format ekspor dari Sarpras/Direktorat Pendidikan ITB/ITS]`. Kalau Sarpras memberi ekspor CSV, LLM tidak berperan.
- Satu-satunya peran AI yang sah adalah **selisih antara jadwal dan okupansi nyata** (kelas batal/pindah, ruang dipakai di luar jadwal) serta **pre-cooling optimal**. Keduanya butuh **data okupansi berlabel** dan data suhu ruang, dan **tim belum punya** `[ISI]`.

### 4.3 Klaim energi masuk akal? **Ya, mekanismenya nyata, tetapi milik aturan, bukan AI.**
- AC mati di ruang kosong menghemat kWh secara fisik. Ini yang terkuat di antara ketiga ide.
- Masalahnya, penghematan terbesar (34 % pada S-CLASS) sudah dicapai baseline tanpa AI. **Kontribusi AI = kWh di atas baseline jadwal**, dan angka ini belum ada.
- AC split ruang kelas umumnya dikendalikan remote tanpa BMS `[ISI: inventaris AC gedung kuliah]`, sehingga eksekusinya butuh perangkat keras per ruang (IR blaster/relai), anggaran, dan izin Sarpras.

### 4.4 Data & legal
- Jadwal ruang: data internal kampus, perlu izin.
- Data okupansi kamera/wifi menyentuh privasi mahasiswa `[ISI: kebijakan kampus/UU PDP]`.
- Data kWh gedung: `[ISI: Sarpras]`.

### 4.5 Siapa bayar?
Kampus. Tetapi listrik dibayar universitas secara terpusat, bukan oleh unit pengguna ruang, sehingga insentif di tingkat pengelola gedung lemah `[ISI: validasi skema anggaran listrik ITB/ITS]`. ESCO bagi-hasil masuk akal hanya kalau ada baseline meter.

### 4.6 Risiko TKT
- **Hari ini TKT 1** (tidak ada kode, tidak ada data). Brainstorm memberi skor TKT 3, dan itu **terlalu optimistis**.
- TKT 3 jujur minimal butuh: data jadwal nyata satu gedung + model okupansi/kelas batal yang diuji terhadap label (mis. observasi manual satu minggu) + baseline "aturan jadwal ala S-CLASS".

### 4.7 Risiko orisinalitas
- Pakai ulang mesin kebijakan Kendali menyeret risiko FinTechathon (§3.7), padahal manfaatnya kecil. **Lebih aman tulis dari nol.**
- Wajib **menyitasi S-CLASS** sebagai karya terdahulu. Kalau tidak disitasi dan juri tahu, itu tampak seperti klaim kebaruan palsu.

### 4.8 Bisa dibangun jujur sebelum ~1 Nov?
**Tidak untuk TKT 3.** Data jadwal + label okupansi tidak bisa dikumpulkan dalam 4 hari tanpa izin Sarpras. Kalau deadline ternyata ≥2 minggu lagi, baru realistis.

### 4.9 Persona pengguna
- **[SIMULASI PERSONA, bukan data wawancara] Teknisi Sarpras gedung kuliah:** "AC di kelas pakai remote, jadi tidak ada BMS yang bisa disambung. Memasang alat di seratus ruang butuh anggaran dan surat dari atasan. Jadwal ada di sistem, saya bisa minta ekspornya. Yang saya takutkan: AC mati saat dosen masih mengajar karena kuliahnya molor. Yang dimarahi saya."
- **[SIMULASI PERSONA, bukan data wawancara] Kepala unit sarana fakultas:** "Listrik dibayar universitas, bukan fakultas, jadi hemat 30 % tidak masuk ke anggaran saya. Kalau mau dipasang, tunjukkan dulu satu ruang selama sebulan dengan kWh meter. Oh, kampus sebelah sudah punya sistem pemutus jadwal? Lalu kenapa saya perlu AI?"

### 4.10 Vonis: **LANJUT DENGAN SYARAT**
Syarat:
1. **Baseline wajib = aturan jadwal ala S-CLASS** (disitasi). Klaim AI hanya untuk **kWh tambahan di atas baseline itu** (kelas batal, ruang di luar jadwal, pre-cooling).
2. **Buang** narasi "LLM membaca PDF jadwal berantakan", kecuali Sarpras memang hanya bisa memberi PDF `[ISI]`.
3. Minimal **satu ruang** dengan kWh meter + log okupansi (observasi manual pun boleh) **sebelum** mengklaim angka hemat.
4. Tulis TKT jujur (1–2 hari ini). Jangan daftar dengan klaim TKT 3 sebelum syarat 3 punya hasil.
5. Kalau deadline benar 1 Nov: E3 **tidak siap**. Jadikan roadmap.

### 4.11 Pertanyaan juri paling mematikan + jawaban jujur terbaik
> **J2:** "Skripsi UKWMS di Surabaya tahun ini sudah memutus daya berdasarkan jadwal dan hemat 34 % tanpa AI. Berapa kWh tambahan dari AI Anda, dan di mana datanya?"

**Jawaban jujur:** "Betul, pemutusan berbasis jadwal tidak butuh AI, dan itu baseline kami. AI kami hanya menangani selisih antara jadwal dan pemakaian nyata: kelas batal, ruang dipakai di luar jadwal, dan pendinginan awal. Di ruang uji kami, selisih itu [ISI: jam AC menyala tanpa penghuni setelah aturan jadwal] dan AI menambah hemat [ISI]. Kalau angkanya belum ada, kami katakan belum terukur."

---

## 5. Apakah ada ide lain di `02_BRAINSTORM.md` yang lebih kuat?

**Tidak ada yang jelas unggul di semua kriteria.** Tetapi kalau kriteria TKT (bobot 3×) dinilai jujur seperti di §1, urutannya berubah.

### E1 LautHemat layak naik menjadi penantang/cadangan
- **TKT paling bisa dipertahankan.**
  - Pipeline OCEANS sudah TKT 4 di **data nyata yang sama** (4,45 juta matchup, LOYO).
  - Model AI prakiraan (vs baseline persistensi/klimatologi) dibangun **di atas data dan pipeline yang sama**, jadi tidak ada lompatan domain seperti rPPG→motor atau invoice→tagihan.
  - Klaim "pipeline data TKT 4, AI prakiraan TKT 3" lebih kuat daripada E5/E2/E3.
- **Pemilik tunggal (Poggy), risiko orisinalitas rendah**, dan Sustainable/Local kuat. Kenjeran ada di Surabaya; Brondong, Muncar, dan Prigi di Jatim.
- **Pesaingnya ada tetapi lemah di lapangan:**
  - PPDPI disusun BROL/KKP dan diperbarui harian **[cuplikan]**.
  - Studi IPB 2023 di PPS Cilacap (Huwaida dkk., *Albacore* 7(3), https://journal.ipb.ac.id/pspalbacore/article/view/33048 **[dibuka]**): PPDPI "belum memberikan manfaat secara nyata terhadap nelayan". Nelayan sulit mengakses dan meragukan akurasinya.
  - Ini **celah yang bisa dijelaskan**: akurasi + penyampaian, bukan sekadar "peta lagi".
- **Kelemahan tetap berat:**
  - energy gap lewat BBM bersumber dari organisasi advokasi (S5);
  - kaitan prakiraan → BBM yang dihemat butuh data trip/tangkapan `[ISI]`;
  - akses nelayan dari Bandung sulit;
  - harmonisasi QM adalah statistik baku, sehingga AI-nya harus benar-benar dibangun;
  - prakiraan 3–5 hari kerja juga sulit untuk 1 Nov.
- **Rekomendasi:** kalau deadline > 1 Nov, orkestrator sebaiknya membandingkan E1 dengan E5 secara langsung di `04_KEPUTUSAN.md`, bukan menaruh E1 di roadmap.

### E4 NafasGedung: tetap di bawah
- Dataset FDD publik ada. OpenEI submission 910 berlisensi CC BY 4.0 tetapi **disimulasikan** dengan model gedung PNNL (https://data.openei.org/submissions/910 **[dibuka]**). Data operasional LBNL 2022 lisensinya belum dicek `[ISI]`.
- Tidak ada aset sendiri (TKT 1), FDD sudah komersial, dan gedung ber-BMS AHU di Surabaya butuh perantara.

### Catatan struktural untuk orkestrator
Kalau deadline benar 1 Nov dan tim terbelah IBSC, **tidak ada ide energi yang bisa didaftarkan dengan klaim TKT ≥3 yang jujur tanpa kerja eksperimen 2+ hari penuh.** Pilihan jujurnya:
- **(a)** E5 dengan TKT 3 di data publik (split ketat), dengan klaim energi ditulis sebagai hipotesis;
- **(b)** menunda pendaftaran kalau deadline ternyata lebih longgar;
- **(c)** jalur kesehatan FaceVitals (TKT 4 HR), dengan menerima energy gap ≈ 0.

Jangan memilih E2 hanya karena paling cepat dibangun.

---

## 6. `[ISI]` paling mendesak (diurutkan berdasarkan dampak ke vonis)
1. **Deadline registrasi** (menentukan apakah E3/E1 masih mungkin).
2. **E5:** akses motor + power meter di lab ITB/ITS untuk eksperimen ΔkW; lisensi CWRU; konfirmasi lisensi Paderborn di halaman resmi.
3. **E5:** angka akurasi dengan split per ukuran fault vs baseline envelope-FFT (eksperimen sendiri).
4. **E3:** format ekspor jadwal dari Sarpras; satu ruang dengan kWh meter + log okupansi; inventaris tipe AC.
5. **E1:** data trip/BBM/tangkapan nelayan Jatim (DKP Jatim/KKP); status PPDPI terkini.
6. **E15 (kalau dipakai sebagai fitur):** pasal kVARh di lampiran resmi Permen ESDM 7/2024.
7. **Semua:** konfirmasi ke panitia ITS soal karya yang sedang ikut lomba lain (Kendali/FinTechathon).

---

## 7. Daftar sumber
### 7.1 Dibuka dan dibaca **[dibuka]**
| Sumber | URL | Dipakai untuk |
|---|---|---|
| Situs Seno Hackathon ITS | https://hackathon-its.id/ | Syarat TKT 3–6; tenggat/rubrik/orisinalitas tidak tercantum |
| Rosa, Braga & Silva, benchmark CWRU multi-label | https://arxiv.org/html/2407.14625v1 | CWRU standar; split bocor; 95 % → 53 % (Hendriks) |
| Vieira dkk. 2025, evaluasi realistis | https://arxiv.org/html/2509.22267v1 | 40/41 studi CWRU rentan bias |
| IEA 4E EMSA, Policy Guidelines MDU 2016 (teks diekstrak) | https://www.iea-4e.org/wp-content/uploads/2020/12/PGmdu_oct2016.pdf | Konteks 45 % / 20–30 % = MEPS, bukan PdM |
| Jesse 2001, tesis Univ. Tennessee | https://trace.tennessee.edu/utk_gradthes/9649 | Misalignment dalam toleransi: tidak ada korelasi signifikan dengan efisiensi |
| DOE fact sheet, *Determining Electric Motor Load and Efficiency* (teks diekstrak) | https://www.energy.gov/sites/prod/files/2014/04/f15/10097517.pdf | Efisiensi turun di bawah ±50 % beban; metode slip tidak dianjurkan |
| Groundup.ai blog | https://groundup.ai/resources/blog/iot-predictive-maintenance-indonesia-plants | Pesaing PdM di pasar Indonesia |
| FAQ Kalkulator Hijau BI (teks diekstrak) | https://www.bi.go.id/id/fungsi-utama/stabilitas-sistem-keuangan/Keuangan-Hijau/Documents/FAQ_Kalkulator_Hijau.pdf | Gratis, UMKM, Scope 2 PLN, sejak 2 Okt 2024 |
| UKMIndonesia.id, 25 Agu 2026 | https://ukmindonesia.id/baca-deskripsi-posts/tagihan-listrik-dan-gas-membengkak-ini-cara-umkm-menghitung-jejak-emisi-dan-energi-bisnisnya | Kalkulator gratis yang sudah direkomendasikan ke UMKM |
| ListrikIndonesia, 24 Nov 2021 | https://listrikindonesia.com/detail/8775/layanan-baca-meter-mandiri-di-pln-mobile-bantu-pelanggan-pantau-penggunaan-listrik | PLN Mobile Catat Meter + estimasi tagihan |
| Arcadia docs | https://docs.arcadia.com/docs/uploaded-bills-processing | OCR/ekstraksi tagihan utilitas; cakupan bahasa Indonesia |
| Republika, 10 Sep 2020 | https://ekonomi.republika.co.id/berita/qgfgad370/250-ribu-meteran-listrik-sudah-terdigitalisasi | ±250 ribu AMR; >33 kVA langsung AMR |
| pasal.id, Permen ESDM 7/2024 | https://pasal.id/en/peraturan/permen/permen-esdm-no-7-tahun-2024 | Judul regulasi; pasal kVARh tidak tampil |
| Budiarto 2026, S-CLASS, UKWMS (abstrak diekstrak) | https://repositori.ukwms.ac.id/47418/10/ABSTRAK.pdf | Pemutusan berbasis jadwal, hemat 34,09 %, Surabaya, tanpa AI |
| Saleh & Azmi 2025 | https://e-journal.sari-mutiara.ac.id/index.php/7/article/view/6313 | Penjadwalan ESP32, hemat 9,8 % |
| SRT Labs 2023 | https://srtlabs.com/2023/07/03/academic-schedule-review-for-energy-savings-potential/ | 81 % jam kosong; 72,48 % waktu |
| OpenEI submission 910 | https://data.openei.org/submissions/910 | Dataset FDD AHU/RTU, CC BY 4.0, simulasi |
| Huwaida dkk. 2023, *Albacore* | https://journal.ipb.ac.id/pspalbacore/article/view/33048 | PPDPI belum memberi manfaat nyata (Cilacap) |

### 7.2 Hanya cuplikan pencarian **[cuplikan]**, belum boleh dikutip
- Smith & Randall 2015, *MSSP* 64–65 (benchmark CWRU)
- Lisensi Paderborn CC BY-NC 4.0 (mb.uni-paderborn.de; halaman 404 saat dibuka)
- Klaim ABB Smart Sensor "hingga 10 %" energi (new.abb.com; timeout saat dibuka)
- Nanoprecise, TMEIC TMASMS (pelanggan Indonesia)
- Studi motor DC 250 kW 13 % (paperity; 403 saat dibuka); angka Ludeca/Reliabilityweb
- Aturan kVARh < 0,85 / 0,62 × kWh (Kepmen 1616/2003, Kepmen 1772/2001; redirect, belum dibuka)
- Studi Korea/Brunel/Fukuoka soal kontrol HVAC berbasis jadwal
- PPDPI BROL, pembaruan harian dan aplikasi Laut Nusantara (sumber 2017)
- Buku 3 Metode Perhitungan Emisi Karbon CRMS OJK 2024

### 7.3 Pemeriksaan repo (dijalankan agen, tanpa mengubah file)
- `FaceVitals2027-SPCup_GAJADI-DAFTAR/facevitals/signal/*.py`, `vitals/hr.py`: daftar fungsi dan `band=(0.7, 3.0)`; total 784 baris (`wc -l`).
- `FinTechathon2026/kendali/kendali/invoices.py` baris 135–142: `read_text` hanya untuk PDF ber-teks/teks, tanpa OCR gambar.

*Semua persona di dokumen ini adalah simulasi agen, bukan hasil wawancara.*
