# 02_BRAINSTORM: 18 ide untuk Seno Hackathon ITS 2026
### Agen A3 "Generator Ide" · 28 Okt 2026 · tim: Aziz (PIC), Uqi, Pio, Poggy

**Dasar:** `07-MEGA-PROMPT-ITS-HACKATHON-28okt2026.md` (§A, §B Fase 2, §C), `00_INFO.md`, `01_INVENTARIS_ASET.md`.

**Cara baca:**
- Ada 18 ide: **E1–E15** di sektor energi/rendah karbon, **N1–N3** di luar energi sebagai pembanding (ditandai **[NON-ENERGI]**).
- Setiap ide berisi: kalimat "aha", energy gap, pengguna + pembayar, AI di inti, aset yang dipakai ulang, jalur ke TKT 3, persona, dan kritik juri.
- **Persona = [SIMULASI PERSONA, bukan data wawancara].** Persona hanya alat berpikir untuk menebak keberatan pengguna, **bukan bukti**. Jangan dikutip di berkas pendaftaran.
- **Kritik juri** memakai persona J1–J4 dari §B Fase 8:
  - **J1:** profesor energi CityU/Tsinghua
  - **J2:** praktisi industri
  - **J3:** investor InvestHK/Kerogen
  - **J4:** reviewer skeptis
- **Estimasi hari kerja** adalah tebakan agen, bukan hasil ukur.
- Semua angka di dokumen ini berasal dari halaman yang **benar-benar dibuka** (tabel §0). Angka lain ditulis `[ISI: …]`.

---

## 0. Angka yang sudah diverifikasi (halaman dibuka 28 Okt 2026)

| # | Angka | Konteks / catatan | Sumber (dibuka) |
|---|---|---|---|
| S1 | AC gedung + rantai dingin pangan = **79 TWh (2020), setara 30 % konsumsi listrik Indonesia**. Listrik AC gedung diproyeksikan naik dari **62 TWh (2020) → 241 TWh (2040)** tanpa intervensi | Artikel IIR mengutip UN ESCAP. Angka 30 % adalah **gabungan** AC gedung dan rantai dingin, bukan AC saja | https://iifiir.org/en/news/indonesia-unveils-its-first-national-action-cooling-plan |
| S2 | Faktor emisi grid **Jamali (termasuk Jawa Timur): 0,87 tCO₂/MWh** (kasus 1: hanya menggantikan listrik grid); 0,80 (kasus 2) | Tabel JCM Jepang tahun fiskal R4 (2022), kategori hemat energi. Ini angka acuan JCM, bukan rilis ESDM langsung. `[ISI: angka FE Jamali terbaru dari gatrik.esdm.go.id]` | https://gec.jp/innovation/R4/T.CO2EmissionFactor_20220406.pdf (Lampiran 2-1, baris 22 "Jamali") |
| S3 | Pada hari mana pun, **40 % AHU dan 30 % unit terminal udara** melaporkan suatu fault. Data: >60.000 unit HVAC, >90 jenis fault | Gedung komersial AS (Crowe dkk., LBNL, 2023). Bukan data Indonesia | https://eta-publications.lbl.gov/sites/default/files/empirical_analysis_of_the_prevalence_.pdf |
| S4 | Sistem motor listrik (pompa, kipas, kompresor, dll.) memakai **45 % konsumsi listrik dunia**. Potensi pengurangan dengan teknologi yang ada **20–30 %** | IEA 4E EMSA, *Policy Guidelines for Motor Driven Units*, Okt 2016, hlm. "4E Electric Motor Systems Annex" | https://www.iea-4e.org/wp-content/uploads/2020/12/PGmdu_oct2016.pdf |
| S5 | **60–70 % biaya operasional melaut nelayan kecil adalah BBM.** **82,2 %** nelayan membeli BBM bersubsidi di pengecer dengan harga di atas harga subsidi (survei koalisi KNTI–Kusuka 2020–2021) | Pernyataan Ketua KNTI (organisasi advokasi), 26 Agu 2022. **Bukan studi tersendiri.** Perlu angka primer `[ISI: studi biaya melaut nelayan Jatim, KKP/BPS]` | https://nasional.kontan.co.id/news/nelayan-60-70-biaya-operasional-nelayan-melaut-adalah-bbm |
| S6 | Timbulan sampah Kota Surabaya **1.800,05 ton/hari (2023)**. TPS3R Tenggilis: rata-rata **5.047,29 kg/hari**, organik **65,789 %**, plastik **12,15 %**. Sampah masuk 1.952,24 ton/tahun, 831,41 ton/tahun dikelola, sisanya ke TPA | Ulum dkk., *EnviroUS* 5(2):33–38, 2025 (UINSA). Angka kota dikutip dari SIPSN 2024 | https://envirous.upnjatim.ac.id/index.php/envirous/article/download/340/176/852 |
| S7 | Sekitar **35 % tangkapan** hilang atau terbuang setiap tahun (global). Es di kapal disebut metode penanganan yang sangat efektif | WWF Food Forward mengutip FAO. **Global, bukan Indonesia** | https://foodforwardndcsnbsaps.panda.org/food-supply-chains/reducing-post-harvest-food-loss-in-fisheries-supply-chains/ |

**Dicari tapi tidak berhasil diverifikasi** (tidak dipakai sebagai fakta):
- kapasitas PLTS atap terpasang di Jatim;
- susut jaringan PLN nasional 2023;
- jumlah nelayan Jatim terbaru;
- angka soiling loss PLTS Indonesia (halaman jurnal Unram minta login);
- status PPDPI KKP saat ini;
- isi Permen ESDM 2/2024 (hanya muncul di hasil pencarian, PDF belum dibuka).

