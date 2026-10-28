# 03_RISET: riset mendalam top 3 (E5 DetakMesin · E2+E15 TagihanJujur · E3 JadwalDingin)
### Agen A4 "Periset" · 28 Okt 2026 · tim: Aziz (PIC), Uqi, Pio, Poggy

**Dasar:** `07-MEGA-PROMPT-ITS-HACKATHON-28okt2026.md` (§A, §B Fase 3, §C), `01_INVENTARIS_ASET.md`, `02_BRAINSTORM.md`.

**Aturan yang dipakai di dokumen ini:**
- Setiap angka punya ID sumber `[Sx]`. Semua URL di tabel §0 **benar-benar dibuka** pada 28 Okt 2026 (halaman web atau PDF yang teksnya diekstrak). Angka dari cuplikan mesin pencari yang halamannya gagal dibuka **tidak dipakai**.
- "Hitungan sendiri" = aritmetika agen dari angka bersumber. Ditandai jelas.
- Yang tidak ketemu ditulis "tidak ketemu" atau `[ISI: ...]`.
- Tidak ada login, form, atau kontak yang dilakukan. Kontak di bawah hanya **alamat kelembagaan resmi** yang tercantum publik.
- Klaim vendor ditandai "(klaim vendor)". Tidak ada yang diverifikasi independen.

---

## 0. Daftar sumber yang dibuka

| ID | Sumber | URL | Catatan |
|---|---|---|---|
| S1 | ESDM, siaran pers 100.Pers/04/SJI/2024 (9 Feb 2024): manajemen energi 2023 | https://www.esdm.go.id/id/media-center/arsip-berita/implementasi-manajemen-energi-tahun-2023-mampu-hemat-1042-juta-sbm- | Ambang TOE per sektor menurut PP 33/2023 |
| S2 | DQS, ringkasan Permen ESDM 8/2025 Manajemen Energi | https://www.dqsglobal.com/id/wawasan/blog/permen-esdm-no-8-tahun-2025 | Sekunder (bukan teks resmi). Teks resmi: `[ISI: buka Permen ESDM 8/2025 di jdih.esdm.go.id]` |
| S3 | IEA 4E EMSA, *Policy Guidelines for Motor Driven Units Part 1*, Okt 2016 | https://www.iea-4e.org/wp-content/uploads/2020/12/PGmdu_oct2016.pdf | Teks PDF diekstrak (pdftotext) |
| S4 | Republika, 15 Jan 2024: penjualan listrik PLN UID Jatim 2023 | https://news.republika.co.id/berita/s7alry370/penjualan-listrik-di-jatim-capai-418-twh-sepanjang-2023 | Media, mengutip PLN UID Jatim |
| S5 | Kontan, 18 Jun 2025: kinerja PLN 2024 | https://industri.kontan.co.id/news/pendapatan-pln-meningkat-119-jadi-rp-545-triliun-sepanjang-tahun-2024 | Media, mengutip PLN. Statistik PLN resmi `[ISI]` |
| S6 | Indra, Rachman, Wafiyuddin, Soedjono, *JIST* 5(2), Feb 2024: efisiensi pompa IPA Ngagel I, PDAM Surya Sembada | https://jist.publikasiindonesia.id/index.php/jist/article/download/925/1599/9100 | Penulis dari ITS + PDAM Surya Sembada. Teks PDF diekstrak |
| S7 | Bisnis.com, 24 Agu 2021: Schneider, PUPR, PDAM (smart water) | https://teknologi.bisnis.com/read/20210824/84/1433657/schneider-pupr-dan-pdam-bermitra-dalam-pengelolaan-smart-water | SEC PDAM Surya Sembada |
| S8 | Mamani Duran & Mayori Machica, *Ciencia Latina* (diterima Apr 2026): konsumsi energi sistem tidak seimbang, bangku uji | https://www.ciencialatina.org/index.php/cienciala/article/download/24064/34187/ | Teks PDF diekstrak, Tabel 16 |
| S9 | Jesse, S., tesis M.S., Univ. of Tennessee, 2001: misalignment vs efisiensi motor | https://trace.tennessee.edu/utk_gradthes/9649 | Abstrak |
| S10 | Nelik, L., *Pumps & Systems*, 3 Okt 2016: daya & efisiensi pompa yang aus | https://pumpsandsystems.com/what-happens-power-efficiency-when-pump-wears-out | Kasus lapangan |
| S11 | CWRU Bearing Data Center, halaman unduh | https://engineering.case.edu/bearingdatacenter/download-data-file | Tidak ada pernyataan lisensi di halaman |
| S12 | Paderborn KAt Bearing DataCenter | https://mb.uni-paderborn.de/kat/forschung/bearing-datacenter/ | Lisensi CC BY-NC 4.0 |
| S13 | Univ. of Ottawa UORED-VAFCLS, Mendeley Data v5 | https://data.mendeley.com/datasets/y2px5tg92h/5 | Lisensi CC BY 4.0 |
| S14 | Vieira dkk., "Towards a more realistic evaluation of ML models for bearing fault diagnosis", arXiv 2509.22267 (MSSP vol. 258, 2026) | https://arxiv.org/abs/2509.22267 | Kebocoran data di benchmark bearing |
| S15 | Zhang, Zhang, Wang, Habetler, review ML/DL diagnosis bearing, IEEE Access 8 (2020) | https://arxiv.org/abs/1901.08247 | Review; CWRU dipakai sebagai benchmark perbandingan |
| S16 | BINDT, Okt 2021: Schaeffler OPTIME | https://www.bindt.org/News/October-2021/schaeffler-introduces-optime/ | Deskripsi produk (klaim vendor) |
| S17 | ITS News, 23 Okt 2023: startup Include Technology Indonesia | https://its.ac.id/news/?p=85462 | Pesaing lokal di ITS sendiri |
| S18 | Groundup.ai, 23 Apr 2026: PdM untuk pabrik Indonesia | https://groundup.ai/resources/predictive-maintenance-software-for-indonesia-factories/ | Konten vendor |
| S19 | Permen ESDM 7/2024 Tarif Tenaga Listrik PLN (salinan PDF via pasal.id) | https://pasal.id/en/peraturan/permen/permen-esdm-no-7-tahun-2024 | Lampiran III (bisnis) & IV (industri) diekstrak. Teks resmi BPK/JDIH `[ISI: cocokkan]` |
| S20 | Naibaho, *Jurnal Teknokris* 24(1), Jun 2021: kapasitor vs motor sinkron | https://jurnalteknik.unkris.ac.id/index.php/teknokris/article/download/91/85/326 | Denda kVArh bila cos φ < 0,85 |
| S21 | GEC/JCM, tabel faktor emisi CO₂ grid Indonesia (TA R4/2022) | https://gec.jp/innovation/R4/T.CO2EmissionFactor_20220406.pdf | Sumber tabel: Ditjen Gatrik ESDM, nilai FE 2019. PDF ESDM asli tidak bisa dibuka (halaman "Loading…") |
| S22 | IPCC 2006 Guidelines Vol. 2 Bab 1, Tabel 1.4 | https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_1_Ch1_Introduction.pdf | Teks PDF diekstrak |
| S23 | UU 27/2022 PDP (Wikisource) | https://id.wikisource.org/wiki/Undang-Undang_Republik_Indonesia_Nomor_27_Tahun_2022 | Pasal 4, 20, 22, 34, 67 |
| S24 | Kontan, 2 Okt 2024: BI luncurkan Kalkulator Hijau | https://nasional.kontan.co.id/news/bi-luncurkan-aplikasi-kalkulator-hijau-bantu-perbankan-hingga-industri-hitung-emisi | Pesaing gratis |
| S25 | UKM Indonesia, 25 Agu 2026: cara UMKM menghitung emisi | https://ukmindonesia.id/baca-deskripsi-posts/tagihan-listrik-dan-gas-membengkak-ini-cara-umkm-menghitung-jejak-emisi-dan-energi-bisnisnya | Menyebut kalkulator gratis |
| S26 | KrASIA, 28 Sep 2020: Jejak.in | https://www.kr-asia.com/how-jejak-in-accelerates-climate-action-with-technology-startup-stories | Pesaing lokal (data lama) |
| S27 | Arcadia, ESG & carbon management | https://www.arcadia.com/esg-and-carbon-management | Pesaing global (klaim vendor) |
| S28 | CORD (Clova AI), GitHub | https://github.com/clovaai/cord | Dataset struk Indonesia, CC BY 4.0 |
| S29 | GoodStats, 15 Jan 2025, mengutip BPS *Statistik Hotel dan Akomodasi Lainnya 2024* | https://data.goodstats.id/statistic/sepanjang-2024-jawa-timur-punya-272-hotel-baru-ZqOk6 | Sekunder dari BPS |
| S30 | BSI, CBAM 2026–2027 | https://www.bsigroup.com/en-GB/insights-and-media/insights/blogs/preparing-for-eu-cbam-the-20262027-transition-explained | Cakupan CBAM |
| S31 | IIR, 23 Agu 2024: Indonesia National Cooling Action Plan | https://iifiir.org/en/news/indonesia-unveils-its-first-national-action-cooling-plan | Mengutip UNESCAP |
| S32 | Irwangsa dkk., *Technologia* 17(3), Jul 2026: monitoring energi gedung akademik UNISKA | https://ojs.uniska-bjm.ac.id/index.php/JIT/article/download/23755/8820/64566 | Teks PDF diekstrak |
| S33 | ITS News, 30 Mar 2012: Earth Hour setiap Jumat | https://www.its.ac.id/news/its-canangkan-earth-hour-setiap-jumat/ | Biaya listrik ITS (data lama) |
| S34 | ITS News, 12 Okt 2018: ITS Smart Eco Campus | https://www.its.ac.id/news/wujudkan-its-smart-eco-campus-lewat-pengurangan-emisi-karbon/ | Biaya listrik ITS (data lama) |
| S35 | Marozas-Aliaga, disertasi RIT, 2018 | https://repository.rit.edu/theses/10158 | Jadwal registrar → HVAC, hasil terukur |
| S36 | Garland, Windham, Richardson, *Int. J. Energy Management* 6(4) (unggahan Okt 2024), Appalachian State | https://www.aeecenter.org/aee-news/case-study-evaluation-of-hvac-energy-use-resulting-from-a-room-usage-calendar-based-hvac-scheduling-tool/ | Alat jadwal berbasis kalender ruang |
| S37 | SRT Labs, 3 Jul 2023: academic schedule review | https://srtlabs.com/2023/07/03/academic-schedule-review-for-energy-savings-potential/ | Studi kasus vendor |
| S38 | Penn State FAS, Events2HVAC | https://fas.psu.edu/who-we-are/enterprise-utility-management-system/events2hvac-program | Produk/program yang sudah jalan sejak 2018 |
| S39 | Stony Brook Univ., Occupancy-Based HVAC Controls | https://www.stonybrook.edu/facilities/projects/occupancy-based-hvac-controls.html | Pilot selesai Spring 2026 |
| S40 | PNNL, Ye dkk., *Applied Energy* 293 (2021) | https://www.pnnl.gov/publications/energy-saving-potential-evaluation-primary-schools-occupant-centric-controls | Halaman tidak memuat angka |
| S41 | BDG2, GitHub + file LICENSE | https://github.com/buds-lab/building-data-genome-project-2 · https://raw.githubusercontent.com/buds-lab/building-data-genome-project-2/master/LICENSE | Lisensi CC BY-SA 4.0 (dari file LICENSE) |
| S42 | pasal.id: Permen ESDM 13/2012 | https://pasal.id/peraturan/permen/permen-esdm-no-13-tahun-2012 | Status: dicabut oleh Permen ESDM 9/2018 (menurut pasal.id) |
| S43 | ITS PPID, Direktori ITS | https://www.its.ac.id/ppid/direktori-its/ | Kontak kelembagaan |

