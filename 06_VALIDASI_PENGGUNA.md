# 06_VALIDASI_PENGGUNA: rencana validasi pengguna DetakPompa
### Agen A7 "Peneliti Pengguna" · 28 Okt 2026 · tim: Aziz (PIC), Uqi, Pio, Poggy

**Dasar:** `04_KEPUTUSAN.md`, `03_RISET.md` (§1, S6, S10, S16, S17), `03b_ADVOKAT_SETAN.md` (§2), ditambah pembacaan ulang **teks lengkap S6** dan *Board Manual* PDAM Surya Sembada (§9).

**Aturan baca:**
- **[H]** = hipotesis tim, **belum** divalidasi. Jangan ditulis sebagai fakta di berkas lomba.
- **[S6-teks]** = fakta yang dibaca langsung dari teks lengkap paper S6 (PDF diekstrak dengan pdftotext pada 28 Okt 2026).
- **[cuplikan]** = hanya dari ringkasan hasil pencarian. Halamannya tidak dibuka, jadi **tidak boleh dikutip**.
- Semua isi §6 adalah **simulasi**. Setiap barisnya diberi tanda dan **dilarang dikutip** di berkas lomba, deck, atau video.
- Agen tidak menghubungi siapa pun dan tidak login. Dokumen ini juga tidak memuat nomor HP atau email pribadi. Nama orang hanya muncul kalau sudah tercantum publik sebagai penulis paper.

---

## 0. Fakta baru dari teks lengkap S6 yang mengubah rencana

Paper S6 (Indra, Rachman, Wafiyuddin, Soedjono; JIST 5(2), Feb 2024) dibaca utuh. Isinya lebih rinci daripada ringkasan di `03_RISET.md`:

| # | Fakta [S6-teks] | Implikasi untuk DetakPompa |
|---|---|---|
| F1 | PDAM Surya Sembada memakai pemompaan di **6 IPA**, ditambah kombinasi gravitasi-pompa di 2 sumber air baku. Topografi Surabaya datar (3–6 m dpl), jadi sistem gravitasi tidak memungkinkan | Pasar internal PDAM lebih dari Ngagel I saja |
| F2 | IPA Ngagel I dibangun 1922 dengan kapasitas 60 L/s, mengalami 6× *uprating* sampai **1.800 L/s (1996)**. Ada **8 pompa air baku + 14 pompa distribusi** | Satu IPA = 22 pompa. Cakupan audit menjadi isu (F3) |
| F3 | Audit energi hanya mengukur **5 dari 8** pompa air baku dan **7 dari 14** pompa distribusi | Separuh pompa tidak terukur pada audit itu. Peluang nilai: **triase**, yaitu pompa mana yang harus diaudit lebih dulu [H] |
| F4 | Daya diukur dengan **power meter analyzer Schneider EasyLogic PM2100 yang terpasang di tiap panel** pompa air baku dan distribusi. Debit diukur dengan **flowmeter ultrasonik clamp-on portabel** (ChronoFLO 2), head dengan manometer, putaran dengan stroboskop/tachometer, suhu dengan termometer inframerah | **Penting.** kW per pompa kemungkinan **sudah tersedia** di panel. Yang mahal dan manual adalah **debit (Q)** dan **head (H)**. Efisiensi pompa = Ph/Pi dengan Ph = 0,163 × Q × H. **Arus + getaran saja tidak bisa menghitung efisiensi** tanpa Q dan H |
| F5 | Efisiensi total: U2 88,77 %, U3 92,91 %, U5 92,06 %, S1 (air baku) 82,43 %; distribusi U1 77,59 %, U3 87,31 %, T4 60,40 %. Yang buruk: air baku U6 **54,26 %**, distribusi U6 **51,76 %**, S1 **51,18 %**, S2 **52,60 %**, T1 **49,77 %** | Ada 5 dari 12 pompa terukur yang di bawah ±55 % |
| F6 | Distribusi S1 dan S2 **baru dipasang 2018**, tetapi efisiensinya sudah ±51–53 %. Paper menyebut penurunan ini "perlu dianalisis" | Efisiensi rendah **tidak selalu karena aus**. Bisa karena titik operasi/kurva sistem tidak cocok. Getaran belum tentu menangkapnya [H] |
| F7 | Aturan praktis yang dipakai paper: pompa dengan efisiensi ≤ 50 % → perbaikan total/penggantian. Pompa yang ≥ 60 % → perawatan rutin (regreasing, kencangkan baut, bersihkan elektromotor) | Keluaran yang dimengerti pengguna adalah **tindakan** (rawat / rekondisi impeller / overhaul), bukan "skor kesehatan" |
| F8 | SEC IPA Ngagel I: **0,27 kWh/m³ (2021), 0,29 kWh/m³ (2022)**, di bawah standar industri air bersih **< 0,4 kWh/m³**. Paper menyimpulkan pengelolaan energi "secara umum efisien", sambil tetap meminta perhatian pada pompa yang efisiensinya turun | **Risiko besar untuk rasa sakit:** di level IPA, manajemen bisa merasa "sudah efisien". Masalahnya hanya terlihat **per pompa** |
| F9 | Paper menulis PDAM "sampai sekarang belum melakukan audit energi" (mengutip Wu 2019, kutipan yang janggal) dan menyarankan dukungan manajemen puncak + sistem manajemen energi | Tanyakan di wawancara: apakah audit energi sekarang rutin? Siapa pemiliknya? |
| F10 | Penulis ke-3 (Wafiyuddin) berafiliasi **PDAM Surya Sembada**; penulis ke-1 dan ke-4 dari **ITS**; penulis ke-2 dari **Kementerian PUPR** | Jalur kontak: ITS → staf PDAM. Lihat §5 |

Fakta tata kelola dari *Board Manual* PDAM Surya Sembada (PDF di pdam-sby.go.id, dibuka 28 Okt 2026):
- Sistem dua badan: **Dewan Pengawas** dan **Direksi**. Direksi = **Direktur Utama, Direktur Operasi, Direktur Pelayanan, Direktur Keuangan**. Anggota Direksi dipilih dan diberhentikan oleh **Kepala Daerah selaku pemilik**.
- Tugas pengawasan Dewan Pengawas antara lain kepatuhan Direksi pada **RKAP** dan **persetujuan atas transaksi**. Direksi menetapkan SOP, termasuk **pengadaan barang dan jasa** serta sistem teknologi informasi.
- Ada bagian **pengendalian gratifikasi**. Konsekuensinya: **jangan memberi uang, hadiah, atau honor** kepada pegawai PDAM yang diwawancarai (§5.4).
- Struktur di bawah Direksi (nama unit produksi/IPA, bagian energi/aset): **tidak ketemu** di dokumen yang dibuka. `[ISI: struktur organisasi di bawah Direksi, tanyakan saat wawancara #1]`

---

## 1. Peta pemangku kepentingan

### 1.1 Pengguna utama: PDAM Surya Sembada Surabaya