Semua ini ditulis sebagai `[ISI]` di bawah.

---

## 1. Skala skor (dipakai di matriks §3)

| Kriteria (bobot) | 1 | 3 | 5 |
|---|---|---|---|
| **Bukti TKT ada / bisa dicapai sebelum deadline (3×)** | Tidak ada jalur ke AI TKT 3 sebelum deadline | AI TKT 3 bisa dicapai dalam 3–5 hari kerja (model baru di atas data publik nyata, pakai ulang sebagian kode) | AI TKT ≥4 **sudah ada** untuk kasus pakai ini. Nilai **4** = TKT 3 jujur dalam ≤2 hari dengan kode yang sudah lulus tes |
| **Energy gap terkuantifikasi (2×)** | Tidak ada angka / hubungan ke energi lemah | Ada angka bersumber untuk konteks (nasional/global), angka lokal masih `[ISI]` | Angka lokal Jatim/pengguna bersumber + rantai kWh/kgCO₂e yang jelas |
| **Akses pengguna validasi ≤2 minggu (2×)** | Pengguna sulit dijangkau dari Bandung, tanpa kontak | Bisa dijangkau tapi butuh perantara (dinas/penyuluh/manajemen pabrik) | Bisa ditemui langsung minggu ini (kampus sendiri, UMKM sekitar, keluarga) |
| **Minat mitra: rendah karbon & investable (1×)** | Tidak terkait karbon, tidak ada pembayar | Terkait energi, pembayar belum jelas | Efisiensi/karbon jelas, pembayar B2B jelas, bisa diskalakan ke kawasan |
| **Keunikan vs ±50 tim (2×)** | Ide pasaran (chatbot hemat energi, CV pemilah sampah) | Ada di pasar/literatur, tapi sudut kita berbeda | Sudut pandang yang hampir pasti tidak dibawa tim lain, dan didukung aset kita |

Skor maks = 5×3 + 5×2 + 5×2 + 5×1 + 5×2 = **50**.

---

## 2. Delapan belas ide

### E1. LautHemat: prakiraan zona tangkap dari klorofil-a satelit terharmonisasi
- **Aha:** "Data satelit yang sudah kami harmonisasi untuk 4,45 juta matchup bisa memberi tahu nelayan Jatim ke mana *tidak* perlu pergi, dan setiap mil yang tidak ditempuh adalah solar yang tidak dibakar."
- **Energy gap:**
  - BBM 60–70 % biaya melaut nelayan kecil (S5; sumbernya advokasi);
  - `[ISI: liter solar per trip nelayan Selat Madura/Prigi/Muncar, sumber DKP Jatim/KKP]`.
- **Pengguna:** nelayan & penyuluh di PPN Brondong (Lamongan), PPP Muncar, Prigi, Kenjeran.
- **Pembayar:** DKP Jatim/KKP (layanan publik), koperasi nelayan, eksportir yang butuh pasokan stabil.
- **AI di inti:** model ML (gradient boosting / ConvLSTM ringan) memprakirakan klorofil-a + SST 1–3 hari ke depan, dibandingkan dengan baseline persistensi/klimatologi. Hasilnya diubah menjadi peta probabilitas front.
- **Aset:** OCEANS (pipeline unduh-regrid-harmonisasi TKT 4, `analysis\common.py` sudah punya kotak `JAV`/`SJU`).
- **Jalur TKT 3:** prakiraan klorofil vs persistensi dengan validasi out-of-sample, estimasi 3–5 hari. **Kaitan ke hasil tangkapan belum bisa divalidasi** tanpa data tangkapan `[ISI: data logbook/TPI]`.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Saya nelayan payang di Brondong. Saya sudah dapat info dari grup WA dan pengalaman bapak saya. Peta di HP itu berguna kalau bisa dibaca sebelum subuh dan tidak butuh sinyal di laut. Kalau sekali saja salah dan saya pulang kosong, saya tidak akan pakai lagi."
- **Kritik juri (J4):** "Indonesia sudah punya peta prakiraan daerah penangkapan ikan dari pemerintah. Apa bukti model Anda lebih baik, dan di mana data tangkapan untuk membuktikannya?" `[ISI: verifikasi status PPDPI KKP/BRIN + URL]`

### E2. TagihanJujur: agen pembaca tagihan energi → emisi Scope 2 + rekomendasi hemat untuk UMKM
- **Aha:** "UMKM tidak punya waktu menghitung jejak karbon, tetapi mereka punya setumpuk struk token PLN, tagihan pascabayar, dan nota LPG. Agen kami membacanya, dan aturan kami memastikan angkanya tidak halusinasi."
- **Energy gap:**
  - faktor emisi Jamali 0,87 tCO₂/MWh (S2), sehingga kWh dari tagihan bisa langsung dikonversi ke kgCO₂e;
  - `[ISI: porsi biaya energi UMKM Jatim, BPS/Kemenkop]`;
  - `[ISI: kebutuhan data emisi pemasok dari pembeli ekspor]`.