**Gagal dibuka (angkanya tidak dipakai):** teks PP 33/2023 (PDF hasil scan, tanpa teks), HEESI 2024 (PDF >10 MB), halaman ABB Ability Smart Sensor (timeout), SKF IMx-1 di control.com (403), Smith & Randall 2015 (peeref redirect), studi motor DC 250 kW di Redalyc (berkas tidak terbaca), dataset pompa 4TU.ResearchData (server menolak koneksi), Nature *Scientific Data* ASHRAE OB Database (redirect login), DITSP ITB (domain tidak ditemukan), Renja Diskop UKM Jatim (404).

### Koreksi terhadap dokumen sebelumnya (penting)
1. **Ambang manajemen energi PP 33/2023 bukan "≥6.000 TOE untuk semua pengguna".** Menurut ESDM [S1]: penyedia energi ≥6.000 TOE/tahun, **industri ≥4.000 TOE/tahun**, transportasi ≥4.000 TOE/tahun, **bangunan gedung ≥500 TOE/tahun**.
2. **Permen ESDM 13/2012** (suhu AC 24–27 °C di gedung negara) **sudah dicabut** oleh Permen ESDM 9/2018 menurut pasal.id [S42]. Jangan dikutip sebagai aturan berlaku. `[ISI: cek isi Permen ESDM 9/2018 di JDIH ESDM]`
3. **Angka AC IIR [S31] ambigu:** artikel menyebut 79 TWh (AC gedung + rantai dingin, ±30 % listrik nasional 2020) **dan** 62 TWh (AC gedung 2020 → 241 TWh 2040). Artikel tidak menjelaskan selisihnya. Pakai keduanya dengan label masing-masing.
4. **FE Jamali 0,87 tCO₂/MWh** [S21] adalah tabel JCM yang bersumber dari **nilai FE 2019** Ditjen Gatrik ESDM, bukan angka terbaru. `[ISI: FE Jamali terbaru dari gatrik.esdm.go.id]`
5. **Potensi hemat motor 20–30 % [S3] berasal dari optimasi Motor Driven Unit (VFD, motor efisien, pencocokan beban), bukan dari deteksi gangguan.** Ini lubang utama E5 (lihat §1.1).