| Peran | Rasa sakit (hipotesis) | Yang dipakai sekarang | Siapa yang memutuskan beli | Pengaruh ke keputusan |
|---|---|---|---|---|
| **Operator rumah pompa** (shift, IPA Ngagel) | [H] Harus menjaga tekanan/debit per zona 24 jam. Pompa yang "terasa beda" (bunyi, panas) sulit dibuktikan ke atasan. Disalahkan kalau pompa mati mendadak | [S6-teks] Panel dengan power meter PM2100. [H] Log manual per jam/shift, indera (bunyi, raba, panas), SCADA kalau ada `[ISI]` | Tidak memutuskan | **Pemakai harian.** Bisa memveto diam-diam (alat tidak dibaca, sensor dicabut) |
| **Teknisi pemeliharaan** (mekanik/listrik) | [H] Jadwal perawatan berbasis waktu/kerusakan. Overhaul butuh izin *downtime* dan suku cadang. Tidak tahu pompa mana yang paling perlu dibongkar dulu | [S6-teks] Rekomendasi: regreasing, kencangkan baut, bersihkan elektromotor, rekondisi/penyetelan impeller. [H] Alat ukur portabel (stroboskop, termometer IR) | Tidak memutuskan; mengusulkan | Menentukan apakah sensor bisa dipasang aman. **Pengguna kedua** |
| **Kepala IPA / kepala unit produksi** | [H] Target produksi dan kontinuitas layanan. Anggaran rekondisi terbatas, jadi harus memilih pompa. Audit manual hanya mencakup sebagian pompa (F3) | [S6-teks] Audit energi (dengan ITS) + data produksi bulanan + kWh PLN bulanan. [H] Laporan bulanan ke Direktur Operasi | Mengusulkan ke Direktur Operasi; bisa menyetujui **pilot non-invasif** kecil `[ISI: batas kewenangan]` | **Champion potensial.** Pemilik masalah "pompa mana dulu" |
| **Manajer energi / aset** (kalau ada) | [H] Biaya energi Rp147,65 M (2021), 24,37 % opex; biaya energi Rp409/m³ vs rata-rata nasional Rp356,34/m³ [S6]. Target potong biaya listrik 30 % [S7]. Harus melaporkan kinerja energi | [S7] Kemitraan *smart water* dengan Schneider/PUPR (2021). [H] SCADA/EMS vendor, spreadsheet SEC | Mengusulkan; kadang memegang anggaran program efisiensi `[ISI: unit ini ada atau tidak]` | Paling paham angka kWh/m³. **Pengguna laporan** |
| **Direksi** (Direktur Operasi, Direktur Keuangan) | [H] Rasio biaya energi terhadap opex, tarif, laporan ke pemilik (Pemkot). Risiko pengadaan (kepatuhan, audit) | Board Manual: RKAP, SOP pengadaan, persetujuan transaksi oleh Dewan Pengawas | **Pembeli sebenarnya.** Anggaran lewat RKAP tahunan | Akan bertanya: siapa vendornya, garansi, keamanan data, apakah ini masuk RKAP |
| **TI / keamanan data SCADA** | [H] Larangan data operasional keluar jaringan, takut perangkat asing di jaringan OT | [H] SCADA tertutup `[ISI]` | Veto teknis | **Penghambat terbesar untuk pilot** kalau data perlu keluar |

### 1.2 Pengguna sekunder

| Segmen | Rasa sakit (hipotesis) | Yang dipakai sekarang | Siapa memutuskan beli | Catatan jujur |
|---|---|---|---|---|
| **Gedung bertingkat / hotel / RS** (pompa transfer & booster ke tangki atap, pompa hidran) | [H] Pompa mati → air tidak sampai ke kamar/ruang rawat → komplain, risiko klinis di RS. Energi pompa **kecil** dibanding chiller/AC | [H] Perawatan preventif terjadwal, kontrak vendor MEP, cek manual teknisi; BMS di gedung besar | Chief engineer mengusulkan → GM/manajemen properti atau direktur RS menyetujui | [H] Nilainya kemungkinan di **downtime**, bukan kWh. Ini bertentangan dengan narasi energi DetakPompa |
| **Kawasan industri SIER** (Rungkut/Berbek) | [H] Pompa proses/utilitas di pabrik; izin downtime sulit; tagihan listrik per pabrik sehingga efek satu motor tidak terlihat (lihat persona di `03b` §2.9) | [H] Vendor sensor getaran (OPTIME [S16], Groundup.ai [S18]), kontrak layanan | Kepala maintenance/engineering → manajemen pabrik | Pesaing komersial paling padat. Jumlah tenant: `[ISI]` |
| **Perumda Tirtawening Kota Bandung** | [H] Sama dengan PDAM Surabaya (biaya energi pompa). Data energi Tirtawening: **tidak ketemu** (pencarian 28 Okt 2026) | `[ISI]` | Direksi Perumda | Akses dari Bandung lebih dekat bagi tim. Bisa jadi **pembanding**, bukan pengganti Surabaya |
| **Sarpras kampus (ITB, ITS)** | [H] Banyak gedung dengan pompa transfer/sumur; perawatan reaktif; anggaran lewat unit | [H] Teknisi gedung, kontrak outsourcing | Direktorat sarana prasarana | **Lokasi pilot paling mudah** (TKT 4–5), tetapi bukan pembayar utama |

---

## 2. Hipotesis kritis (urut dari paling berisiko)

"Risiko" = (peluang salah) × (dampak ke ide kalau salah). Kriteria lulus/gagal memakai **perilaku masa lalu** dan **komitmen nyata**, bukan pujian.

| # | Hipotesis [H] | Kenapa berisiko | Lulus kalau … | Gagal kalau … | Ditanya ke |
|---|---|---|---|---|---|
| **H1** | **Akses:** PDAM (atau minimal satu lokasi sekunder) mengizinkan **sensor non-invasif** (clamp arus + akselerometer magnet) dipasang di ≥1 pompa, **atau** memberi data historis kW/arus/tekanan per pompa, dalam ≤ 6 minggu | Tanpa ini tidak ada TKT 5 dan tidak ada validasi lapangan. F4 + `03b` §2.9: aset 24 jam, SCADA tertutup, izin direksi | ≥1 pemangku PDAM (kepala IPA ke atas) menyebut **jalur izin konkret** (surat ke siapa, berapa lama) **dan** bersedia memulai prosesnya, atau ≥1 lokasi sekunder memberi izin tertulis | Semua responden PDAM bilang "harus Direksi" tanpa jalur, atau perkiraan izin > 3 bulan, **dan** tidak ada lokasi sekunder yang mau |
| **H2** | **Sinyal cukup:** pola arus + getaran (tanpa debit dan head) bisa memberi tanda **perubahan kinerja hidraulik** yang berguna untuk memilih pompa yang perlu diukur/rekondisi | F4: efisiensi butuh Q dan H. F6: pompa baru pun bisa ±52 %. `03b` §2.3: rantai fault → kWh lemah | Pakar (penulis S6 / dosen mesin fluida) menyebut minimal satu indikator dari arus/getaran yang **mereka pakai sendiri** untuk menduga penurunan efisiensi (mis. kW naik pada tekanan yang sama, getaran pada frekuensi sudu impeller), **dan** setuju bahwa "triase lalu ukur manual" masuk akal | Pakar menyatakan tanpa debit/head tanda itu tidak bisa dibedakan dari perubahan titik operasi, **dan** PDAM tidak punya data tekanan per pompa yang bisa digabung |
| **H3** | **Rasa sakit cukup besar:** di PDAM, "tidak tahu pompa mana yang boros/menurun di antara audit" adalah masalah yang **sudah** menimbulkan biaya atau kejadian dalam 12 bulan terakhir | F8: SEC IPA 0,27–0,29 < 0,4, jadi manajemen bisa merasa sudah efisien | ≥3 dari 5 responden PDAM menceritakan **kejadian spesifik** (pompa ketahuan rusak/boros terlambat, overhaul darurat, komplain tekanan) **dan** menyebut perkiraan biayanya (Rp, jam downtime, atau kWh) | ≤1 responden punya cerita spesifik, atau semua menjawab "sudah ditangani audit/vendor" |
| **H4** | **Mereka bertindak atas tanda:** hambatan utama adalah **informasi** (pompa mana), bukan anggaran atau izin downtime | Kalau hambatannya anggaran, alat kita hanya menambah daftar yang tidak dikerjakan | ≥2 responden PDAM menyebut contoh rekomendasi audit (mis. T1, U6, S1, S2) yang **sudah ditindaklanjuti**, atau menyebut bahwa pemilihan pompa untuk rekondisi saat ini "tebak-tebakan" | Rekomendasi S6 belum ditindaklanjuti karena anggaran/downtime, dan responden menyebut itu sebagai hambatan utama |
| **H5** | **Celah belum diisi:** PDAM belum punya pemantauan kondisi/efisiensi per pompa yang berjalan (dari Schneider [S7], SCADA, atau vendor PdM) | Kemitraan Schneider 2021 [S7] bisa sudah mencakup ini | Responden mengonfirmasi data per pompa hanya dicatat/dilihat manual **atau** dashboard yang ada tidak menghitung kinerja per pompa | Ada sistem yang sudah menghitung efisiensi/kWh per m³ per pompa secara rutin dan dipakai |
| **H6** | **Abstain dihargai:** jawaban "tidak tahu, sinyal jelek, cek sensor" menambah kepercayaan, bukan mengurangi | Inti pembeda tim. Bisa dianggap "alat tidak berguna" | Setelah demo, ≥3 dari 5 responden memilih "alat yang kadang bilang tidak tahu" daripada "alat yang selalu memberi skor", **dengan alasan mereka sendiri** | Mayoritas bilang "kalau tidak tahu, buat apa dipasang" |
| **H7** | **Jalur pembayar:** ada jalur realistis dari pilot gratis ke pembelian (mis. RKAP tahun berikut, kerja sama riset ITS–PDAM, program efisiensi energi) | `03b` §2.5: BUMD, siklus anggaran tahunan | Responden manajerial menyebut **pos anggaran/jalur** yang pernah dipakai untuk hal serupa (alat ukur, audit, SCADA) dan siapa penandatangannya | Tidak ada yang bisa menyebut jalur; semua pembelian TI/alat lewat vendor besar dengan tender |
| **H8** | **Segmen sekunder** (hotel/RS/gedung) mau mencoba DetakPompa **untuk alasan energi** | [H] Pompa transfer kecil; nilai lebih ke downtime | ≥1 chief engineer menyebut biaya listrik pompa sebagai keluhan spesifik | Semua hanya peduli "pompa jangan mati" → narasi untuk segmen ini harus downtime, bukan energi |

