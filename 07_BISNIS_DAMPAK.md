# 07_BISNIS_DAMPAK: model bisnis, unit economics, dan dampak DetakPompa
### Agen A8 "Analis Bisnis" · 28 Okt 2026 · tim: Aziz (PIC), Uqi, Pio, Poggy

**Dasar:** `04_KEPUTUSAN.md`, `03_RISET.md` (S1–S43), `03b_ADVOKAT_SETAN.md` §2, `06_VALIDASI_PENGGUNA.md` (§0 F1–F10, §6.6 L1–L10), `00_INFO.md`, ditambah teks lengkap S6 yang diekstrak ulang (pdftotext, 28 Okt 2026) dan sumber baru B1–B11 (§10).

**Aturan baca:**
- `[Sx]` = sumber di `03_RISET.md`. `[Bx]` = sumber baru yang **benar-benar dibuka** agen ini (§10).
- **[ASUMSI]** = angka karangan tim untuk keperluan hitungan. Wajib diganti data nyata sebelum dipakai di berkas lomba. `[ISI]` = data belum ada.
- "Hitungan sendiri" = aritmetika dari angka bersumber. Semua langkahnya ditulis.
- Tidak ada satu pun angka di dokumen ini yang berasal dari pengukuran tim atau wawancara pengguna. Belum ada wawancara (`06` §7 masih kosong).

---

## 0. Posisi produk (setelah koreksi `06_VALIDASI_PENGGUNA.md`)

Tiga fakta dari teks lengkap S6 mengubah cara produk dijual:
1. **Efisiensi pompa butuh debit (Q) dan head (H)**: Ph = 0,163 × Q × H, η = Ph/Pi [S6]. Arus dan getaran saja **tidak bisa** menghitung efisiensi (`06` F4).
2. **Tiap panel pompa di IPA Ngagel I sudah punya power meter Schneider EasyLogic PM2100** [S6]. kW per pompa kemungkinan sudah tersedia. Yang mahal dan manual adalah Q dan H (flowmeter ultrasonik portabel + manometer).
3. **SEC IPA Ngagel I 0,27 kWh/m³ (2021) dan 0,29 kWh/m³ (2022)**, sudah di bawah standar < 0,4 kWh/m³ [S6]. Di level IPA, manajemen bisa merasa "sudah efisien". Masalahnya baru terlihat **per pompa**: 5 dari 12 pompa yang diaudit berefisiensi di bawah ±55 % [S6].

**Maka DetakPompa diposisikan sebagai alat triase**, bukan "AI pengukur efisiensi" dan bukan "PDAM boros":

> DetakPompa memantau tiap pompa terhadap **baseline pompa itu sendiri**. Datanya kW/arus/cos φ dari power meter panel yang sudah ada, ditambah getaran. Keluarannya adalah **urutan pompa yang paling patut diukur debitnya atau direkondisi lebih dulu**, dengan KPI **kW pada tekanan/debit setara** dan **Rp/bulan selisih terhadap baseline**. KPI dampak di tingkat stasiun adalah **kWh/m³ pada permintaan atau tekanan header yang sama** (§3.3, catatan Hanson). Kalau sinyal jelek atau kondisi operasi berubah (katup, permintaan zona), sistem **abstain dan menyebut langkah berikutnya**.

Tiga rantai yang **harus dipisah tegas** di semua angka di bawah:

| Mata rantai | Siapa yang melakukan | Apa yang bisa diklaim DetakPompa |
|---|---|---|
| ① **Alat menandai** perubahan relatif dan mengurutkan pompa | DetakPompa | Ketepatan urutan, tingkat salah alarm, tingkat abstain. **Hanya ini** yang kelak bisa diukur sebagai kinerja produk |
| ② **Audit memastikan**: ukur Q dan H, hitung η | Tim PDAM/auditor dengan flowmeter | Tidak ada. Ini kerja manusia dengan alat ukur standar |
| ③ **Rekondisi menghemat** kWh | PDAM (anggaran, izin *downtime*, teknisi) | Tidak ada. Hemat hanya terjadi **kalau PDAM menindaklanjuti** |

Yang boleh dihitung sebagai "nilai DetakPompa" hanyalah **kWh yang dihemat lebih awal** karena pompa yang menurun ketahuan lebih cepat (atau ketahuan sama sekali, untuk pompa yang tidak tercakup audit). Nilai rekondisinya sendiri milik PDAM.

---

## 1. Lean Canvas