---

## 1. E5 DetakMesin: pelacak frekuensi FaceVitals untuk deteksi gangguan motor/pompa

### 1.1 Ukuran masalah
| Angka | Nilai | Sumber | Catatan kejujuran |
|---|---|---|---|
| Porsi sistem motor dalam listrik dunia | **45 %** (hlm. sampul dalam); di bagian lain **47 %, ±9.370 TWh/tahun**; pompa+kipas+kompresor = **70 %** dari itu | [S3] | Dua angka berbeda di dokumen yang sama |
| Potensi hemat sistem motor | **20–30 %** dengan teknologi yang ada | [S3] | Dari MDU yang dioptimasi (VFD, motor efisien, pencocokan beban). **Bukan** dari deteksi gangguan |
| Penjualan listrik PLN UID Jatim 2023 | **41,8 TWh** (TR 24,3; **TM 13,94**; TT 3,67 TWh). TM "banyak menopang sektor bisnis" | [S4] | Angka industri Jatim saja: **tidak ketemu**. `[ISI: Statistik PLN 2024, tabel per UID per kelompok]` |
| Porsi industri dalam penjualan PLN nasional 2024 | **30 %** dari 306,22 TWh | [S5] | Hitungan sendiri: ≈ 92 TWh. Artikel juga menulis "92,28 TWh" sebagai "kenaikan", yang kemungkinan besar maksudnya total |
| Biaya energi PDAM Surya Sembada 2021 | **Rp147.654.439.569**; rasio biaya energi thd biaya operasional **24,37 %**; listrik unit produksi **76 %** dari total energi PDAM; biaya energi **Rp409/m³** (rata-rata nasional Rp356,34/m³) | [S6] | Data Surabaya, ditulis bersama staf PDAM + dosen ITS |
| Efisiensi pompa terendah di IPA Ngagel I (dibangun 1922) | Pompa distribusi T1 **49,77 %**; beberapa pompa butuh rekondisi/penyetelan impeller | [S6] | Bukti bahwa degradasi pompa nyata di Surabaya. Diukur lewat audit energi manual |
| SEC PDAM Surya Sembada | **< 0,3 kWh/m³**; target jangka panjang potong biaya listrik **30 %** | [S7] | 2021 |
| Kaitan gangguan → kenaikan energi (lab) | Ketidakseimbangan rotor (massa 5–50 g, motor 1,1 kW): kenaikan **arus** 0,57–1,53 % (ringan), 2,51–3,01 % (sedang), 4,67–6,81 % (berat) | [S8] | Bangku uji kecil; yang diukur arus, bukan daya nyata. Belum tentu berlaku di motor industri |
| Kaitan misalignment → efisiensi | **Tidak ada** hubungan signifikan selama masih dalam batas pabrikan kopling (motor 50–60 HP). Umur bearing bisa turun **hingga 50 %** pada offset 5 mil | [S9] | **Kontra-bukti.** Misalignment terutama soal umur, bukan kWh |
| Kaitan keausan pompa → efisiensi (lapangan) | Celah wear-ring terbuka: efisiensi **65,2 % → 53,6 %**, daya naik 270 → 285 hp sambil debit turun 4.100 → 3.900 gpm | [S10] | Satu kasus, kolom praktisi. Jalur energi paling kuat ada di **pompa**, bukan bearing |

**Kesimpulan ukuran masalah (jujur):**
- Narasi "motor = 45 % listrik dunia" kuat sebagai konteks. Tetapi menghubungkan **deteksi bearing** ke kWh lemah: S9 bahkan menunjukkan misalignment dalam toleransi tidak menaikkan daya.
- Jalur energi yang **bisa dipertahankan**: (a) degradasi efisiensi **pompa** (S6, S10), (b) ketidakseimbangan (S8, skala lab).
- Saran: geser fokus dari "bearing CWRU" ke **"indeks efisiensi pompa dari arus motor + getaran"** dengan PDAM Surya Sembada sebagai kasus lokal.

### 1.2 Pengguna & pembayar
| Segmen | Siapa (Jatim/Surabaya) | Alternatif Bandung | Pembayar | Jalur kontak realistis | Bukti/sumber |
|---|---|---|---|---|---|
| Utilitas air | **PDAM Surya Sembada Surabaya**, khususnya IPA Ngagel | Perumda Tirtawening Bandung `[ISI: verifikasi data energi]` | PDAM (biaya energi Rp147,65 M/tahun, 24 % opex [S6]) | **Lewat penulis S6 dari ITS** (Teknik Lingkungan ITS; korespondensi lewat jurnal), lalu ke staf PDAM yang ikut menulis. Permintaan resmi lewat DIKST/LPPM ITS | [S6] |
| Industri di kawasan | Tenant SIER Rungkut/Berbek, PIER Pasuruan | Kawasan industri Bandung Raya `[ISI]` | Bagian engineering/maintenance pabrik | Lewat pengelola kawasan atau alumni. `[ISI: jumlah tenant SIER/PIER dari sier.id; angka di hasil pencarian hanya dari skripsi, tidak dipakai]` | — |
| Pengguna energi wajib manajemen energi | Industri ≥4.000 TOE/tahun, gedung ≥500 TOE/tahun [S1] | Sama | Manajer energi bersertifikat (wajib) | Lewat asosiasi manajer/auditor energi `[ISI: nama asosiasi + kontak]` | [S1], [S2] |
| Lab kampus | Lab mesin listrik ITS | Lab konversi energi ITB `[ISI: nama lab + PIC]` | — (validasi, bukan pembayar) | Dosen pembimbing tim | — |

Fakta pendukung pembayar: 410 entitas melapor manajemen energi 2023 (114 penyedia energi, 217 industri, 79 gedung), total hemat 10,42 juta SBM [S1]. Artinya ada pasar "pelapor wajib" yang butuh data efisiensi.

### 1.3 Solusi yang sudah ada & kejenuhan
**Riset (jenuh):**
| Karya | Isi | Implikasi untuk kita | Sumber |
|---|---|---|---|
| Zhang dkk. 2020, IEEE Access | Review ML/DL diagnosis bearing; membandingkan akurasi algoritma di **CWRU** | CWRU adalah benchmark standar. Akurasi tinggi di CWRU **bukan kebaruan** | [S15] |
| Vieira dkk. 2026, MSSP 258 | Split per-segmen / per-kondisi menimbulkan **kebocoran data** dan menggelembungkan metrik. Usul: split **per-bearing**. Jumlah bearing unik di data latih menentukan generalisasi. Dataset: CWRU, Paderborn, Ottawa, HUST | Wajib pakai split per-bearing. Kalau tidak, juri J1 yang paham akan menolak | [S14] |
| Smith & Randall 2015 (MSSP 64–65) | Benchmark CWRU dengan metode klasik (envelope, spectral kurtosis, cepstrum) | Baseline klasik sudah kuat. Halaman gagal dibuka, jadi isi detail **tidak dikutip** | — |
| Jumlah paper yang memakai CWRU | **tidak ketemu** angka bersumber | Jangan menulis "ribuan paper" tanpa sumber | — |