**Aturan berhenti (diusulkan untuk orkestrator):** kalau **H1 dan H3 sama-sama gagal** setelah 5 wawancara, DetakPompa turun ke cadangan dan E1 LautHemat dievaluasi ulang (sesuai `04_KEPUTUSAN.md`). Kalau hanya H2 gagal, ubah produk menjadi **alat triase + penggabung data panel**, bukan "AI efisiensi" (lihat §6.6).

---

## 3. Skrip wawancara 15 menit

### 3.0 Aturan pewawancara (gaya *The Mom Test*)
- Tanyakan **kejadian yang sudah terjadi** ("terakhir kali …"), bukan pendapat tentang masa depan ("apakah Bapak akan …").
- **Jangan menyebut DetakPompa, AI, atau sensor** sebelum menit 10. Kalau responden bertanya, jawab "nanti kami tunjukkan, kami ingin dengar cara kerja Bapak/Ibu dulu."
- Jangan memancing angka. Kalau responden menyebut "boros", tanyakan "seberapa? dari mana Bapak tahu?"
- Pujian ("bagus sekali idenya") **bukan data**. Catat sebagai "pujian" dan lanjutkan ke permintaan komitmen.
- Satu orang bertanya, satu orang mencatat **kata-kata responden apa adanya**. Rekam audio **hanya** kalau ada persetujuan tertulis (§4).
- Akhiri dengan **permintaan komitmen kecil** (waktu, data, perkenalan). Ini mata uang validasi yang sebenarnya.

### 3.1 Versi OPERATOR / TEKNISI (rumah pompa)

| Menit | Bagian | Pertanyaan (non-leading) | Yang dicari / catat |
|---|---|---|---|
| 0–1 | Pembuka | "Terima kasih waktunya. Kami mahasiswa yang sedang belajar soal pengoperasian pompa air. Tidak ada jawaban benar atau salah, dan nama Bapak/Ibu tidak akan ditulis. Boleh saya cek dulu form persetujuannya?" | Persetujuan ditandatangani; rekam audio ya/tidak |
| 1–4 | Masalah | "Ceritakan satu shift biasa: apa saja yang Bapak/Ibu cek di pompa?" · "Apa bagian yang paling bikin repot dalam seminggu terakhir?" · "Kapan terakhir kali ada pompa yang bermasalah? Ceritakan dari awal." | Kejadian spesifik, tanggal kira-kira, gejala pertama yang terlihat |
| 4–7 | Cara sekarang | "Bagaimana Bapak/Ibu tahu ada yang tidak beres dengan pompa itu?" · "Dicatat di mana? Siapa yang membaca catatannya?" · "Angka apa saja yang terlihat di panel? Mana yang benar-benar dilihat?" · "Kalau Bapak/Ibu curiga pompa menurun, apa yang dilakukan selanjutnya?" | Alat yang dipakai (panel kW/arus, SCADA, log kertas, indera); jalur lapor |
| 7–10 | Biaya / sakit | "Waktu kejadian itu, apa akibatnya: tekanan turun, ada komplain, lembur, pompa diganti?" · "Berapa lama sampai beres?" · "Pernah tidak, pompa sebenarnya sudah lama menurun tapi baru ketahuan belakangan? Bagaimana ketahuannya?" | Biaya dalam jam, Rp, komplain. **Jangan** menyebut "boros listrik" lebih dulu |
| 10–13 | Reaksi demo | Tunjukkan demo ≤90 detik (layar: daftar pompa, satu pompa ditandai "berubah sejak bulan lalu", satu pompa "tidak tahu, sinyal jelek"). Lalu: "Apa yang Bapak/Ibu lihat di sini?" · "Kalau layar ini muncul di shift Bapak, apa yang akan dilakukan?" · "Bagian mana yang tidak masuk akal?" · "Yang 'tidak tahu' ini, menurut Bapak bagaimana?" | Interpretasi spontan; apakah tanda bisa ditindaklanjuti; reaksi terhadap abstain |
| 13–15 | Mau pakai? Siapa menyetujui? | "Kalau ada alat ditempel di luar motor (tanpa membuka panel), siapa yang harus mengizinkan?" · "Apa yang membuat Bapak/Ibu tidak mau alat seperti ini ada di rumah pompa?" · "Boleh kami kembali 15 menit untuk melihat rumah pompanya, kalau atasan mengizinkan?" · "Siapa lagi yang sebaiknya kami ajak bicara?" | Nama **jabatan** pemberi izin; keberatan; komitmen (kunjungan, perkenalan) |

### 3.2 Versi MANAJER (kepala IPA/unit produksi, manajer energi/aset, chief engineer, kepala sarpras)