| Kotak | Isi |
|---|---|
| **1. Masalah** | (a) Di antara 22 pompa satu IPA, hanya sebagian yang terukur saat audit: 5 dari 8 pompa air baku dan 7 dari 14 pompa distribusi di Ngagel I [S6]. (b) Pompa yang menurun tidak terlihat di SEC bulanan IPA, karena SEC IPA sudah 0,27–0,29 kWh/m³ [S6]. (c) Anggaran rekondisi terbatas, jadi keputusan "pompa mana dulu" diambil dari audit sesekali + pengalaman [H, `06` H3/H4]. **Alternatif yang ada:** audit energi manual (flowmeter portabel), log panel per shift, vendor PdM (OPTIME [S16], Groundup.ai [S18]), kemitraan *smart water* Schneider–PDAM [S7] |
| **2. Segmen pelanggan** | **Early adopter:** PDAM Surya Sembada Surabaya, IPA Ngagel I (6 IPA total [S6]). **Berikutnya:** 38 Perumda air minum di Jatim [B7]. **Sekunder** (narasi downtime, bukan energi; `06` L8): gedung/RS/hotel, kampus, tenant SIER/PIER |
| **3. Nilai unik (UVP)** | "Tahu pompa mana yang perlu diukur debitnya minggu ini, dalam bahasa kW dan Rp, **dari data panel yang sudah Anda punya**, dan alat yang berani bilang *tidak tahu* lalu menyebut langkah berikutnya." |
| **4. Solusi** | (a) Pembaca data panel PM2100 (RS-485/Modbus pada varian PM2120 [B8]; varian di PDAM `[ISI]`) + node getaran murah. (b) Baseline per pompa per titik operasi (tekanan kalau tersedia). (c) Skor perubahan + abstain berbasis SNR/kualitas data, selalu dengan langkah berikut (`06` L4). (d) Laporan mingguan: urutan pompa, ΔkW vs baseline, estimasi Rp/bulan, tindakan yang disarankan sesuai praktik S6 (rawat rutin / cek impeller / overhaul). (e) **Offline/on-prem**, tanpa koneksi ke SCADA (`06` L7) |
| **5. Saluran** | Fase 0: **pilot riset ITS–PDAM** lewat penulis S6 (Teknik Lingkungan ITS) dan DIKST/LPPM ITS (`06` §5.2). Fase 1+: forum PD Perpamsi Jatim (Rakerda dihadiri dirut Perumda dari 38 kab/kota [B7]), studi kasus bersama ITS, auditor/manajer energi (PP 33/2023 [S1]) |
| **6. Arus pendapatan** | Fase 0: **tidak ada** (riset). Fase 1: **kampanye triase** per IPA (jasa, berbatas waktu). Fase 2: **langganan per pompa per bulan** (perangkat lunak on-prem + dukungan). Fase 3 (opsional): berbagi hasil ala ESCO, hanya kalau M&V dengan Q dan H tersedia. Rincian §2 |
| **7. Struktur biaya** | Node sensor ±Rp0,99 jt/pompa (§3.1, sebagian [ASUMSI]), edge per IPA ±Rp7,5 jt, pemasangan, waktu analis/dukungan `[ISI]`, cloud pengembangan US$6/bulan [B4]. Biaya izin & pengadaan (waktu, dokumen) `[ISI]` |
| **8. Metrik kunci** | **Presisi top-3**: dari 3 pompa teratas yang ditandai, berapa yang terbukti menurun saat diukur Q dan H. Tingkat salah alarm per bulan. Tingkat abstain. ΔkW pada tekanan setara. **Rasio tindak lanjut**: berapa tanda yang berujung audit/rekondisi. kWh yang dihemat setelah rekondisi, diukur PDAM |
| **9. Keunggulan tak mudah ditiru** | **Jujur: belum ada yang benar-benar "unfair".** Kandidatnya: (a) jalur co-design ke PDAM lewat paper bersama ITS–PDAM [S6], tapi **belum dihubungi**; (b) data audit S6 sebagai *ground truth* awal (pompa baik vs buruk sudah diketahui); (c) teknik abstain dari FaceVitals, tapi tekniknya DSP umum (`03b` §2.2). Semuanya bisa ditiru vendor besar |

---

## 2. Siapa membayar dan berapa

### 2.1 Pembayar per fase

| Fase | Pembayar | Bentuk | Kenapa bentuk ini |
|---|---|---|---|
| **0. Pilot riset** (Nov 2026 – ±Mar 2027) | **Tidak ada pembelian.** Biaya perangkat ditanggung tim / hibah riset `[ISI: skema hibah LPPM ITS atau program pra-inkubasi lomba]` | Kerja sama riset ITS–PDAM di 1–2 pompa yang kondisinya sudah diketahui dari S6 | Persona S-2 (simulasi, `06` §6.2): "lewat kerja sama dengan ITS, bukan pembelian". Board Manual: pembelian masuk RKAP dan SOP pengadaan (`06` §0). **Tidak ada uang, hadiah, atau honor untuk staf PDAM** (ada pengendalian gratifikasi) |
| **1. Kampanye triase** | PDAM (unit produksi / program efisiensi) | Jasa berbatas waktu, mis. 3 bulan per IPA, keluaran laporan urutan pompa + rekomendasi pompa yang perlu diukur Q dan H | Mirip jasa audit, jadi lebih mudah masuk pos anggaran yang sudah ada daripada sistem TI baru `[ISI: validasi H7]` |
| **2. Langganan** | PDAM, lewat RKAP tahunan | Per pompa per bulan; perangkat keras dijual putus atau dipinjamkan | Setelah ada bukti presisi triase di Fase 0–1 |
| **3. Berbagi hasil (ESCO)** | PDAM membayar dari penghematan terukur | Persentase dari kWh hemat setelah rekondisi | **Belum layak.** Butuh M&V dengan Q dan H, dan hemat bergantung pada keputusan rekondisi PDAM (mata rantai ③). Kontrak kinerja untuk BUMD `[ISI: aturan]` |

### 2.2 Harga pembanding

| Pembanding | Harga | Sumber | Catatan kejujuran |
|---|---|---|---|
| Augury (AS), PdM per mesin | **US$50–200 per mesin per bulan**; implementasi US$15.000–319.000 | [B6] | **Estimasi pihak ketiga**, bukan daftar harga resmi. Hitungan sendiri dengan kurs Rp17.917/US$ [B5]: **Rp0,90–3,58 jt per mesin per bulan** |
| Schaeffler OPTIME, SKF, ABB | Tidak ketemu harga yang bisa dibuka | — | `[ISI]`. Listing distributor Schaeffler di RS Components muncul di pencarian, tetapi tidak jelas apakah itu OPTIME dan halamannya tidak dibuka |
| Include Technology Indonesia, Groundup.ai | Tidak ketemu | [S17], [S18] | `[ISI]` |
| Biaya audit energi bersertifikat untuk 1 IPA | Tidak ketemu | — | `[ISI]`. Pembanding paling relevan untuk harga kampanye triase |

### 2.3 Harga yang diusulkan (semua [ASUMSI])

| Produk | Harga usulan | Dasar |
|---|---|---|
| Kampanye triase 3 bulan, 1 IPA (22 pompa) | **[ASUMSI] Rp30 jt** `[ISI: bandingkan dengan biaya audit energi]` | Biaya dasar (hitungan sendiri, §3.1): perangkat bisa dipakai ulang; pasang 22 × Rp0,5 jt = Rp11 jt; sisanya waktu analis `[ISI]` |
| Langganan | **[ASUMSI] Rp300.000 per pompa per bulan** | ±⅓ dari batas bawah estimasi Augury (Rp0,90 jt). Sengaja jauh lebih murah karena produk kita lebih sempit (triase, tanpa garansi aset, tanpa jaringan layanan) |

