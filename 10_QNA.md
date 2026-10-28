# 10_QNA: 31 pertanyaan tersulit untuk DetakPompa
### Agen A9 "Penulis Pitch" · 28 Okt 2026 · panel: J1 profesor energi/AI · J2 praktisi industri · J3 investor · J4 reviewer skeptis

**Cara memakai:**
- Jawaban di bawah adalah **isi**, bukan naskah hafalan. Ucapkan dengan kata sendiri, ±30–45 detik per jawaban.
- Pola jawaban: **akui dulu** apa yang benar dari pertanyaannya → **angka + file** → **apa yang kami lakukan berikutnya**.
- Kalau tidak tahu, katakan "kami belum tahu" lalu sebutkan cara mencari tahunya. Jangan menebak angka.
- Persona simulasi (`03b` §2.9, `06` §6) **tidak boleh** dipakai sebagai "kata pengguna" dalam jawaban mana pun.
- Rujukan `[Sx]` = `03_RISET.md` §0; `[Bx]` = `07_BISNIS_DAMPAK.md` §10; path file relatif terhadap folder `ITSHackathon2026\`.

**Enam angka yang wajib hafal** (semua dari `prototype\results\`, kecuali [S6]):
| Angka | Isi | File |
|---|---|---|
| 0,640 vs 0,608 | Akurasi seimbang ambang RMS vs usulan; selisih −0,030 [−0,145; +0,067] | `metrics_summary.csv`, `paired_bootstrap.csv` |
| 0,639 vs 0,605 | Akurasi seimbang RMS + gerbang SNR yang sama vs usulan; −0,034 [−0,155; +0,071]. Presisi 3 pompa teratas 0,952 vs 0,971 (armada 2/3 bermasalah; 3/22 bermasalah: 0,682 vs 0,707; 5/22: 0,765 vs 0,791): setara. Recall waspada 0,213 vs 0,415 = beda label, bukan deteksi dini (tahap awal ditandai perlu cek 0,840 vs 0,830) | `rmsgate_metrics.csv`, `rmsgate_paired_bootstrap.csv`, `triase\eval_log.txt`, `triase\eval_prevalensi_log.txt` |
| 98,8 % | Jendela "sensor lepas" yang ditolak gerbang SNR (DSP, bukan AI; sama untuk RMS) | `degradation_summary.csv`, `rmsgate_degradation_summary.csv` |
| 20 / 600 | 20 bantalan (unit), 600 jendela 1 s, leave-one-bearing-out | `summary.json`, `folds.csv` |
| 12 dari 22 | Pompa Ngagel I yang terukur di audit; 5 di bawah ±55 %, terendah 49,77 % | [S6] |
| SKAB: GAGAL | Uji di data lab pompa pihak lain (1 testbed), prareg terkunci sebelum unduh. H1 katup vs fault: residual 1,000 = ambang arus 1,000. H2 anomali umum: 0,532 vs 0,581. Perancu sesi (katup ±32 L/min, fault ±125 L/min) | `skab\summary.json`, `skab\posthoc_log.txt` |

---

## J1: Profesor energi/AI

### Q1. Split kalian apa, dan bagaimana kalian yakin tidak ada kebocoran data?
**Jawaban:** Leave-one-bearing-out, 20 fold. Ketiga rekaman satu bantalan (sehat, berkembang, rusak) beserta semua jendelanya selalu berada di sisi uji yang sama. Fungsi `assert_no_leakage` dijalankan di setiap fold, dan ada tes yang memastikan irisan unit dan rekaman latih–uji kosong. Tidak ada penyetelan di data uji: ambang aturan dipilih di unit latih, hiperparameter random forest tetap, ambang SNR diambil dari kuantil 99 % derau putih (tanpa melihat label), dan ambang keyakinan dari validasi silang di dalam unit latih. Satu hal yang **tidak** bisa kami singkirkan: rekaman sehat dan rusak di Ottawa berasal dari sesi berbeda, jadi perbedaan pemasangan sensor mungkin ikut terbaca. Data ini tidak bisa memisahkan efek itu.
**Rujukan:** `prototype\README.md` (Desain evaluasi; Keterbatasan #4), `prototype\detakpompa\splits.py`, `prototype\tests\test_split.py`, [S14].

### Q2. Data kalian bantalan, bukan pompa. Kenapa hasil ini relevan untuk PDAM?
**Jawaban:** Benar, ini rig bantalan Ottawa dan tidak berisi arus motor. Dataset pompa 4TU yang kami incar tidak bisa diakses (server menolak koneksi). Satu-satunya data pompa yang sudah kami pakai adalah data lab SKAB milik pihak lain, dan uji katup vs fault di sana gagal (Q31). Yang kami buktikan di TKT 3 adalah **rangkaian kerjanya**: pemotongan sinyal, pelacakan frekuensi poros, model, gerbang abstain, dan cara evaluasi tanpa kebocoran. Gerbang sinyal berbasis garis putaran poros berlaku untuk mesin berputar umumnya. Yang **tidak** bisa dipindahkan: bobot model, ambang, dan kelas kerusakan. Kerusakan khas pompa (keausan impeller, celah wear-ring, kavitasi, titik operasi bergeser) tidak ada di data ini. Karena itu klaim kami TKT 3 untuk komponen AI getaran, bukan untuk pompa. TKT 4 butuh rekaman pompa lab dengan kondisi yang kami induksi sendiri.
**Rujukan:** `05_BUKTI_TKT.md` §1, §3; `prototype\DATA.md` §1; `prototype\README.md` Keterbatasan #1.

### Q3. Efisiensi pompa butuh debit dan head. Tanpa itu, bagaimana kalian bicara energi?
**Jawaban:** Kami tidak menghitung efisiensi, dan tidak akan mengklaimnya. Efisiensi pompa = daya hidraulik ÷ daya listrik, dengan daya hidraulik = 0,163 × Q × H [S6]. Getaran, bahkan ditambah arus, tidak bisa menggantikan Q dan H. Peran DetakPompa adalah **triase**: memilih pompa mana yang didatangi tim flowmeter dan manometer lebih dulu. Di audit Ngagel I, debit diukur dengan flowmeter portabel dan hanya 12 dari 22 pompa yang terukur [S6]. Kalau PDAM punya data tekanan per pompa, KPI yang kami incar adalah **kW pada tekanan setara** dibanding baseline pompa itu sendiri, yang masih hipotesis (H2) dan akan kami tanyakan ke pakar audit. Satu catatan penting: setelah rekondisi, kW pompa bisa **naik** karena debitnya naik. Di 63 uji pompa irigasi, daya input naik di 58 % instalasi walaupun efisiensi rata-rata naik 33 %; energi baru turun (−22 %) kalau volume air tetap [Hanson 2002]. Karena itu KPI dampak yang kami pakai adalah **kWh/m³ per stasiun pada permintaan atau tekanan header yang sama**, bukan "kW pompa turun".
**Rujukan:** [S6]; `06_VALIDASI_PENGGUNA.md` §0 F4, §2 H2; `04_KEPUTUSAN.md` (revisi posisi); Hanson, *California Agriculture* 56(4), 2002, peer-reviewed (`11_RISET_KELEMAHAN.md` L6.4).

### Q4. Dua puluh unit, selang kepercayaan lebar. Apa yang sebenarnya bisa disimpulkan?
**Jawaban:** Sedikit, dan kami membatasi diri pada yang sedikit itu. Satu-satunya perbedaan yang selang kepercayaannya tidak memuat nol: usulan lebih baik dari aturan envelope + kurtosis (+0,179 [+0,083; +0,292]). Terhadap ambang RMS (−0,030 [−0,145; +0,067]) dan RF fitur statistik (+0,057 [−0,028; +0,138]), kami tidak bisa membedakan. Untuk abstain, AURC usulan vs ambang RMS + gerbang yang sama: −0,062 [−0,195; +0,076], tidak signifikan. Setelah koreksi Holm atas 22 uji berpasangan, tidak ada satu pun selisih usulan vs RMS yang signifikan.
**Rujukan:** `prototype\results\paired_bootstrap.csv`, `rmsgate_paired_bootstrap.csv`, `prototype\README.md` Keterbatasan #3.

### Q5. Pelacak Viterbi dan SNR dari FaceVitals itu DSP buku teks. Apa yang baru?
**Jawaban:** Setuju, algoritmanya bukan hal baru, dan kami tidak menjualnya sebagai kebaruan. Bahkan satu bagian FaceVitals gagal di mesin: SNR rasio pita justru **naik** saat derau ditambahkan, karena garis 60/120 Hz mendominasi pita. Kami menggantinya dengan prominensi garis lokal. Yang kami anggap baru untuk konteks ini ada tiga: (1) keluaran berupa urutan pompa untuk diaudit, bukan alarm kerusakan; (2) abstain yang selalu memberi langkah berikutnya; (3) rencana validasi memakai pompa yang kondisinya sudah diketahui dari audit ITS–PDAM sebagai *ground truth*. Ketiganya masih harus dibuktikan di pompa.
**Rujukan:** `03b_ADVOKAT_SETAN.md` §2.2; `prototype\README.md` (Keputusan desain setelah melihat data); [S6].

### Q6. Kalian mengubah pita frekuensi dan definisi SNR setelah melihat data. Bukankah itu overfitting?
**Jawaban:** Risikonya ada, dan karena itu kami menuliskannya. Dua keputusan dibuat setelah inspeksi: pita poros dilebarkan ke 15–35 Hz karena bantalan 16–19 berputar di ~19,5 Hz, dan gerbang SNR diganti ke prominensi garis lokal. Keduanya diputuskan dari inspeksi spektrum dan uji derau sintetis, **bukan** dari skor klasifikasi uji. Tetap saja, kami sudah melihat data ini. Uji yang bersih baru terjadi di TKT 4: rangkaian kerja dibekukan, lalu dijalankan pada rekaman pompa lab yang belum pernah kami lihat.
**Rujukan:** `prototype\README.md` (Desain evaluasi), `prototype\DATA.md` (Pengamatan sendiri), `05_BUKTI_TKT.md` §3.

### Q7. Mode deviasi dari baseline unit sendiri dapat AUC 1,0. Kenapa tidak itu yang dijual?
**Jawaban:** Karena angka itu tidak informatif. RMS saja juga mendapat AUC 1,0. Jendela "sehat" uji diambil dari rekaman yang sama dengan baseline, sedangkan rekaman rusak berasal dari sesi lain, jadi perubahan pemasangan sensor saja mungkin sudah cukup untuk memisahkan. Urutan rusak > waspada > sehat benar di 14/20 unit (RMS saja 12/20). Untuk mengukur alarm palsu mode ini, butuh beberapa rekaman sehat dari sesi berbeda. Itu masuk desain rekaman TKT 4: ≥5 × 30 detik per kondisi, dengan sensor dilepas-pasang di antaranya.
**Rujukan:** `prototype\results\deviation_scores.csv`, `prototype\README.md` (Mode deviasi), `05_BUKTI_TKT.md` §3.

---

## J2: Praktisi industri

### Q8. PDAM sudah punya power meter PM2100 di tiap panel, mungkin juga SCADA. Untuk apa alat kalian?
**Jawaban:** Betul, paper audit Ngagel I menyebut power meter Schneider PM2100 terpasang di tiap panel [S6], dan Schneider bermitra dengan PDAM untuk *smart water* sejak 2021 [S7]. Karena itu rencana kami adalah **membaca** meter itu, bukan memasang alat arus baru. Yang tidak diberikan meter: daya listrik naik karena pompa menurun atau karena katup diatur dan permintaan zona berubah. kW saja tidak membedakannya, dan audit pun hanya menjangkau 12 dari 22 pompa karena Q harus diukur manual [S6]. Kami ingin menjadi lapisan yang membandingkan tiap pompa dengan baseline-nya sendiri, lalu mengurutkan mana yang perlu diukur. Apakah SCADA PDAM sudah menghitung kinerja per pompa, kami belum tahu [ISI: hasil wawancara, H5]. Kalau sudah, celah kami jauh lebih kecil, dan kami akan mengatakannya.
**Rujukan:** [S6], [S7]; `06_VALIDASI_PENGGUNA.md` §2 H5, §6.6 L2; `07_BISNIS_DAMPAK.md` §6, R9.

### Q9. SEC Ngagel I 0,27–0,29 kWh/m³, sudah di bawah 0,4. Masalahnya apa?
**Jawaban:** Di level IPA memang efisien, dan paper itu sendiri menyimpulkan pengelolaan energinya secara umum efisien [S6]. Tetapi di level pompa, 5 dari 12 pompa yang terukur bekerja di bawah ±55 % [S6]. Satu pompa yang menurun hampir tidak menggeser angka bulanan IPA. Jadi kami tidak datang dengan pesan "PDAM boros". Pesannya: memilih pompa yang akan diaudit tanpa harus mengaudit 22 pompa secara manual. Apakah ini rasa sakit yang nyata bagi PDAM, itu hipotesis H3 kami, dan jawabannya [ISI: hasil wawancara].
**Rujukan:** [S6]; `04_KEPUTUSAN.md` (revisi posisi); `06_VALIDASI_PENGGUNA.md` §0 F5, F8, §2 H3.

### Q10. Operator tidak boleh menempel alat di aset tanpa surat Direksi, dan data tidak boleh keluar. Bagaimana pilotnya?
**Jawaban:** Kami menganggap ini risiko terbesar (H1). Pendekatannya: pilot lewat kerja sama riset ITS–PDAM, bukan pembelian, dengan izin tertulis pejabat berwenang. Alatnya non-invasif (akselerometer bermagnet, panel tidak dibuka), hanya membaca, berjalan offline di lokasi, tanpa sambungan ke SCADA atau internet. Kalau izin PDAM lama, kami menjalankan TKT 4 di pompa gedung Sarpras ITB sebagai lokasi cadangan. Lamanya proses izin itu sendiri kami catat sebagai data. Status permohonan saat ini: [ISI].
**Rujukan:** `06_VALIDASI_PENGGUNA.md` §2 H1, §5.2, §5.4; `07_BISNIS_DAMPAK.md` §7 R1–R2.

### Q11. Kalau alat kalian salah alarm, tim flowmeter dikirim ke pompa yang sehat. Kepercayaan langsung hilang.
**Jawaban:** Setuju, salah alarm adalah biaya nyata. Di data bantalan, pada tingkat jendela: usulan mengenali 186 dari 200 jendela sehat (RMS 182/200) dan menandai 352 dari 400 jendela rusak/berkembang (RMS 362/400). Jadi sekitar 7 % jendela sehat ditandai, dan angka itu dari bantalan, bukan pompa. Untuk produk: ambang dipilih untuk presisi, bukan sensitivitas; jumlah tanda per bulan dibatasi; dan metrik yang kami laporkan ke PDAM adalah **presisi top-3**, yaitu dari 3 pompa teratas, berapa yang terbukti menurun saat diukur. Di simulasi armada bantalan (leave-one-bearing-out), presisi@3 usulan 0,971 dan RMS + gerbang 0,952, tetapi armada itu dua pertiganya bermasalah (dasar acak 0,667). Pada armada 22 pompa yang lebih mirip IPA: 3 bermasalah (dasar acak 0,136) 0,707 vs 0,682; 5 bermasalah (0,227) 0,791 vs 0,765. Artinya ±5–6 dari 10 armada simulasi masih punya satu pompa sehat di daftar 3 teratas, dan kedua model salah menandai rekaman sehat yang sama (H_13_0). Angka itu belum dari pompa. Biaya satu kunjungan ukur: [ISI], dan itu akan dikurangkan dari nilai produk.
**Rujukan:** `05_BUKTI_TKT.md` §2 (matriks kebingungan), `prototype\results\summary.json`; `07_BISNIS_DAMPAK.md` §1 (metrik kunci), R4.

### Q12. Pompa S1 dan S2 baru dipasang 2018 tapi efisiensinya ±52 %. Itu bukan aus, dan getaran tidak akan melihatnya.
**Jawaban:** Benar. Paper audit sendiri menyebut penurunan S1/S2 "perlu dianalisis" [S6], dan penyebab yang masuk akal adalah titik operasi yang tidak cocok sejak awal. DetakPompa mendeteksi **perubahan terhadap baseline pompa itu sendiri**. Pompa yang sudah tidak efisien sejak dipasang tidak berubah, jadi tidak akan ditandai. Masalah seperti itu tetap milik audit dan desain sistem, dan kami bukan pengganti audit.
**Rujukan:** [S6]; `06_VALIDASI_PENGGUNA.md` §0 F6, §6.6 L5.

### Q13. Sensor murah kalian cukup? Arus motor di Ngagel I ratusan ampere.
**Jawaban:** Untuk sebagian, tidak. Akselerometer ADXL343 yang kami hitung di biaya punya laju sampel maksimum 3.200 Hz [B2], jadi pita efektifnya di bawah 1,6 kHz. Itu cukup untuk putaran poros ±24,8 Hz (±1.489 rpm [S6]), harmoniknya, dan frekuensi sudu, tetapi tidak cukup untuk analisis envelope bantalan frekuensi tinggi. Model kami yang sekarang dilatih di 42 kHz, jadi **tidak bisa dipakai langsung** di sensor itu; fiturnya harus dibatasi dan modelnya dilatih ulang. Arus motor Ngagel I 97–326 A per fasa [S6], melebihi clamp kelas hobi 100 A. Karena itu jalur utama adalah membaca PM2100 di panel, atau clamp di sisi sekunder CT panel [ISI: rating CT].
**Rujukan:** `07_BISNIS_DAMPAK.md` §3.1; [B2]; [S6].

---

## J3: Investor

### Q14. Kenapa PDAM mau bekerja dengan tim mahasiswa?
**Jawaban:** Kami belum tahu, dan itu yang sedang kami uji. Alasan yang mungkin membuat mereka mau: paper audit Ngagel I ditulis bersama staf PDAM dan dosen ITS [S6], jadi kerja sama riset dengan ITS sudah pernah terjadi; audit itu hanya menjangkau 12 dari 22 pompa; pilot tidak memakan anggaran PDAM, data tidak keluar dari lokasi, dan hasilnya bisa mereka cek dengan audit mereka sendiri. Alasan mereka mungkin menolak: SEC sudah di bawah patokan, pembelian lewat RKAP dan pengadaan, keamanan data operasional, dan Schneider sudah ada di dalam. Kami punya aturan berhenti: kalau akses (H1) dan rasa sakit (H3) sama-sama gagal setelah lima wawancara, ide ini turun ke cadangan. Kami juga tidak memberi uang atau hadiah apa pun ke staf PDAM, karena ada aturan gratifikasi. Bukti sejauh ini: [ISI: hasil wawancara dan status surat ke PDAM].
**Rujukan:** [S6]; `06_VALIDASI_PENGGUNA.md` §0, §2, §5.4; `07_BISNIS_DAMPAK.md` §5, §7.

### Q15. Siapa yang bayar, berapa, dan kapan balik modal?
**Jawaban:** Fase 0 tidak ada yang bayar; itu pilot riset. Fase 1: kampanye triase 3 bulan per IPA, [ASUMSI] Rp30 juta. Fase 2: langganan [ASUMSI] Rp300.000 per pompa per bulan, atau Rp79,2 juta per tahun untuk 22 pompa, ditambah capex ±Rp40,2 juta per IPA yang separuhnya lebih masih asumsi. Balik modal bagi PDAM sangat bergantung pada perilaku PDAM sendiri: skenario moderat ±8 bulan, skenario konservatif ±112 bulan, artinya praktis tidak balik modal. Karena itu kami menjual kampanye berbatas waktu lebih dulu, bukan langganan. Titik impas yang bisa dicek siapa pun: 76.464 kWh per tahun per IPA.
**Rujukan:** `07_BISNIS_DAMPAK.md` §2.3, §3.1, §3.4, §3.5.

### Q16. Apa bedanya dengan Include Technology (startup ITS) atau Schaeffler OPTIME?
**Jawaban:** Keduanya sudah lebih maju dari kami dalam produk. OPTIME adalah sensor getaran nirkabel dengan gateway dan aplikasi untuk motor, kipas, dan pompa, mendeteksi imbalance, misalignment, dan komponen longgar [S16]. Include, juara 3 University Startup World Cup 2023, mengerjakan integrasi IoT, deteksi kegagalan, dan predictive maintenance [S17]. Dari sumber yang kami buka, keduanya tidak menyebut energi per pompa atau abstain. Beda kami sempit: keluaran berupa **urutan pompa yang perlu diukur debitnya** untuk PDAM, memakai meter panel yang sudah ada, dan berani menjawab "tidak tahu" dengan langkah berikutnya. Itu bisa ditiru. Kami tidak mengklaim yang pertama.
**Rujukan:** [S16], [S17]; `03_RISET.md` §1.3; `07_BISNIS_DAMPAK.md` §6.

### Q17. Schneider tinggal menambah fitur triase. Apa yang tidak bisa ditiru?
**Jawaban:** Jujur, saat ini belum ada yang benar-benar tidak bisa ditiru. Kandidat kami: akses co-design ke PDAM lewat ITS (belum terjadi), data audit sebagai *ground truth* (bisa dipakai siapa saja), dan disiplin abstain (tekniknya umum). Strategi kami bukan bersaing dengan Schneider, melainkan menjadi lapisan analitik yang membaca meternya, dan kalau perlu bermitra. Kalau Schneider merilis fitur yang sama lebih dulu, nilai kami turun, dan kami lebih baik tahu itu cepat.
**Rujukan:** `07_BISNIS_DAMPAK.md` §1 (kotak 9), §6, §7 R9.

### Q18. Berapa ukuran pasarnya?
**Jawaban:** Yang bersumber: PDAM Surya Sembada memakai pemompaan di 6 IPA [S6]; Ngagel I saja punya 22 pompa [S6]; ada 38 Perumda air minum di Jawa Timur [B7]. Yang belum kami punya: jumlah pompa di IPA lain dan di tiap Perumda. Tanpa itu kami tidak mau menulis angka pasar dalam rupiah. Hitungan per unit yang bisa dicek: satu IPA dengan 22 pompa = Rp79,2 juta per tahun pada harga asumsi.
**Rujukan:** [S6], [B7]; `07_BISNIS_DAMPAK.md` §5, §9 #8.

### Q19. Berapa kWh dan tCO₂ yang sudah kalian hemat? Dan apakah ini layak investasi?
**Jawaban:** Nol. Kami belum menghemat satu kWh pun. Pilot pun tidak akan menghemat langsung; hemat terjadi hanya kalau PDAM mengaudit lalu merekondisi pompa yang ditandai. Skenario per IPA yang bisa diatribusikan ke kami: 12.352 kWh/tahun (konservatif) sampai 171.766 kWh/tahun (moderat), atau 10,7–149 tCO₂e dengan faktor emisi Jamali 0,87 [S21], semuanya berlabel skenario. Untuk investor, kami belum layak investasi: pra-pendapatan, belum berbadan hukum [ISI], belum ada data lapangan. Yang kami minta di Demo Day adalah akses pilot dan mentoring. Soal lisensi: model dilatih di Ottawa CC BY 4.0 yang boleh dipakai komersial; kami sengaja tidak memakai Paderborn yang non-komersial.
**Rujukan:** `07_BISNIS_DAMPAK.md` §3.4, §4.2, §7 R10, §8; [S12], [S13], [S21].

---

## J4: Reviewer skeptis

### Q20. AI kalian kalah dari ambang RMS. Kenapa pakai AI?
**Jawaban:** Di data ini, benar: kami belum bisa menunjukkan bahwa AI diperlukan. Tanpa abstain, ambang RMS 0,640 dan AI kami 0,608 (−0,030 [−0,145; +0,067]). Kami lalu memberi RMS **gerbang sinyal yang sama** dan skor keyakinan (jarak ke ambang, ditetapkan sebelum run). Hasilnya tetap setara: akurasi 0,639 vs 0,605 (−0,034 [−0,155; +0,071]), AURC 0,291 vs 0,229 (tidak signifikan), dan presisi 3 pompa teratas 0,952 vs 0,971 (+0,019 [−0,333; +0,333]) di armada simulasi yang 2/3 bermasalah, dan 0,765 vs 0,791 bila hanya 5 dari 22 bermasalah. RMS lebih jeli mengenali yang sudah rusak (recall 0,795 vs 0,470). AI lebih sering memberi label **waspada** (recall 0,415 vs 0,213, +0,202 [−0,056; +0,453], tidak signifikan setelah Holm), tetapi itu bukan deteksi lebih dini: kedua model menandai tahap awal untuk dicek sama seringnya (0,830 vs 0,840). Tidak ada metrik di mana AI terbukti lebih baik. Jadi klaim AI kami adalah **hipotesis**: di pompa, kW dan getaran juga berubah karena katup dan permintaan zona, dan model dengan beberapa masukan *mungkin* bisa memisahkannya dari keausan. Syarat lulusnya sudah kami bekukan dengan SHA-256 sebelum ada data baru (`prototype\PRAREG_TKT4.md` v2): di unit fisik yang tidak pernah dilihat, AI harus mengalahkan RMS + gerbang dalam akurasi seimbang, dan, bila data punya throttling katup, dalam membedakan throttling dari kerusakan; batas bawah CI 95 % selisih > 0 setelah koreksi Holm, tanpa kehilangan pompa rusak dan tanpa menambah alarm palsu. Kalau gagal, kata "AI" kami cabut dan yang kami kirim ke PDAM adalah gerbang sinyal + ambang RMS + antrean triase. Alasan throttling itu sudah kami uji sekali, di data lab pompa SKAB dengan prareg terkunci, dan **gagal** (Q31). Produknya triase, bukan modelnya.
**Rujukan:** `prototype\results\skab\summary.json`; `prototype\results\paired_bootstrap.csv`, `rmsgate_metrics.csv`, `rmsgate_paired_bootstrap.csv`, `triase\eval_log.txt`, `triase\eval_prevalensi_log.txt`; `05_BUKTI_TKT.md` §2b, §2c, §2d, §3; `prototype\PRAREG_TKT4.md`; [S14].

### Q21. Gerbang SNR itu aturan DSP. Bisa dipasang di depan RMS juga. Jadi abstain kalian bukan AI.
**Jawaban:** Benar, dan kami sudah mengujinya. Gerbang SNR adalah DSP warisan FaceVitals, dan itulah komponen yang **terbukti** mencegah jawaban palsu: ia menolak 98,8 % jendela sensor lepas, sama persis di depan RMS maupun di depan AI. Gerbang keyakinan model saja, baik RF maupun RMS, meloloskan 88–97 % jendela derau. Tahap kedua (gerbang ragu) juga bisa dipasang di RMS: jarak log ke ambang terdekat adalah skor keyakinan yang sah. Dengan itu, kurva cakupan-risiko RMS + gerbang tidak berbeda signifikan dari AI (AURC 0,291 vs 0,229, selisih −0,062 [−0,195; +0,076]), dan di cakupan praktis galat RMS sama atau lebih rendah. Jadi angka 98,8 % adalah jasa gerbang sinyal, bukan AI, dan kami tidak lagi menjual abstain sebagai nilai tambah AI.
**Rujukan:** `prototype\results\rmsgate_degradation_summary.csv`, `rmsgate_coverage_risk.png/.csv`, `rmsgate_paired_bootstrap.csv`; `prototype\detakpompa\models.py` (`RMSGateBaseline`, `rule_margin`); `05_BUKTI_TKT.md` §2b.

### Q22. Mana bukti wawancara pengguna?
**Jawaban:** [ISI: hasil wawancara — jumlah responden, peran, hipotesis yang lulus/gagal, komitmen nyata]. Kalau belum ada: "Belum ada wawancara yang selesai. Kami tidak mau mengutip siapa pun sebelum ada jawaban asli. Yang sudah siap: skrip 15 menit gaya *The Mom Test*, form persetujuan sesuai UU PDP, delapan hipotesis dengan kriteria lulus/gagal, dan aturan berhenti. Surat ke PDAM [ISI: status]." Jangan pernah menyebut isi persona simulasi sebagai pendapat pengguna.
**Rujukan:** `06_VALIDASI_PENGGUNA.md` §2–§4, §7; `AKSI_MANUSIA.md` #4.

### Q23. Alat kalian menjawab "tidak tahu" pada pompa yang benar-benar rusak. Itu berbahaya.
**Jawaban:** Benar, dan kami menunjukkan contohnya sendiri: rekaman C_16_2 (rusak) dijawab TIDAK TAHU karena garis putaran poros tenggelam oleh kerusakan (SNR 0,2 dB). Gerbang sinyal menolak 4,5 % jendela bersih, dan semuanya berasal dari rekaman rusak atau berkembang (C_16_1, C_16_2, C_17_2, O_7_1, O_7_2). Karena itu aturan produknya: TIDAK TAHU **tidak pernah** berarti aman. Setiap TIDAK TAHU disertai langkah berikutnya (pasang ulang sensor, ukur ulang, atau ukur debit manual), dan pompa itu masuk antrean UKUR ULANG yang dikerjakan sebelum ronde berikutnya. Kami sengaja **tidak** memberinya skor prioritas, karena skor dari sinyal yang ditolak tidak bisa dipercaya (sensor lepas dulu mendapat 0,87). Di uji, 69 dari 76 jendela TIDAK TAHU (91 %) berasal dari bantalan berkembang/rusak, dan itu alasan aturan "TIDAK TAHU = ukur ulang". Gagasan bahwa "SNR rendah dengan energi getaran tinggi" bisa menjadi tanda tersendiri belum kami uji.
**Rujukan:** `prototype\results\demo\laporan_C_16_2.txt`, `prototype\README.md` (Abstain; Keterbatasan #5).

### Q24. FaceVitals kalian TKT 4. Apakah TKT itu diwariskan? Dan kenapa ini TKT 3, bukan 2?
**Jawaban:** Tidak diwariskan. TKT 4 FaceVitals hanya berlaku untuk detak jantung dari video wajah. Yang dipakai ulang hanya fungsi DSP (spektrum daya, SNR, puncak frekuensi, pelacak Viterbi), dan metode inti FaceVitals (proyeksi warna kulit) tidak berlaku untuk getaran. Sebelum 28 Oktober status kami TKT 2. TKT 3 berarti fungsi utama terbukti secara eksperimental: rangkaian kerja berjalan di data nyata publik, dengan tiga baseline dan tanpa kebocoran, dan hasilnya ada di file. TKT 4 butuh validasi komponen di lab dengan rekaman sendiri, dan itu belum.
**Rujukan:** `05_BUKTI_TKT.md` §1; `03b_ADVOKAT_SETAN.md` §1; `04_KEPUTUSAN.md` (Syarat); `07-MEGA-PROMPT-ITS-HACKATHON-28okt2026.md` §A (arti TKT).

### Q25. Apa kelemahan terbesar kalian?
**Jawaban:** Kami belum punya pompa sendiri dan belum merekam pompa PDAM. Satu-satunya uji di data pompa, yaitu data lab publik SKAB milik pihak lain (1 testbed), **gagal**: model residual kami tidak lebih baik dari ambang arus, dan data itu juga tidak tajam untuk klaim kami (Q31). Model getaran kami belum pernah dilatih dengan arus motor, belum ada izin PDAM, dan [ISI: belum ada / baru N] wawancara pengguna. Tiga anggapan inti produk masih hipotesis: sinyal cukup untuk triase tanpa Q dan H (H2), PDAM mengizinkan akses (H1), dan "pompa mana dulu" adalah rasa sakit yang nyata (H3). Yang kami punya adalah cara uji yang jujur, sehingga kalau salah satu anggapan itu keliru, kami akan tahu dengan cepat. Rencananya sudah ada, dan aturan berhentinya juga.
**Rujukan:** `05_BUKTI_TKT.md` §2e, §3; `prototype\results\skab\summary.json`; `06_VALIDASI_PENGGUNA.md` §2, §6.6; `07_BISNIS_DAMPAK.md` §7.


### Q26. Kalau RMS diberi skor keyakinan berupa jarak ke ambang, apa bedanya dengan AI kalian?
**Jawaban:** Di data bantalan ini, tidak ada beda yang bisa kami buktikan. Skor itu kami tetapkan **sebelum** menjalankan pembanding: jarak log10 skor RMS ke ambang terdekat, dengan τ dari validasi silang di unit latih, resep yang sama dengan AI. Hasilnya, RMS + gerbang setara dengan AI di akurasi, AURC, dan presisi top-3. Bedanya hanya pada bentuk galat: 60 jawaban AI yang paling yakin semuanya benar, sedangkan 10 % jawaban RMS yang paling yakin memuat 16 jendela waspada yang disebut "rusak". Di sisi lain, RMS lebih jarang menurunkan bantalan rusak menjadi waspada. Tidak satu pun dari ini signifikan dengan 20 bearing.
**Rujukan:** `prototype\README.md` (Eksperimen tambahan), `prototype\results\rmsgate_coverage_risk.csv`, `rmsgate_per_class_disagreement.csv`.

### Q27. Rekaman sensor lepas dulu dapat prioritas 0,87, lebih tinggi dari pompa rusak. Masih begitu?
**Jawaban:** Tidak. Itu bug, dan sudah diperbaiki. Rekaman yang ditolak gerbang sinyal sekarang **tidak diberi prioritas** dan masuk antrean **UKUR ULANG** dengan langkah berikutnya, sehingga tidak bisa menyalip pompa yang benar-benar dinilai. Rekaman yang ditahan karena model ragu hanya menampilkan prioritas "sementara" dan juga masuk UKUR ULANG. Ada tes khusus untuk ini (`tests\test_triage.py`). Di armada contoh 22 rekaman, sensor lepas dan rekaman derau −10 dB sama-sama masuk UKUR ULANG, sementara 3 teratas AUDIT DULU adalah bantalan rusak.
**Rujukan:** `prototype\results\demo\laporan_sensor_lepas.txt`, `prototype\results\triase\armada_22\antrean_usulan.txt`, `05_BUKTI_TKT.md` §2c.

### Q28. Kenapa 10 dari 22 pompa Ngagel I tidak diaudit? Mungkin pompa itu cadangan atau mati saat audit.
**Jawaban:** Kami belum tahu, dan kami tidak mau menebak. Paper audit [S6] melaporkan 5 dari 8 pompa air baku dan 7 dari 14 pompa distribusi yang terukur, dengan debit diukur memakai flowmeter ultrasonik portabel. Alasan 10 pompa lainnya tidak ada di tulisan itu. Bisa saja sebagian adalah cadangan atau sedang tidak beroperasi. Ini pertanyaan pertama kami untuk penulis S6 dan unit produksi PDAM. Kalau ternyata pompa itu cadangan, argumen "tidak terjangkau audit" melemah, dan yang tersisa adalah argumen kapasitas: berapa pompa yang bisa diukur debitnya per ronde.
**Rujukan:** [S6]; `06_VALIDASI_PENGGUNA.md` §3 (skrip wawancara); `JURI_90\SKOR.md` §9 pertanyaan 1–2.

### Q29. Alat kalian menjawab TIDAK TAHU sekitar 12 % dari waktu. Operator tidak akan malas mengukur ulang?
**Jawaban:** Itu risiko nyata, dan kami belum mengujinya dengan operator. Angkanya: di titik operasi, usulan menjawab 87,3 % jendela (jadi 12,7 % TIDAK TAHU); di tingkat rekaman, 53 dari 60 rekaman dijawab (7 TIDAK TAHU: 2 karena sinyal, 5 karena ragu). Kami memilih menjawab TIDAK TAHU karena 69 dari 76 jendela TIDAK TAHU (91 %) ternyata berasal dari bantalan yang berkembang rusak atau rusak, jadi mengabaikannya berbahaya. Setiap TIDAK TAHU membawa satu langkah konkret (pasang ulang sensor, rekam ulang), dan antrean UKUR ULANG dipisah dari AUDIT DULU supaya tidak menyita kapasitas audit. Apakah operator mau melakukannya adalah hipotesis H6 di wawancara.
**Rujukan:** `prototype\results\summary.json` (cakupan 0,873), `results\triase\eval_log.txt` (53/60), `05_BUKTI_TKT.md` §2c; `06_VALIDASI_PENGGUNA.md` §2 (H6).

### Q30. Recall waspada 0,415 vs 0,213. Itu artinya AI kalian mendeteksi lebih dini?
**Jawaban:** Tidak. Kami sempat menulisnya begitu dan sudah kami cabut. Kalau dihitung berapa jendela tahap awal (waspada) yang ditandai "perlu cek" sama sekali, hasilnya 156/188 = 0,830 untuk AI dan 158/188 = 0,840 untuk RMS + gerbang. Bedanya hanya nama tahapnya: RMS menyebut tahap awal "rusak", AI menyebutnya "waspada", dan akibatnya AI juga menurunkan banyak bantalan rusak menjadi "waspada" (recall rusak 0,470 vs 0,795). Untuk triase, yang penting adalah dicek atau tidak, dan di situ keduanya setara. Karena itu recall waspada di prareg baru kami hanya metrik sekunder, dengan catatan "label tahap, bukan deteksi dini".
**Rujukan:** `prototype\results\rmsgate_metrics.csv` (baris `lolos_gerbang_sinyal_sama`), `05_BUKTI_TKT.md` §2b, `prototype\PRAREG_TKT4.md` §6.

---

### Q31. Kalian bilang model hidraulik bisa membedakan katup ditutup dari pompa rusak. Sudah diuji di pompa nyata?
**Jawaban:** Sudah kami uji di data lab pompa nyata milik pihak lain, yaitu SKAB (Skoltech, 1 testbed). Prareg-nya kami kunci dengan hash sebelum data diunduh. Hasilnya **gagal**: model residual hidraulik tidak lebih baik dari ambang sederhana.
- **Memisahkan katup vs fault (H1):** AUROC 1,000 vs ambang arus juga 1,000.
- **Deteksi anomali umum (H2):** AUROC 0,532 vs 0,581.

Dari diagnosis post-hoc, H1 di SKAB terutama mengukur sesi rekaman, karena run katup berada di ±32 L/min sedangkan run fault di ±125 L/min. Throttling-nya juga kecil (debit turun ±6 %).

Jadi klaim "AI memisahkan throttling dari keausan" masih **hipotesis**. Literaturnya ada (metode QP/QH kelompok LUT, paten ABB), tapi kami belum membuktikannya sendiri. Pengujian yang benar butuh rig dengan beberapa pompa dan throttling bertingkat, atau data PM2100 + tekanan header PDAM.
**Rujukan:** `prototype\PRAREG_SKAB.md` (+ `.sha256`), `prototype\results\skab\summary.json`, `run_skab_log.txt`, `05_BUKTI_TKT.md` §2e, `11_RISET_KELEMAHAN.md` §2–§3.

---

## Pertanyaan cadangan (kalau waktu Q&A panjang)
- "Angka motor 45 % listrik dunia dan potensi hemat 20–30 %?" → Hanya konteks. Sumbernya [S3] membahas standar efisiensi sistem motor, bukan deteksi kerusakan; kami tidak menautkan 20–30 % ke DetakPompa (`03b` §2.3).
- "Misalignment kan menaikkan konsumsi listrik?" → Bukti tidak konsisten. Tesis Jesse 2001 tidak menemukan korelasi signifikan selama masih dalam toleransi kopling [S9]. Jalur energi yang bisa dipertahankan adalah keausan pompa [S10] dan ketidakseimbangan skala lab [S8].
- "Siapa merawat alatnya setelah lomba?" → Belum terjawab. Rencana: README perawatan, komponen murah yang bisa diganti, serah terima ke unit (`06` §6.6 L10). [ISI: siapa di PDAM/Sarpras yang menerima].