| Menit | Bagian | Pertanyaan (non-leading) | Yang dicari / catat |
|---|---|---|---|
| 0–1 | Pembuka | Sama dengan 3.1, ditambah: "Kami tidak sedang menjual apa pun. Kami ingin memahami bagaimana keputusan perawatan pompa diambil." | Persetujuan |
| 1–4 | Masalah | "Dalam setahun terakhir, keputusan soal pompa apa yang paling sulit Bapak/Ibu ambil?" · "Bagaimana Bapak/Ibu memilih pompa mana yang direkondisi atau di-overhaul lebih dulu?" | Proses keputusan nyata, siapa terlibat |
| 4–7 | Cara sekarang | "Terakhir kali kinerja pompa dievaluasi, bagaimana caranya? Siapa yang melakukan, alatnya apa, berapa pompa yang tercakup?" · "Setelah evaluasi itu, apa yang terjadi dengan rekomendasinya?" · "Sistem atau laporan apa yang Bapak/Ibu lihat tiap bulan soal energi?" | Frekuensi audit, cakupan (bandingkan F3), tindak lanjut (H4), sistem yang ada (H5) |
| 7–10 | Biaya / sakit | "Kalau satu pompa besar menurun tanpa ketahuan selama beberapa bulan, apa dampaknya untuk unit Bapak/Ibu?" · "Pernah terjadi? Berapa kira-kira biayanya, dalam Rp, kWh, atau jam layanan terganggu?" · "Angka apa yang paling sering ditanyakan atasan atau Direksi soal energi?" | Angka dari mulut responden; KPI yang benar-benar dipakai (kWh/m³? Rp/m³?) |
| 10–13 | Reaksi demo | Demo ≤90 detik yang sama. Lalu: "Kalau laporan ini ada di meja Bapak/Ibu tiap minggu, keputusan apa yang berubah?" · "Data apa yang kurang supaya Bapak/Ibu percaya tanda ini?" · "Bagaimana dengan pompa yang ditandai 'tidak tahu'?" | Keputusan yang berubah (atau tidak); syarat kepercayaan; reaksi abstain |
| 13–15 | Mau pakai/bayar? Siapa menyetujui? | "Untuk mencoba alat seperti ini di satu pompa, langkah izinnya apa dan siapa yang tanda tangan?" · "Pernahkah unit Bapak/Ibu mencoba alat atau kerja sama riset serupa? Lewat jalur apa anggarannya?" · "Apa yang harus terbukti dulu sebelum hal seperti ini masuk anggaran?" · "Boleh kami kirim ringkasan hasil wawancara ini, lalu Bapak/Ibu bantu kenalkan ke [jabatan yang disebut]?" | Jalur izin & anggaran (H1, H7); kriteria bukti; komitmen (perkenalan, data historis, surat) |

**Pertanyaan yang DILARANG** (leading / hipotetis): "Apakah Bapak setuju pompa yang aus itu boros listrik?", "Apakah Bapak mau membeli alat ini?", "Berapa Bapak mau bayar?", "Bukankah AI akan membantu?".

### 3.3 Pertanyaan khusus untuk PAKAR (penulis S6 / dosen mesin fluida / ahli pompa), 20 menit
1. "Waktu audit Ngagel I, apa yang paling sulit diukur? Kenapa hanya sebagian pompa yang diukur?" (F3)
2. "Kalau hanya ada kW atau arus dan getaran per pompa, tanpa debit, apa yang masih bisa Bapak/Ibu simpulkan?" (H2)
3. "Untuk S1/S2 yang baru dipasang 2018 tapi efisiensinya ±52 %, dugaan Bapak/Ibu penyebabnya apa? Apakah itu terlihat dari getaran?" (F6)
4. "Setelah paper, rekomendasi untuk T1 dan pompa lain ditindaklanjuti? Kalau tidak, apa penghambatnya?" (H4)
5. "Kalau kami ingin membuktikan satu klaim saja dalam 2 bulan, klaim apa yang paling jujur dan paling berguna bagi PDAM?"
6. "Siapa di PDAM yang paling tepat kami temui, dan bagaimana cara yang sopan untuk memintanya?"

---

## 4. Form persetujuan wawancara (Bahasa Indonesia)

> **PERSETUJUAN MENGIKUTI WAWANCARA**
> Proyek: DetakPompa, tim mahasiswa peserta Seno Hackathon ITS 2026
> Pewawancara: [[NAMA PEWAWANCARA]] dari [[INSTITUSI]]
>
> **Tujuan.** Kami ingin memahami bagaimana pompa air dipantau dan dirawat, untuk mengembangkan purwarupa alat pemantau pompa. Wawancara ini **bukan** penjualan dan **bukan** penilaian kinerja Bapak/Ibu.
>
> **Apa yang terjadi.** Wawancara berlangsung sekitar 15 menit. Kami mencatat jawaban. Rekaman suara **hanya** dibuat kalau Bapak/Ibu mencentang kotak di bawah.
>
> **Data yang kami simpan.** Jawaban, jabatan umum (mis. "operator rumah pompa"), dan jenis organisasi. **Nama, nomor telepon, nama unit spesifik, dan data internal perusahaan tidak akan ditulis di dokumen lomba, presentasi, atau publikasi.** Kutipan hanya dipakai **tanpa nama** dan **hanya** kalau Bapak/Ibu mengizinkan di bawah. Catatan disimpan di penyimpanan tim yang terbatas dan dihapus paling lambat [[TANGGAL HAPUS, mis. 31 Maret 2027]].
>
> **Hak Bapak/Ibu.** Ikut wawancara bersifat sukarela. Bapak/Ibu boleh menolak menjawab pertanyaan apa pun, berhenti kapan saja, dan meminta catatan dihapus dengan menghubungi [[KONTAK TIM, email kelembagaan]]. Kami tidak memberi uang atau hadiah untuk wawancara ini.
>
> **Data perusahaan.** Kami tidak meminta data SCADA, dokumen internal, atau foto fasilitas. Kalau nanti dibutuhkan, kami akan meminta izin tertulis terpisah dari pejabat yang berwenang.
>
> Saya menyetujui:
> ☐ Ikut wawancara
> ☐ Wawancara direkam suara (boleh tidak dicentang)
> ☐ Jawaban saya boleh dikutip **tanpa nama** di dokumen lomba
> ☐ Saya bersedia dihubungi lagi untuk pertanyaan lanjutan
>
> Nama: [[NAMA RESPONDEN]]  Jabatan umum: [[JABATAN UMUM]]
> Organisasi: [[ORGANISASI]]  Tanggal: [[TANGGAL]]
> Tanda tangan: [[TTD]]  (atau persetujuan terekam di awal rekaman, sesuai UU PDP Pasal 22 [S23])

Catatan pelaksanaan:
- Simpan form asli dan catatan **lokal** (bukan grup chat publik). Isi `[[...]]` tidak boleh di-commit ke repo.
- Di semua file tim, responden ditulis sebagai kode (`R1-PDAM-OP`, `R2-PDAM-MGR`, …).
- Untuk pegawai PDAM, tanyakan dulu apakah mereka butuh izin atasan untuk diwawancarai. Kalau butuh, **jangan** lanjut tanpa izin itu.

---

## 5. Rencana rekrutmen (≥5 calon pengguna + 1 pakar)

### 5.1 Target kuota

| Kode | Profil | Jumlah minimum | Hipotesis utama yang diuji |
|---|---|---|---|
| R-PDAM-OP | Operator/teknisi rumah pompa PDAM Surya Sembada | 1–2 | H3, H4, H6, H1 (izin dari bawah) |
| R-PDAM-MGR | Kepala IPA/unit produksi **atau** manajer energi/aset PDAM | 1–2 | H1, H3, H4, H5, H7 |
| R-SEK-GED | Chief engineer hotel/RS di Surabaya **atau** Bandung | 1 | H8, H1 (lokasi alternatif) |
| R-SEK-KAMPUS | Teknisi/staf sarpras ITB (atau ITS) | 1 | H1 (lokasi pilot TKT 4–5), H6 |
| R-PAKAR | Penulis S6 (ITS) atau dosen mesin fluida/sistem pompa | 1 | H2, H4 |
| Opsional | Perumda Tirtawening Bandung; tenant SIER | 0–1 | Generalisasi |