- **Pengguna:** UMKM makanan/laundry/konveksi di Bandung (validasi cepat) dan Surabaya (lokal), BUMDes, koperasi.
- **Pembayar:** pembeli/agregator ekspor yang meminta data emisi pemasok, bank/lembaga pembiayaan hijau (data untuk kredit hijau), UMKM (freemium).
- **AI di inti:** ekstraksi dokumen multimodal (foto struk, PDF, teks ID/EN) dengan pola "LLM mengusulkan, aturan memutuskan" (validasi tarif, kWh × tarif = rupiah, deteksi anomali bulan ke bulan).
- **Aset:** Kendali (`invoices.py`, `nlu.py`, `llm.py`, `policy.py`, `audit.py`; pytest 116/116). Blockchain dibuang.
- **Jalur TKT 3:** kumpulkan 20–30 tagihan/struk **asli milik anggota tim dan keluarga** (dengan izin, data pribadi disamarkan), lalu ukur akurasi ekstraksi aturan saja vs LLM asli. Estimasi 1–2 hari.
  - `[ISI: API key LLM + izin pemakaian; jalankan model asli. LLM_SCORECARD Kendali menulis belum ada model asli yang dijalankan]`.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Saya punya usaha keripik di Sidoarjo. Listrik saya naik terus, tapi saya tidak tahu kenapa. Laporan karbon saya tidak butuh, kecuali pembeli meminta. Kalau aplikasinya bisa bilang 'freezer Anda boros' cukup dari foto struk, saya mau coba, asal gratis dulu."
- **Kritik juri (J3):** "Kalkulator karbon sudah banyak dan UMKM tidak membayar. Siapa persisnya yang mengeluarkan uang, dan kenapa sekarang?"

### E3. JadwalDingin: jadwal kuliah sebagai sensor okupansi gratis untuk AC kampus
- **Aha:** "Kampus sudah tahu kapan setiap ruang dipakai karena ada di jadwal kuliah. AI kami membaca jadwal itu dan memberi tahu AC kapan *tidak* perlu menyala."
- **Energy gap:**
  - AC + rantai dingin 30 % listrik nasional, AC gedung 62 TWh pada 2020 (S1);
  - kampus: `[ISI: kWh bulanan gedung kuliah ITB/ITS dari Sarpras + jam AC menyala vs jam terjadwal]`.
- **Pengguna:** Direktorat Sarana Prasarana ITB (akses langsung, kita mahasiswa ITB) dan ITS (lokal), pengelola gedung kuliah, kampus swasta di Surabaya.
- **Pembayar:** kampus (biaya listrik), ESCO berbasis bagi hasil penghematan.
- **AI di inti:**
  1. ekstraksi jadwal ruang dari PDF/spreadsheet/sistem akademik yang formatnya berantakan (LLM + guardrail);
  2. prediksi okupansi aktual (kelas batal, ruang kosong) dari riwayat;
  3. optimasi jadwal pre-cooling dengan batas kenyamanan sebagai aturan keras.
- **Aset:** pola ekstraksi + mesin kebijakan Kendali. Pengetahuan elektronika daya tim (AC inverter).
- **Jalur TKT 3:** ekstraksi jadwal satu gedung (dokumen publik/izin Sarpras), simulasi jam AC vs jadwal, akurasi ekstraksi vs label manual. Estimasi 3–4 hari. Angka hemat kWh butuh data meter `[ISI]`.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Saya teknisi Sarpras. AC dinyalakan satpam pagi dan dimatikan sore, karena tidak ada yang mengecek jadwal setiap ruang. Saya mau pakai kalau tidak perlu memasang alat baru dan tidak ada dosen yang komplain kepanasan. Keputusan beli ada di atasan saya."
- **Kritik juri (J2):** "Ini bisa dikerjakan dengan timer dan BMS biasa. Di mana kebutuhan AI-nya, dan berapa kWh yang benar-benar terukur?"

### E4. NafasGedung: deteksi fault AHU/chiller dari data BMS
- **Aha:** "Di gedung komersial, 40 % AHU melaporkan fault setiap hari (S3). Gedung di Surabaya membayar fault itu dalam tagihan listrik tanpa tahu."
- **Energy gap:** S3 (fault prevalence, AS) + S1 (porsi AC). `[ISI: data fault/energi HVAC gedung Indonesia]`.
- **Pengguna:** engineering manager mal/rumah sakit/hotel di Surabaya, gedung kampus dengan BMS.
- **Pembayar:** pengelola gedung, ESCO, vendor BMS (lisensi modul).
- **AI di inti:** klasifikasi fault (gradient boosting / autoencoder anomali) pada sinyal BMS (suhu suplai/kembali, posisi damper, katup). Baseline: aturan APAR (AHU Performance Assessment Rules).
- **Aset:** tidak ada aset langsung. Teknik DSP/abstain FaceVitals bisa dipakai untuk menolak prediksi saat data jelek.
- **Jalur TKT 3:** dataset fault AHU publik LBNL/DOE `[ISI: nama dataset + lisensi, cek data.openei.org]`, model vs APAR. Estimasi 2–3 hari.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Saya chief engineer mal di Surabaya Barat. BMS kami sudah punya ratusan alarm, dan sebagian besar kami abaikan. Saya tidak butuh alarm baru. Saya butuh daftar lima masalah yang paling mahal minggu ini."
- **Kritik juri (J1):** "FDD HVAC sudah jadi produk komersial di luar negeri. Apa kontribusi Anda selain melatih ulang di dataset AS?"

### E5. DetakMesin: algoritma detak jantung dari wajah dipakai untuk "mendengar" detak motor & pompa
- **Aha:** "Kami sudah membuat pelacak frekuensi yang bisa menemukan detak jantung dari piksel wajah yang berisik. Motor dan pompa juga punya 'detak', dan saat detak itu bergeser, mesin membuang listrik sebelum akhirnya rusak."
- **Energy gap:**
  - sistem motor memakai 45 % listrik dunia, potensi pengurangan 20–30 % (S4);
  - lokal: `[ISI: porsi listrik industri Jatim dari Statistik PLN/ESDM]`;
  - `[ISI: hubungan kuantitatif fault (unbalance/misalignment/kavitasi) → kenaikan kWh, dari jurnal]`.
