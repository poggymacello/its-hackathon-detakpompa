# JURI_90 / SKOR_AWAL: DetakPompa (Seno Hackathon ITS 2026)
### Agen A10 "Panel Juri" · 28 Okt 2026 · protokol `03-MEGA-PROMPT-JURI-90.md` · rubrik **asumsi** `07-MEGA-PROMPT-ITS-HACKATHON-28okt2026.md` §C (panitia belum merilis rubrik)

**Yang dinilai:** `08_PENDAFTARAN.md`, `09_DECK_OUTLINE.md`, `10_QNA.md`, `05_BUKTI_TKT.md`, `07_BISNIS_DAMPAK.md`, `06_VALIDASI_PENGGUNA.md` (§6 simulasi persona **tidak** dihitung sebagai bukti), `prototype\` (README, kode, `results\`).

**Catatan waktu:** selama penilaian (±20:33–20:43), proses lain mulai mengubah `prototype\` (`detakpompa\models.py: RMSGateBaseline`, `metrics.py`, README §baru, `run_eval_rms_gate.py`, `results\rmsgate_*`). Pekerjaan itu sejalan dengan gap a1 di bawah. Skor ini menilai keadaan **sebelum** perubahan tersebut. Berkas kiriman 05/08/09/10 tidak berubah selama penilaian. **Skor ulang setelah pekerjaan itu selesai dan klaim di 08/09/10 disesuaikan.**

**Yang diverifikasi sendiri oleh panel (28 Okt 2026):**
- `pytest -q tests` dijalankan ulang: **23 passed** (cocok dengan `results\pytest_output.txt`).
- `demo.py ...\O_8_2.mat` dijalankan ulang: keluaran identik dengan `results\demo\laporan_O_8_2.txt` (TIDAK TAHU, prioritas 0,48).
- Semua angka utama di 05/08/09/10 cocok dengan `run_eval_log.txt`, `metrics_summary.csv`, `paired_bootstrap.csv`, `degradation_summary.csv`, `oof_predictions.csv`: 0,640 / 0,608 / 0,553 / 0,432; selisih −0,030 [−0,145; +0,067]; AURC 0,235 vs 0,305; cakupan 0,873; galat 0,344 vs 0,392; 98,8 %; 4,5 % (27 jendela, semuanya dari C_16_1, C_16_2, C_17_2, O_7_1, O_7_2); 186/200 dan 352/400; F1 waspada 0,429; deviasi 14/20 vs 12/20; prioritas C_16_2 0,75; "rusak" 0,74 pada sensor lepas. **Tidak ditemukan angka yang dikarang atau salah salin.**
- **Eksperimen tambahan panel J4** (hanya membaca `results\features.csv` + `results\oof_predictions.csv`, tidak mengubah file proyek). Skrip: `C:\Users\POGGY\AppData\Local\Temp\claude\C--Users-POGGY--claude-spares-spare-xjE250\c0f1913a-f688-4e27-af57-a6dab34be300\scratchpad\j4_rms_selective.py`. Prediksi ambang RMS direplikasi persis (bacc 0,640) dengan `ThresholdRule("rms")` per fold LOBO, lalu diberi skor keyakinan paling sederhana: jarak log ke ambang terdekat.

| Uji panel | Hasil |
|---|---|
| AURC galat, RMS + skor margin | 0,306 (usulan 0,235; RF statistik 0,305) |
| Selisih AURC usulan − RF statistik, bootstrap per unit (1000×) | −0,066 **[−0,145; +0,003]**: selang memuat 0 |
| Selisih AURC usulan − RMS-margin | −0,065 **[−0,191; +0,059]**: selang memuat 0 |
| Cakupan sama 0,873, gerbang SNR yang sama dipasang di depan keduanya | **RMS + gerbang + margin: galat 0,336, bacc 0,664** · usulan + gerbang: galat 0,347, bacc 0,634 |
| Cakupan 0,80 / 0,70 | RMS 0,304 / 0,293 · usulan 0,329 / 0,302 (galat) |
| Triase biner (sehat vs perlu cek), AUROC tingkat jendela | usulan 0,945 · RMS mentah 0,947 |
| Triase biner, AUROC tingkat rekaman (n = 60) | usulan 0,949 · RMS 0,945 |
| Presisi@10 / @20 dari 60 rekaman (dasar 0,67) | usulan 1,00 / 0,95 · RMS 0,90 / 0,95 (n kecil, tanpa CI) |
| Komposisi TIDAK TAHU (76 jendela) | **91 % berasal dari jendela fault** (69/76): 49 "ragu", 27 "sinyal" |

**Arti temuan ini:** klaim "RMS tidak punya skor keyakinan, jadi tidak punya kurva" (08 §3, 09 slide 5, 10 Q20/Q21, README) **tidak benar**. Jarak ke ambang adalah skor keyakinan yang sah. Dengan skor itu dan gerbang SNR yang sama, ambang RMS **setara atau sedikit lebih baik** dari usulan di titik operasi. Keunggulan AURC atas RF statistik juga belum signifikan. Jadi di data ini **belum ada satu metrik pun di mana AI terbukti lebih baik dari ambang RMS**.

---

## 1. Tabel skor per juri × kriteria (0–10)

Bobot: Masalah 20 · AI + purwarupa + TKT 25 · Inovasi 15 · Dampak 15 · Bisnis 10 · Validasi 10 · Presentasi 5.

### J1: profesor energi/AI (CityU SEE / Tsinghua)
| Kriteria | Skor | Alasan | Apa yang membuat ini 10/10 |
|---|---|---|---|
| Masalah & energy gap | 7 | Angka lokal bersumber dan spesifik per pompa (12/22 terukur, 5 di bawah ±55 %, T1 49,77 % [S6]). Energy gap didefinisikan sebagai "waktu sampai diaudit", tapi waktunya tidak dikuantifikasi (interval audit `[ISI]`). | Interval audit nyata dan kWh yang hilang per bulan keterlambatan, dari log PDAM atau penulis S6. |
| AI inti + purwarupa + TKT | 5 | Desain evaluasinya di atas rata-rata hackathon: LOBO, tes anti-bocor, 3 baseline, CI per unit, uji degradasi. Hasilnya: AI ≤ RMS, keunggulan abstain tidak signifikan, mode deviasi (inti produk "baseline pompa sendiri") tidak informatif. | AI > RMS + gerbang yang sama, dengan CI tidak memuat 0, pada kondisi yang relevan untuk pompa (perubahan beban/throttling), di data yang dibekukan sebelum dilihat. |
| Inovasi | 5 | Prediksi selektif dan gerbang CFAR adalah teknik standar. Pembingkaian "triase, bukan pengukur efisiensi" sudah tepat secara fisika, tapi bukan kebaruan metode. | Satu ide teknis yang tidak dimiliki vendor, misalnya deteksi perubahan kW pada tekanan setara terhadap baseline pompa sendiri, yang tervalidasi melawan audit Q–H. |
| Dampak lokal & efisiensi | 5 | Rantai ①→②→③ dipisah dengan jujur dan semua skenario diberi label. Angka atribusinya kecil (12–172 MWh/tahun) dan semua parameternya [ASUMSI]. | ΔkW dan ΔkWh/m³ diukur sendiri di pompa lab, ditambah satu pompa PDAM yang ditandai, diaudit, lalu hasil auditnya terkonfirmasi. |
| Bisnis | 5 | Fase pilot → kampanye → langganan masuk akal untuk BUMD. Harganya asumsi. | Biaya audit energi nyata sebagai jangkar harga kampanye, plus satu pembeli yang menyebut pos anggarannya. |
| Validasi & co-design | 2 | Nol wawancara. Hipotesis, skrip, dan aturan berhentinya sangat baik (itulah nilai 2-nya). | ≥5 wawancara + pakar S6, dengan papan skor H1/H3/H6 dan satu perubahan produk yang lahir dari wawancara. |
| Presentasi & demo | 6 | Satu pesan per slide, angka di slide, dan baseline yang menang tetap ditebalkan. Deck belum dibuat, figur baru satu, dan demo masih CLI. | Deck jadi dengan 4–5 figur yang terbaca dalam 5 detik, plus demo daftar triase armada. |
| **Skor berbobot J1** | **51,5** | | |

### J2: praktisi industri energi/pompa/semikonduktor Indonesia
| Kriteria | Skor | Alasan | Apa yang membuat ini 10/10 |
|---|---|---|---|
| Masalah & energy gap | 7 | Nyata dan lokal. Tapi angka S6 sendiri janggal (U2/U3/U5 88–93 % *wire-to-water*), dan status rekondisi 5 pompa sejak 2024 tidak diketahui. | Konfirmasi PDAM: pompa mana yang masih buruk hari ini, dan bagaimana pompa dipilih untuk rekondisi sekarang. |
| AI inti + purwarupa + TKT | 4 | Yang jalan hanya klasifikasi file .mat 42 kHz di laptop. Belum ada pembacaan PM2100, tampilan armada, maupun sensor. Model 42 kHz tidak cocok dengan ADXL343 (ODR 3,2 kHz) yang ada di BOM (diakui di Q13). | Rekaman sendiri dari pompa sentrifugal dengan sensor yang memang ada di BOM, mode A membaca PM2100/Modbus, dan daftar urutan pompa. |
| Inovasi | 5 | Posisi "lapisan di atas meter Schneider" itu cerdas, tapi belum dibangun sama sekali. | Purwarupa yang benar-benar membaca data panel yang sudah ada, tanpa memasang alat baru. |
| Dampak lokal & efisiensi | 5 | Titik impas 76.464 kWh/tahun bisa dicek siapa pun. Biaya salah alarm dan biaya kunjungan ukur belum dikurangkan. | Biaya kunjungan flowmeter dan presisi top-3 nyata, lalu dihitung nilai neto per IPA. |
| Bisnis | 5 | Paham pengadaan BUMD dan gratifikasi, dan tidak menjual dulu. Margin vendor belum bisa dihitung. | Mitra pemasang/servis lokal dan biaya dukungan per pompa. |
| Validasi & co-design | 2 | Belum ada teknisi atau operator yang melihat laporannya. | Operator memakai laporan dalam satu ronde dan mencatat apa yang membingungkan. |
| Presentasi & demo | 6 | Laporannya jujur dan ada langkah berikutnya. Tapi terlalu panjang untuk ruang pompa (lihat §6). | Laporan 5 baris untuk operator dan laporan mingguan untuk kepala IPA. |
| **Skor berbobot J2** | **49,0** | | |

### J3: investor (InvestHK / Kerogen CelerateX)
| Kriteria | Skor | Alasan | Apa yang membuat ini 10/10 |
|---|---|---|---|
| Masalah & energy gap | 7 | Rp147,65 M/tahun adalah angka besar dan bersumber. Bagian yang bisa diatribusikan ke alat hanya ±1,2 % listrik satu IPA, dan rasa sakit "pompa mana dulu" (H3) belum terbukti. | Bukti bahwa keterlambatan triase pernah menimbulkan biaya nyata (kejadian, Rp). |
| AI inti + purwarupa + TKT | 4 | Demonya jalan dan jujur, tapi AI belum terbukti diperlukan. Investor akan bertanya "kenapa bukan aturan RMS + gerbang saja". | Bukti bahwa model memberi nilai yang tidak bisa diberikan aturan sederhana. |
| Inovasi | 5 | Diakui sendiri: tidak ada parit (moat). Include dan OPTIME lebih maju. | Akses data eksklusif (data audit dan log PDAM) yang dikunci oleh kerja sama riset. |
| Dampak lokal & efisiensi | 5 | Kecil dan jujur. Skala kota masih ilustrasi. | Jumlah pompa per Perumda Jatim dan satu studi kasus terukur. |
| Bisnis | 4 | Pra-pendapatan, belum berbadan hukum, tanpa LOI. Payback 8–112 bulan. TAM tidak dihitung (dengan alasan yang benar). | Satu pembayar yang berkomitmen untuk Fase 1, plus TAM dari data pompa. |
| Validasi & co-design | 2 | Nol. | Komitmen nyata (perkenalan, kunjungan, data) dari PDAM. |
| Presentasi & demo | 6 | Narasi kejujurannya kuat. Tapi "kami kalah dari RMS" tanpa nilai tambah yang terbukti melemahkan *ask*. | Hook 20 detik + satu angka bukti milik sendiri. |
| **Skor berbobot J3** | **48,0** | | |

### J4: reviewer skeptis (veto)
| Kriteria | Skor | Alasan | Apa yang membuat ini 10/10 |
|---|---|---|---|
| Masalah & energy gap | 6 | Masalahnya ada. Tapi "10 pompa tidak terlihat" bisa karena alasan lain (pompa cadangan atau mati saat audit), dan H3 belum diuji. | Penjelasan PDAM kenapa 10 pompa tidak diukur. |
| AI inti + purwarupa + TKT | 3 | AI ≤ RMS. Klaim keunggulan abstain **runtuh** begitu RMS diberi skor margin dan gerbang yang sama (uji panel di atas). 98,8 % adalah jasa gerbang DSP, bukan AI (diakui di Q21). TKT 3 masih wajar karena dibatasi ke "komponen getaran di bantalan". | Tabel baseline (d) "RMS + gerbang + margin" ada di berkas, dan AI menang di uji stres yang ditentukan sebelum datanya dilihat. |
| Inovasi | 4 | "Tahu kapan harus diam" bisa dipasang di baseline apa pun. | Ide yang tidak bisa disalin dengan satu baris `if snr < τ`. |
| Dampak lokal & efisiensi | 4 | 0 kWh terukur. Semua skenario bergantung pada asumsi perilaku PDAM. | Satu ΔkW terukur sendiri. |
| Bisnis | 4 | Semua harga [ASUMSI]. | Satu harga pembanding nyata (audit energi) dan satu pembayar. |
| Validasi & co-design | 1 | Tidak ada data pengguna sama sekali. Poin positifnya: tidak ada yang dikarang. | Wawancara asli dengan rekaman persetujuan. |
| Presentasi & demo | 5 | Banyak `[ISI]`, slide 3 kosong, video belum ada. | Semua `[ISI]` terisi dari data asli. |
| **Skor berbobot J4** | **39,0** | | |

### Rekap
| Kriteria (bobot) | J1 | J2 | J3 | J4 | Rata-rata | Poin berbobot |
|---|---|---|---|---|---|---|
| Masalah & energy gap (20) | 7 | 7 | 7 | 6 | 6,75 | 13,50 |
| AI inti + purwarupa + TKT (25) | 5 | 4 | 4 | 3 | 4,00 | 10,00 |
| Inovasi (15) | 5 | 5 | 5 | 4 | 4,75 | 7,13 |
| Dampak lokal & efisiensi (15) | 5 | 5 | 5 | 4 | 4,75 | 7,13 |
| Bisnis (10) | 5 | 5 | 4 | 4 | 4,50 | 4,50 |
| Validasi & co-design (10) | 2 | 2 | 2 | 1 | 1,75 | 1,75 |
| Presentasi & demo (5) | 6 | 6 | 6 | 5 | 5,75 | 2,88 |
| **Total** | 51,5 | 49,0 | 48,0 | 39,0 | | **46,9 / 100** |

---

## 2. Skor akhir, fatal flaw, veto

**Skor akhir (rata-rata 4 juri): 46,9 / 100.** **Veto J4: AKTIF** (batas atas 80). Saat ini batas itu belum mengikat, tetapi akan mengikat plafon setelah aksi manusia.

| # | Fatal flaw (daftar §C) | Status | Bukti | Cara menutup |
|---|---|---|---|---|
| FF1 | **AI yang tidak perlu** | **AKTIF → veto** | Usulan − RMS = −0,030 [−0,145; +0,067]. Dengan gerbang yang sama, RMS + margin setara atau lebih baik di cakupan 0,873 (galat 0,336 vs 0,347). AURC usulan vs RMS-margin −0,065 [−0,191; +0,059]. Triase biner AUROC 0,945 vs 0,947. Satu-satunya argumen AI (throttling/katup di pompa) masih hipotesis. | (1) Agen: perbaiki klaim dan tambahkan baseline (d) (§4 a1). Ini menutup overclaim, **bukan** flaw-nya. (2) Agen dengan izin unduh: uji Paderborn di bawah pergeseran kondisi operasi + arus (§4 a5). (3) Manusia: pompa lab dengan throttling (§4 b4). Kalau AI tetap tidak menang: jual "RMS + gerbang + triase armada" secara jujur, lalu letakkan AI di tempat yang memang perlu (fusi kW–tekanan–getaran terhadap baseline pompa). Tanpa itu, kriteria "AI di inti" tetap rendah. |
| FF1b | **Overclaim turunan** (bagian dari "klaim melebihi bukti") | **AKTIF**, bisa ditutup agen | 08 §1: "Nilai tambahnya ada di abstain". 08 §2: "kurva cakupan-risiko lebih baik daripada RF". 08 §3 dan 09 slide 5: "RMS tidak punya skor keyakinan". 10 Q20: "RMS … tidak bisa ikut kurva itu". 09 slide 4: "Tanpa gerbang itu, tim teknisi akan dikirim ke pompa yang baik-baik saja", padahal laporan sensor lepas tetap mencetak **prioritas 0,87** (§6). | §4 a1, a2. |
| FF2 | Klaim TKT tanpa bukti | **Tidak aktif**, risiko sedang | TKT 3 sudah dibatasi ke "komponen AI getaran di bantalan" dan buktinya ada di file. Tapi inti produk yang dijual (baseline pompa sendiri, data PM2100, kW pada tekanan setara) masih TKT 2, dan mode deviasi diakui tidak informatif. | Di 08 §3, tulis eksplisit: "fungsi produk 'perubahan terhadap baseline pompa sendiri' = TKT 2". |
| FF3 | Angka tanpa sumber | Tidak aktif | Semua angka punya rujukan S/B/file. Asumsi diberi label. | Jaga label [ASUMSI]/[SKENARIO] saat memotong teks untuk form. |
| FF4 | Hasil wawancara karangan | Tidak aktif | Persona simulasi dilarang dikutip, dan ini konsisten di semua berkas. | **Risiko terbesar saat mengisi `[ISI]` di menit terakhir.** Kalau wawancara belum ada, pakai kalimat "dijadwalkan". |
| FF5 | Orisinalitas aset | Tidak aktif, menunggu konfirmasi | FaceVitals milik dua anggota dan diberi atribusi. Ottawa CC BY 4.0 dengan atribusi. | `AKSI_MANUSIA.md` #3: konfirmasi pemilik dan bahwa FaceVitals tidak sedang dikirim ke lomba lain. |
| — | Diskualifikasi formal | Risiko tinggi | Deadline dan isi form belum diketahui. Bentrok 1 Nov dengan IBSC (PIC sama). | `AKSI_MANUSIA.md` #1 hari ini. |

---

## 3. Uji anti-generik

| Pertanyaan | Jawaban panel |
|---|---|
| Apakah 50 tim lain bisa mengirim hal yang hampir sama? | **Sebagian besar ya, untuk bagian teknisnya.** "RF + fitur getaran di dataset bantalan publik untuk predictive maintenance" adalah salah satu proyek mahasiswa paling umum. Bagian yang **tidak** bisa disalin: (1) angka audit Ngagel I 12/22 dan 49,77 % dengan jalur kontak ke penulis ITS–PDAM; (2) budaya evaluasi yang jujur (LOBO, baseline menang ditebalkan); (3) posisi "triase, bukan pengukur efisiensi" yang benar secara fisika. |
| Hook sudah memakai sudut unik? | Ya untuk slide 1 ("22 pompa, 12 terukur, 5 di bawah 55 %"). Tidak untuk judul: "yang tahu kapan harus diam" menjual fitur yang sebenarnya jasa gerbang DSP dan bisa dipasang di RMS. |
| Kata kosong? | Bersih. Tidak ada "revolusioner/seamless/pertama". Satu masalah: "**AI** kami tahu kapan harus diam" (05 §2, 09 slide 5) secara teknis tidak tepat, karena yang tahu adalah gerbang SNR. |
| Setiap angka bersumber? | Ya (diverifikasi, §0). |
| Pemenang tahun lalu? | Tidak ada data publik (Seno Hackathon 2026 adalah edisi yang dinilai). Tidak bisa dibandingkan. |
| **Sudut unik yang disarankan untuk judul/hook** | **"Triase saat ronde operator: 30 detik per pompa, dibandingkan dengan pompa itu sendiri, divalidasi terhadap 12 pompa yang sudah diaudit ITS–PDAM."** Dasar fakta: S6 F4 menyebut PDAM sudah membawa alat genggam (stroboskop, termometer IR, flowmeter portabel) saat audit. Alat genggam juga menghindari risiko H1 (izin memasang alat permanen). Ini masih hipotesis yang harus diuji di wawancara (H1/H6), bukan klaim. |

**Vonis anti-generik: LULUS SEBAGIAN.** Masalah dan konteksnya unik, tetapi purwarupa dan metodenya generik.

---

## 4. Daftar gap (diurutkan kenaikan skor ÷ usaha)

### (a) Bisa ditutup agen sekarang tanpa mengarang

| # | Gap | Kenaikan (poin total) | Usaha | Instruksi perbaikan spesifik |
|---|---|---|---|---|
| **a1** | Overclaim abstain + baseline RMS yang tidak adil (FF1b) | +1,5–2 (J4 AI +1, J1 +0,5; mencegah Q&A runtuh) | 1–2 jam | (1) Di `run_eval.py`, tambahkan baseline **(d) `rms_gate_margin`**: `ThresholdRule("rms")` per fold, conf = `min(|log(rms/t1)|, |log(rms/t2)|)`, lewat `AbstainGate` yang sama (SNR 11,52 dB + clip/flat). Masukkan ke `coverage_risk`, kurva di `coverage_risk.png`, dan tabel degradasi. (2) Tambahkan **CI bootstrap per unit untuk AURC** dan selisihnya (semua pasangan) → `results/coverage_risk_ci.csv`. Panel mendapat: usulan − RF stat −0,066 [−0,145; +0,003]; usulan − RMS-margin −0,065 [−0,191; +0,059]; di cakupan 0,873 RMS + gerbang galat 0,336 vs usulan 0,347. (3) Ganti kalimat di 08 §1 ("Nilai tambahnya ada di abstain…"), 08 §2, 08 §3 (baris "Abstain lebih baik"), 09 slide 5 (judul + naskah "kurva oranye…"), 10 Q20/Q21, 05 §2, README. Kalimat aman: *"Di data bantalan ini, aturan RMS yang diberi gerbang sinyal yang sama setara dengan model kami, termasuk saat boleh abstain. Yang kami tawarkan saat ini adalah alur triase + gerbang kualitas sinyal + langkah berikutnya. Peran AI baru akan kami uji di kondisi operasi pompa yang berubah."* (4) Tambahkan Q26 di `10_QNA.md`: "RMS diberi margin ke ambang, apa bedanya?" |
| **a2** | Prioritas tetap dicetak untuk rekaman yang gagal gerbang sinyal (sensor lepas → **prioritas 0,87**, derau −10 dB → 0,83) | +1 (J2 purwarupa +0,5; presentasi; juri tamu) | 1 jam | Di `demo.py` (baris prioritas ±78) dan `report.py`: kalau alasan = `sinyal`, cetak `Prioritas cek: — (ukur ulang dulu; tidak diurutkan)` dan masukkan ke antrean **UKUR ULANG**. Untuk `ragu`, tetap tampilkan prioritas dengan tanda "ragu". Tambahkan tes `test_gated_has_no_priority`. Tulis fakta dari OOF di README: *76 jendela TIDAK TAHU, 91 % berasal dari jendela fault* → aturan produk "TIDAK TAHU = ukur ulang ≤ 48 jam, bukan aman", sekarang dengan angka. Perbaiki juga naskah slide 4. |
| **a3** | Demo tidak menunjukkan produk yang dijual ("urutan pompa"); yang ada hanya laporan satu rekaman | +2,5–3 (J2/J3 purwarupa +1, presentasi +1, inovasi +0,5) | 2–3 jam | Buat `triase.py <folder>`: satu rekaman per "pompa", model LOBO (unit uji dikeluarkan dari latih), keluaran **"Daftar cek minggu ini"** (maks. 3 teratas), antrean UKUR ULANG, dan sisanya SEHAT, dalam CSV + HTML/teks satu halaman. Evaluasi **presisi top-3** (KPI Lean Canvas) dengan simulasi armada: 2000 × ambil 20 bearing, satu rekaman acak per bearing, lalu hitung distribusi presisi@3 untuk usulan vs RMS + gerbang. Laporkan apa adanya (dugaan panel: setara). Beri label "bearing Ottawa sebagai pengganti pompa". |
| **a4** | Metrik utama tidak sesuai produk (bacc 3 kelas 0,608 menjual rendah tugas triase) | +0,5–1 | 30 menit | Tambahkan metrik biner "sehat vs perlu cek" sebagai metrik produk: AUROC jendela 0,945 (usulan) vs 0,947 (RMS); rekaman 0,949 vs 0,945; sensitivitas/spesifisitas di titik operasi. Tulis bahwa metrik ini **ditetapkan setelah data dilihat** (eksploratif). Taruh di 05 §2 dan slide 5 sebagai baris kedua, tanpa mengklaim AI menang. |
| **a5** | FF1: tidak ada uji di mana AI *mungkin* diperlukan | +0 s.d. +6 (kalau positif dan CI tidak memuat 0: AI +2–3, veto bisa dicabut J4) | 1–2 hari + **izin unduh dari user** | Paderborn KAt (Univ. Paderborn; ada **arus motor** dan 4 kondisi operasi kecepatan/torsi/gaya radial; **CC BY-NC 4.0** → hanya riset/lomba, harus dideklarasikan, bukan basis produk komersial). **Sebelum melihat data**, tulis `PRAREG_PADERBORN.md`: hipotesis "di bawah pergeseran kondisi operasi (latih di N15_M07_F10, uji di kondisi lain), RF getaran+arus > RMS + gerbang"; metrik bacc biner + AUROC; uji pada bantalan kerusakan *nyata*; split per bantalan × per kondisi; aturan keputusan "klaim hanya kalau CI 95 % selisih > 0; kalau tidak, AI dicabut dari klaim". Unduh hanya subset yang perlu. Catat ukuran dan sumber saat meminta izin. |
| **a6** | Ketidakcocokan sensor BOM (ADXL343 3,2 kHz) vs model 42 kHz | +1–1,5 (J2 purwarupa +1) | 1–2 jam | Decimasi Ottawa ke 3,2 kHz (anti-alias, pita < 1,6 kHz). Batasi fitur (hapus envelope 2–10 kHz dan pita > 1,6 kHz). Jalankan ulang LOBO untuk keempat model + baseline (d). Laporkan penurunan apa adanya di 05 §2 dan Q13. |
| **a7** | Figur dan deck belum ada (1 dari 5 lampiran siap) | +1 (presentasi +1,5–2) | 2–3 jam | Buat dengan matplotlib dari CSV/S6, simpan ke `results/fig/`: (i) 22 ikon pompa (8+14; 5 merah, 7 abu, 10 tanda tanya) dari S6; (ii) batang SEC 0,27 vs garis 0,4 dengan 5 titik pompa (U6 54,26; U6d 51,76; T1 49,77; S1 51,18; S2 52,60); (iii) tabel hasil dengan baris RMS ditebalkan **+ baris (d)**; (iv) abstain per tingkat derau; (v) tangkapan tiga laporan demo (L5) dan 23 tes (L7). Lalu susun deck 10 slide dari `09_DECK_OUTLINE.md` (slide 3 versi "sedang berjalan"). |
| **a8** | Laporan tidak cocok untuk ruang pompa (lihat §6) | +0,5–1 (presentasi, bahan uji H6) | 1–2 jam | Tambahkan `--mode operator` (≤6 baris): STATUS, APA YANG DILAKUKAN, KAPAN, rpm terukur vs pelat nama (`[ISI: rpm pelat]`, Ngagel ±1.489 rpm [S6]), kualitas pemasangan sensor, dan perbandingan dalam bahasa awam ("getaran total 2,5× median pompa sehat"). Pindahkan probabilitas, fitur, dan catatan energi (Rp147 M, hp/gpm S10) ke `--mode manajer`. Hapus duplikasi `std`/`rms` di "Fitur dominan". Tambahkan tes. |
| **a9** | Klaim "AI" di judul/hook | +0,5 (J4 inovasi) | 15 menit | Ganti "AI kami tahu kapan harus diam" menjadi "alat kami tahu kapan harus diam". Pertimbangkan judul dengan sudut unik §3 (*triase saat ronde, terhadap pompa itu sendiri*). Tetap tandai hipotesis. |
| **a10** | Uji stres kecil di data yang ada (eksploratif) | +0–1 | 1–2 jam | (i) Ottawa **mikrofon** (kolom 1 MAT): fusi akselerometer + mikrofon vs RMS + gerbang, dengan LOBO. (ii) Pergeseran kecepatan: latih di unit 29,7 Hz, uji di unit 16–19 (19,5 Hz). Tulis bahwa (ii) **dirancukan jenis fault** (semua cage) dan keduanya eksploratif karena data sudah dilihat. Laporkan apa pun hasilnya. |
| **a11** | Q&A belum siap untuk temuan panel | +0,5 | 30 menit | Tambahkan di `10_QNA.md`: Q26 (RMS + margin), Q27 ("sensor lepas tetap dapat prioritas 0,87?"), Q28 ("kenapa 10 pompa tidak diaudit?" → "kami belum tahu, H-pertanyaan ke penulis S6"), Q29 ("TIDAK TAHU 12,7 %, operator tidak akan malas?"). |

**Total realistis dari (a) tanpa a5:** ±+7 → **±54**. Dengan a5 positif: ±+6 lagi → **±60**, dan J4 dapat mencabut veto (tetap bantalan, bukan pompa).

### (b) Hanya bisa ditutup manusia

| # | Aksi | Siapa | Kenaikan (estimasi) | Catatan |
|---|---|---|---|---|
| b1 | Login portal, catat **deadline WIB + field form**. Selesaikan bentrok 1 Nov dengan IBSC | Aziz | 0 poin, tapi **syarat ikut** | Tanpa ini semua skor = 0. Hari ini. |
| b2 | ≥5 wawancara PDAM/operator + 1 pakar (penulis S6), dengan skrip `06` §3 dan papan skor H1/H3/H4/H5/H6 | Uqi, Pio | **+6–8** (Validasi 1,75→6–7; Masalah +0,75; Bisnis +0,5; slide 3 terisi) | Tunjukkan laporan versi operator (a8) dan uji H6 langsung. |
| b3 | Surat/izin tertulis pilot (PDAM lewat DIKST/penulis S6, atau Sarpras ITB) | Aziz, Pio | **+3–5** (Bisnis +1,5, Validasi +1, Dampak +0,5) | Tanpa hadiah atau uang. Jangan lampirkan apa pun yang menyerupai LOI sebelum ada aslinya. |
| b4 | **TKT 4:** pompa sentrifugal lab + akselerometer BOM + clamp + power meter + flowmeter/manometer; kondisi sehat / imbalance / misalignment / **throttling**, ≥5 × 30 s dari sesi berbeda; pipeline dibekukan sebelum rekaman | Poggy | **+9–11 kalau AI > RMS + gerbang dengan CI > 0** (AI +2,5, Dampak +1 dari ΔkW milik sendiri, Inovasi +0,5, veto dicabut). **+4 kalau tidak** (TKT 4 sah, tapi FF1 tetap → plafon 80) | Satu-satunya jalan nyata untuk menutup FF1 di domain pompa. |
| b5 | Data PDAM: log PM2100 / ampere per shift + catatan perawatan + status rekondisi 5 pompa S6 sejak 2024 | Aziz (lewat penulis S6) | **+4–6** (jalur TKT 5, energy gap terkuantifikasi, ground truth triase) | Tanpa data keluar dari lokasi (on-prem). |
| b6 | Video demo ≤2 menit, data tim, foto, dosen pembimbing, latihan Q&A (terutama Q20/Q26) | Poggy, semua | +1 | Video harus memakai versi setelah a2, supaya sensor lepas tidak tampil dengan prioritas 0,87. |
| b7 | Konfirmasi izin aset FaceVitals dan tidak ada pengiriman ganda | Poggy, Aziz | 0, mencegah FF5 | — |
| b8 | Coba ulang dataset pompa 4TU dari jaringan lain | siapa saja | +0–2 (data pompa nyata untuk TKT 3 di domain pompa) | Cek lisensi dan ukuran dulu. |

---

## 5. Plafon

| Keadaan | Skor | Catatan |
|---|---|---|
| **Sekarang (sebelum perbaikan)** | **46,9** | Veto aktif (FF1). |
| **Plafon sekarang** (semua aksi agen a1–a4, a6–a11) | **±54** | FF1b tertutup, FF1 tetap. Validasi tetap ±2. |
| Plafon sekarang + a5 Paderborn positif | ±60 | Veto bisa dicabut. Hasil tidak dijamin, jadi jangan direncanakan sebagai pasti. |
| + b2 wawancara (5 + pakar) | +7 → ±61 (±67) | |
| + b3 izin/surat pilot | +4 → ±65 (±71) | |
| + b4 TKT 4 lab, AI menang | +10 → ±75 (±80) | Kalau AI **tidak** menang: +4 dan veto tetap → batas keras 80. |
| + b5 data PDAM / ground truth | +5 → ±80 (±85) | |
| + b6 video/deck/latihan | +1 → **±81 (±86)** | |
| **Plafon setelah aksi manusia** | **±81–86** (realistis sebelum Demo Day Jan 2027: ±75–80) | Skor 90 butuh **presisi top-3 terukur di pompa PDAM** + AI terbukti lebih baik dari RMS + gerbang di kondisi operasi pompa. Itu TKT 5, yang kecil kemungkinannya selesai sebelum Jan 2027. |

**Rekomendasi panel:** daftar, karena purwarupa ini memenuhi syarat TKT 3 dengan bukti yang jarang sejujur ini, dan itu kemungkinan cukup untuk seleksi 15 tim. Tetapi a1 + a2 harus dikerjakan **sebelum** berkas dikirim, karena klaim "RMS tidak punya skor keyakinan" adalah satu-satunya hal di berkas yang bisa dibantah juri J1/J4 dalam satu kalimat.

---

## 6. Juri tamu (non-skor): operator / manajer pompa PDAM

> **SIMULASI PERSONA, BUKAN BUKTI.** Disusun panel dari fakta S6 (`06` §0 F4–F8) dan dari membaca laporan demo asli di `results\demo\`. Tidak boleh dikutip di berkas, deck, atau video. Semua butir di bawah adalah **pertanyaan untuk wawancara asli (b2)**, bukan temuan.

**Persona:** operator shift rumah pompa distribusi (±10 tahun) dan kepala unit produksi, melihat demo `demo.py` dan tujuh laporan contoh.

**Yang langsung berguna (menurut persona):**
- "rpm terlacak ~1.788" bisa dicocokkan dengan pelat nama. Ini cek cepat yang dimengerti operator. Taruh di baris atas.
- Langkah berikutnya untuk TIDAK TAHU ("pasang sensor kencang di bearing housing, arah radial, 30 detik") adalah instruksi yang bisa langsung dikerjakan saat ronde.
- Kalimat "tidak mengukur efisiensi, efisiensi butuh debit + head" membuat kepala IPA percaya bahwa tim paham pompa.

**Yang membuat tidak dipakai:**
1. **"Saya tidak punya file .mat 42 kHz."** Tidak ada cara merekam: alat apa, ditempel di mana, siapa yang membawa. Operator sudah membawa stroboskop dan termometer IR saat audit (S6 F4). Yang masuk akal baginya adalah **alat genggam 30 detik per pompa saat ronde**, bukan alat permanen yang butuh surat Direksi.
2. **Sensor lepas tetap mendapat "Prioritas cek: 0,87".** Kalau laporan ini masuk daftar urutan, pompa yang sensornya lepas akan berada di atas pompa yang benar-benar rusak (I_3_1 0,88). Persis ini yang slide 4 janjikan tidak akan terjadi (gap a2).
3. **Terlalu panjang dan bahasanya bukan bahasa ruang pompa.** Probabilitas tiga kelas, "fitur dominan std/rms/p2p" (std dan rms sama persis), dan catatan energi Rp147 miliar plus hp/gpm dari kasus AS tidak berguna bagi operator. Operator butuh: status, lakukan apa, kapan, dan seberapa yakin.
4. **"Bandingkan dengan rekaman baseline unit ini (mode --baseline)": baseline-nya dari mana?** Sistem harus merekam baseline sendiri setelah overhaul atau pemasangan, dan mengingatnya per nomor pompa (U6, T1, S1, …).
5. **TIDAK TAHU 12,7 % dari waktu, dan 17 % pada jendela rusak.** Kalau 1 dari 8 pengukuran harus diulang, operator shift akan berhenti memakai alat. Batas yang bisa diterima harus ditanyakan (H6).
6. **Kepala IPA:** "Daftar Anda hanya berguna kalau saya bisa menindaklanjutinya. T1 sudah ketahuan 49,77 % sejak audit. Kalau belum direkondisi karena anggaran, daftar baru menambah PR saja." (H4: hambatannya informasi atau anggaran?)
7. **Kepala IPA:** "Getaran tidak akan melihat S1/S2 yang salah titik operasi sejak 2018." Tim sudah mengakui ini (Q12). Persona ingin melihatnya **di laporan**, bukan hanya di Q&A.

**Yang membuat persona mau memakai (hipotesis untuk diuji):**
- Satu lembar mingguan untuk kepala IPA: **maksimal 3 pompa** untuk diukur flowmeter minggu ini, dengan alasan dalam bahasa awam ("getaran naik 2,5× dibanding pompa ini bulan lalu"), plus antrean "ukur ulang" yang terpisah.
- **Rekam jejak:** dari tanda bulan lalu, berapa yang terbukti saat diukur (presisi top-3). Kepercayaan dibangun dari riwayat, bukan dari AUROC.
- Memakai yang sudah ada: angka ampere/kW dari panel PM2100 atau buku log shift digabung dengan rekaman 30 detik.
- Bisa dicetak atau dikirim sebagai PDF lewat grup WhatsApp unit. Tanpa cloud dan tanpa sambungan ke SCADA.
- TIDAK TAHU yang **jarang** dan **selalu bisa diselesaikan di tempat** (pasang ulang, rekam ulang 30 detik).

**Pertanyaan yang harus masuk wawancara asli (tambahan untuk `06` §3):** (1) Apakah operator merekam/mencatat sesuatu per pompa saat ronde, dan alat genggam apa yang sudah dibawa? (2) Berapa pengukuran ulang per shift yang masih bisa diterima? (3) Bagaimana pompa dipilih untuk rekondisi tahun lalu, dan siapa yang memutuskan? (4) Kenapa 10 dari 22 pompa tidak diukur di audit S6? (5) Apakah 5 pompa buruk di S6 sudah direkondisi?