---

## 3. Unit economics

### 3.1 Biaya per pompa dan per IPA

Kurs: **Rp17.917/US$** (JISDOR 6 Okt 2026, dikutip media [B5]; `[ISI: cek kurs BI saat berkas ditulis]`).

| Komponen | Harga | Rupiah | Sumber | Catatan |
|---|---|---|---|---|
| Mikrokontroler ESP32-DevKitC-32E | US$10,00 | Rp179.170 | [B1] Digi-Key, qty 1 | Kelas pengembangan, bukan industri |
| Akselerometer MEMS ADXL343 (breakout) | US$5,95 | Rp106.606 | [B2] Adafruit | ODR maks **3.200 Hz** [B2], jadi pita efektif < 1,6 kHz. Putaran pompa Ngagel I ±1.483–1.493 rpm [S6] ≈ **24,8 Hz** (hitungan sendiri: 1.489/60). Cukup untuk 1×, harmonik, dan frekuensi sudu; **tidak cukup** untuk envelope bearing frekuensi tinggi. Untuk triase ini bisa diterima |
| Penginderaan arus, **mode A: baca PM2100 di panel** | — | `[ISI]` (transceiver RS-485 + kabel) | [S6], [B8] | Varian **PM2120** punya port RS-485 [B8]. Varian yang terpasang di Ngagel I dan izin membacanya `[ISI]` |
| Penginderaan arus, **mode B: clamp sendiri** | — | `[ISI]` | — | Harga SCT-013 di marketplace **tidak bisa dibuka** (Tokopedia timeout), jadi tidak dipakai. Catatan teknis: arus motor Ngagel I **97–326 A per fasa** [S6 Tabel 2], melebihi clamp hobi 100 A. Perlu CT lebih besar atau clamp di sekunder CT panel `[ISI: rating CT panel]` |
| Enclosure IP65, catu daya, kabel, magnet dudukan | — | **[ASUMSI] Rp700.000** | — | `[ISI: harga nyata]` |
| **Node per pompa (mode A)** | | **Rp985.776** | hitungan sendiri | 179.170 + 106.606 + 700.000 |
| Pemasangan per pompa | — | **[ASUMSI] Rp500.000** | — | `[ISI]`. Non-invasif, tanpa membuka panel |
| Edge per IPA: Raspberry Pi 5 16 GB | US$305 | Rp5.464.685 | [B3] | Batas atas. Varian RAM lebih kecil lebih murah, tapi harganya tidak tampil di halaman [B3] |
| SSD, UPS kecil, switch per IPA | — | **[ASUMSI] Rp2.000.000** | — | `[ISI]` |
| Cloud | US$6/bulan (1 GiB) | Rp107.502/bulan | [B4] | **Hanya untuk pengembangan/demo tim.** Data PDAM tetap on-prem (`06` L7) |

**Capex 1 IPA (22 pompa)**, hitungan sendiri:
- Node + pasang per pompa = 985.776 + 500.000 = **Rp1.485.776**.
- 22 pompa × Rp1.485.776 = Rp32.687.072.
- Edge = 5.464.685 + 2.000.000 = Rp7.464.685.
- **Total ≈ Rp40,2 jt** (Rp40.151.757). Lebih dari separuhnya [ASUMSI].

**Opex PDAM (langganan)** = 22 pompa × Rp300.000 × 12 bulan = **Rp79,2 jt/tahun** [ASUMSI harga].

**Biaya PDAM tahun 1** = 40,2 + 79,2 = **Rp119,4 jt**. Tahun 2 dan seterusnya = Rp79,2 jt.

Sisi vendor: pendapatan Rp3,6 jt per pompa per tahun. Biaya dukungan per pompa (kunjungan, analis, garansi) `[ISI]`, jadi margin kontribusi belum bisa dihitung.

### 3.2 Angka dasar dari sumber

| Angka | Nilai | Sumber |
|---|---|---|
| Biaya energi PDAM Surya Sembada 2021 | Rp147.654.439.569; 24,37 % biaya operasional; listrik unit produksi 76 % energi PDAM; Rp409/m³ (nasional Rp356,34/m³) | [S6] |
| Konsumsi listrik IPA Ngagel I | **14.738.920 kWh (2021)**; 15.066.960 kWh (2022) | [S6] Tabel 4 |
| Produksi IPA Ngagel I | 54.041.746 m³ (2021); 51.878.025 m³ (2022) → SEC 0,27 / 0,29 kWh/m³ | [S6] Tabel 4 |
| Lima pompa terukur yang buruk (Ph hidraulik / Pi listrik / η total) | Air baku U6: 63,97 / 117,90 kW / 54,26 %. Distribusi U6: 98,30 / 189,90 / 51,76 %. T1: 78,74 / 158,20 / 49,77 %. S1: 110,71 / 216,30 / 51,18 %. S2: 112,72 / 214,30 / 52,60 % | [S6] Tabel 3 |
| Batas praktik | η ≥ 60 % → rawat rutin; ≤ 50 % → perbaikan total/ganti | [S6] |
| Kasus keausan | η 65,2 % → 53,6 % (celah wear-ring terbuka) | [S10] |
| Tarif | **Rp1.035,78/kWh** LWBP golongan B-3/TM dan I-3/TM; WBP = K × LWBP, 1,4 ≤ K ≤ 2 | [S19]. **Golongan tarif PDAM `[ISI]`** |

Catatan: angka efisiensi pompa air baku U2/U3/U5 di S6 (88,77–92,91 % total *wire-to-water*) sangat tinggi untuk pompa sentrifugal. Kami tidak memakainya di hitungan, tapi itu tanda bahwa pengukuran audit sendiri punya ketidakpastian `[ISI: tanyakan ke penulis S6]`.

### 3.3 Langkah 1: nilai rekondisi (milik PDAM, **bukan** klaim DetakPompa)