**Produk:**
| Produk | Negara | Apa yang dilakukan | Energi? | Sumber |
|---|---|---|---|---|
| Schaeffler **OPTIME** | Jerman (global) | Sensor getaran nirkabel baterai + gateway + app; motor, kipas, pompa; deteksi imbalance, misalignment, komponen longgar; "proprietary algorithms" + model fisik. Klaim: hingga 95 % aset fasilitas tidak dipantau/hanya periodik (klaim vendor) | Tidak disebut | [S16] |
| SKF Enlight Collect IMx-1 | Swedia | Sensor getaran+suhu nirkabel, dipakai dalam kontrak layanan SKF | Tidak diverifikasi (halaman 403) | — |
| ABB Ability Smart Sensor | Swiss | Sensor motor tegangan rendah | Klaim hemat energi muncul di hasil pencarian, **halaman gagal dibuka, tidak dipakai** | — |
| Augury | AS | Sensor getaran/suhu/magnetik + AI | Studi kasus yang terlihat menyebut biaya pemeliharaan, **bukan kWh**; halaman tidak dibuka | — |
| **Include Technology Indonesia** | **Indonesia, startup mahasiswa ITS** | Integrasi IoT, deteksi kegagalan, predictive maintenance mesin; juara 3 University Startup World Cup 2023 | Tidak disebut | [S17] |
| Groundup.ai | (HQ tidak disebut) | Sensor magnetik getaran/suhu/suara + "Asset Library" transfer learning; menyasar pabrik Jakarta/Surabaya. Klaim −50 % downtime tanpa bukti (klaim vendor) | Tidak disebut | [S18] |

**Di mana kita bisa beda (jujur):**
| Klaim pembeda | Kuat? | Alasan |
|---|---|---|
| "Pelacak detak jantung dari wajah → detak motor" | **Cerita kuat, teknik tidak baru.** Pelacakan frekuensi Viterbi + abstain SNR adalah DSP umum | Juri J1 akan bertanya "apa bedanya dengan order tracking biasa?" |
| Diagnosis bearing di CWRU | **Lemah / generik** | Jenuh [S14, S15]. Dan produk komersial sudah melakukannya [S16] |
| **Indeks efisiensi pompa dari arus motor (MCSA) + abstain saat sinyal jelek** | **Sedang–kuat** | Produk di tabel menonjolkan downtime, bukan kWh. Ada data lokal yang menunjukkan masalah (S6: efisiensi 49,77 %, rekondisi manual). Paderborn punya arus motor [S12] |
| Pengguna lokal yang sudah pernah diaudit (PDAM Surya Sembada + ITS) | **Kuat** | Ada paper bersama ITS–PDAM [S6], jadi jalur co-design nyata |
| Ada pesaing di kampus sendiri (Include) | **Risiko** | Juri ITS mungkin mengenal Include. Harus jelas bedanya: energi (kWh/m³), bukan sekadar "mesin rusak" |

### 1.4 Dataset legal yang bisa dipakai sekarang
| Dataset | Isi | Lisensi | Ukuran | Cocok untuk | Sumber |
|---|---|---|---|---|---|
| CWRU Bearing | Normal + cacat titik bearing DE/FE; 12 kHz (48 kHz untuk DE); file MATLAB berisi DE/FE/BA + RPM | **Tidak ada pernyataan lisensi** di halaman unduh. Lazim dipakai akademik dengan sitasi | `[ISI: total GB]` | Baseline & sanity check saja (jenuh) | [S11] |
| **Paderborn KAt** | Getaran **dan arus fasa motor** untuk bearing sehat/rusak buatan/rusak alami | **CC BY-NC 4.0** (non-komersial; komersial harus kontak penulis). Wajib sitasi Lessmeier dkk. PHME 2016 | `[ISI: jumlah bearing & GB; halaman tidak mencantumkan]` | **MCSA**, split per-bearing | [S12] |
| **Ottawa UORED-VAFCLS v5** | 20 bearing (inner/outer/ball/cage), masing-masing sehat → berkembang → rusak; 42 kHz, 10 s; akselerometer + mikrofon + load cell + hall + termokopel | **CC BY 4.0** | 60 set mentah + 24.000 spektrogram | Kelas "fault berkembang" (lebih realistis), komersial boleh | [S13] |
| Dataset pompa sentrifugal 4TU (arus motor + getaran, banyak fault) | Disebut di hasil pencarian | **Tidak terverifikasi** (server 4TU menolak koneksi) | — | Paling cocok untuk "pompa" kalau lisensinya terbuka. `[ISI: buka data.4tu.nl, cek lisensi]` | — |
| MaFaulDa (UFRJ) | Imbalance/misalignment | **Tidak terverifikasi** (halaman sumber tidak dibuka) | — | Jangan dipakai sampai lisensi jelas | — |
| Rekaman sendiri | 1 motor/pompa lab + akselerometer ponsel/MEMS + clamp arus | Milik tim | — | **Wajib** untuk TKT 4 yang meyakinkan, dan langkah ke TKT 5 | — |

### 1.5 Regulasi terkait
| Regulasi | Isi yang relevan | Sumber | Status verifikasi |
|---|---|---|---|
| PP 33/2023 Konservasi Energi | Manajemen energi wajib: penyedia energi ≥6.000 TOE/th, industri ≥4.000, transportasi ≥4.000, gedung ≥500. Kewajiban: manajer energi bersertifikat, program konservasi, audit energi oleh auditor bersertifikat, tindak lanjut, pelaporan | [S1] | Lewat rilis ESDM. PDF PP adalah scan tanpa teks, pasalnya `[ISI]` |
| Permen ESDM 8/2025 Manajemen Energi | Pelaksana PP 33/2023, berlaku 13 Mar 2025, menggantikan Permen ESDM 14/2012; laporan kinerja energi tahunan; audit energi berkala; disinsentif (peringatan, audit khusus, pengumuman publik) | [S2] | Sekunder. `[ISI: teks resmi + interval audit]` |
| Standar kinerja energi minimum (SKEM) motor listrik Indonesia | **Tidak ketemu** | — | `[ISI: cek JDIH ESDM]` |
| ISO 10816/20816 (getaran mesin) | Dipakai sebagai acuan ambang di riset Indonesia | — | Standar berbayar; tidak dikutip angkanya |

**Implikasi:** pembeli yang "wajib" adalah industri ≥4.000 TOE dan gedung ≥500 TOE. Data DetakMesin bisa diposisikan sebagai **masukan audit energi/laporan manajemen energi**, bukan sekadar alarm perawatan.