Total target: **6 pengguna + 1 pakar**. Minimum lulus untuk berkas: **5 + 1**, dengan **≥2 dari PDAM**.

### 5.2 Jalur kontak realistis (urut dari yang paling mungkin)

| Urutan | Jalur | Cara (dikerjakan manusia) | Kenapa realistis | Risiko |
|---|---|---|---|---|
| 1 | **Penulis S6 dari ITS** (penulis korespondensi, Departemen Teknik Lingkungan ITS) | Surel singkat ke **alamat korespondensi yang tercantum di paper** atau lewat sekretariat departemen. Minta 20 menit wawancara pakar (§3.3) **dan** perkenalan ke staf PDAM yang ikut menulis (penulis ke-3, afiliasi PDAM). Lampirkan ringkasan 1 halaman + form persetujuan | Mereka sudah pernah bekerja di IPA Ngagel I dan punya relasi dengan PDAM (F10) | Dosen sibuk; balasan bisa > 1 minggu. Tindak lanjut sopan 1× setelah 5 hari kerja |
| 2 | **DIKST / LPPM ITS** (penyelenggara lomba; kontak kelembagaan di `03_RISET.md` S43) | Tanya apakah ada mekanisme fasilitasi "validasi pengguna" bagi peserta, atau kerja sama ITS–PDAM yang sudah berjalan | Format lomba = pra-inkubasi dengan validasi pengguna (`00_INFO.md`) | Bisa lambat atau hanya berlaku setelah lolos seleksi |
| 3 | **Surat resmi ke PDAM Surya Sembada** (lewat kanal pengaduan/humas resmi di situs PDAM) | Surat permohonan wawancara 15 menit, ditandatangani dosen pembimbing `[ISI: nama dosen pembimbing]`, ditujukan ke **Direktur Operasi** (jabatan dari Board Manual) dengan tembusan kepala unit produksi | Jalur formal yang dihormati BUMD; sekaligus menguji H1 (berapa lama izin) | Lama. **Waktu responsnya sendiri adalah data untuk H1** |
| 4 | **Alumni ITS/ITB/PENS/UNAIR yang bekerja di PDAM** | Cari lewat jaringan alumni jurusan atau LinkedIn berdasarkan **jabatan** (bukan scraping). Pesan perkenalan singkat, minta rujukan, bukan wawancara langsung | Cepat dan informal | Responden mungkin butuh izin atasan → hormati |
| 5 | **Sarpras ITB** (Direktorat Sarana dan Prasarana; dekat dengan tim di Bandung) | Lewat dosen/unit fakultas, minta bicara dengan teknisi gedung yang menangani pompa transfer/booster. Sekaligus jajaki izin **memasang sensor di 1 pompa gedung** sebagai pilot TKT 4 | Paling cepat diakses dan bisa jadi lokasi rekaman nyata. [cuplikan] SOP FTI ITB menyebut perbaikan yang melibatkan pihak ketiga perlu persetujuan direktorat ini (PDF tidak bisa dibuka) | Pompa gedung ≠ pompa PDAM (skala jauh lebih kecil) |
| 6 | **PHRI Jatim / PHRI Jabar** (kontak kelembagaan `[ISI]`) | Minta rujukan 1 chief engineer hotel untuk wawancara 15 menit | Hotel punya pompa transfer dan chief engineer yang memegang perawatan | Nilai kemungkinan downtime, bukan energi (H8) |
| 7 | **Perumda Tirtawening Bandung** | Lewat dosen Teknik Lingkungan ITB `[ISI: nama dosen yang punya relasi]` | Dekat dengan tim | Data energi belum ditemukan |
| 8 | **PERPAMSI** (asosiasi perusahaan air minum) | Hanya kalau jalur 1–4 buntu | Asosiasi kelembagaan | Terlalu jauh dari operator |

### 5.3 Pesan pertama (templat, dikirim manusia)
> Yth. [[JABATAN/NAMA]],
> Kami [[NAMA TIM]], mahasiswa [[INSTITUSI]] yang sedang mengikuti Seno Hackathon ITS 2026. Kami membaca makalah tentang efisiensi pompa IPA Ngagel I (JIST, Feb 2024) dan ingin belajar langsung cara pompa dipantau dan dirawat. Bolehkah kami meminta waktu 15 menit (daring atau tatap muka) pada [[2–3 pilihan waktu]]? Kami tidak menjual apa pun dan tidak meminta data internal. Ringkasan proyek 1 halaman dan form persetujuan kami lampirkan.
> Hormat kami, [[NAMA, KONTAK KELEMBAGAAN]]

### 5.4 Etika & kepatuhan
- **Tidak ada uang, hadiah, voucher, atau honor** untuk pegawai PDAM (BUMD; Board Manual memuat pengendalian gratifikasi). Ucapan terima kasih cukup berupa ringkasan hasil wawancara dan laporan akhir yang bisa berguna bagi mereka.
- Jangan masuk rumah pompa, memotret, atau menempel alat apa pun tanpa izin tertulis pejabat berwenang.
- Jangan meminta ekspor SCADA. Kalau responden menawarkan data, minta lewat surat resmi dan simpan sesuai §4.
- Jangan menulis nama responden, unit spesifik, atau angka internal yang belum publik di berkas lomba tanpa izin tertulis.

---

## 6. SIMULASI PERSONA (berpikir sebagai pengguna)

> **Peringatan:** seluruh isi §6.1–§6.5 adalah tebakan agen berdasarkan riset di §0 dan file `03_*`. Isinya **bukan** hasil wawancara, **tidak boleh** dikutip, diparafrasekan sebagai "kata pengguna", atau dijadikan bukti validasi di berkas lomba, deck, atau video. Gunanya hanya untuk menyiapkan pertanyaan dan menebak keberatan.

### 6.1 Sesi S-1: Operator rumah pompa IPA Ngagel (shift, ±10 tahun pengalaman)
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Masalah:** "Tugas saya menjaga tekanan ke zona tetap aman. Kalau tekanan turun, telepon dari distribusi langsung masuk. Pompa jarang benar-benar mati; yang sering justru pompa yang 'kelihatan jalan' tapi tekanannya kurang, sehingga kami nyalakan pompa tambahan."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Cara sekarang:** "Di panel ada angka arus, tegangan, daya. Saya catat tiap jam di buku log. Selebihnya pakai telinga dan tangan: bunyi kasar, getar di bantalan, motor panas. Kalau curiga, saya lapor ke teknisi lewat buku laporan shift."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Biaya/sakit:** "Yang paling repot kalau pompa harus dibongkar mendadak di malam hari. Soal listrik, saya tidak tahu tagihannya; itu urusan kantor. Saya tidak pernah lihat kWh per kubik."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Reaksi demo:** "Pompa yang ditandai 'berubah sejak bulan lalu' itu, saya juga bisa bilang dari bunyinya. Tapi kalau ada catatan yang bisa saya tunjukkan ke atasan, itu membantu. Biasanya laporan saya dianggap 'perasaan operator'."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Tentang abstain:** "Kalau alatnya bilang 'tidak tahu', saya harus apa? Kalau ada perintahnya, misalnya cek kabel sensor atau ukur manual, oke. Kalau hanya 'tidak tahu', nanti diabaikan."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Keberatan:** "Saya tidak boleh menempel apa pun di motor tanpa perintah. Kalau pompa rusak setelah ada alat Anda, saya yang ditanya. Jangan sampai ada kabel melintang di lantai rumah pompa."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Yang membuat mau mencoba:** "Kalau atasan yang menyuruh, alatnya tidak perlu dibuka panel, dan saya tidak perlu input apa-apa tambahan di luar log yang sudah ada."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Pertanyaan balik:** "Alatnya pakai baterai atau colok listrik? Kalau hujan atau lembap bagaimana? Siapa yang dihubungi kalau alatnya rusak?"