Rumus (hitungan sendiri): kalau pompa direkondisi ke efisiensi target η_t pada Q dan H yang sama, Pi_baru = Ph/η_t, dan ΔP = Pi − Ph/η_t.

| Pompa | Pi (kW) | ΔP bila η_t = 60 % (batas "rawat rutin" S6) | ΔP bila η_t = 65,2 % (nilai sebelum aus di S10) |
|---|---|---|---|
| Air baku U6 | 117,90 | 117,90 − 63,97/0,60 = **11,28** | 19,79 |
| Distribusi U6 | 189,90 | 189,90 − 163,83 = **26,07** | 39,13 |
| T1 | 158,20 | 158,20 − 131,23 = **26,97** | 37,43 |
| S1 | 216,30 | 216,30 − 184,52 = **31,78** | 46,50 |
| S2 | 214,30 | 214,30 − 187,87 = **26,43** | 41,42 |
| **Total** | 896,60 | **122,53 kW** (rata-rata 24,51 kW/pompa) | **184,27 kW** |

Jam operasi per pompa **tidak ada di S6** `[ISI: log PDAM]`. Pakai dua asumsi: 50 % (4.380 jam/tahun) dan 80 % (7.008 jam/tahun). Sebagai cek kewajaran: total Pi 12 pompa terukur = 1.652,73 kW, dan rata-rata beban IPA = 14.738.920/8.760 = 1.682,5 kW (hitungan sendiri). Jadi banyak pompa kemungkinan jalan hampir terus, tetapi ini tidak membuktikan jam per pompa.

| | 122,53 kW × 4.380 j | 122,53 kW × 7.008 j | 184,27 kW × 4.380 j | 184,27 kW × 7.008 j |
|---|---|---|---|---|
| kWh/tahun | 536.681 | 858.690 | 807.103 | 1.291.364 |
| Rp/tahun (× Rp1.035,78) | Rp555,9 jt | Rp889,4 jt | Rp836,0 jt | Rp1.337,6 jt |
| % listrik IPA Ngagel I 2021 | 3,6 % | 5,8 % | 5,5 % | 8,8 % |

**Ini nilai yang sudah ditemukan audit manual S6.** DetakPompa tidak boleh mengklaimnya. Biaya rekondisi per pompa `[ISI]` belum dikurangkan. Status rekondisi pompa-pompa ini sejak 2024 juga `[ISI]`; bisa jadi sudah diperbaiki.

**Catatan KPI (Hanson 2002).** Nilai di atas menghitung kW yang turun bila η naik pada Q dan H yang sama. Di lapangan, pompa yang direkondisi biasanya memompa **lebih banyak**, sehingga kW-nya bisa **naik**: dari 63 uji pompa irigasi sebelum/sesudah perbaikan, efisiensi rata-rata naik 33 %, tetapi daya input naik di 58 % instalasi (rata-rata +17 %). Energi baru turun (rata-rata −22 %) kalau **volume air yang dipompa tetap** [Hanson, *California Agriculture* 56(4), 2002, peer-reviewed; pompa irigasi deep-well, bukan PDAM; `11_RISET_KELEMAHAN.md` L6.4]. Di PDAM, hemat hanya terjadi kalau permintaan zona yang sama dilayani dengan lebih sedikit pompa paralel atau jam operasi yang lebih pendek. Karena itu KPI dampak = **kWh/m³ per stasiun pada permintaan atau tekanan header yang sama**, bukan "kW pompa turun". Bukti bahwa program pemantauan efisiensi di utilitas air bisa balik modal: Wellington Water, 34 pompa air curah, hemat listrik 8 % (±$200 rb/tahun dari $2,5 jt), payback < 3 bulan (`11` L6.3). Label: laporan utilitas + konsultan, **bukan peer-review**, metode termodinamik (bukan getaran). Angka ini **tidak** berarti DetakPompa menghemat 8 %.

### 3.4 Langkah 2: nilai yang bisa diatribusikan ke DetakPompa

Rumus (hitungan sendiri):
> kWh_atribusi = jumlah kejadian penurunan/tahun × ΔP per kejadian × jam operasi selama "waktu lebih awal"
> waktu lebih awal = selisih antara kapan DetakPompa menandai dan kapan PDAM akan tahu tanpa alat (audit berikutnya, atau tidak pernah, untuk pompa di luar cakupan audit)

Semua parameter skenario adalah **[ASUMSI]**. Kontrafaktual "kapan PDAM akan tahu sendiri" adalah `[ISI: interval audit nyata, `06` H4/H5]`.

| Parameter | Konservatif | Moderat |
|---|---|---|
| Kejadian penurunan yang ditandai **dan** ditindaklanjuti PDAM per IPA per tahun | 1 | 2 |
| ΔP per kejadian | 11,28 kW (terkecil di tabel §3.3) | 24,51 kW (rata-rata 5 pompa, η_t = 60 %) |
| Waktu lebih awal | 3 bulan | 6 bulan |
| Utilisasi pompa | 50 % | 80 % |
| Jam efektif | 3/12 × 8.760 × 0,5 = 1.095 j | 6/12 × 8.760 × 0,8 = 3.504 j |
| **kWh/tahun** | 1 × 11,28 × 1.095 = **12.352 kWh** | 2 × 24,51 × 3.504 = **171.766 kWh** |
| **Rp/tahun** (× Rp1.035,78) | **Rp12,8 jt** | **Rp177,9 jt** |
| Biaya PDAM tahun 1 (§3.1) | Rp119,4 jt | Rp119,4 jt |
| **Payback** (biaya tahun 1 / nilai per bulan) | 119,4 / (12,8/12) ≈ **112 bulan**, praktis **tidak balik modal** (lebih lama dari umur perangkat) | 119,4 / (177,9/12) ≈ **8 bulan** |
| Neto tahun 2 | 12,8 − 79,2 = **−Rp66,4 jt** | 177,9 − 79,2 = **+Rp98,7 jt** |

