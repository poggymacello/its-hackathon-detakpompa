# CARA_KIRIM: pendaftaran Seno Hackathon ITS 2026 (DetakPompa)
### Agen A9 · 28 Okt 2026 · **yang klik kirim: Aziz (manusia)**. Agen tidak login, tidak mengisi form, dan tidak mengirim apa pun.

## 1. Link dan fakta yang sudah diketahui
| Butir | Isi | Sumber |
|---|---|---|
| Link daftar | https://hackathon-its.id/register | `00_INFO.md` |
| Form publik (sebelum login) | Nama lengkap, email, password, konfirmasi password | `00_INFO.md` |
| Isi form setelah login | **Belum diketahui** (dokumen apa, format, batas ukuran, batas karakter) | `00_INFO.md` "Belum diketahui" #2 |
| Deadline registrasi | **[ISI: tanggal + jam WIB]**. Tidak ada di situs maupun berita. Tanggal "1 Nov" di list tim tidak bersumber | `00_INFO.md` #1 |
| Syarat | Purwarupa/desain awal AI di TKT 3–6; tim 1–5 orang | FAQ situs (`00_INFO.md`) |
| Bentrok | 1 Nov: IBSC prelim, PIC Aziz | `00_INFO.md` |

**Langkah pertama (hari ini, Aziz):** buat akun, login, lalu catat semua field dan deadline ke `00_INFO.md` (`AKSI_MANUSIA.md` #1). Setelah itu kolom `[ISI]` di §3 bisa diisi dan teks dari `08_PENDAFTARAN.md` dipotong sesuai batas karakter.

## 2. Siapa mengerjakan apa
| Tugas | Siapa | Catatan |
|---|---|---|
| Buat akun, baca form, catat field + deadline | Aziz | Akun atas nama siapa: [ISI: email kelembagaan atau email ketua tim] |
| Isi semua `[ISI]` data tim (nama lengkap, prodi, kampus, peran) | semua, dikumpulkan Pio | Data tim **jangan** di-commit kalau memuat NIK/HP/alamat |
| Rekam video demo ≤2 menit | Poggy | `AKSI_MANUSIA.md` #5 |
| Screenshot lampiran L4–L7 | Poggy | `08_PENDAFTARAN.md` §5 |
| Salin teks ke form, sesuaikan panjang | Poggy atau Pio | Pakai versi 150/300/1 halaman di `08_PENDAFTARAN.md` |
| Review akhir 10 menit | Aziz | Pakai checklist §4 |
| **Klik kirim** | **Aziz** | Sebelum deadline, idealnya H-1 |

## 3. Berkas yang (kemungkinan) dibutuhkan
Daftar ini tebakan dari syarat lomba dan `07-MEGA-PROMPT-ITS-HACKATHON-28okt2026.md` §B Fase 7. Cocokkan dengan form asli setelah login.

| # | Berkas | Sumber di folder ini | Status | Format/batas di form |
|---|---|---|---|---|
| B1 | Data tim (nama lengkap, prodi, kampus, peran, kontak ketua) | `08_PENDAFTARAN.md` §3 butir 7 | [ISI] | [ISI: field form] |
| B2 | Judul + ringkasan proyek | `08_PENDAFTARAN.md` §1 (150 kata) / §2 (300 kata) | Siap, kecuali `[ISI]` tim dan wawancara | [ISI: batas karakter] |
| B3 | Ringkasan 1 halaman / proposal | `08_PENDAFTARAN.md` §3 | Siap, kecuali `[ISI]` | [ISI: PDF? template panitia?] |
| B4 | Deskripsi purwarupa + TKT + bukti | `08_PENDAFTARAN.md` §4, `05_BUKTI_TKT.md` | Siap | [ISI] |
| B5 | Link video demo | `08_PENDAFTARAN.md` §5 L1 | **Belum direkam** | [ISI: YouTube unlisted / Drive?] |
| B6 | Link repo kode | `08_PENDAFTARAN.md` §5 L2 | [ISI: tim setuju repo dibuka atau tidak] | [ISI] |
| B7 | Gambar/screenshot | `prototype\results\coverage_risk.png` + L4–L7 | 1 dari 5 siap | [ISI: jumlah/ukuran maks] |
| B8 | Deck (kalau diminta saat daftar) | `09_DECK_OUTLINE.md` | Outline saja, belum dibuat slide | [ISI] |
| B9 | Surat pernyataan orisinalitas / persetujuan / KTM | — | [ISI: apakah diminta] | [ISI] |
| B10 | Tanda tangan anggota / dosen pembimbing | — | [ISI: apakah diminta] | [ISI] |

## 4. Checklist H-1
**Isi dan kejujuran**
- [ ] TKT yang ditulis = **3**, dengan bukti path file. Tidak ada "TKT 4" warisan FaceVitals.
- [ ] Hasil ditulis apa adanya: usulan 0,608, ambang RMS 0,640, usulan tidak mengalahkan RMS. Tidak ada "akurasi 9x %".
- [ ] Ada kalimat bahwa data adalah **rig bantalan publik, bukan pompa, tanpa arus motor**.
- [ ] Hasil uji data lab pompa SKAB tertulis sebagai **GAGAL** di teks yang disalin (versi 150, 300, dan 1 halaman di `08_PENDAFTARAN.md` sudah memuatnya). Mengirim tanpa SKAB = pelaporan selektif (`JURI_90\SKOR_P3.md` FF1d). Tidak ada "TKT 4" untuk SKAB.
- [ ] Panjang teks sesuai batas form (`08_PENDAFTARAN.md` §8: 148 dan 297 kata termasuk judul).
- [ ] Tidak ada klaim "mengukur efisiensi" atau "menghemat X kWh". Angka energi berlabel [SKENARIO] atau bersumber [S6]/[S10].
- [ ] **Tidak ada kutipan persona simulasi** (`03b` §2.9, `06` §6) di form, ringkasan, deck, atau video.
- [ ] Bagian validasi pengguna hanya berisi hasil wawancara asli, atau kalimat "wawancara dijadwalkan".
- [ ] Tidak ada surat minat/LOI yang dikarang. Lampirkan surat hanya kalau aslinya ada.
- [ ] Include (startup ITS) dan OPTIME disebut kalau ada kolom pesaing. Tidak ada kata "pertama".
- [ ] Atribusi: dataset Ottawa UORED-VAFCLS (CC BY 4.0) dan asal kode DSP FaceVitals (Poggy + Aziz).

**Teknis**
- [ ] Semua `[ISI]` sudah terisi atau kalimatnya dihapus (cari teks `[ISI` di teks yang akan disalin).
- [ ] Video demo bisa diputar dari jendela penyamaran (izin tautan: siapa pun yang punya link).
- [ ] Link repo (kalau dipakai) bisa dibuka tanpa login, dan **tidak** memuat folder `data\` atau berkas pribadi.
- [ ] Ukuran dan format berkas sesuai batas form [ISI].
- [ ] Nama, prodi, kampus semua anggota sudah dicek ejaannya oleh masing-masing anggota.
- [ ] `prototype\.venv\Scripts\python.exe -I -m pytest -q tests` dijalankan ulang di laptop pengirim (hasil yang diharapkan: 54 passed, sesuai `prototype\results\pytest_output.txt` 28 Okt 2026 23:12; dijalankan ulang agen 28 Okt: 54 passed), supaya klaim "54/54 tes" masih benar saat kirim. Kalau data SKAB belum diunduh di laptop itu, 1 tes dilewati (53 passed, 1 skipped); itu bukan gagal, tetapi tulis "54 tes, 1 butuh data SKAB" atau unduh datanya dulu (`prototype\DATA.md` §4).

**Privasi**
- [ ] Tidak ada NIK, nomor HP, alamat rumah, atau rekening di file yang di-commit. Isi data pribadi langsung di form.
- [ ] Tidak ada nama responden wawancara atau angka internal PDAM yang belum publik.

## 5. Hari H
1. Aziz login di https://hackathon-its.id/register (atau halaman login yang ditunjuk).
2. Salin teks dari `08_PENDAFTARAN.md` sesuai field. Unggah lampiran.
3. Simpan draf kalau form mendukung, lalu minta satu anggota lain membaca ulang di layar yang sama.
4. **Aziz klik kirim.**
5. Screenshot halaman konfirmasi + email konfirmasi, simpan di folder ini sebagai bukti: [ISI: nama file screenshot].
6. Catat tanggal dan jam kirim di `AKSI_MANUSIA.md` #7, lalu centang.

## 6. Kalau deadline ternyata sangat dekat
- Kirim dengan apa yang sudah benar: ringkasan, bukti TKT, `coverage_risk.png`. Video dan wawancara boleh menyusul kalau form mengizinkan pembaruan [ISI: apakah bisa diedit setelah kirim].
- **Jangan** mengisi bagian wawancara dengan tebakan untuk "melengkapi" form. Lebih baik kosong atau "dijadwalkan".