- **Pengguna:** teknisi maintenance pabrik di SIER Rungkut/PIER Pasuruan, operator pompa PDAM (Surya Sembada Surabaya / Tirtawening Bandung), lab mesin listrik kampus.
- **Pembayar:** pabrik (biaya listrik + downtime), PDAM (kWh/m³), vendor sensor/IoT.
- **AI di inti:** fitur spektral + pelacak frekuensi (Viterbi) + abstain berbasis SNR dari FaceVitals, lalu klasifikasi kondisi (sehat/unbalance/bearing/kavitasi) dan regresi indeks efisiensi. Sinyal: getaran akselerometer murah atau arus motor (MCSA).
- **Aset:** inti DSP FaceVitals (`facevitals\signal`, pelacak, abstain; tes 56/56 lulus). Kemampuan elektronika daya tim untuk MCSA.
- **Jalur TKT 3:** dataset bantalan CWRU / Paderborn `[ISI: lisensi]`, bandingkan dengan baseline envelope-FFT klasik, plus uji cepat satu motor lab (rekaman sendiri). Estimasi 2 hari untuk dataset publik, ditambah 1–2 hari untuk rekaman lab.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Saya kepala maintenance pabrik pakan ternak di Sidoarjo. Kami ganti bearing kalau sudah bunyi. Alat vibration analyzer mahal dan cuma vendor yang bisa membacanya. Kalau ada sensor murah yang bilang 'pompa 3 boros', saya mau coba di satu mesin dulu. Anggaran ada di bagian engineering."
- **Kritik juri (J2):** "Predictive maintenance menghemat downtime, bukan energi. Buktikan bahwa deteksi Anda menurunkan kWh, bukan sekadar mencegah kerusakan."

### E6. PV-Sehat: deteksi soiling & fault PLTS atap dari data inverter
- **Aha:** "Pemilik PLTS atap tidak tahu panelnya sedang kotor. AI kami membandingkan produksi aktual dengan prediksi cuaca dan memberi tahu kapan cuci panel layak secara rupiah."
- **Energy gap:**
  - `[ISI: soiling loss PLTS di iklim tropis Indonesia, jurnal]` (studi Unram soiling 7 MWp ditemukan, tetapi halamannya minta login);
  - `[ISI: kapasitas PLTS atap Jatim, ESDM/PLN UID Jatim]`.
- **Pengguna:** pemilik PLTS atap rumah/sekolah/pabrik di Surabaya, installer/EPC di Jatim.
- **Pembayar:** EPC/installer (layanan O&M), pemilik pabrik.
- **AI di inti:** model regresi produksi yang diharapkan (irradiance satelit + suhu), lalu deteksi deviasi dan klasifikasi soiling vs shading vs fault inverter.
- **Aset:** simulasi PLTS `SwiftStudentChallenge2027\04_KODE\reference_model\simulate.py` (domain knowledge). **Lomba individu, cek aturan sebelum dipakai ulang.**
- **Jalur TKT 3:** data publik NREL PVDAQ `[ISI: lisensi]`. Estimasi 3–4 hari.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Saya pasang PLTS atap 3 kWp di rumah Surabaya. Aplikasi inverter sudah ada grafiknya, tapi saya tidak tahu angka normalnya berapa. Saya tidak mau bayar langganan lagi. Kalau installer saya yang menawarkan, mungkin."
- **Kritik juri (J3):** "Vendor inverter besar sudah memberi monitoring gratis. Di mana parit kompetitif Anda?"

### E7. DesaTerang: penjadwal beban baterai PLTS komunal off-grid dengan prakiraan
- **Aha:** "Di desa ber-PLTS komunal, lampu padam jam 1 pagi karena kipas dinyalakan jam 7 malam. AI yang memprakirakan cuaca besok bisa membagi baterai malam ini secara adil."
- **Energy gap:**
  - aset SSC mencatat 2,2 kWp / 2 kWh / ±6 jam di satu desa (dari `cv.md`, di luar repo; belum publik);
  - `[ISI: jumlah PLTS komunal off-grid di Jatim/kepulauan Madura, ESDM]`.
- **Pengguna:** operator PLTS desa (situs Sangiang, Banten, lewat kontak yang ada); pulau kecil Sumenep `[ISI: kontak]`.
- **Pembayar:** pemda/ESDM (program listrik desa), BUMDes.
- **AI di inti:** prakiraan irradiance + beban, lalu optimasi prioritas beban.
- **Aset:** `simulate.py` SSC (model fisika, bukan AI).
- **Jalur TKT 3:** ≥1 minggu (perlu data beban nyata).
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Saya operator PLTS desa. Kalau baterai habis, warga marahnya ke saya. Saya mau alat yang membatasi beban otomatis, asal tidak perlu internet."
- **Kritik juri (J4):** "Satu situs di Banten bukan 'Local' untuk Jatim, dan tanpa data beban ini masih simulasi."

### E8. EsCerdas: prakiraan pendaratan ikan untuk menjadwalkan produksi es & cold storage TPI
- **Aha:** "Pabrik es di pelabuhan memproduksi berdasarkan kebiasaan, bukan berdasarkan ikan yang akan datang. Prakiraan pendaratan mengurangi es yang mencair sia-sia dan ikan yang busuk karena es kurang."
- **Energy gap:**
  - ±35 % tangkapan hilang secara global (S7);
  - `[ISI: kWh per ton es balok + kapasitas pabrik es PPN Brondong]`.