**Titik impas** (lebih jujur daripada skenario): langganan Rp79,2 jt/tahun ÷ Rp1.035,78/kWh = **76.464 kWh/tahun**. Artinya, DetakPompa untuk 22 pompa baru layak kalau dalam setahun membuat **satu pompa yang menurun ±24,5 kW direkondisi ±3.120 jam operasi lebih awal** (±4,3 bulan kalau pompa jalan 24 jam). Kalimat ini bisa dipertahankan di depan juri karena setiap angkanya bisa dicek.

### 3.5 Uji sensitivitas (dari skenario moderat; satu parameter diubah tiap baris)

| Perubahan | kWh/tahun | Nilai (Rp jt/th) | Biaya th-1 (Rp jt) | Payback (bulan) | Neto th-2 (Rp jt) |
|---|---|---|---|---|---|
| Dasar moderat | 171.766 | 177,9 | 119,4 | 8,1 | +98,7 |
| Waktu lebih awal 3 bulan | 85.883 | 89,0 | 119,4 | 16,1 | +9,8 |
| Hanya 1 kejadian/tahun | 85.883 | 89,0 | 119,4 | 16,1 | +9,8 |
| ΔP 11,28 kW (bukan 24,51) | 79.050 | 81,9 | 119,4 | 17,5 | +2,7 |
| Utilisasi 50 % | 107.354 | 111,2 | 119,4 | 12,9 | +32,0 |
| Tarif rata-rata dengan WBP (K = 1,4 selama 5 jam/hari) [ASUMSI jam WBP] → Rp1.122,10/kWh | 171.766 | 192,7 | 119,4 | 7,4 | +113,5 |
| Harga langganan Rp600.000 | 171.766 | 177,9 | 198,6 | 13,4 | +19,5 |
| Harga langganan Rp150.000 | 171.766 | 177,9 | 79,8 | 5,4 | +138,3 |

**Bacaan:**
- Hasil paling peka terhadap **jumlah kejadian yang benar-benar ditindaklanjuti** dan **waktu lebih awal**. Keduanya bergantung pada perilaku PDAM (mata rantai ③), bukan pada AI.
- Dua parameter "buruk" sekaligus (mis. 1 kejadian + 3 bulan) membuat langganan **tidak balik modal**. Jadi Fase 1 (kampanye triase berbatas waktu) lebih aman untuk dijual lebih dulu daripada langganan.
- Biaya salah alarm (kunjungan flowmeter ke pompa yang ternyata baik) **belum dikurangkan** `[ISI: biaya satu kunjungan ukur]`.

---

## 4. Dampak lokal: kWh dan tCO₂e

### 4.1 Faktor emisi
- **Jamali 0,87 tCO₂/MWh (kasus 1) / 0,80 (kasus 2)** dari tabel JCM yang bersumber nilai FE 2019 Ditjen Gatrik ESDM [S21]. Agen membuka ulang PDF-nya: nilai ini ada di Tabel 2-1. Tabel 2-2 khusus proyek PV memuat 0,613/0,533 untuk Jamali, dan **tidak dipakai** di sini karena DetakPompa bukan proyek PV.
- FE Jamali terbaru dari ESDM: **tidak ketemu** pada pencarian 28 Okt 2026. `[ISI: FE GRK sistem interkoneksi Jamali terbaru dari gatrik.esdm.go.id]`

### 4.2 Pilot → kota (hitungan sendiri; tCO₂e = MWh × FE)

| Skala | Jenis angka | MWh/tahun | tCO₂e/tahun (0,87) | tCO₂e (0,80) |
|---|---|---|---|---|
| **Pilot Fase 0: 1–2 pompa** | Hemat langsung dari pilot | **0** | **0** | 0 |
| Pilot, kalau 1 pompa ditandai lalu direkondisi | Rekondisi 1 pompa (mis. T1, 26,97 kW pada η_t 60 %, utilisasi 80 %) | 26,97 × 7.008 / 1.000 = 189,0 | 164 | 151 |
| 1 IPA (Ngagel I), **atribusi DetakPompa** | §3.4 konservatif / moderat | 12,4 / 171,8 | **10,7 / 149** | 9,9 / 137 |
| 1 IPA, **nilai rekondisi** (milik PDAM, §3.3) | rentang | 536,7 – 1.291,4 | 467 – 1.123 | 429 – 1.033 |
| Kota (6 IPA PDAM [S6]) | **Ilustrasi saja**, dengan asumsi tiap IPA mirip Ngagel I (**belum diverifikasi**) | 6 × 171,8 = 1.031 (moderat, atribusi) | ±897 | ±825 |

**Penjelasan wajib di pitch:**
- Pilot riset **tidak menghemat kWh**. Pilot hanya membuktikan mata rantai ① (presisi triase).
- Penghematan diukur sebagai **kWh/m³ per stasiun pada permintaan yang sama**, bukan kW pompa: setelah rekondisi, kW pompa bisa naik karena debitnya naik [Hanson 2002; §3.3].
- Hemat terjadi **hanya kalau PDAM mengaudit lalu merekondisi** pompa yang ditandai. Angka tCO₂e baris 2–5 bersyarat pada keputusan itu.
- Baris "kota" butuh kWh dan jumlah pompa tiap IPA `[ISI]`. Jangan tampilkan tanpa label "ilustrasi".
- Pembanding skala: listrik IPA Ngagel I 14.738,9 MWh/tahun [S6] ≈ 12.823 tCO₂e (× 0,87, hitungan sendiri). Atribusi moderat ≈ 1,2 % dari itu. Angka ini kecil, dan memang sebaiknya kecil supaya bisa dipertahankan.

---

## 5. Jalur adopsi di Jawa Timur