### 6.2 Sesi S-2: Kepala unit produksi PDAM (insinyur, membawahi beberapa IPA)
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Masalah:** "Pompa kami banyak, umurnya campur aduk, dan anggaran rekondisi tiap tahun terbatas. Keputusan tersulit adalah memilih pompa mana yang dibongkar duluan."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Cara sekarang:** "Kami pernah audit bersama ITS, tapi tidak semua pompa diukur karena flowmeter-nya portabel dan pemasangannya makan waktu. Hasilnya bagus untuk pompa yang diukur. Yang tidak diukur, ya kami pakai pengalaman."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Biaya/sakit:** "SEC kami masih di bawah 0,4. Di atas kertas sudah efisien. Jadi kalau Anda datang membawa cerita 'boros', Direksi akan menunjukkan angka SEC itu. Yang bisa saya jual ke atas hanya: pompa X menyedot sekian kW lebih banyak untuk debit yang sama, jadi sekian rupiah per bulan."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Reaksi demo:** "Daftar pompa yang diurutkan dari 'paling patut dicurigai' itu berguna, asal urutannya bisa saya cek. Kalau saya kirim tim dengan flowmeter ke pompa nomor satu dan ternyata baik-baik saja, kepercayaan langsung hilang."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Keberatan:** "Efisiensi itu butuh debit dan head. Anda hanya baca arus dan getaran. Bagaimana Anda tahu itu boros, bukan karena katupnya kami atur atau permintaan zonanya berubah? Pompa yang baru dipasang 2018 pun ada yang efisiensinya rendah, dan itu bukan karena aus."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Yang membuat mau mencoba:** "Pilot di satu atau dua pompa yang sudah kami tahu kondisinya, supaya hasil Anda bisa dibandingkan dengan hasil audit. Lewat kerja sama dengan ITS, bukan pembelian. Data tidak keluar dari jaringan kami."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Siapa menyetujui:** "Untuk pilot non-invasif, saya bisa mengusulkan ke Direktur Operasi. Kalau sudah menyangkut pembelian dan sistem TI, itu masuk RKAP dan pengadaan; prosesnya tahunan."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Pertanyaan balik:** "Berapa pompa yang sudah Anda uji? Di data apa? Bisa membaca data dari power meter panel yang sudah ada, atau harus pasang alat baru? Siapa yang merawat alatnya setelah lomba selesai?"

### 6.3 Sesi S-3: Manajer energi PDAM (bagian perencanaan/energi)
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Masalah:** "Biaya energi kami lebih dari Rp400 per kubik, di atas rata-rata nasional. Direksi menanyakan Rp per kubik dan rasio biaya energi, bukan kondisi bantalan."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Cara sekarang:** "Tagihan PLN bulanan per IPA, data produksi bulanan, lalu kami hitung SEC. Ada juga dashboard dari kerja sama dengan vendor besar beberapa tahun lalu, tapi isinya lebih ke tekanan dan debit jaringan, bukan kinerja per pompa." (catatan agen: ini tebakan; status kerja sama Schneider [S7] adalah `[ISI]`)
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Biaya/sakit:** "SEC bulanan terlalu kasar. Kalau satu pompa besar turun efisiensinya, angka bulanan IPA hampir tidak bergerak, apalagi kalau produksinya juga berubah."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Reaksi demo:** "Saya lebih tertarik kalau keluarannya kWh per kubik per pompa, atau setidaknya per zona distribusi. Getaran itu urusan teknisi. Kalau Anda bisa menunjukkan 'pompa ini memakan Rp sekian lebih banyak per bulan dibanding bulan pertama', itu bahasa saya."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Keberatan:** "Vendor besar sudah menawarkan hal serupa dengan garansi. Kenapa saya harus percaya tim mahasiswa? Lalu klaim hemat Anda dari mana? Jangan pakai angka luar negeri."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Tentang abstain:** "Justru menarik. Banyak dashboard vendor yang selalu hijau. Alat yang berani bilang datanya jelek lebih mudah saya pertanggungjawabkan, asal tidak terlalu sering."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Yang membuat mau mencoba:** "Kalau bisa memakai data yang sudah kami punya (power meter panel, tekanan), tidak perlu alat baru, dan hasilnya dibandingkan dengan audit terakhir."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Pertanyaan balik:** "Berapa persen pompa yang bisa Anda nilai tanpa flowmeter? Seberapa sering alat Anda salah menandai? Bagaimana keamanan datanya, apakah ada yang dikirim ke cloud?"

### 6.4 Sesi S-4: Chief engineer hotel bintang 4 di Surabaya
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Masalah:** "Mimpi buruk saya adalah air tidak sampai ke lantai atas saat hotel penuh. Pompa transfer ke tangki atap kami ada dua, saling cadang. Kalau keduanya bermasalah, komplain tamu langsung masuk."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Cara sekarang:** "Perawatan preventif terjadwal, ganti bearing dan seal sesuai jam operasi. Ada BMS untuk chiller; pompa transfer hanya alarm *trip*. Vendor MEP datang kalau ada kerusakan besar."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Biaya/sakit:** "Listrik pompa transfer kecil dibanding chiller dan AC kamar. Kalau Anda mau bicara hemat listrik, bicaralah soal chiller. Untuk pompa, yang saya bayar adalah ketenangan: jangan sampai mati di akhir pekan."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Reaksi demo:** "Tanda 'berubah sejak bulan lalu' itu berguna kalau datang dua minggu sebelum pompa mati, bukan dua jam. Saya tidak butuh kWh per kubik."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Keberatan:** "Harga. Kalau lebih mahal dari satu set bearing dan seal per tahun, lebih murah saya ganti rutin saja. Lalu alat ini terhubung ke internet lewat jaringan hotel? IT kami pasti menolak."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Yang membuat mau mencoba:** "Uji gratis di pompa cadangan, tanpa sambungan ke jaringan hotel, dengan notifikasi ke ponsel teknisi jaga."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Siapa menyetujui:** "Saya usulkan ke GM; kalau di atas batas tertentu, harus persetujuan pemilik/manajemen grup."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Pertanyaan balik:** "Berapa harganya per pompa? Garansinya? Kalau alatnya salah alarm tengah malam, siapa yang tanggung jawab?"

### 6.5 Sesi S-5: Teknisi Sarpras ITB (penanggung jawab utilitas beberapa gedung)
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Masalah:** "Gedungnya banyak, teknisinya sedikit. Pompa air di gedung-gedung lama sering baru ketahuan rusak waktu toilet di lantai atas kering dan ada laporan masuk."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Cara sekarang:** "Keliling cek rutin kalau sempat, sisanya reaktif. Perbaikan besar pakai pihak ketiga dan harus lewat persetujuan direktorat."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Biaya/sakit:** "Yang mahal waktu dan komplain. Tagihan listrik kampus besar, tapi pompa tidak diukur terpisah; kami tidak tahu porsinya."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Reaksi demo:** "Kalau bisa memberi tahu pompa mana yang mulai aneh di antara puluhan gedung, itu membantu kami mengatur rute keliling."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Keberatan:** "Siapa yang merawat alatnya setelah mahasiswanya lulus? Kami sudah punya beberapa alat hibah riset yang akhirnya mati dan tidak ada yang urus."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Yang membuat mau mencoba:** "Uji di satu gedung dengan surat dari dosen, alat tidak mengganggu panel, dan ada laporan singkat di akhir uji yang bisa kami pakai untuk usulan anggaran."
- [SIMULASI PERSONA — bukan data wawancara, dilarang dikutip di berkas lomba] **Pertanyaan balik:** "Perlu listrik dan Wi-Fi di ruang pompa? Kebanyakan ruang pompa tidak ada sinyal. Datanya siapa yang lihat?"