### 1.6 Estimasi effort TKT 3 → 4
**Asumsi tertulis:**
- 1 orang penuh waktu (±8 jam/hari) yang sudah paham kode FaceVitals.
- Fungsi `facevitals/signal/quality.py` (`psd`, `spectral_snr`, `whiten`, `peak_frequency`) dan `facevitals/vitals/hr.py` (`viterbi_track`, `CausalTracker`) menerima argumen `band`. Default-nya pita detak jantung (0,6–4 Hz), jadi pada dasarnya **bisa diparametrisasi ulang** ke pita mesin (hasil membaca signature fungsi, belum diuji).
- Dataset Paderborn/Ottawa bisa diunduh tanpa login `[ISI: konfirmasi saat unduh]`.
- Tidak ada perangkat keras baru selain akselerometer MEMS/ponsel dan clamp arus milik lab.

| Langkah | Hari kerja | Bukti keluaran |
|---|---|---|
| Bungkus DSP FaceVitals jadi modul `detak/` (pita & resolusi baru), tes unit pada sinyal sintetis sinus+noise | 1 | Tes lulus, frekuensi poros terlacak di sintetis |
| Loader Paderborn + Ottawa, **split per-bearing** [S14], baseline: RMS/ambang + envelope-FFT klasik + fitur sederhana + random forest | 1,5 | Tabel metrik baseline |
| Model kita: pelacak frekuensi poros/slip dari arus (MCSA) + fitur sideband + abstain SNR; metrik vs baseline + tingkat abstain | 1,5 | **TKT 3** (fungsi terbukti di data publik nyata) |
| Rekaman 1 motor/pompa lab (sehat vs tidak seimbang dengan massa, mengikuti desain S8), ukur arus & daya | 1–2 (+ akses lab) | Data sendiri |
| Pipeline end-to-end (sinyal → kondisi → estimasi kenaikan arus/daya) diuji di data held-out + rekaman sendiri, README, tes otomatis | 1,5 | **TKT 4** (validasi komponen di lab, metrik vs baseline) |
| **Total** | **≈ 6,5–7,5 hari kerja** (TKT 3 di hari ke-4) | |

Risiko terbesar: klaim kWh. Tanpa rekaman daya sendiri, angka energi hanya bersandar pada S8 (lab kecil) dan S10 (satu kasus).

---

## 2. E2 TagihanJujur (+E15 TagihanIndustri): ekstraksi tagihan PLN/LPG → emisi & saran hemat

### 2.1 Ukuran masalah
| Angka | Nilai | Sumber | Catatan |
|---|---|---|---|
| Tarif bisnis B-3/TM & industri I-3/TM (>200 kVA) | LWBP **Rp1.035,78/kWh**, WBP = **K × 1.035,78** (1,4 ≤ K ≤ 2, ditetapkan Direksi PLN) | [S19] Lampiran III & IV | Tarif bisa disesuaikan per triwulan (tariff adjustment, pasal terkait di Permen yang sama) |
| **Biaya kelebihan daya reaktif** | B-3: **Rp1.114,74/kVArh**; I-2/TR: Rp1.057; I-3/TM: **Rp1.114,74**; I-4/TT: Rp996,74; dikenakan bila **faktor daya rata-rata bulanan < 0,85** | [S19] | Inti E15. Aturan lama memakai ambang kVArh > 0,62 × kWh; itu muncul di cuplikan pencarian untuk Permen 2011 dan **tidak diverifikasi** dari sumber yang dibuka. Secara matematis, cos φ = 0,85 ↔ tan φ ≈ 0,62 (hitungan sendiri) |
| Praktik denda kVArh | PLN mengenakan denda kVArh untuk cos φ < 0,85; contoh kebutuhan kapasitor 436 kVAr (11 × 40 kVAr) di satu pabrik | [S20] | Satu studi kasus |
| Faktor emisi grid Jamali (termasuk Jatim) | **0,87 tCO₂/MWh** (kasus 1) / 0,80 (kasus 2) | [S21] | Nilai FE 2019 Gatrik ESDM, lewat tabel JCM |
| Faktor emisi CO₂ LPG (IPCC default) | **63.100 kg CO₂/TJ** (rentang 61.600–65.600) | [S22] Tabel 1.4 | Konversi ke kg CO₂/kg LPG butuh NCV dari Tabel 1.2. Ekstraksi tabel itu berantakan → `[ISI: verifikasi NCV LPG Tabel 1.2]`. Faktor nasional KLHK `[ISI]` |
| Jumlah hotel di Jatim | **4.055 unit (2024)**, naik dari 3.783 (2023) | [S29] (mengutip BPS) | Segmen E15. Jumlah hotel bintang: **tidak ketemu** di sumber yang dibuka |
| Penjualan TM PLN UID Jatim 2023 | **13,94 TWh** | [S4] | Pelanggan TM = segmen yang bisa kena denda kVArh. Jumlah pelanggan B-3/I-3 Jatim: **tidak ketemu** |
| Jumlah UMKM Jatim | **tidak terverifikasi**. Hasil pencarian memberi dua angka yang jauh berbeda (±9,78 juta vs ±943 ribu); dokumen Diskop UKM Jatim 404 | — | `[ISI: angka resmi Diskop UKM Jatim / BPS Jatim + URL]` |
| Permintaan data emisi dari pembeli | Artikel UMKM: makin banyak perusahaan besar meminta data emisi pemasok, termasuk UMKM | [S25] | Pernyataan artikel, bukan survei. CBAM UE (2026) hanya mencakup besi-baja, aluminium, semen, pupuk, listrik, hidrogen [S30]. **UMKM makanan/laundry tidak terkena CBAM** |

**Kesimpulan:** E15 (denda kVArh) punya rupiah yang jelas dan bersumber regulasi [S19]. E2 (UMKM, emisi) punya masalah yang lebih kabur: pesaing gratis sudah ada (§2.3) dan tekanan pembeli belum terbukti untuk sektor UMKM.

Ilustrasi rumus (bukan data pengguna): `denda_kVArh/bulan = kVArh_kelebihan × Rp1.114,74`. Nilai kVArh kelebihan per pelanggan: `[ISI: dari tagihan asli]`.

### 2.2 Pengguna & pembayar
| Segmen | Siapa (Surabaya/Jatim) | Alternatif Bandung | Pembayar | Jalur kontak | Catatan |
|---|---|---|---|---|---|
| E15: gedung/pabrik TM (B-3, I-3) | Hotel (4.055 hotel di Jatim [S29]), RS, pabrik | Hotel/pabrik Bandung | Pelanggan (hemat denda); **vendor kapasitor/ESCO** (lead generation) | Lewat PHRI Jatim `[ISI: kontak kelembagaan]`, chief engineer via alumni | Pembayar paling jelas |
| E15: wajib manajemen energi | Gedung ≥500 TOE, industri ≥4.000 TOE [S1] | Sama | Manajer energi | Asosiasi manajer energi `[ISI]` | Tagihan = data dasar laporan |
| E2: UMKM | UMKM makanan/laundry Surabaya-Sidoarjo | UMKM sekitar kampus/keluarga tim | Freemium; bank (data kredit hijau) | Dinas Koperasi `[ISI]`; jaringan keluarga | Pesaing gratis (BI, Jejakkarbonku) |
| Bank | Bank yang pakai Kalkulator Hijau BI | Sama | Bank | `[ISI]` | BI menyasar perbankan & pelaku usaha termasuk UMKM [S24] |