| Tahap | Waktu (target) | Isi | Syarat lulus ke tahap berikutnya | Peran regulasi |
|---|---|---|---|---|
| **0. Pilot riset ITS–PDAM** | Nov 2026 – Mar 2027 | 1–2 pompa Ngagel I yang kondisinya diketahui dari S6 (mis. satu pompa "baik" dan satu "buruk") sebagai *ground truth*. Baca PM2100 bila diizinkan, plus node getaran. Offline. **Bukan pembelian, tanpa pemberian apa pun ke staf** | Izin tertulis (H1); DetakPompa membedakan pompa baik/buruk di data nyata; tingkat abstain wajar | — |
| **1. Kampanye triase 1 IPA** | 2027 | 22 pompa, 3 bulan, laporan urutan + pompa yang perlu diukur Q dan H | **Presisi top-3 terukur** (dicek dengan flowmeter PDAM); ≥1 tanda ditindaklanjuti (H4) | Masukan untuk **program konservasi** dan audit energi (PP 33/2023, Permen ESDM 8/2025 [S1, S2]). **Bukan pengganti** auditor bersertifikat |
| **2. 6 IPA PDAM Surya Sembada** | RKAP berikutnya `[ISI: siklus]` | Langganan | Neto positif sesuai §3.4, diukur PDAM | Sama |
| **3. Perumda lain di Jatim** | 2028+ | **38 Perumda** (Rakerda PD Perpamsi Jatim 24 Nov 2025 dihadiri dirut Perumda dari 38 kab/kota [B7]). Saluran: forum Perpamsi Jatim + studi kasus ITS | Studi kasus Surabaya terbit; ada mitra pemasang lokal | Pengadaan BUMD diatur peraturan kepala daerah masing-masing (PP 54/2017 Pasal 93, seperti dikutip di [B9]) → **38 aturan berbeda**. Jumlah pompa per Perumda `[ISI]` |
| **4. Industri SIER/PIER** | Setelah Tahap 3 | Pompa utilitas/proses. **Narasi downtime**, bukan energi (`06` L8) | Ada produk dengan sertifikasi industri `[ISI]` | Industri ≥4.000 TOE/tahun wajib manajemen energi [S1]. Jumlah tenant SIER/PIER resmi `[ISI]`; angka di hasil pencarian tidak dibuka, jadi tidak dipakai |
| **5. Nasional** | Jangka panjang | PDAM/Perumda di luar Jatim | — | Jumlah anggota Perpamsi nasional `[ISI]`; angka di cuplikan media tidak dibuka |

**PP 33/2023 dan ambang TOE** [S1]: penyedia energi ≥6.000 TOE/tahun, industri ≥4.000, transportasi ≥4.000, bangunan gedung ≥500.
- Hitungan sendiri (konversi 1 TOE = 11,63 MWh, seperti di `03_RISET.md` §3.2): IPA Ngagel I saja = 14.738,92 MWh / 11,63 ≈ **1.267 TOE (2021)**.
- PDAM masuk kategori mana, apakah ambang dihitung per entitas atau per lokasi, dan apakah listrik dikonversi dengan faktor energi final atau primer: semuanya `[ISI: teks PP 33/2023 dan Permen ESDM 8/2025]`. Jadi **jangan menulis "PDAM wajib manajemen energi"** sebelum dicek.
- Kalau wajib, DetakPompa bisa dijual sebagai **alat bantu data** untuk laporan kinerja energi tahunan dan prioritas audit [S2], bukan sebagai audit itu sendiri.

---

## 6. Posisi terhadap pesaing

| | **DetakPompa** (rencana) | Schneider (mitra *smart water* PDAM [S7]; PM2100 di panel [S6]) | Schaeffler OPTIME [S16] | SKF (Enlight/IMx-1) | ABB Ability Smart Sensor | Augury | Include Technology Indonesia (startup ITS) [S17] |
|---|---|---|---|---|---|---|---|
| Fokus | Triase pompa: ΔkW dan Rp/bulan vs baseline sendiri | Meter energi, *smart water* | Getaran nirkabel: imbalance, misalignment, longgar | Getaran + suhu, dalam kontrak layanan | Sensor motor LV | Getaran/suhu/magnetik + AI | IoT, deteksi kegagalan, PdM |
| Bicara kWh/Rp per pompa? | **Ya (tujuan)**, belum terbukti | Data kW ada; analitik triase per pompa `[ISI]` | Tidak disebut | Tidak diverifikasi | Klaim hemat hanya dari cuplikan, **tidak dipakai** | Studi kasus yang terlihat tentang biaya perawatan | Tidak disebut |
| Abstain eksplisit | **Ya**, dengan langkah berikut | `[ISI]` | Tidak disebut | — | — | — | — |
| Memakai data panel yang ada | **Ya (mode A)** | Ya, milik mereka | Tidak, sensor sendiri | Tidak | Tidak | Tidak | `[ISI]` |
| Harga | [ASUMSI] Rp300 rb/pompa/bulan | `[ISI]` | `[ISI]` | `[ISI]` | `[ISI]` | Estimasi US$50–200/mesin/bulan [B6] | `[ISI]` |
| Kehadiran lokal | Tim mahasiswa; jalur ITS–PDAM belum dihubungi | **Sudah bermitra dengan PDAM** [S7] | Global | Global | Global | Global | **ITS, Surabaya**; juara 3 University Startup World Cup 2023 [S17] |

**Di mana kita kalah (jujur):**
- Perangkat keras bersertifikat industri, baterai nirkabel, jaringan layanan, garansi, rekam jejak: semua pesaing global unggul. Node kita memakai komponen kelas pengembangan [B1, B2].
- **Schneider sudah ada di dalam PDAM** [S7] dan memiliki meter di panel [S6]. Kalau Schneider menambah analitik triase, posisi kita hilang.
- Include berada di kampus yang sama dan kemungkinan dikenal juri ITS.
- Model yang dilatih di Paderborn (CC BY-NC [S12]) **tidak boleh dijual** tanpa izin. Produk komersial harus memakai Ottawa (CC BY [S13]) dan data sendiri.

**Di mana kita beda (masih hipotesis):**
1. Keluaran berupa **urutan tindakan dalam kW dan Rp**, sesuai bahasa manajer energi (`06` L3). Pesaing yang dibuka menonjolkan downtime.
2. **Abstain + langkah berikut** (`06` L4). H6 belum diuji.
3. **Tanpa sensor arus baru** kalau PM2100 bisa dibaca. Capex turun, dan juga lebih sedikit benda asing di rumah pompa.
4. **On-prem, tanpa sambungan ke SCADA**, cocok dengan kekhawatiran keamanan data BUMD (`06` L7).
5. **Validasi dengan audit S6 sebagai *ground truth***. Tidak ada pesaing yang punya titik awal ini di Surabaya, tetapi titik awal ini juga bisa dipakai siapa saja.