### 6.6 Pelajaran dari simulasi
> Pelajaran di bawah adalah **dugaan yang harus diuji** di wawancara nyata. Sebagian besar didukung fakta [S6-teks] di §0, dan itu ditandai.

**Fitur/klaim yang harus diubah sekarang (sebelum berkas lomba ditulis):**

| # | Klaim/fitur saat ini (`04_KEPUTUSAN.md`) | Ubah menjadi | Dasar |
|---|---|---|---|
| L1 | "AI membaca arus + getaran lalu menandai pompa yang **boros listrik**" | "AI menandai **perubahan perilaku listrik-mekanik pompa dibanding baseline pompa itu sendiri**, lalu mengurutkan pompa yang **paling patut diaudit/diukur debitnya lebih dulu**." Efisiensi tetap diukur dengan Q dan H | F4: efisiensi = Ph/Pi butuh Q dan H. F3: separuh pompa tidak terukur pada audit |
| L2 | Sensor baru (clamp + akselerometer) sebagai satu-satunya input | Tambahkan mode **"baca data yang sudah ada"**: kW/arus/cos φ dari power meter panel + tekanan, kalau tersedia. Sensor getaran jadi tambahan | F4: PM2100 terpasang di tiap panel; persona S-2/S-3 menolak alat baru |
| L3 | KPI "kondisi pompa"/skor kesehatan | KPI utama: **kW pada tekanan yang sama** dan **Rp/bulan selisih terhadap baseline**, plus kWh/m³ per pompa/zona kalau debit ada. Keluaran berupa **tindakan** sesuai praktik S6 (rawat rutin / cek impeller / overhaul) | F7, F8; persona S-3 |
| L4 | Abstain = "tidak tahu" | Abstain **selalu disertai langkah berikut**: "cek pemasangan sensor", "ukur debit manual minggu ini", "kondisi operasi berubah (katup/zona), baseline diulang" | Persona S-1 |
| L5 | Narasi "pompa aus = boros" | Akui dua penyebab: **aus/rusak** (terlihat di getaran) dan **titik operasi tidak cocok** (S1/S2 baru 2018 tapi ±52 %, belum tentu terlihat di getaran). DetakPompa mendeteksi **perubahan**, bukan penyebab | F6 |
| L6 | Pitch "PDAM boros" | Pitch "**SEC IPA sudah di bawah standar, tetapi 5 dari 12 pompa yang diaudit di bawah ±55 %; SEC bulanan menyembunyikan pompa yang menurun**" | F5, F8. Mencegah bantahan "kami sudah efisien" |
| L7 | Data ke cloud | **Offline/on-prem dulu**, tanpa koneksi ke SCADA atau jaringan pelanggan; notifikasi opsional | Persona S-1, S-2, S-4, S-5 |
| L8 | Segmen sekunder dipasarkan dengan narasi energi | Untuk hotel/RS/kampus: narasi **"jangan sampai pompa mati"** (downtime), dan dipakai sebagai **lokasi pilot TKT 4–5**, bukan sumber klaim energi | Persona S-4, S-5 |
| L9 | "Siapa bayar = PDAM" | Langkah pertama = **pilot kerja sama riset lewat ITS** di 1–2 pompa yang hasil auditnya sudah diketahui (mis. pompa yang di S6 tercatat baik vs buruk) sebagai *ground truth*. Pembelian lewat RKAP baru setelah itu | Board Manual (RKAP, pengadaan); persona S-2 |
| L10 | Purwarupa yang hanya ada selama lomba | Siapkan jawaban "siapa merawat setelah lomba": README perawatan, perangkat murah yang bisa diganti, serah terima ke unit | Persona S-5 |

**Hipotesis yang paling mungkin gagal (urut):**
1. **H1 (akses):** semua persona PDAM mengaitkan pemasangan alat dengan izin direksi dan keamanan data. Kemungkinan besar **gagal di PDAM dalam jangka lomba** dan hanya lulus lewat lokasi sekunder (Sarpras ITB). Rencana: kejar izin PDAM paralel, siapkan pilot ITB sebagai jalur TKT 4.
2. **H2 (sinyal cukup):** F4 dan F6 menunjukkan arus + getaran tanpa Q dan H tidak bisa menghitung efisiensi. Kemungkinan lulus **hanya** dalam bentuk lemah: "triase + deteksi perubahan relatif", bukan "estimasi efisiensi".
3. **H8 (segmen sekunder untuk energi):** hampir pasti gagal. Nilai di segmen ini adalah downtime.
4. **H3 (rasa sakit):** berisiko karena SEC IPA < 0,4 (F8). Kemungkinan lulus kalau pertanyaan diarahkan ke **pemilihan pompa untuk rekondisi**, bukan ke "boros listrik".

**Pertanyaan yang ditambahkan ke skrip karena simulasi:** (sudah dimasukkan di §3) cakupan audit, nasib rekomendasi S6, data panel yang tersedia, siapa merawat alat, apakah ada sinyal/listrik di ruang pompa.

---

## 7. Template pencatatan hasil wawancara ASLI

Isi dalam ≤24 jam setelah wawancara. Responden ditulis dengan **kode**, bukan nama. Kutipan hanya kata-kata asli responden dan hanya kalau kotak "boleh dikutip tanpa nama" dicentang.

### 7.1 Ringkasan per wawancara

| Kolom | #1 | #2 | #3 | #4 | #5 | #6 | Pakar |
|---|---|---|---|---|---|---|---|
| Kode responden | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Peran / jenis organisasi | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Tanggal, durasi, mode (daring/tatap muka) | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Pewawancara / pencatat | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Persetujuan: ikut / rekam / kutip / dihubungi lagi | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Kejadian spesifik yang diceritakan (apa, kapan) | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Cara sekarang (alat, data, siapa membaca) | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Biaya/sakit yang disebut responden (angka + satuan + sumbernya) | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| KPI yang benar-benar dipakai (kWh/m³, Rp/m³, downtime, lainnya) | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Reaksi spontan terhadap demo | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Reaksi terhadap abstain ("tidak tahu") | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Keberatan utama | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Jalur izin / pemberi persetujuan (jabatan) + perkiraan waktu | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Jalur anggaran yang pernah dipakai untuk hal serupa | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| **Komitmen nyata** (perkenalan, kunjungan, data, surat) atau "tidak ada" | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Pertanyaan yang diajukan balik ke tim | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Kutipan asli (hanya jika boleh, tanpa nama) | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Pujian/opini yang **tidak** dihitung sebagai bukti | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Kejutan (hal yang tidak ada di simulasi §6) | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |
| Rujukan ke orang berikutnya (jabatan saja) | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] |

### 7.2 Papan skor hipotesis (diisi setelah tiap wawancara)

Isi tiap sel dengan **L** (mendukung), **G** (membantah), **–** (tidak dibahas), ditambah satu frasa bukti.