### 2.3 Solusi yang sudah ada
| Solusi | Siapa | Apa | Gratis? | Beda dengan kita | Sumber |
|---|---|---|---|---|---|
| **Kalkulator Hijau** | **Bank Indonesia** + Kemenko Marves (diluncurkan 2 Okt 2024) | Hitung emisi GRK berbasis ponsel, mengacu SNI ISO 14064-1:2018, faktor emisi nasional | **Ya** | Input **manual**. Kita: baca dokumen otomatis + cek konsistensi | [S24] |
| Jejakkarbonku.id, GHG Emissions Calculator | Disebut di artikel UMKM | Kalkulator emisi gratis tanpa registrasi | Ya | Input manual | [S25] |
| Jejak.in | Startup Jakarta | Kalkulator emisi langsung/tak langsung perusahaan, marketplace offset; mitra Gojek, MRT Jakarta | — | Fokus offset/kehutanan. Data 2020, status terkini `[ISI]` | [S26] |
| PLN Mobile | PLN | Riwayat pemakaian kWh pascabayar (muncul di hasil pencarian; halaman tidak dibuka) | Ya | Tidak menganalisis denda kVArh, emisi, atau anomali | `[ISI: buka halaman resmi PLN Mobile]` |
| **Arcadia** (termasuk Urjanet) | AS | Agregasi data utilitas otomatis dari **12.000+ penyedia di 50+ negara**, siap untuk laporan Scope 1–2, terlacak ke tagihan asli (klaim vendor) | Tidak | PLN ada di cakupannya atau tidak: **tidak ketemu** | [S27] |
| Vendor kapasitor / ESCO | Lokal | Survei manual faktor daya | — | Calon **mitra/pembayar**, bukan sekadar pesaing | [S20] (praktik) |

**Di mana kita bisa beda (jujur):**
- Kalkulator emisi = **komoditas gratis**. Jangan jual "hitung emisi".
- Yang tidak ditemukan di pesaing yang dibuka: **audit otomatis tagihan PLN TM terhadap Permen 7/2024** (cek LWBP/WBP × K, deteksi denda kVArh, rekomendasi ukuran kapasitor, anomali bulan ke bulan), dengan pola "LLM membaca, aturan memutuskan" dari Kendali. Ini E15.
- Juri J4 tetap bisa bilang "ini aturan tarif + OCR". Pembelaan harus berupa **angka LLM asli vs aturan saja di tagihan asli** (belum ada; `LLM_SCORECARD.md` Kendali: belum ada model asli yang dijalankan).

### 2.4 Dataset
| Dataset | Lisensi | Ukuran | Kegunaan | Sumber |
|---|---|---|---|---|
| **Tagihan PLN / struk token / nota LPG asli** | **Butuh persetujuan pemilik** (UU PDP, §2.5). Tidak ada dataset publik yang ditemukan | Target 20–30 (E2) + 5–10 tagihan TM (E15) | Satu-satunya cara mencapai TKT 3/4 yang jujur di domain ini | `[ISI: kumpulkan dengan form persetujuan; data pribadi disamarkan [[...]]]` |
| CORD (Clova AI) | **CC BY 4.0** | Rilis unduhan: 1.000 struk (800/100/100) per versi; halaman juga menyebut "lebih dari 11.000" (tidak konsisten) | Struk **Indonesia** (toko/restoran) untuk menguji OCR + parsing; proxy, **bukan** tagihan listrik | [S28] |
| SROIE (ICDAR 2019) | **Tidak terverifikasi** | — | Jangan dipakai sampai lisensinya jelas | — |
| Tagihan sintetis | Milik tim | Bebas | Uji regresi aturan (seperti `scripts/make_data.py` Kendali). **Bukan bukti TKT 4** | — |
| Tabel tarif Permen 7/2024 | Dokumen publik | — | Aturan deterministik | [S19] |

### 2.5 Regulasi
| Regulasi | Isi relevan | Sumber |
|---|---|---|
| **UU 27/2022 PDP** | Data pribadi umum termasuk nama lengkap dan data yang dikombinasikan sehingga mengidentifikasi seseorang (Pasal 4 ayat 3). Tagihan memuat nama, alamat, ID pelanggan, jadi **termasuk data pribadi**. Dasar pemrosesan: persetujuan eksplisit dll. (Pasal 20 ayat 2). Persetujuan **tertulis atau terekam**; persetujuan yang tidak memenuhi syarat **batal demi hukum** (Pasal 22). Penilaian dampak PDP wajib untuk pemrosesan berisiko tinggi (Pasal 34). Pidana: perolehan/pengumpulan melawan hukum hingga 5 tahun dan/atau Rp5 M (Pasal 67 ayat 1); pengungkapan hingga 4 tahun/Rp4 M (ayat 2); penggunaan hingga 5 tahun/Rp5 M (ayat 3) | [S23] |
| Permen ESDM 7/2024 Tarif PLN | Tarif, faktor K, biaya kVArh bila cos φ < 0,85 | [S19] |
| PP 33/2023 + Permen ESDM 8/2025 | Laporan manajemen energi (tagihan = data dasar) | [S1], [S2] |
| SNI ISO 14064-1:2018 | Acuan Kalkulator Hijau BI | [S24] |

**Konsekuensi praktis:** sebelum mengumpulkan tagihan, siapkan form persetujuan tertulis/terekam (tujuan jelas, terpisah, bahasa sederhana), simpan lokal, samarkan nama/alamat/ID pelanggan sebelum dikirim ke LLM pihak ketiga. `[ISI: cek apakah mengirim gambar tagihan ke API LLM luar negeri = transfer data ke luar wilayah hukum RI; pasal terkait UU PDP]`.

### 2.6 Estimasi effort TKT 3 → 4
**Asumsi tertulis:**
- 1 orang penuh waktu yang paham Kendali (`kendali/invoices.py`, `nlu.py`, `llm.py`, `policy.py`, `audit.py`; pytest 116/116 menurut `01_INVENTARIS_ASET.md`).
- **API key LLM + izin pemakaian tersedia** `[ISI]`. Tanpa ini komponen AI tetap TKT 3 (stub).
- 20–30 tagihan/struk asli + 5–10 tagihan TM **sudah terkumpul dengan persetujuan**. Ini kerja manusia yang tidak termasuk dalam hitungan hari di bawah.
- Modul blockchain tidak disentuh.

| Langkah | Hari kerja | Bukti keluaran |
|---|---|---|
| Skema data tagihan PLN (pascabayar, token, TM dengan LWBP/WBP/kVArh) + nota LPG; generator tagihan sintetis untuk tes | 1 | Tes skema |
| Aturan deterministik dari Permen 7/2024: kWh × tarif = Rp, cek K, deteksi denda kVArh, emisi (FE Jamali), anomali bulan ke bulan | 1 | Tes aturan lulus |
| Ekstraksi: aturan saja vs LLM asli (+ guardrail Kendali) pada tagihan asli; label manual sebagai ground truth | 1–1,5 | **TKT 3** (akurasi per-field, LLM vs aturan saja) |
| Evaluasi held-out + kasus serangan/berantakan (foto miring, blur) + CORD sebagai uji OCR tambahan; README; tes otomatis | 1,5 | **TKT 4** (pipeline end-to-end di data uji nyata, metrik vs baseline) |
| **Total** | **≈ 4,5–5 hari kerja** setelah tagihan & API key tersedia | |

