# 04_KEPUTUSAN: ide utama dan cadangan
### Orkestrator · 28 Okt 2026 · dasar: `02_BRAINSTORM.md`, `03_RISET.md`, `03b_ADVOKAT_SETAN.md`

## Keputusan
| | Ide | Status |
|---|---|---|
| **Utama** | **DetakPompa**: E5 DetakMesin, dipersempit ke **pompa air PDAM** | LANJUT DENGAN SYARAT |
| **Cadangan** | **E1 LautHemat**: prakiraan zona tangkap dari pipeline OCEANS | Dipakai kalau deadline > 7 Nov atau DetakPompa gagal Gerbang 3 |
| Dibunuh | E2 TagihanJujur (BI Kalkulator Hijau sudah gratis, tidak ada mekanisme hemat), E15 sebagai ide berdiri sendiri (cukup satu rasio kVArh/kWh), E3 JadwalDingin (Events2HVAC sudah jadi produk sejak 2018; tanpa data meter, TKT 3 tidak tercapai) | — |

**Kalimat "aha" (draf):** *Pompa distribusi PDAM Surabaya sudah terbukti bisa bekerja di efisiensi 49,77 %, dan itu baru ketahuan lewat audit manual. DetakPompa membaca "detak" arus dan getaran motor pompa terus-menerus, lalu menandai pompa yang mulai boros listrik. Kalau sinyalnya jelek, sistem berani bilang "tidak tahu" daripada menebak.*

### Revisi posisi setelah Fase 5 (`06_VALIDASI_PENGGUNA.md`)
- Di IPA Ngagel I ada 8 pompa air baku dan 14 pompa distribusi. **Setiap panel sudah punya power meter Schneider PM2100.** Debit diukur dengan flowmeter ultrasonik portabel, jadi audit hanya mencakup 12 dari 22 pompa (S6).
- **Efisiensi pompa butuh debit + head.** Arus dan getaran saja tidak bisa menghitung efisiensi. Karena itu DetakPompa **tidak** mengklaim mengukur efisiensi.
- **Posisi baru:** *triase*, yaitu memilih pompa mana yang diaudit atau direkondisi duluan, berdasarkan perubahan relatif terhadap baseline pompa itu sendiri. Datanya getaran/arus ditambah data panel yang sudah ada.
- **KPI:** kW pada tekanan/debit setara, atau Rp/bulan.
- Setiap keluaran "TIDAK TAHU" harus disertai langkah berikutnya.
- **Hati-hati klaim "boros":** SEC Ngagel I 0,27–0,29 kWh/m³ sudah di bawah standar 0,4. Pesannya diubah menjadi: "memilih pompa yang akan diaudit tanpa harus mengaudit 22 pompa secara manual".
- **Jalur awal:** pilot riset ITS–PDAM, bukan pembelian. Tidak ada hadiah atau uang untuk staf PDAM (ada bagian pengendalian gratifikasi di Board Manual).

## Alasan (5 kalimat)
1. Angka masalahnya paling kuat dan paling lokal: biaya energi PDAM Surya Sembada **Rp147,65 M (2021), 24,37 % opex**, dan ada pompa dengan efisiensi **49,77 %** (paper bersama ITS–PDAM, `03_RISET.md` S6). Ini cocok dengan checklist "Energy Gap" + "Local" dan memberi jalur kontak ke pengguna lewat penulis ITS.
2. Jalur energinya bisa dipertahankan **hanya kalau fokusnya pompa**: keausan pompa menurunkan efisiensi (S10: 65,2 % → 53,6 %). Deteksi bearing saja tidak sama dengan hemat kWh (S9, `03b`).
3. Komponen AI bisa dibangun **jujur di TKT 3 dalam hitungan hari** dengan dataset legal (Ottawa CC BY; Paderborn CC BY-NC dengan arus motor). Teknik abstain berbasis SNR dari FaceVitals (56/56 tes) menjadi pembeda yang nyata.
4. Pembedanya dari OPTIME/SKF/Include adalah **metrik kWh/m³ dan abstain**, bukan "mesin rusak". Penilaian memakai split per-bearing tanpa kebocoran data, yang justru menjadi kelemahan 40 dari 41 studi CWRU.
5. LautHemat jadi cadangan. Klaim TKT-nya kuat karena pipeline data nyatanya TKT 4, tapi akses ke nelayan dari Bandung dan kaitan prakiraan → BBM masih `[ISI]`.

## Syarat (dari advokat setan; wajib dipenuhi)
- **Klaim TKT jujur:**
  - hari ini **TKT 2** di domain pompa;
  - setelah model + split per-bearing di data publik → **TKT 3**;
  - setelah rekaman motor/pompa lab sendiri + ukur ΔkW → **TKT 4**.
  - Jangan pernah mewarisi "TKT 4" FaceVitals.
- **Tanpa kebocoran data:** split per-bearing/per-unit. Baseline klasik (RMS/ambang, envelope-FFT, random forest fitur sederhana) wajib ditampilkan.
- **Klaim energi:** "AI mendeteksi gangguan" harus dipisah dari "rekondisi menghemat kWh". Angka hemat kWh hanya boleh dari sumber (S6, S10) atau dari pengukuran sendiri, dengan asumsi tertulis.
- **Pesaing lokal:** sebut Include (startup ITS) dan OPTIME secara terang. Jangan klaim "pertama".

## Gerbang 3: status
| Syarat gerbang | Status |
|---|---|
| Energy gap terkuantifikasi + sumber | ✅ S6 (PDAM), S3 (IEA sistem motor), S10 (kasus pompa aus) |
| Pengguna bisa dihubungi | ⚠️ Jalurnya ada (penulis ITS di S6 → PDAM), belum dihubungi → `AKSI_MANUSIA.md` |
| Aset TKT ≥3 jelas | ⚠️ Belum. Akan dicapai di Fase 4 (model di data publik). Sampai itu selesai, **jangan daftar dengan klaim TKT 3** |

Gerbang dinyatakan **lolos bersyarat**. Fase 4 dijalankan untuk menutup baris ketiga.