- **Pengguna:** pengelola pabrik es/cold storage di PPN Brondong, PPP Muncar.
- **Pembayar:** pabrik es, pengelola pelabuhan.
- **AI di inti:** prakiraan volume pendaratan dari musim, cuaca, dan klorofil (OCEANS).
- **Aset:** OCEANS (sebagian).
- **Jalur TKT 3:** butuh data pendaratan harian `[ISI]`. Tidak tercapai sebelum deadline.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Saya pengelola pabrik es. Kalau es kurang, nelayan pindah ke pabrik lain. Lebih aman saya produksi lebih. Prakiraan baru berguna kalau salahnya lebih kecil dari insting saya."
- **Kritik juri (J1):** "Rantai sebab-akibat dari klorofil ke volume pendaratan ke kWh es terlalu panjang untuk divalidasi."

### E9. PilahPintar TPS3R: kamera di konveyor TPS3R untuk mengarahkan sampah ke BSF/kompos/RDF
- **Aha:** "TPS3R Tenggilis menerima 5 ton sampah sehari dengan 66 % organik (S6). Kamera yang menghitung komposisi per gerobak bisa mengarahkan lebih banyak sampah ke maggot BSF, bukan ke TPA."
- **Energy gap:**
  - S6 (Surabaya 1.800 ton/hari; TPS3R Tenggilis hanya mengelola 831 dari 1.952 ton/tahun yang masuk);
  - `[ISI: emisi metana TPA Benowo / energi angkut per ton]`.
  - Kaitan ke energi tidak langsung.
- **Pengguna:** pengelola TPS3R Tenggilis (Surabaya), TPS3R di Bandung untuk validasi cepat.
- **Pembayar:** DLH Kota, pengepul/offtaker RDF.
- **AI di inti:** deteksi objek / segmentasi komposisi sampah.
- **Aset:** tidak ada.
- **Jalur TKT 3:** dataset publik TACO `[ISI: lisensi]` + model pralatih. Estimasi 3 hari.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Saya petugas pilah. Saya sudah tahu mana yang organik tanpa kamera. Yang kurang itu tenaga dan alat pencacah, bukan data."
- **Kritik juri (J4):** "Pemilah sampah berbasis CV adalah ide hackathon yang paling sering muncul, dan energy gap-nya tidak langsung."

### E10. MeterSatu: disagregasi beban (NILM) UMKM dari satu titik meter
- **Aha:** "Satu sensor arus di meteran sudah cukup untuk tahu berapa rupiah yang dimakan freezer, mesin cuci, dan AC Anda."
- **Energy gap:** `[ISI: konsumsi listrik UMKM per golongan tarif]`.
- **Pengguna:** laundry, warung frozen food, kos-kosan.
- **Pembayar:** UMKM, PLN (program efisiensi), penjual peralatan hemat energi.
- **AI di inti:** disagregasi sinyal (seq2point / HMM).
- **Aset:** DSP FaceVitals (sebagian).
- **Jalur TKT 3:** dataset UK-DALE/REDD `[ISI: lisensi]`. Estimasi 3 hari, tetapi data rumah tangga Inggris tidak mewakili UMKM Indonesia.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Saya punya laundry kiloan. Saya tahu yang boros mesin pengering. Saya tidak mau tempel alat di meteran PLN, nanti dikira mencuri listrik."
- **Kritik juri (J2):** "Pasang CT clamp di sisi pelanggan perlu teknisi. Biaya per UMKM bisa lebih mahal dari penghematannya."

### E11. GeserPuncak: prakiraan beban & penjadwalan untuk pelanggan industri bertarif WBP/LWBP
- **Aha:** "Pabrik membayar lebih mahal di jam puncak. AI yang memprakirakan beban 24 jam ke depan bisa menggeser proses fleksibel ke luar jam puncak tanpa mengurangi produksi."
- **Energy gap:** `[ISI: selisih tarif WBP/LWBP golongan I-3/I-4, Permen ESDM tarif + URL]`.
- **Pengguna:** pabrik di SIER/PIER.
- **Pembayar:** pabrik.
- **AI di inti:** prakiraan beban + optimasi.
- **Aset:** tidak ada.
- **Jalur TKT 3:** butuh data beban pabrik `[ISI]`; dataset publik industri terbatas.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Jadwal produksi saya ditentukan pesanan, bukan tarif. Yang bisa digeser paling kompresor dan chiller, dan itu urusan orang utilitas."
- **Kritik juri (J1):** "Menggeser beban menghemat rupiah, belum tentu menghemat emisi. Tunjukkan profil emisi per jam grid Jamali."

### E12. KualitasDaya: klasifikasi gangguan kualitas daya (harmonik, sag) dari bentuk gelombang
- **Aha:** "Harmonik dari VFD dan beban non-linear memanaskan trafo diam-diam. AI kami membaca bentuk gelombang dan menunjukkan sumbernya."
- **Energy gap:** `[ISI: rugi energi akibat harmonik pada trafo distribusi, jurnal]`.
- **Pengguna:** engineer listrik pabrik, PLN UP3.
- **Pembayar:** pabrik, vendor filter harmonik.
- **AI di inti:** CNN/klasifikasi pada sinyal.
- **Aset:** keahlian elektronika daya tim (IFEC/MorphUPPU, dilepas), DSP FaceVitals.
- **Jalur TKT 3:** kebanyakan dataset PQ bersifat sintetis. Hanya TKT 3 sintetis dalam 3–4 hari.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Kami sudah punya power analyzer. Masalahnya, tidak ada yang sempat menganalisis datanya."
- **Kritik juri (J4):** "Divalidasi di data sintetis berarti belum terbukti apa-apa di lapangan."