---

## 7. Risiko dan mitigasi

| # | Risiko | Peluang / dampak | Mitigasi |
|---|---|---|---|
| R1 | **Akses data dan izin** (H1). Pemasangan alat butuh izin Direksi; data tidak boleh keluar | Tinggi / fatal | Jalur riset ITS–PDAM; mulai dari **mode baca saja** (data panel yang dicatat operator, atau ekspor yang disetujui); lokasi pilot cadangan di Sarpras ITB untuk TKT 4 (`06` §5.2). Lama waktu izin dicatat sebagai data |
| R2 | **Keamanan OT.** Membaca RS-485/Modbus tetap berarti menyambung ke jaringan operasional | Sedang / tinggi | Hanya baca (tanpa perintah tulis), edge offline, tanpa koneksi internet/SCADA, persetujuan tertulis TI PDAM, dokumentasi kabel. Kalau ditolak: node getaran mandiri + data kW dari log manual |
| R3 | **Akurasi (H2).** Perubahan kW bisa karena katup, permintaan zona, atau titik operasi, bukan aus. Pompa S1/S2 dipasang 2018 tapi sudah ±52 % [S6] | Tinggi / tinggi | Baseline per titik operasi (pakai tekanan kalau ada); abstain saat kondisi berubah; klaim hanya "perubahan relatif → ukur Q dan H", **bukan** "efisiensi". Lapor presisi top-3 apa adanya |
| R4 | **Salah alarm** menghabiskan kunjungan flowmeter dan menghilangkan kepercayaan (persona S-2, simulasi) | Sedang / tinggi | Ambang dipilih untuk presisi, bukan sensitivitas; maksimal N tanda per bulan; laporan tingkat salah alarm ke pengguna; biaya per kunjungan `[ISI]` masuk perhitungan nilai |
| R5 | **Adopsi organisasi BUMD.** Direksi dipilih kepala daerah; anggaran lewat RKAP tahunan; Dewan Pengawas menyetujui transaksi (Board Manual, `06` §0). Alat hibah sering mati setelah tim pergi (persona S-5, simulasi) | Tinggi / tinggi | Champion di level kepala IPA; mulai dengan produk jasa berbatas waktu (Fase 1); README perawatan, komponen murah yang bisa diganti, serah terima ke unit (`06` L10) |
| R6 | **Pengadaan.** BUMD memakai aturan pengadaan yang ditetapkan kepala daerah (PP 54/2017 Pasal 93 seperti dikutip [B9]); Perpres 16/2018 kadang dirujuk sebagai dasar hukum [B9]. Aturan Kota Surabaya, relevansi e-katalog LKPP, dan syarat TKDN `[ISI]`. Startup tanpa badan hukum dan rekam jejak sulit ikut | Tinggi / tinggi | Fase 0–1 lewat kerja sama riset ITS (bukan pengadaan); bentuk badan usaha `[ISI]` sebelum Fase 2; pertimbangkan bermitra dengan integrator yang sudah terdaftar sebagai vendor PDAM |
| R7 | **Gratifikasi.** Board Manual memuat pengendalian gratifikasi | Rendah (kalau patuh) / fatal | Tidak ada uang, hadiah, honor, atau voucher untuk staf PDAM. Ucapan terima kasih cukup berupa laporan hasil |
| R8 | **Klaim energi tidak terjadi** karena PDAM tidak merekondisi (anggaran/downtime; H4) | Sedang / tinggi untuk narasi dampak | Pisahkan mata rantai ①②③ di semua materi; KPI produk = presisi triase, bukan kWh |
| R9 | **Pesaing incumbent** (Schneider [S7]) menambah fitur serupa | Sedang / tinggi | Posisikan sebagai lapisan analitik yang **membaca** meter Schneider, bukan pengganti; cari peran sebagai mitra |
| R10 | **Lisensi data** (Paderborn CC BY-NC [S12]) | Pasti untuk komersial | Model komersial dilatih ulang di Ottawa CC BY [S13] + data sendiri |

**Tiga risiko terbesar:** R1 (akses/izin), R3 (akurasi tanpa Q dan H), R5 + R6 (adopsi dan pengadaan BUMD).

---

## 8. Relevansi untuk mitra lomba di Demo Day (business matching)

| Mitra | Apa yang mereka kerjakan (bersumber) | Apa yang mungkin menarik bagi mereka | Apa yang **jujur belum siap** |
|---|---|---|---|
| **InvestHK** | Badan promosi investasi Pemerintah Hong Kong; membantu perusahaan luar negeri, dari multinasional hingga startup, merencanakan, mendirikan, dan memperluas usaha lewat Hong Kong [B10] | Hanya relevan kalau ada rencana masuk HK/Greater Bay Area | **Tidak ada rencana ekspansi ke HK.** Pasar kita PDAM/Perumda Indonesia. Jangan dipaksakan; cukup minta masukan jaringan |
| **Kerogen CelerateX** | Kerogen dikenal sebagai GP *private equity* berbasis HK yang mengkhususkan diri pada investasi energi internasional, dengan fokus historis migas hulu [B11]. Fokus terbarunya (SAF, panas bumi) hanya terlihat di cuplikan LinkedIn, **tidak dibuka** | Narasi **kWh dan tCO₂e terukur per pompa**, model ringan modal (membaca meter yang sudah ada), bisa direplikasi ke 38 Perumda Jatim [B7] | **Pra-pendapatan, TKT 3 (data rig bantalan publik, belum pompa; lihat `05_BUKTI_TKT.md`)**, tanpa data lapangan, tanpa badan hukum `[ISI]`, ukuran pasar dalam Rp belum bisa dihitung. Untuk investor, kita belum *investable*; yang bisa diminta adalah mentoring atau akses pilot |
| **CityU School of Energy & Environment** | Mitra strategis lomba (`00_INFO.md`). Halaman riset CityU SEE kosong saat dibuka, jadi cakupan risetnya **tidak dikutip** | Kemungkinan kolaborasi riset nexus energi–air (pompa air minum, M&V) [tafsiran] | Belum ada data atau publikasi yang bisa dibagi; belum ada kontak |
| **Tsinghua University, Green & Low-carbon Technology Committee, Garage Plus** | Tidak diriset di dokumen ini | `[ISI]` | `[ISI]` |

