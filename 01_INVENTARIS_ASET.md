# 01_INVENTARIS_ASET: aset AI yang sudah ada di repo, untuk Seno Hackathon ITS 2026
### Agen A2 "Auditor Aset" · 28 Okt 2026 · tim: Aziz (PIC), Uqi, Pio, Poggy

**Cara audit:**
- README/STATUS/JURI_90/hasil di tiap folder dibaca langsung.
- Tes dijalankan **dengan venv milik folder itu**, tanpa memasang paket baru.
- Folder `.venv*`, `node_modules`, `site-packages` dilewati. `.env*`, `bantuan-dana/`, `submission/private/` tidak dibuka.
- Tidak ada file sumber yang diubah. Satu efek samping: tes Kendali menulis ulang `deployments/pytest-31337.json`. File ini dibuat oleh fixture tes dan di-*gitignore* (`.gitignore:14`). `git status` di repo Kendali dan FaceVitals tetap bersih.
- Semua angka di bawah punya path sumber. Path relatif terhadap `C:\Users\POGGY\Downloads\barengpoggy\`.

**Definisi TKT yang dipakai** (Permenristekdikti 42/2016, versi brief):
- 3 = proof of concept: notebook/model jalan + uji awal.
- 4 = validasi komponen di lab: pipeline end-to-end di data uji, metrik vs baseline.
- 5 = validasi di lingkungan relevan: data/kondisi lapangan nyata.
- 6 = demo prototipe terintegrasi yang dipakai calon pengguna.

---

## 1. Tabel ringkas

Skala kecocokan 1–5 menilai Sustainable · AI Driven · Innovative · Local + Energy Gap, **dalam kondisi aset saat ini**, sebelum dipivot. Effort pivot adalah **estimasi auditor**, bukan hasil ukur.

| # | Aset (folder) | Yang benar-benar jalan | TKT jujur | Kecocokan (1–5) | Risiko orisinalitas | Effort pivot ke energi/lokal Jatim |
|---|---|---|---|---|---|---|
| A | **FaceVitals**: rPPG detak jantung dari video wajah (`FaceVitals2027-SPCup_GAJADI-DAFTAR\`) | Pipeline HR + demo real-time + paket submisi. **Tes 56/56 lulus** (dijalankan ulang hari ini). Dievaluasi di dataset nyata publik rppg_biases (n = 88) vs CHROM/POS/GREEN | **4** untuk HR (data nyata publik, ada baseline). SpO2/BP: **3** (hanya data sintetis). Bukan 5: tidak ada data lapangan sendiri/pengguna; r ≈ 0,03 | **2** (AI kuat; energi ±0; kesehatan boleh menurut FAQ) | **Rendah.** SP Cup **tidak jadi didaftar**, jadi tidak ada aturan lomba yang mengikat. Pemilik: Poggy + Aziz (commit awal oleh Aziz) | Tetap di kesehatan: rendah–sedang. Ke energi: **tinggi** (yang terpakai ulang hanya inti DSP, TKT turun) |
| B | **Kendali**: agen AI treasury dengan guardrail kebijakan + smart contract (`FinTechathon2026\kendali\`) | Agen end-to-end di devnet: ekstraksi invoice EN/ID/PDF, NLU, mesin kebijakan, kontrak. **Pytest 116/116 lulus** (dijalankan ulang hari ini). Eval 57/57 skenario. Bukti di testnet Sepolia | Sistem: **4** (data sintetis + testnet; belum ada bisnis/pengguna nyata). Komponen LLM: **3** (hanya stub offline; belum pernah diukur dengan model asli) | **2** (fintech; AI ada tetapi hasil utama dari aturan deterministik) | **Sedang.** Sedang aktif di FinTechathon (diterima, finalis diumumkan ≤31 Okt, final 20–23 Nov). Aturan: IP tetap milik peserta; tidak ditemukan larangan pakai ulang. Pemilik: Poggy + Aziz | **Sedang–tinggi.** Modul ekstraksi dokumen + guardrail bisa dipakai untuk tagihan energi; blockchain dibuang |
| C | **OCEANS**: harmonisasi klorofil-a MODIS→VIIRS, perairan Indonesia (`OCEANS2027-StudentPoster\`) | Pipeline analisis data satelit **nyata** (4,45 juta matchup), validasi silang LOYO, cek in-situ. Tidak ada tes otomatis. Bukti: CSV + log hasil | Komponen data/statistik: **4** (data nyata, ada baseline, validasi out-of-sample). **Komponen AI: belum ada.** Quantile mapping adalah statistik, bukan ML | **2,5** as-is (Sustainable/Local kuat, AI lemah). Potensi setelah pivot: 4 | **Rendah.** Pemilik tunggal: Poggy. OCEANS adalah abstrak paper (tenggat 15 Jan 2027). Di repo tidak ada aturan yang melarang pemakaian di hackathon | **Sedang.** Pipeline data siap; model AI (prakiraan) harus dibangun dari nol untuk komponen AI |
| D | **KalenderApi**: kalender api/karhutla MODIS–VIIRS (`KalenderApi-SpaceApps2026\`) | **Belum ada kode.** Hanya dokumen rencana 01–11 + `JURI_90/` | **1–2** (konsep + rencana) | 2 (lingkungan, tapi fokus Kalimantan/Sumatra; AI belum ada) | **Tinggi.** Aturan NASA Space Apps 2026 melarang mulai mengerjakan sebelum hackathon 14 Nov | Tidak disarankan sebelum 15 Nov |
| E | **JagaOrtu**: deteksi penipuan WhatsApp untuk lansia (`Hackvidia11-JagaOrtu\`) | **Tanpa kode aplikasi.** Proposal, wireframe, video, rancangan arsitektur. Data survei kosong (hanya header) | **2** (konsep teknologi + desain) | 1–2 (bukan energi) | **Tinggi** kalau Hackvidia masih dikejar: guidebook mensyaratkan karya belum pernah ikut kompetisi lain | Tinggi, dan tidak relevan |
| F | **SIGAP-IC**: ASIC detonator presisi (`Hackathon ITB\`) | Hanya dokumen + PDF. **Folder RTL/sim (`purwarupa/`) tidak ada di repo**, jadi tidak bisa diverifikasi. **Tidak ada komponen AI** | AI: **tidak ada**. Klaim di dokumen untuk perangkat keras: simulasi + sintesis + bitstream FPGA, belum silikon | **1** (tidak memenuhi syarat "purwarupa AI") | Sedang–tinggi: proyek pemenang DeepTech Smart-X dengan mitra industri; HKI/lisensi dibahas dengan mitra | Tidak disarankan |
| G | Lainnya (lihat §3) | Tidak ada model AI/ML. Di luar aset yang dicek, impor ML hanya muncul di kode vendor KiboRPC (`vision_opencv` milik ROS) | — | — | — | — |

---

## 2. Detail per aset

### A. FaceVitals: rPPG (HR, prototipe SpO2/BP) dari video wajah
**(1) Yang benar-benar jalan + bukti**
- **Tes, dijalankan ulang 28 Okt:** `.venv311\Scripts\python.exe -m pytest -q tests` → **`56 passed in 176.56s`**. Angka ini sama dengan klaim di `FaceVitals2027-SPCup_GAJADI-DAFTAR\STATUS.md` ("56 passed").
- **Evaluasi di data nyata publik** rppg_biases (88 rekaman, India + Sierra Leone, lisensi MIT menurut STATUS.md). Sumber angka: `FaceVitals2027-SPCup_GAJADI-DAFTAR\results\real\rppg_biases\by_condition.csv`, `paired_bootstrap.csv`, `summary.json`.
  - MAE FaceVitals (median per rekaman) **8,39 bpm**, RMSE 11,06, Pearson r **0,028**, AAMI EC13 terpenuhi 54,5 % rekaman (`by_condition.csv`, baris Baseline/facevitals/median).
  - Baseline pada trace yang sama (MAE): CHROM 10,18 · POS 15,82 · GREEN 19,09 (`STATUS.md` §Hasil NYATA, dari `by_condition.csv`).
  - Bootstrap berpasangan: FV lebih baik dari CHROM secara signifikan **hanya** di cahaya redup 50 lux dan 20 lux. Di C5 (10 fps + JPEG) CHROM yang lebih baik (`paired_bootstrap.csv`; ringkasan di `STATUS.md`).
  - Catatan jujur dari STATUS.md sendiri: r ≈ 0 untuk semua metode, **"Jauh dari agreement klinis."**
- **Uji semi-sintetis** (foto + denyut yang disuntikkan; *bukan* data nyata): `results\synthetic\dynamic_by_condition.csv`, `adaptive_before_after.csv`.
- **Demo real-time:** `facevitals\realtime.py` (webcam/file). Waktu proses stage 1 = 3,5 ms/frame, stage 2 = 150 ms/update di i7-13620H (`STATUS.md` §Laporan). Tidak ada log pemakaian oleh calon pengguna.
- **Paket submisi dry-run lulus checker:** `results\round1_dryrun_check.json` (`"ok": true`, 0 error). Isinya data semi-sintetis.
- **SpO2/BP:** model ada dan dites fit/predict dengan **data sintetis** (`STATUS.md` §Tes 23 Okt). Belum ada data nyata.

**(2) TKT jujur**
- HR: **TKT 4**. Pipeline end-to-end jalan di dataset nyata publik, dengan metrik vs baseline dan uji statistik.
- Bukan TKT 5: datanya bukan dari lapangan/kondisi pengguna kita sendiri, dan akurasinya belum memadai (r ≈ 0,03).
- SpO2/BP: **TKT 3** (hanya sintetis).

**(3) Kecocokan: 2/5**
| Prinsip | Penilaian |
|---|---|
| AI Driven | Kuat: DSP + MediaPipe + regresor SpO2/BP |
| Innovative | Sedang |
| Sustainable / Energy Gap | Hampir nol. Satu-satunya argumen: perangkat edge berdaya rendah (Raspberry Pi), dan itu belum diukur. **Timing Raspberry Pi masih TBD** (`STATUS.md`) |
| Local | Belum ada data/pengguna Jatim |

FAQ membolehkan sektor kesehatan. Tetapi juri condong ke energi, sehingga aset ini lemah di checklist "Energy Gap".

**(4) Pemilik dan risiko orisinalitas**
- **Pemilik:** commit awal "core pipeline" 9 Okt 2026 oleh **Mohammad Ari Alexander Aziz**; 6 commit lainnya oleh Poggy Macello (`git log` di folder ini). STATUS.md juga menyebut `.venv` lama dibuat di laptop Ari. Jadi Aziz dan Poggy keduanya ada di tim ITS. *Asumsi auditor: "Aziz" di tim ITS = Mohammad Ari Alexander Aziz.* `[ISI: konfirmasi]`
- **Aturan lomba asal:** SP Cup **tidak jadi didaftar**. Sumber: `05-PETA-TIM-vs-INDIVIDU-25okt2026.md` bagian C ("Lepas … Kodenya (56/56 tes lolos) tetap disimpan") dan nama folder `_GAJADI-DAFTAR`. Tidak ada aturan lomba yang mengikat.
- **Lisensi data:** rppg_biases MIT (`STATUS.md`). UBFC-rPPG hanya ground truth yang didapat, videonya tidak ("shared for research purpose"). **Risiko: rendah.**

**(5) Kecepatan pivot**
| Arah | Effort | Catatan |
|---|---|---|
| Tetap di kesehatan, dilokalkan (mis. skrining di layanan kesehatan Jatim) | Rendah–sedang | Kode siap. Butuh data/pengguna lokal untuk TKT 5 |
| Ke energi | Tinggi | Hanya teknik DSP yang terbawa (estimasi spektral, pelacak Viterbi, abstain berbasis SNR), mis. ke analisis sinyal beban/getaran mesin. TKT untuk aplikasi baru turun ke ±2–3 |

### B. Kendali: agen AI treasury dengan guardrail kebijakan
**(1) Yang benar-benar jalan + bukti**
- **Tes, dijalankan ulang 28 Okt** dengan `.venv-local`: **`116 passed, 2 warnings in 27.49s`**. Sama dengan klaim README ("116 / 116 pass"). Tes on-chain ikut lulus.
- **Evaluasi skenario:** `FinTechathon2026\kendali\reports\EVAL_REPORT.md` (dibuat 2026-10-23, devnet anvil, LLM mode off): **57/57 skenario lulus** (22 tugas + 35 serangan), task completion 100 %, attack prevention 100 %, 113 transaksi on-chain. Data invoice/vendor **sintetis** (`data/`, dibuat `scripts/make_data.py`).
- **Komponen AI/LLM:** `FinTechathon2026\kendali\reports\LLM_SCORECARD.md`.
  - Pada 10 invoice berantakan: aturan saja **3/10**, stub "pembaca sempurna" **10/10**, stub "pembaca disusupi" **2/10**. Penyerang tidak pernah didanai.
  - **Kedua kolom stub bukan pengukuran model.** File itu sendiri menulis: "No real model has been run yet".
- **Testnet publik:** `reports\TESTNET_EVIDENCE.md` (Sepolia, 14/14 langkah menurut README).
- **FISCO BCOS lokal:** `reports\FISCO_AGENT_RUN.md`.
- **Tes kontrak:** forge 33/33 (klaim README). **Tidak dijalankan ulang**, karena `forge`/`anvil` tidak ada di PATH shell auditor.

**(2) TKT jujur**
- Sistem: **TKT 4**. End-to-end di data uji sintetis, dengan metrik dan skenario serangan. Testnet bukan lingkungan bisnis nyata.
- Komponen "AI" yang sebenarnya (LLM pembaca dokumen): **TKT 3**. Hanya stub offline, belum ada angka model asli.
- Hasil 57/57 dicapai **tanpa LLM** (NLU + ekstraktor deterministik).

**(3) Kecocokan: 2/5**
| Prinsip | Penilaian |
|---|---|
| AI Driven | Sedang. Panel juri internal sendiri mencatat risiko "AI hanya hiasan" (`FinTechathon2026\kendali\submission\FINAL_PREP\JURI_90\SKOR.md`, F1) |
| Innovative | Kuat (guardrail + kontrak) |
| Sustainable / Energy Gap / Local | Lemah: domain pembayaran pemasok lintas negara |

**(4) Pemilik dan risiko orisinalitas**
- **Pemilik:** `CONTRIBUTORS.md` mencantumkan Poggy Macello Gultom (lead) dan Mohammad Ari Alexander Aziz. Lisensi MIT (`LICENSE`, "Copyright (c) 2026 Kendali team"). Semua 19 commit oleh Poggy.
- **Aturan lomba asal** (`FinTechathon2026\fintechathon-2026-international-track.md` §2): "IP | Tetap milik peserta; panitia boleh memakai karya untuk promosi non-komersial". Di repo **tidak ditemukan** larangan memakai karya di lomba lain.
- **Risiko praktis:**
  - Kendali sedang menunggu pengumuman finalis (≤31 Okt) dan mungkin final 20–23 Nov (`05-PETA-TIM-vs-INDIVIDU-25okt2026.md` bagian B). Waktu tim akan bentrok.
  - `STARTUP-2027\` juga merencanakan Kendali untuk CICSIC/HKUST-SINO.
- **Risiko: sedang.** Kalau dipakai, ungkapkan asal-usulnya terang-terangan. `[ISI: cek aturan Seno Hackathon soal karya yang sedang/pernah dilombakan]`

**(5) Kecepatan pivot: sedang–tinggi**
- Yang bisa dipakai ulang:
  - pipeline ekstraksi dokumen EN/ID/PDF (`kendali/invoices.py`, `nlu.py`, `llm.py`) beserta tesnya;
  - pola "LLM mengusulkan, aturan memutuskan";
  - audit trail.
- Contoh arah: membaca tagihan/struk energi (listrik, LPG, BBM) untuk UMKM atau gedung, lalu memberi rekomendasi penghematan.
- Smart contract/blockchain kemungkinan dibuang.
- Untuk domain baru, TKT ekstraksi kembali ke **3** sampai ada data uji tagihan asli.

### C. OCEANS: harmonisasi klorofil-a MODIS→VIIRS (perairan Indonesia)
**(1) Yang benar-benar jalan + bukti**
- Skrip `OCEANS2027-StudentPoster\analysis\01–13_*.py` (+ `run_all.bat`), dengan log `results\run02–09.log`. **Tidak ada tes otomatis.** Skrip tidak dijalankan ulang (butuh data mentah ±besar), jadi buktinya adalah CSV hasil.
- Data satelit **nyata**, publik, tanpa login (NASA L3 lewat ERDDAP; `01_ABSTRAK.md`). Data in-situ: kompilasi kapal + BGC-Argo.
- **Angka** (`OCEANS2027-StudentPoster\results\loyo_summary.csv`):
  - N = 4.452.710 matchup;
  - log-RMSD offset global (H0) 0,1131 → regresi bertingkat (H2) 0,0960 → **quantile mapping bertingkat (H3) 0,0974**;
  - rasio sd H3 1,0013 vs H2 0,9648.
- **Uji alarm** (`results\events_controlled_loyo_2012_2016.csv`, region ALL): Cohen's κ raw (H0) **0,669** → QM (H3) **0,745**; F1 0,726 → 0,788.
- **In-situ** (`results\insitu_ship_stats.csv`): 69 piksel-bulan kapal. log-RMSD raw 0,332 vs harmonized 0,320. Abstrak sendiri menyebut keduanya **setara** (CI selisih melewati nol).
- **Cakupan Jatim:** kotak sub-wilayah `JAV` (Laut Jawa, 105,5–117° BT, 7–3,5° LS) dan `SJU` (upwelling selatan Jawa, 102–116° BT, 11–8,6° LS) di `analysis\common.py` mencakup **sebagian** perairan sekitar Jatim. Selat Bali dan Selat Madura belum dipisah sebagai wilayah sendiri.

**(2) TKT jujur**
- Komponen pengolahan data: **TKT 4**. Pipeline end-to-end di data nyata, validasi leave-one-year-out vs baseline, ditambah cek in-situ.
- **Komponen AI: belum ada (setara TKT 0–1).** QM/CDF matching dan regresi adalah statistik. Abstrak v3 sendiri mengakui QM sebagai "metode baku" (`JURI_90\SKOR.md` G1).
- **Tidak memenuhi syarat "purwarupa AI" kalau diajukan apa adanya.**

**(3) Kecocokan: 2,5/5 as-is, berpotensi 4 setelah pivot**
| Prinsip | Penilaian |
|---|---|
| Sustainable | Kuat (pemantauan laut/perikanan) |
| Local | Sedang: Indonesia, sebagian Jatim |
| AI Driven | Lemah, sampai ada model ML |
| Energy Gap | Hanya tidak langsung. Mis. BBM kapal nelayan yang terbuang untuk mencari daerah tangkap, `[ISI: angka konsumsi BBM nelayan Jatim dari KKP/BPS/DKP Jatim, dengan URL]` |

**(4) Pemilik dan risiko orisinalitas**
- **Pemilik tunggal:** Poggy (lead author di `01_ABSTRAK.md`; satu-satunya author di git).
- **Aturan lomba asal:** OCEANS 2027 SPC adalah kompetisi abstrak/paper. Tenggat 15 Jan 2027 (`00_ATURAN.md` §2). Riset yang sama direncanakan juga untuk IGARSS (`05-PETA-TIM-vs-INDIVIDU-25okt2026.md`).
- Di repo **tidak ditemukan** aturan yang melarang karya dipakai di hackathon. `[ISI: cek kebijakan prior publication di portal OCEANS/IEEE begitu akun dibuat]`
- **Risiko: rendah.** Catatan: ITS memakai 4 anggota, sedangkan OCEANS mewajibkan Poggy sebagai lead author/presenter. Itu tidak bertentangan.

**(5) Kecepatan pivot: sedang**
- Pipeline unduh, regrid, stratifikasi, dan validasi siap pakai.
- Yang harus dibangun:
  1. model AI, mis. prakiraan klorofil/SST → peta potensi daerah tangkap;
  2. baseline pembanding (mis. persistensi / klimatologi);
  3. metrik out-of-sample.
- Komponen AI baru mencapai TKT 3 setelah model dilatih dan diuji. Itu harus **dibuat dulu sebelum didaftarkan**.

### D. KalenderApi: kalender musim api MODIS–VIIRS (NASA Space Apps)
1. **Yang jalan:** tidak ada kode, notebook, atau data olahan. Isinya dokumen `01-…11-*.md` dan `JURI_90/` (`SKOR.md`: "Yang dinilai adalah rencana"; kode dibuat 14–15 Nov).
2. **TKT 1–2** (konsep dirumuskan).
3. **Kecocokan: 2/5.** Lingkungan/karhutla dan data satelit, tetapi fokusnya Kalimantan/Sumatra (`02-konteks-indonesia-karhutla.md`) dan belum ada AI.
4. **Pemilik:** Poggy (git). Tim Space Apps direncanakan 4–5 orang di local event Bandung. **Aturan:** FAQ 2026 yang dikutip di `KalenderApi-SpaceApps2026\JURI_90\SKOR.md` menyebut tim tidak boleh mengerjakan tantangan sebelum hackathon dimulai. Membangun purwarupa sekarang untuk ITS dengan ide yang sama berisiko dianggap mulai lebih awal. **Risiko: tinggi** sebelum 14 Nov.
5. **Pivot:** tidak disarankan sebelum hackathon selesai (15 Nov).

### E. JagaOrtu: pendamping anti-penipuan WhatsApp untuk lansia (Hackvidia)
1. **Yang jalan:**
   - Pipeline **dokumen** (`build_all.py` membangun PDF/wireframe/video).
   - **Tidak ada kode aplikasi/model**: `07_Final_24Jam\ARSITEKTUR_MVP.md` baris 3 menulis "Dokumen desain saja, **tanpa kode**".
   - `06_Riset_Pengguna\data\*.csv` hanya berisi header (1 baris). Folder `contoh_FIKTIF\` berisi contoh fiktif, bukan data.
2. **TKT 2** (konsep + arsitektur L0 aturan / L1 TF-IDF+LR / L2 LLM di atas kertas).
3. **Kecocokan: 1–2/5.** Kelompok rentan, bukan energi.
4. **Pemilik:** nama anggota masih `[ISI]` di `config_tim.json`. Git: Poggy.
   - **Aturan:** `arkavidia-11-analisis-pendaftaran-09okt2026.md` baris 166: guidebook mensyaratkan solusi "belum pernah diikutsertakan di kompetisi lain". Surat orisinalitas yang disiapkan (`build\surat.py` baris 63) juga berbunyi "belum pernah diikutsertakan dalam kompetisi lain".
   - Final Hackvidia juga mensyaratkan "Semua kode dibuat saat final".
   - **Risiko: tinggi**, selama Hackvidia masih opsi (pendaftaran 31 Okt).
5. **Pivot:** tidak relevan untuk energi, dan memakainya bisa menggugurkan Hackvidia.

### F. SIGAP-IC: ASIC detonator presisi (Hackathon ITB / DeepTech Smart-X)
1. **Yang jalan (menurut dokumen, tidak bisa diverifikasi):** `Hackathon ITB\MENTORING_HARI_2_SIGAP_Updated.md` dan `KIMI_STATUS.md` melaporkan:
   - `tb_top_dual` 74/74, Ascon 3281/3281 vektor, bus N = 200 6/6;
   - rantai pemicu (timer 10/10, TMR 13/13, …);
   - area 0,087 mm².

   **File RTL/testbench (`purwarupa/…`) tidak ada di repo**, sama seperti dicatat di `02-STATUS-LENGKAP-23okt2026.md` ("file sumbernya tidak ada di folder ini"). Tes tidak bisa dijalankan.
2. **Komponen AI: tidak ada** (front-end aman NFC/bus/auth/timer/TMR, analog HV). Perangkat keras menurut dokumen: simulasi + sintesis + bitstream FPGA, "belum silikon".
3. **Kecocokan: 1/5** untuk syarat "purwarupa AI". Catatan: berita ITS menyebut fokus semikonduktor (SDG 9), tetapi syarat AI tetap tidak terpenuhi.
4. **Pemilik/tim:** peran di dokumen mentoring: Ari (juru bicara), Syauqi (operator demo), Heart (bisnis), Poggy (analog). *Asumsi auditor: Ari = Aziz dan Syauqi = Uqi*, `[ISI: konfirmasi]`.
   - Status: **menang** DeepTech Smart-X 23 Okt (`05-PETA-TIM-vs-INDIVIDU-25okt2026.md`).
   - Ada mitra industri (Hariff) untuk bagian analog HV, dan HKI/model lisensi sedang dibahas dengan mitra (`MENTORING_HARI_2_SIGAP_Updated.md` bagian peran/sesi 2). **Risiko: sedang–tinggi** (HKI bersama mitra, anggota Heart tidak ada di tim ITS).
5. **Pivot:** tidak disarankan.

---

## 3. Folder lain di root (sudah discan, tidak ada model AI)
| Folder | Isi kode | AI/ML? | Catatan relevan |
|---|---|---|---|
| `CodeAChip-ISSCC27\` | Notebook LDO + POR + RF energy harvesting SKY130 | Tidak | Tema energi (harvesting), tapi sirkuit analog, bukan AI. Sedang dikirim ke Code-a-Chip |
| `IFEC2027_ITB_DILEPAS\` | Kalkulasi + simulasi switching konverter (MorphUPPU) | Tidak | Elektronika daya; lomba sudah dilepas 26 Okt |
| `SwiftStudentChallenge2027\04_KODE\` | App Swift "Lights On, Sangiang" + `reference_model/simulate.py` (model energi PLTS desa) | Tidak (model fisika/simulasi) | **Domain knowledge PLTS off-grid** yang relevan untuk narasi energi. Angka 2,2 kWp / 2 kWh / ±6 jam ada di `02_KONSEP.md` (sumbernya `cv.md`, di luar repo). Swift Student Challenge adalah lomba individu, jadi cek aturannya sebelum dipakai ulang |
| `KiboRPC7\` | Perencana rute Held-Karp + model waktu + simulator | Tidak (optimasi klasik). Impor OpenCV hanya di kode vendor ROS | Tes ada (`tests/test_all.py`), tidak dijalankan karena bukan aset AI |
| `APS-SDC2027_DILEPAS\`, `CASS-SDC2027_GUGUR-MEMBERSHIP\` | Simulasi antena/FDTD, simulasi energi | Tidak | Dilepas/gugur |
| `IEEEXtreme20_GAJADI-DAFTAR\`, `AtCoder-AHC-WTF2027\` | Library competitive programming | Tidak | — |
| `STARTUP-2027\` | Skrip deck/unit economics untuk KENDALI & KALENDERAPI | Tidak | Menunjukkan Kendali/KalenderApi juga direncanakan untuk lomba startup lain |
| `Wasit-SeaxOpenAI-2026\` | Hanya skrip proposal dana (`bantuan-dana/`, **tidak dibuka**) | Tidak | Hackathon 7 Nov; kode dibuat di hari-H |
| `AFMAM-EAS2026`, `AIBuilder2026-Xdemia`, `APAN63-Fellowship`, `EAGx*`, `FORMULIR`, `IGARSS2027`, `TreeHacks2027`, `USTC-WinterCamp2027` | Tidak ada kode | — | Dokumen aplikasi |

---

## 4. Aset di luar repo
`[ISI: proyek AI milik Aziz/Uqi/Pio yang tidak ada di repo]`. Untuk tiap proyek, sebutkan: nama proyek, tautan repo/notebook, apa yang sudah jalan (model, data, metrik + file hasil), pernah/sedang diikutkan ke lomba apa beserta aturan orisinalitasnya, dan siapa saja pemiliknya. Prioritaskan proyek bertema energi, lingkungan, atau Jatim/Surabaya.

---

## 5. Rekomendasi basis (2–3 aset)
Ada satu syarat yang menentukan: **saat daftar, purwarupa AI sudah harus TKT ≥ 3.** Deadline registrasi masih belum diketahui (`00_INFO.md`). Kalau deadline-nya dekat (mis. 1 Nov), hanya aset yang **sudah** punya komponen AI berjalan yang aman diklaim, yaitu A dan B.

1. **OCEANS → "AI prakiraan daerah tangkap untuk menghemat BBM nelayan Jatim"** (paling cocok dengan juri; perlu kerja paling banyak sebelum daftar).
   - **Kelebihan:**
     - data nyata, publik, dan tanpa login, dengan pipeline TKT 4;
     - pemilik tunggal Poggy, risiko orisinalitas rendah;
     - Sustainable/Local kuat;
     - energy gap bisa dirumuskan sebagai BBM terbuang, `[ISI: angka bersumber]`.
   - **Syarat:** komponen ML (prakiraan + baseline + metrik out-of-sample) harus dibangun dan diuji **sebelum** daftar supaya klaim "AI TKT 3" jujur. Klaim TKT 4 hanya berlaku untuk pipeline data.
   - **Langkah pertama:** pengguna nyata (nelayan/penyuluh di Jatim) untuk validasi.
2. **Kendali (modul ekstraksi dokumen + guardrail) → agen AI pembaca tagihan energi untuk UMKM/gedung.**
   - **Kelebihan:**
     - kode dan tes sudah jalan (116/116);
     - pemiliknya Poggy dan Aziz, keduanya di tim ITS;
     - pola "LLM mengusulkan, aturan memutuskan" mudah dijelaskan.
   - **Kekurangan:**
     - AI-nya belum pernah diukur dengan model asli;
     - perlu data tagihan asli untuk domain baru, sehingga TKT kembali ke 3;
     - sedang aktif di FinTechathon. Ungkapkan asal-usulnya, dan cek apakah ITS keberatan.
3. **FaceVitals (cadangan, jalur sektor kesehatan).**
   - **Kelebihan:**
     - bukti AI terkuat di repo: TKT 4 di data nyata publik, 56/56 tes;
     - pemilik Poggy + Aziz;
     - tidak terikat lomba lain.
   - **Kekurangan:** hampir tidak ada energy gap, dan akurasinya jauh dari klinis (r ≈ 0,03).
   - Pakai ini kalau tim memilih sektor kesehatan, atau kalau deadline terlalu dekat untuk membangun komponen AI baru.

**Jangan dipakai:**
- **KalenderApi:** aturan NASA melarang mulai sebelum 14 Nov.
- **JagaOrtu:** syarat orisinalitas Hackvidia; selain itu belum ada kode.
- **SIGAP-IC:** tidak ada AI, ada HKI mitra, dan sumbernya tidak ada di repo.