### E13. PompaSurya Petani: rekomendasi konversi pompa irigasi diesel ke surya
- **Aha:** "Petani bawang di Nganjuk menyiram dengan pompa diesel. AI kami menghitung kapan pompa surya balik modal dari foto lahan dan pola tanam."
- **Energy gap:** `[ISI: konsumsi solar pompa irigasi Jatim, Kementan/BPS]`.
- **Pengguna:** kelompok tani.
- **Pembayar:** Dinas Pertanian, bank (kredit usaha).
- **AI di inti:** lemah; sizing pada dasarnya rumus fisika.
- **Aset:** `simulate.py` SSC (sebagian).
- **Jalur TKT 3:** tidak jujur sebagai "AI".
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Pompa surya mahal di depan. Yang saya butuh pinjaman, bukan aplikasi."
- **Kritik juri (J4):** "AI di sini tempelan, kalkulator spreadsheet sudah cukup."

### E14. SolarTepat: prakiraan kebutuhan solar per SPBU Nelayan (SPBUN)
- **Aha:** "82,2 % nelayan membeli BBM subsidi di atas harga subsidi (S5) karena SPBUN sering kosong saat cuaca bagus. Prakiraan permintaan bisa membuat stok datang sebelum antrean."
- **Energy gap:** S5 (akses BBM). Ini soal distribusi bahan bakar fosil, **bukan pengurangan karbon**.
- **Pengguna:** pengelola SPBUN, koperasi.
- **Pembayar:** Pertamina Patra Niaga / koperasi.
- **AI di inti:** prakiraan permintaan dari cuaca, musim ikan, dan klorofil.
- **Aset:** OCEANS (sebagian).
- **Jalur TKT 3:** butuh data penjualan SPBUN `[ISI]`.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Stok saya ditentukan kuota, bukan prakiraan. Kalau kuota habis ya habis."
- **Kritik juri (J3):** "Mitra kami fokus rendah karbon. Mengoptimalkan distribusi solar bertentangan dengan tesis investasi kami."

### E15. TagihanIndustri: pembaca tagihan PLN industri/hotel untuk deteksi denda kVARh dan daya kontrak berlebih
- **Aha:** "Banyak gedung membayar denda daya reaktif setiap bulan tanpa sadar. Agen kami membaca 12 tagihan terakhir dan menghitung ukuran kapasitor bank yang balik modal."
- **Energy gap:** `[ISI: aturan kelebihan kVARh dalam tarif PLN + URL]`, `[ISI: jumlah pelanggan B-3/I-3 di Jatim]`.
- **Pengguna:** engineering hotel/RS/pabrik.
- **Pembayar:** pelanggan, vendor kapasitor/ESCO (lead generation).
- **AI di inti:** ekstraksi tagihan (LLM + aturan) dan deteksi anomali. Sebagian besar keputusannya tetap aturan.
- **Aset:** Kendali (ekstraksi + kebijakan), keahlian elektronika daya tim (koreksi faktor daya).
- **Jalur TKT 3:** butuh contoh tagihan industri asli `[ISI: 5–10 tagihan dengan izin]`. Estimasi 1–2 hari setelah tagihan didapat.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Saya chief engineer hotel di Surabaya. Tagihan langsung ke bagian keuangan, saya jarang lihat rinciannya. Kalau ada yang bilang ada denda yang bisa hilang, saya dengar, tapi vendor kapasitor sudah sering datang menawarkan hal yang sama."
- **Kritik juri (J4):** "Ini aturan tarif dan perhitungan kapasitor; LLM hanya OCR mahal."

### N1. [NON-ENERGI] PanasKerja: pemantau beban panas pekerja luar ruang via rPPG di kamera ponsel
- **Aha:** "Surabaya makin panas. Mandor proyek bisa mengecek detak jantung pekerja hanya dari kamera ponsel saat istirahat."
- **Gap:** adaptasi iklim/K3. `[ISI: data heat stress pekerja konstruksi Indonesia]`.
- **Pengguna:** kontraktor, K3.
- **Pembayar:** kontraktor, asuransi.
- **AI di inti:** rPPG FaceVitals.
- **Aset:** FaceVitals (HR TKT 4 di data publik, **tetapi r ≈ 0,03**).
- **Jalur TKT 3:** belum diuji di kondisi panas/berkeringat/outdoor.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Pekerja saya tidak mau difoto-foto. Kalau ada yang pingsan baru kami bertindak."
- **Kritik juri (J1):** "Korelasi 0,03 dengan referensi tidak bisa dipakai untuk keputusan keselamatan."

### N2. [NON-ENERGI] CekNadi Posyandu: skrining HR tanpa kontak di posyandu lansia
- **Aha:** "Kader posyandu bisa mengukur nadi lansia dari kamera tanpa alat tambahan."
- **Gap:** kesehatan; tidak ada energy gap.
- **Pengguna:** kader posyandu, puskesmas.
- **Pembayar:** dinkes/puskesmas.
- **Aset:** FaceVitals.
- **Jalur TKT 3:** HR sudah TKT 4 di data publik, tetapi akurasinya belum klinis.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Kami sudah punya tensimeter digital yang juga mengukur nadi. Kenapa harus pakai kamera?"
- **Kritik juri (J4):** "Oksimeter jari murah sudah menyelesaikan masalah ini dengan akurasi klinis."