Risiko terbesar: (1) pengumpulan tagihan + persetujuan, (2) orisinalitas Kendali (FinTechathon aktif; ungkapkan asal-usul), (3) AI bisa dianggap tempelan kalau LLM tidak jelas lebih baik dari aturan.

---

## 3. E3 JadwalDingin: jadwal kuliah sebagai sensor okupansi untuk AC kampus

### 3.1 Ukuran masalah
| Angka | Nilai | Sumber | Catatan |
|---|---|---|---|
| Listrik pendinginan Indonesia 2020 | **79 TWh** (AC gedung + rantai dingin pangan) ≈ **30 %** konsumsi listrik nasional | [S31] mengutip UNESCAP | |
| Listrik AC gedung | **62 TWh (2020) → 241 TWh (2040)** tanpa intervensi; target I-NCAP **104 TWh (2040)** | [S31] | Lihat koreksi #3 |
| Porsi AC di gedung akademik (Indonesia) | **48 %** listrik gedung akademik UNISKA Banjarmasin (pencahayaan 27 %, perangkat 18 %); IKE **16,42 kWh/m²/bulan**; hemat hingga **27,11 %** setelah monitoring + konservasi | [S32] | Satu kampus, bukan ITS/ITB |
| Biaya listrik ITS | **±Rp6 miliar/tahun (2012)** [S33]; **±Rp7 miliar/tahun (2018)** [S34] | | **Data lama.** `[ISI: biaya & kWh listrik ITS/ITB terbaru dari Biro Manajemen Aset ITS / DITSP ITB]` |
| Jam AC menyala vs jam terjadwal di kampus kita | **tidak ketemu** | — | `[ISI: log BMS/meter + jadwal ruang satu gedung]` |
| Hemat dari jadwal registrar → HVAC (terukur) | Listrik **−39 %**, gas **−31 %** untuk AC ruang kelas di satu gedung LEED Platinum (RIT) | [S35] | Iklim AS (pemanas), bukan tropis |
| Hemat dari alat jadwal berbasis kalender ruang (terukur) | Aliran energi per ruang **−40 %** keseluruhan, **−26 %** hari kerja (satu lantai, Appalachian State) | [S36] | |
| Jam ruang kosong saat dikondisikan | **±81 %** jam ber-AC kosong (4 gedung); hemat waktu rata-rata **72,48 %** jika "occupied" hanya dari kelas pertama s.d. terakhir | [S37] | **Studi kasus vendor**, yang dihemat adalah **jam**, bukan kWh. Batas atas |

### 3.2 Pengguna & pembayar
| Segmen | Siapa | Pembayar | Jalur kontak (kelembagaan resmi) | Sumber |
|---|---|---|---|---|
| ITS (lokal, Surabaya) | **Biro Manajemen Aset ITS** (Gedung Rektorat Lt. 2; sarpras@its.ac.id; 031-5990756 ext. 1000); Direktorat Perencanaan dan Pengembangan Strategis (tu_dpal@its.ac.id) | ITS (biaya listrik ±Rp7 M/tahun pada 2018 [S34]) | Surat resmi lewat dosen pembimbing; juga lewat **DIKST/STP** (inovasi.kst@its.ac.id), penyelenggara lomba | [S43] |
| ITS riset energi | Pusat Penelitian Energi Berkelanjutan (lppm@its.ac.id) | — (mitra validasi) | Lewat LPPM | [S43] |
| ITB (Bandung, akses tercepat) | Direktorat Sarana dan Prasarana ITB (DITSP) | ITB | Situs ditsp.itb.ac.id **tidak bisa dibuka** hari ini. `[ISI: kontak kelembagaan DITSP]` | — |
| Kampus swasta Surabaya | `[ISI: 2–3 nama + unit sarpras]` | Kampus | — | — |
| Gedung wajib manajemen energi | Gedung ≥500 TOE/tahun [S1]. Hitungan sendiri: 500 TOE × 11,63 MWh/TOE ≈ 5.815 MWh/tahun (konversi dari [S2]). Kampus besar mungkin melewati ambang ini `[ISI: kWh ITS/ITB]` | Pengelola gedung | — | [S1], [S2] |

### 3.3 Solusi yang sudah ada
| Solusi | Siapa | Apa | Hasil | Sumber |
|---|---|---|---|---|
| **Events2HVAC** (dipakai Penn State sejak Fall 2018) | Produk komersial yang terhubung ke sistem pemesanan ruang (25Live/EMS) | Ruang kelas di-*occupy/unoccupy* sesuai jadwal sebenarnya, bukan blok tetap; potensi hingga ±1.900 ruang | Halaman tidak memberi angka hemat | [S38] |
| Stony Brook Occupancy-Based HVAC | Kampus | Sistem jadwal kelas dihubungkan ke kontrol HVAC; pilot di Javits Lecture Center, selesai Spring 2026 | Tidak ada angka | [S39] |
| RIT (disertasi 2018) | Riset | Data registrar + BAS: persingkat jadwal, setpoint, aliran udara minimum | −39 % listrik, −31 % gas | [S35] |
| Appalachian State (RUSch) | Riset | Penjadwalan HVAC berbasis kalender pemesanan ruang | −40 % / −26 % | [S36] |
| SRT Labs | Vendor | Audit jadwal akademik vs kebijakan HVAC | 81 % jam kosong (estimasi) | [S37] |
| Occupant-centric control sekolah (Ye dkk. 2021) | PNNL | Simulasi 96 model gedung | Halaman tidak memuat angka | [S40] |
| Produk BMS/AC Indonesia | Indosat, LG, SensorFlow muncul di hasil pencarian | — | Halaman tidak dibuka, **tidak dipakai** | — |

**Di mana kita bisa beda (jujur):**
- **Ide intinya sudah ada dan sudah jadi produk** (Events2HVAC, sejak 2018). Klaim "jadwal kuliah sebagai sensor gratis" **tidak baru**.
- Pembeda yang masih mungkin:
  1. **Konteks tropis**: semua bukti terukur di atas dari AS, dengan beban pemanas/gas. Di Indonesia yang ada hanya AC (48 % di satu kampus [S32]). Hemat pendinginan tropis dari jadwal **belum ketemu** di literatur yang dibuka.
  2. **Kampus tanpa BMS dan tanpa sistem pemesanan ruang terstruktur**: produk AS butuh 25Live/EMS + BAS. Kita bisa mulai dari **jadwal berantakan (PDF/spreadsheet/pengumuman)** dan AC split yang dikendalikan manual/IR. Ini adalah inti AI (ekstraksi + prediksi kelas batal), dan juga titik terlemah karena data kelas batal tidak tersedia publik.
