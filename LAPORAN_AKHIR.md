# LAPORAN AKHIR: Seno Hackathon ITS 2026 · DetakPompa
### Orkestrator · 28–29 Okt 2026 · diperbarui setelah putaran juri 3 (`JURI_90/SKOR_P3.md`)

**Tenggat:** belum diketahui. Situs dan berita ITS tidak menyebut deadline registrasi, dan "1 Nov" di list tim tidak bersumber. Aksi pertama: Aziz login portal hari ini (`AKSI_MANUSIA.md` #1).

**Ide terpilih:** DetakPompa, alat triase pompa air PDAM Surya Sembada.
- **Dasar angka:** biaya energi Rp147,65 M/tahun, 24,37 % opex. Audit manual hanya mencakup 12 dari 22 pompa di IPA Ngagel I (S6).
- **Cara kerja:** random forest dengan fitur spektral getaran memberi skor kondisi untuk mengurutkan pompa mana yang diaudit duluan. Rekaman bersinyal buruk (sensor lepas) masuk antrean "UKUR ULANG".
- **Tidak** mengklaim mengukur efisiensi, karena efisiensi butuh debit dan head. KPI dampak = kWh/m³ per stasiun pada permintaan yang sama, karena kW pompa bisa naik setelah rekondisi (Hanson 2002).

**TKT jujur: 3.**
- Data rig bantalan publik Ottawa (CC BY), split leave-one-bearing-out, **54/54 tes lulus** (`prototype/results/pytest_output.txt`; dijalankan ulang 28 Okt: 54 passed).
- Hasil apa adanya: model ML **setara** dengan ambang RMS + gerbang SNR di semua metrik.
  - balanced accuracy 0,608 vs 0,640;
  - presisi@3 0,971 vs 0,952 di armada 2/3 rusak; 0,791 vs 0,765 bila 5 dari 22 rusak;
  - tidak ada uji yang signifikan setelah koreksi Holm.
- Penolakan sensor lepas (98,8 %) berasal dari gerbang SNR (DSP), bukan dari ML.
- **TKT 4 belum**, dan tidak diklaim.

**Hasil SKAB (uji pertama di data lab pompa, milik pihak lain).**
- Data lab pompa publik SKAB (1 testbed). Prareg `prototype/PRAREG_SKAB.md` dikunci SHA-256 sebelum data diunduh.
- **H1 GAGAL:** memisahkan penutupan katup dari fault pompa, AUROC residual 1,000 = ambang arus 1,000 (p = 1,000).
- **H2 GAGAL:** deteksi anomali umum, AUROC 0,532 vs 0,573 / 0,502 / 0,581 (p = 0,912).
- Diagnosis post-hoc (tidak diprareg, dikonfirmasi panel): eksperimen katup direkam di ±32 L/min, fault di ±125 L/min, jadi H1 terutama mengukur sesi rekaman. Throttling hanya ±6 % Q, dan tekanan terkuantisasi. Data ini tidak membuktikan dan juga tidak membantah klaim "AI memisahkan throttling dari aus".
- Uji berikutnya: rig pompa sendiri dengan throttling bertingkat (≥ 20–30 % Q), sesi diacak, ≥ 3 unit; atau data PM2100 + tekanan header PDAM dengan prareg baru.
- Sumber: `05_BUKTI_TKT.md` §2e, `prototype/results/skab/summary.json`.

**Skor juri:** 46,9 → 48,9 → **50,3**/100 (putaran 1 → 2 → 3).
- **Veto J4 "AI tidak perlu" masih aktif.** Disiplin prareg menaikkan kepercayaan pada angka, tetapi angkanya tetap berkata AI belum diperlukan.
- Plafon:
  - semua aksi agen selesai: ±55;
  - setelah aksi manusia, kalau AI lulus prareg di rig sendiri atau data PDAM: ±82–86;
  - kalau AI tidak lulus: maks 80 (realistis ±70–74).
- Realistis saat berkas dikirim (perbaikan agen + login portal + 1–2 wawancara + video): ±57–60.
- **Target ≥90 tidak tercapai, dan tidak bisa dicapai dengan jujur tanpa data pompa sendiri.**

**Perbaikan putaran 3 yang sudah dikerjakan agen (gap kategori a):**
- a1: SKAB masuk `08_PENDAFTARAN.md` (150 kata, 300 kata, 1 halaman), `09_DECK_OUTLINE.md` slide 5 dan 9, `10_QNA.md` Q2/Q20/Q25. Q25 tidak lagi bertentangan dengan Q31.
- a2: versi 150 = 148 kata, versi 300 = 297 kata (termasuk judul, dihitung skrip; `08` §8). Angka tes 54 di 08, 09, CARA_KIRIM. `10_QNA` = 31 pertanyaan. Slide 8 "① Alat menandai".
- a3: berkas prareg + hash di-commit di cabang lokal `prareg-stempel` (commit `44c2ff4`, 28 Okt 23:29 WIB), tanpa `data/`. Ini hanya mengunci mulai saat itu; stempel eksternal (b8) tetap tugas manusia.
- a4: KPI kWh/m³ (Hanson 2002) di `07` §0, §3.3, §4.2; `08` §5; `10` Q3. Wellington Water hanya sebagai bukti program pemantauan bisa balik modal, berlabel non-peer-review.
- a5: abstrak menyebut peran AI (skor kondisi RF untuk antrean) dan hasil ujinya.
- Belum: a6 (rpm palsu di laporan sensor lepas), a8 (decimasi 3,2 kHz) karena mengubah kode; a7 (figur + deck); a9/a10 (Paderborn, perlu izin user).

**3 `[ISI]` terpenting:**
1. Deadline + isi form portal.
2. Rig pompa sendiri dengan throttling bertingkat (TKT 4 + uji P2 prareg AI vs RMS).
3. ≥5 wawancara PDAM/operator + izin pilot.

**Rekomendasi final (SKOR_P3 §8): DAFTAR dengan DetakPompa, dengan syarat.**
- Syarat wajib: (1) login portal: deadline, field, batas karakter, pengirim yang tidak bentrok IBSC; (2) teks yang disalin ke form adalah versi 08 yang sudah memuat SKAB dan sesuai batas kata, karena mengirim versi lama = pelaporan selektif; (3) tidak ada klaim TKT 4 dan tidak ada "AI membedakan katup vs aus" sebagai hasil; (4) validasi pengguna hanya wawancara asli atau "dijadwalkan", tanpa persona; (5) izin FaceVitals, repo publik tanpa `data/skab/` (GPL-3.0); (6) video direkam setelah rpm palsu diperbaiki, atau rpm dipotong dari video.
- Setelah 15 besar: kalau rig (P2) lulus, pitch sebagai karya AI dengan prareg sebagai bukti. Kalau gagal atau tidak sempat, jangan pitch "AI-driven": pitch jujur sebagai triase DSP + ambang + antrean, atau pindahkan peran AI ke kurva kinerja per pompa yang dipelajari dari log PM2100 + tekanan header PDAM, dengan prareg baru (jalur yang paling realistis menutup veto).
- **Tidak ikut**, kalau deadline 1 Nov dan tidak ada yang bisa login, mengisi `[ISI]`, dan menyalin teks yang sudah diperbaiki tanpa mengorbankan IBSC.
- **Jangan** pivot ke LautHemat, karena komponen AI-nya belum ada.

Detail: `JURI_90/SKOR_P3.md` (skor, gap a/b, plafon), `05_BUKTI_TKT.md` (bukti, §2e SKAB, PRAREG-TKT4), `AKSI_MANUSIA.md`.