### N3. [NON-ENERGI, borderline] IzinSurya: asisten dokumen perizinan PLTS atap dengan guardrail regulasi
- **Aha:** "Calon pelanggan PLTS atap tersesat di persyaratan. Agen kami membaca dokumen mereka dan menjawab persis pasal mana yang belum dipenuhi."
- **Gap:** hambatan adopsi PLTS atap. `[ISI: nomor + isi regulasi PLTS atap berlaku, URL JDIH ESDM]`, `[ISI: waktu/biaya rata-rata pengajuan]`.
- **Pengguna:** rumah tangga, UMKM, installer.
- **Pembayar:** installer (efisiensi penjualan).
- **AI di inti:** QA dokumen dengan kebijakan (Kendali).
- **Aset:** Kendali.
- **Jalur TKT 3:** 3–4 hari.
- **Persona [SIMULASI PERSONA, bukan data wawancara]:** "Yang mengurus izin itu installer, bukan saya."
- **Kritik juri (J3):** "Pasar ini kecil dan tergantung satu regulasi yang bisa berubah."

---

## 3. Matriks skor

Bobot: TKT 3× · Gap 2× · Akses 2× · Mitra 1× · Unik 2×. Maks 50.

| Ide | TKT (×3) | Gap (×2) | Akses (×2) | Mitra (×1) | Unik (×2) | **Total** |
|---|---|---|---|---|---|---|
| **E5 DetakMesin** | 4 → 12 | 3 → 6 | 3 → 6 | 4 → 4 | 4 → 8 | **36** |
| **E2 TagihanJujur** | 4 → 12 | 3 → 6 | 4 → 8 | 4 → 4 | 3 → 6 | **36** |
| **E3 JadwalDingin** | 3 → 9 | 3 → 6 | 4 → 8 | 4 → 4 | 4 → 8 | **35** |
| E15 TagihanIndustri | 4 → 12 | 3 → 6 | 3 → 6 | 4 → 4 | 3 → 6 | 34 |
| E4 NafasGedung (FDD) | 3 → 9 | 4 → 8 | 3 → 6 | 4 → 4 | 3 → 6 | 33 |
| N3 IzinSurya | 3 → 9 | 2 → 4 | 3 → 6 | 4 → 4 | 4 → 8 | 31 |
| E6 PV-Sehat | 3 → 9 | 3 → 6 | 3 → 6 | 5 → 5 | 2 → 4 | 30 |
| N1 PanasKerja | 3 → 9 | 1 → 2 | 4 → 8 | 2 → 2 | 4 → 8 | 29 |
| E1 LautHemat | 3 → 9 | 3 → 6 | 2 → 4 | 3 → 3 | 3 → 6 | 28 |
| E9 PilahPintar | 3 → 9 | 2 → 4 | 4 → 8 | 3 → 3 | 2 → 4 | 28 |
| E10 MeterSatu | 3 → 9 | 2 → 4 | 3 → 6 | 3 → 3 | 2 → 4 | 26 |
| E14 SolarTepat | 1 → 3 | 3 → 6 | 2 → 4 | 2 → 2 | 5 → 10 | 25 |
| E7 DesaTerang | 2 → 6 | 2 → 4 | 2 → 4 | 4 → 4 | 3 → 6 | 24 |
| E8 EsCerdas | 1 → 3 | 3 → 6 | 2 → 4 | 3 → 3 | 4 → 8 | 24 |
| N2 CekNadi | 3 → 9 | 1 → 2 | 4 → 8 | 1 → 1 | 2 → 4 | 24 |
| E12 KualitasDaya | 2 → 6 | 2 → 4 | 2 → 4 | 3 → 3 | 3 → 6 | 23 |
| E11 GeserPuncak | 2 → 6 | 2 → 4 | 2 → 4 | 4 → 4 | 2 → 4 | 22 |
| E13 PompaSurya | 1 → 3 | 2 → 4 | 3 → 6 | 4 → 4 | 2 → 4 | 21 |

**Dasar skor (singkat):**
- **TKT:**
  - Nilai 4 hanya untuk ide yang inti AI-nya memakai kode yang **sudah lulus tes**: Kendali 116/116 (E2, E15) dan DSP FaceVitals 56/56 (E5). Klaim TKT 3 untuk domain baru bisa dicapai jujur dalam ±2 hari. E15 baru bisa mencapainya setelah ada tagihan industri asli.
  - Nilai 3 untuk model baru di atas data publik nyata (E1, E3, E4, E6, E9, E10).
  - Nilai 1–2 kalau data kuncinya tidak ada (E8, E11, E14) atau AI-nya lemah (E13).
  - N1/N2 tetap 3: HR sudah TKT 4, tetapi r ≈ 0,03 dan kondisi pakainya belum diuji.
- **Gap:**
  - Nilai 4 untuk E4: ada dua angka bersumber yang langsung terkait (S1 + S3).
  - Nilai 3 untuk ide yang punya angka konteks bersumber (S1, S2, S4, S5, S7), tetapi angka lokal Jatim masih `[ISI]`.
  - Nilai 2 kalau angka utamanya sendiri masih `[ISI]` atau kaitannya ke energi tidak langsung (E9).
  - Nilai 1 untuk non-energi.
- **Akses:**
  - Nilai 4 untuk pengguna yang bisa ditemui minggu ini dari Bandung: Sarpras ITB, UMKM/keluarga, TPS3R Bandung, pekerja/kader.
  - Nilai 3 kalau butuh perantara: manajemen pabrik/gedung/installer.
  - Nilai 2 untuk nelayan/pelabuhan/SPBUN/desa terpencil. Tim di Bandung, sementara lomba di Surabaya.
- **Mitra:**
  - Nilai 5 untuk surya.
  - Nilai 4 untuk efisiensi listrik dengan pembayar B2B.
  - Nilai 3 kalau pembayarnya publik/tidak jelas.
  - Nilai 2 untuk BBM fosil.
  - Nilai 1–2 untuk kesehatan.