**Satu kalimat jujur untuk Demo Day:** "Kami belum menghemat satu kWh pun. Yang kami bawa adalah cara menunjuk pompa mana yang perlu diukur duluan, dengan angka presisi [ISI: hasil pilot] dari pilot bersama ITS–PDAM. Penghematannya datang dari rekondisi yang dilakukan PDAM, dan kami ukur bersama mereka."

---

## 9. `[ISI]` terpenting dari dokumen ini
1. Jam operasi per pompa, golongan tarif PLN PDAM, dan status rekondisi U6/T1/S1/S2 sejak 2024. Ketiganya menentukan semua angka §3–§4.
2. Varian power meter di panel Ngagel I (PM2110 atau PM2120 ber-RS-485) dan izin membacanya.
3. Interval audit nyata, sebagai kontrafaktual "waktu lebih awal" (§3.4).
4. Biaya satu kunjungan ukur debit, biaya rekondisi per pompa, biaya audit energi 1 IPA (pembanding harga).
5. FE Jamali terbaru (Gatrik ESDM); kategori PDAM menurut PP 33/2023 dan cara konversi TOE.
6. Aturan pengadaan BUMD Kota Surabaya; relevansi e-katalog/TKDN; badan hukum tim.
7. Harga nyata: clamp/CT kelas industri, enclosure, catu daya, pemasangan.
8. Jumlah pompa per IPA lain dan per Perumda Jatim (ukuran pasar).

---

## 10. Sumber baru yang dibuka agen ini (28 Okt 2026)

| ID | Sumber | URL | Dipakai untuk |
|---|---|---|---|
| B1 | Digi-Key, Espressif ESP32-DEVKITC-32E | https://www.digikey.com/en/products/detail/espressif-systems/ESP32-DEVKITC-32E/12091810 | US$10,00 (qty 1) |
| B2 | Adafruit, ADXL343 breakout (produk 4097) | https://www.adafruit.com/product/4097 | US$5,95; ODR 0,1–3.200 Hz |
| B3 | Raspberry Pi 5 | https://www.raspberrypi.com/products/raspberry-pi-5/ | 16 GB US$305 (varian lain tidak tampil harganya) |
| B4 | DigitalOcean, Droplet pricing | https://www.digitalocean.com/pricing/droplets | US$6/bulan (1 GiB) |
| B5 | JournalArta, 6 Okt 2026 (mengutip JISDOR BI) | https://journalarta.com/news/2026/10/06/rupiah-hari-ini-6-oktober-2026/ | Rp17.917/US$. Media sekunder; cek situs BI |
| B6 | SoftwareFinder, Augury (diperbarui 25 Agu 2026) | https://softwarefinder.com/facility-management-software/augury | Estimasi US$50–200/mesin/bulan; implementasi US$15k–319k. **Estimasi pihak ketiga** |
| B7 | TIMES Indonesia, Rakerda Perpamsi Jatim (24 Nov 2025) | https://timesindonesia.co.id/indonesia-positif/566391/ajak-daerah-kompak-jaga-sumber-air-bupati-banyuwangi-buka-rakerda-perpamsi-2025 | Dirut Perumda air minum dari 38 kota/kabupaten se-Jatim |
| B8 | Hokione (distributor), Schneider EasyLogic PM2120 | https://www.hokione.id/products/easylogic-pm2120-power-energy-meter-up-to-15th-h-led-rs485-class-1 | Judul produk menyebut RS485. Protokol Modbus **tidak** tertulis di bagian yang terbaca; `[ISI: datasheet resmi se.com]` |
| B9 | Perbup Ciamis 62/2022, Pedoman Pengadaan Barang dan Jasa pada BUMD (JDIH BPK) | https://peraturan.bpk.go.id/Download/315120/PERATURAN%20BUPATI%20CIAMIS%20NOMOR%2062%20TAHUN%202022%20TENTANG%20PEDOMAN%20PENGADAAN%20BARANG%20DAN%20JASA%20PADA%20BUMD.pdf | Konsiderans: PP 54/2017 Pasal 93, pengadaan BUMD ditetapkan dengan peraturan kepala daerah; Perpres 16/2018 jo. 12/2021 di dasar hukum. **Contoh daerah lain, bukan Surabaya** |
| B10 | InvestHK, About us | https://www.investhk.gov.hk/en/about-us/ | Peran InvestHK |
| B11 | AVCJ, "Hong Kong's Kerogen makes Israel energy investment" | https://www.avcj.com/avcj/news/3003765/hong-kongs-kerogen-makes-israel-energy-investment | Profil Kerogen (PE energi, migas hulu; berita lama) |
| S6 (ulang) | Teks lengkap JIST 5(2) | lihat `03_RISET.md` | Tabel 2–4: Pi, Ph, η per pompa; kWh dan produksi Ngagel I; arus 97–326 A; putaran ±1.489 rpm |
| S21 (ulang) | Tabel FE JCM | lihat `03_RISET.md` | Jamali 0,87/0,80 di Tabel 2-1; 0,613/0,533 di Tabel 2-2 (PV, tidak dipakai) |

**Gagal dibuka / tidak dipakai:** Tokopedia SCT-013 (timeout) → harga clamp `[ISI]`; Dealroom Augury (403); Walmart/eBay SCT-013 (verifikasi bot / 403); halaman riset CityU SEE (konten kosong); Bisnis.com soal jumlah anggota Perpamsi (403); FE Jamali terbaru ESDM (tidak ketemu); harga OPTIME (tidak ketemu); jumlah tenant SIER/PIER (hanya cuplikan dan skripsi, tidak dipakai).