- Juri J2 akan bertanya "kenapa bukan timer". Tanpa data prediksi okupansi asli, AI-nya hanya ekstraksi dokumen.

### 3.4 Dataset
| Dataset | Isi | Lisensi | Ukuran | Kegunaan | Sumber |
|---|---|---|---|---|---|
| Building Data Genome 2 (BDG2) | 3.053 meter dari 1.636 gedung non-residensial, 19 situs Amerika Utara & Eropa; listrik, chilled water, steam, dll.; per jam 2016–2017; data cuaca | **CC BY-SA 4.0** (dari file LICENSE; sumber sekunder lain menyebut MIT, jadi pakai file LICENSE) | 17.544 titik/meter | Model baseline konsumsi gedung pendidikan vs jam operasi. Tidak berisi jadwal kelas. Iklim bukan tropis | [S41] |
| ASHRAE Global Occupant Behavior Database | 34 dataset okupansi (muncul di hasil pencarian) | **Tidak terverifikasi** (halaman Nature redirect login) | — | Pola okupansi | `[ISI: cek ashraeobdatabase.com]` |
| Jadwal kuliah ITS/ITB | Biasanya di sistem akademik yang butuh login | **Butuh izin** kampus. Jangan login dengan akun mahasiswa untuk scraping | — | Inti ekstraksi | `[ISI: izin Biro Manajemen Aset/Direktorat Akademik]` |
| Meter listrik gedung kuliah | — | **Butuh izin** pengelola | — | Satu-satunya cara mengklaim kWh | `[ISI]` |

### 3.5 Regulasi
| Regulasi | Isi relevan | Sumber |
|---|---|---|
| PP 33/2023 | Gedung ≥500 TOE/tahun wajib manajemen energi | [S1] |
| Permen ESDM 8/2025 | Laporan kinerja energi tahunan, audit berkala | [S2] |
| Permen ESDM 13/2012 | Suhu ruang kerja 24–27 °C (gedung negara/BUMN/BUMD/BHMN). **Dicabut** oleh Permen ESDM 9/2018 menurut pasal.id | [S42] |
| UU PDP 27/2022 | Jadwal yang memuat **nama dosen/mahasiswa** = data pribadi. Pakai hanya kode ruang + jam | [S23] |

### 3.6 Estimasi effort TKT 3 → 4
**Asumsi tertulis:**
- 1 orang penuh waktu. Memakai pola ekstraksi + mesin kebijakan Kendali.
- **Tanpa data kampus**: hanya dokumen jadwal publik (kalau ada) + BDG2. **Dengan izin kampus**: jadwal satu gedung + data meter/log AC.
- Tidak ada pemasangan alat.

| Langkah | Hari kerja | Bukti keluaran |
|---|---|---|
| Kumpulkan 5–10 dokumen jadwal ruang (format berbeda), label manual ruang × jam sebagai ground truth | 1 (+ izin) | Set uji berlabel |
| Ekstraksi jadwal: parser aturan vs LLM + guardrail (jam valid, ruang ada di daftar, tidak tumpang tindih) | 1,5 | **TKT 3** (akurasi ekstraksi vs label) |
| Simulasi jam AC: jadwal "satpam pagi–sore" vs jadwal hasil ekstraksi (+ pre-cooling, batas kenyamanan) → jam AC yang bisa dihemat; model baseline konsumsi dari BDG2 (gedung pendidikan) | 1,5 | Estimasi jam & kWh (berlabel **simulasi**) |
| Validasi dengan meter/log AC satu gedung + pipeline end-to-end, README, tes | 2–3 (**butuh data meter**) | **TKT 4** |
| **Total** | **≈ 4 hari ke TKT 3; 6–7 hari ke TKT 4 kalau data meter tersedia.** Tanpa data meter: **mentok di TKT 3** | |

Risiko terbesar: (1) izin data jadwal & meter, (2) sudah ada produk [S38], (3) komponen "prediksi kelas batal" tidak punya data latih.

---

## 4. Ringkasan pembanding tiga ide (untuk A5 & orkestrator)

| Aspek | E5 DetakMesin | E2+E15 TagihanJujur | E3 JadwalDingin |
|---|---|---|---|
| Angka masalah terkuat | Motor 45 % listrik dunia, hemat 20–30 % [S3]; **PDAM Surabaya Rp147,65 M energi/tahun, 24,37 % opex** [S6] | **Denda kVArh Rp1.114,74/kVArh bila cos φ < 0,85** [S19] | AC 48 % listrik gedung akademik [S32]; −39 % listrik di RIT [S35] |
| Lubang energi | Deteksi bearing ≠ hemat kWh [S9]; jalur pompa lebih kuat [S6, S10] | Emisi UMKM = komoditas gratis [S24, S25] | Bukti hemat dari iklim AS; kWh lokal `[ISI]` |
| Pengguna lokal dengan jalur kontak | **PDAM Surya Sembada lewat penulis ITS di S6** | Hotel/pabrik TM (PHRI `[ISI]`) | **Biro Manajemen Aset ITS** [S43] |
| Pesaing terdekat | OPTIME [S16]; **Include (startup ITS)** [S17] | BI Kalkulator Hijau (gratis) [S24]; Arcadia [S27] | **Events2HVAC** (sejak 2018) [S38] |
| Dataset legal sekarang | Paderborn CC BY-NC [S12], **Ottawa CC BY** [S13], CWRU (tanpa lisensi tertulis) [S11] | CORD CC BY (proxy) [S28]; tagihan asli **butuh persetujuan** | BDG2 CC BY-SA [S41]; jadwal/meter **butuh izin** |
| Effort ke TKT 4 | ≈ 6,5–7,5 hari | ≈ 4,5–5 hari **setelah** tagihan + API key | 6–7 hari **kalau** ada data meter, kalau tidak mentok TKT 3 |
| Blok manusia terbesar | Akses 1 motor/pompa lab | Persetujuan PDP + API key + asal-usul Kendali | Izin jadwal + meter kampus |

---

## 5. `[ISI]` terpenting hasil riset
1. **E5:** lisensi dataset pompa 4TU (arus + getaran); akses rekaman 1 pompa/motor lab; kontak kelembagaan ke penulis S6 (ITS) / PDAM Surya Sembada; jumlah tenant SIER/PIER dari sumber resmi.
2. **E2/E15:** 5–10 tagihan PLN TM asli (hotel/pabrik) dengan persetujuan tertulis; API key LLM; teks resmi Permen 7/2024 (BPK/JDIH) untuk mencocokkan tarif; angka UMKM Jatim resmi; aturan UU PDP soal transfer data ke LLM luar negeri.
3. **E3:** kWh & biaya listrik ITS/ITB terbaru; izin jadwal ruang + log meter satu gedung; kontak DITSP ITB.
4. **Umum:** FE Jamali terbaru (Gatrik ESDM); teks pasal PP 33/2023 dan Permen ESDM 8/2025; Statistik PLN 2024 per UID per kelompok pelanggan.