- **Unik:**
  - Nilai 5 untuk SPBUN, sudut yang hampir pasti tidak dibawa tim lain.
  - Nilai 4 untuk cerita yang hanya tim ini bisa bawa: rPPG → motor (E5), jadwal kuliah sebagai sensor (E3), harmonisasi satelit (E1 turun ke 3 karena PPDPI diduga sudah ada).
  - Nilai 2 untuk ide pasaran: CV sampah, NILM, monitoring PV, load shifting.

---

## 4. Top 3

### #1 E5 DetakMesin (36/50): ide utama yang disarankan
- **Paling "Innovative" dan tidak bisa ditiru.** Cerita "pelacak detak jantung dari wajah → detak motor" lahir dari aset yang benar-benar kita punya dan sudah lulus tes. Hampir pasti tidak ada tim lain yang membawanya.
- **Energy gap besar dan bersumber kuat:** motor 45 % listrik dunia, potensi hemat 20–30 % (S4, IEA 4E). Ini bahasa yang dipahami profesor energi CityU/Tsinghua.
- **Cocok dengan kekuatan tim:** sinyal (rPPG) + elektronika daya (MCSA/arus motor). Pengguna B2B jelas (pabrik SIER/PIER, PDAM), dan ini investable.
- **Lubang yang harus ditutup:**
  - kaitan kuantitatif fault → kWh `[ISI: jurnal]`;
  - satu rekaman motor/pompa nyata (lab ITB atau pabrik).
  - Tanpa keduanya, J2 akan bilang "ini PdM, bukan energi".
- **Waktu:** 2 hari untuk dataset publik + baseline, 1–2 hari untuk rekaman lab. Bisa dikejar untuk deadline 1 Nov **hanya kalau** tim fokus penuh (bentrok dengan IBSC 1 Nov, lihat `00_INFO.md`).

### #2 E2 TagihanJujur (36/50, bisa digabung dengan E15): **pilihan paling realistis kalau deadline 1 Nov**
- **Kode ekstraksi + guardrail sudah ada dan lulus 116/116.** Adaptasi ke struk/tagihan PLN dan nota LPG adalah perubahan data, bukan arsitektur. Bukti TKT 3 bisa dikumpulkan dari tagihan asli milik tim sendiri dalam 1–2 hari.
- **Pengguna ada di sekitar tim**, dan ada faktor emisi Jamali bersumber (S2) untuk mengubah kWh → kgCO₂e.
- **Kelemahan:**
  - keunikan sedang;
  - "AI hanya hiasan" (catatan juri internal Kendali). Harus ada **angka LLM asli vs aturan saja** di tagihan asli;
  - asal-usul Kendali (FinTechathon) harus diungkapkan terang-terangan;
  - pembayar perlu divalidasi.
- **Saran:** gabungkan dengan E15 sebagai segmen B2B (hotel/pabrik dengan denda kVARh). Ini memberi pembayar yang lebih jelas dan memakai keahlian elektronika daya.

### #3 E3 JadwalDingin (35/50)
- **Sudutnya segar dan sangat mudah dijelaskan:** jadwal kuliah adalah sensor okupansi gratis. Didukung angka AC bersumber (S1).
- **Akses pengguna terbaik:** Sarpras ITB bisa ditemui minggu ini. Kampus ITS adalah pengguna lokal yang natural untuk co-design di Surabaya, dan juri ITS kemungkinan merasakan masalahnya sendiri.
- **Kelemahan:**
  - TKT 3 butuh 3–4 hari;
  - klaim kWh butuh data meter gedung `[ISI]`;
  - J2 akan bertanya "kenapa bukan timer". Jawabannya harus terletak pada **ekstraksi jadwal yang berantakan + prediksi kelas batal**, dengan angka akurasi.
- Memakai mesin kebijakan Kendali yang sama dengan E2, jadi kalau E2 dipilih, E3 bisa menjadi modul kedua.

**Cadangan yang patut dicatat:**
- **E4 NafasGedung (33):** gap terkuat (S1 + S3), tetapi tanpa aset sendiri dan FDD sudah komersial.
- **E1 LautHemat (28):** paling cocok dengan narasi "Local/Sustainable" dan aset OCEANS, tetapi akses nelayan dari Bandung, validasi tangkapan, dan pesaing PPDPI membuatnya berat sebelum deadline. Cocok sebagai roadmap Nov–Des.

---

## 5. `[ISI]` terpenting sebelum Fase 3
1. **Deadline registrasi ITS** (`00_INFO.md`). Ini menentukan pilihan antara E2 (aman 1 Nov) dan E5 (butuh fokus 3–4 hari).
2. **E5:** sumber jurnal kaitan fault motor/pompa → kenaikan kWh; akses ke 1 motor/pompa nyata (lab mesin listrik ITB / pabrik); lisensi dataset CWRU/Paderborn.
3. **E2/E15:** 20–30 tagihan/struk energi asli dengan izin (data pribadi disamarkan `[[...]]`); API key LLM untuk mengukur model asli; aturan kVARh PLN + URL; konfirmasi bahwa ITS tidak keberatan dengan karya yang sedang ikut FinTechathon.
4. **E3:** data kWh gedung kuliah + akses jadwal ruang dari Sarpras ITB/ITS.
5. Angka lokal Jatim yang belum ketemu: konsumsi listrik industri Jatim (Statistik PLN), FE Jamali terbaru (gatrik.esdm.go.id), kapasitas PLTS atap Jatim.

*Semua persona di dokumen ini adalah simulasi agen, bukan hasil wawancara. Wawancara asli dilakukan manusia di Fase 5.*