| Hipotesis | #1 | #2 | #3 | #4 | #5 | #6 | Pakar | Status akhir (lulus/gagal/belum) |
|---|---|---|---|---|---|---|---|---|
| H1 Akses | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] | [ISI] |
| H2 Sinyal cukup | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] | [ISI] |
| H3 Rasa sakit | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] | [ISI] |
| H4 Bertindak atas tanda | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] | [ISI] |
| H5 Celah belum diisi | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] | [ISI] |
| H6 Abstain dihargai | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] | [ISI] |
| H7 Jalur pembayar | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] | [ISI] |
| H8 Segmen sekunder (energi) | [ISI: hasil wawancara #1] | [ISI: hasil wawancara #2] | [ISI: hasil wawancara #3] | [ISI: hasil wawancara #4] | [ISI: hasil wawancara #5] | [ISI: hasil wawancara #6] | [ISI: hasil wawancara #pakar] | [ISI] |

### 7.3 Log kontak (tanpa data pribadi)

| # | Jalur (§5.2) | Jabatan yang dihubungi | Tanggal kirim | Tanggal balas | Hasil (wawancara/rujukan/ditolak/tidak ada balasan) |
|---|---|---|---|---|---|
| 1 | [ISI] | [ISI] | [ISI] | [ISI] | [ISI] |
| 2 | [ISI] | [ISI] | [ISI] | [ISI] | [ISI] |
| 3 | [ISI] | [ISI] | [ISI] | [ISI] | [ISI] |

---

## 8. Tugas manusia (untuk dimasukkan orkestrator ke `AKSI_MANUSIA.md`)

Agen tidak menghubungi, tidak login, dan tidak mewawancarai siapa pun. Semua aksi di bawah dikerjakan anggota tim. Pembagian mengikuti `AKSI_MANUSIA.md` #4 (Uqi, Pio) dan saran `00_INFO.md` agar beban Aziz minimal.

| # | Aksi | Siapa | Kapan | Selesai kalau … |
|---|---|---|---|---|
| V1 | Baca §3–§4. Cetak/siapkan form persetujuan; isi `[[...]]` **di salinan lokal**, bukan di repo | Uqi, Pio | 29 Okt | Form siap dipakai |
| V2 | Kirim pesan §5.3 ke **penulis korespondensi S6 (ITS)** lewat alamat korespondensi di paper atau sekretariat departemen. Minta wawancara pakar + perkenalan ke staf PDAM | Uqi | **29–30 Okt** | Pesan terkirim; dicatat di §7.3 |
| V3 | Minta dosen pembimbing menandatangani **surat permohonan wawancara** ke PDAM Surya Sembada (ditujukan ke Direktur Operasi, tembusan unit produksi). Kirim lewat kanal resmi PDAM | Pio (siapkan), Aziz (review 10 menit) | 30–31 Okt | Surat terkirim; **tanggal kirim dicatat** (data untuk H1) |
| V4 | Hubungi **Sarpras ITB** lewat dosen/unit fakultas: wawancara 1 teknisi + jajaki izin pilot sensor di 1 pompa gedung | Pio | 30 Okt – 4 Nov | Wawancara #1 terlaksana atau jadwal ada |
| V5 | Tanya **DIKST/LPPM ITS** (kontak kelembagaan di `03_RISET.md` S43): adakah fasilitasi validasi pengguna atau kerja sama ITS–PDAM yang berjalan | Uqi | 31 Okt | Jawaban dicatat |
| V6 | Siapkan **demo ≤90 detik** untuk wawancara: daftar pompa, satu "berubah sejak baseline", satu "tidak tahu + langkah berikut" (sesuai L1, L3, L4). Jangan menampilkan angka hemat kWh yang belum terukur | Poggy | 3 Nov | Video/layar demo siap |
| V7 | Cari rujukan **chief engineer hotel/RS** lewat PHRI Jatim/Jabar atau alumni | Uqi | 2–7 Nov | 1 wawancara terjadwal |
| V8 | Lakukan wawancara. **Target: ≥2 sebelum berkas didaftarkan** (kalau deadline memungkinkan), **≥5 + 1 pakar sebelum 20 Nov**, dengan ≥2 dari PDAM | Uqi, Pio | 30 Okt – 20 Nov | §7.1 terisi untuk #1–#5 + pakar |
| V9 | Isi §7.1–§7.3 dalam ≤24 jam setelah tiap wawancara. Simpan form dan rekaman **di luar repo** | Pewawancara | tiap wawancara | Tabel terisi |
| V10 | Setelah wawancara ke-5: sintesis papan skor §7.2, terapkan aturan berhenti §2 (H1 + H3 gagal → evaluasi ulang E1) | Aziz (keputusan), Pio (sintesis) | ±21 Nov | Keputusan tertulis di `04_KEPUTUSAN.md` |
| V11 | Revisi narasi berkas/deck sesuai L1–L10 **sebelum** menulis berkas lomba, terutama L1 (jangan klaim "estimasi efisiensi dari arus + getaran") | Poggy (tulis), Aziz (review) | sebelum daftar | Narasi baru disetujui |
| V12 | Pastikan tidak ada isi §6 (simulasi) yang masuk berkas, deck, atau video | Aziz | sebelum daftar & sebelum Demo Day | Dicek |

**Larangan untuk semua anggota:** tidak memberi uang/hadiah ke pegawai PDAM; tidak memotret atau memasang alat di fasilitas tanpa izin tertulis; tidak menyebut nama responden atau angka internal yang belum publik di berkas lomba.

---

## 9. Sumber yang dipakai di dokumen ini

| Status | Sumber | URL | Dipakai untuk |
|---|---|---|---|
| **[dibuka, teks diekstrak]** | Indra, Rachman, Wafiyuddin, Soedjono, *JIST* 5(2), Feb 2024 (S6) | https://jist.publikasiindonesia.id/index.php/jist/article/download/925/1599/9100 | F1–F10 |
| **[dibuka, teks diekstrak]** | PDAM Surya Sembada, *Board Manual: Pedoman Tata Kerja Dewan Pengawas dan Direksi* (metadata PDF: Jun 2026) | https://www.pdam-sby.go.id/uploads/media/wRRAiradqYmzxG6jutkWyxXp46iqRP38MgLshWbN.pdf | Struktur Direksi, RKAP, pengadaan, gratifikasi |
| [dari `03_RISET.md`] | S7, S16, S17, S18, S23, S43 | lihat `03_RISET.md` §0 | Pesaing, UU PDP, kontak kelembagaan |
| [cuplikan, tidak dikutip] | Kapasitas per IPA (NG I 1.800, NG II 1.000, NG III 1.750, KP I 1.450, KP II 2.500, KP III 2.000 L/s; total ±10.500 L/s), dari repositori skripsi UKWMS/UPN | https://repositori.ukwms.ac.id/38829/2/BAB%20I.pdf (dan hasil serupa) | **Tidak dipakai.** Hanya NG I 1.800 L/s yang dikonfirmasi oleh S6 |
| [cuplikan, PDF gagal dibuka] | SOP FTI ITB 2025: pemeriksaan sarpras berkala & prosedur perbaikan | https://fti.itb.ac.id/wp-content/uploads/sites/9/2025/02/001-SP-2025-SOP-FTI-PEMERIKSAAN-KONDISI-SARANA-DAN-PRASARANA-SECARA-BERKALA-SERTA-PROSEDUR-PERBAIKANNYA.pdf | Hanya sebagai petunjuk jalur izin di §5.2; `[ISI: buka dan konfirmasi]` |
| tidak ketemu | Data energi/pompa Perumda Tirtawening Bandung; struktur organisasi PDAM di bawah Direksi; status kerja sama Schneider [S7] saat ini | — | `[ISI]` |
