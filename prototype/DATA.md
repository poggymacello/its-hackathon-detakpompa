# DATA: sumber data purwarupa DetakPompa

Dicek 28 Okt 2026 oleh Agen A6. Semua unduhan **tanpa login**.

## 1. Dataset pompa 4TU (prioritas pertama): TIDAK DIPAKAI
- Dicoba: `https://data.4tu.nl/` dan API pencarian `https://data.4tu.nl/v2/articles/search`.
- Hasil: `curl: (28) Failed to connect to data.4tu.nl port 443 ... Could not connect to server` (3 percobaan, timeout 20-30 s). Ini sama dengan catatan `03_RISET.md` §0 ("server menolak koneksi").
- Karena lisensi dan ukurannya tidak bisa diverifikasi, dataset ini tidak dipakai. `[ISI: coba lagi dari jaringan lain; kalau terbuka, cek lisensi + ukuran]`

## 2. Dataset yang dipakai: Ottawa UORED-VAFCLS v5
| Butir | Isi |
|---|---|
| Nama | University of Ottawa Rolling-element Dataset – Vibration and Acoustic Faults under Constant Load and Speed conditions (UORED-VAFCLS), versi 5 |
| URL | https://data.mendeley.com/datasets/y2px5tg92h/5 |
| DOI | 10.17632/y2px5tg92h.5 |
| Lisensi | **CC BY 4.0** (dari metadata API Mendeley, field `data_licence`: "Creative Commons Attribution 4.0 International") |
| Penulis | Mert Sehri, Patrick Dumond (University of Ottawa) |
| Isi resmi (deskripsi dataset) | 20 bearing (5 inner race, 5 outer race, 5 ball, 5 cage). Tiap bearing direkam dalam 3 keadaan: sehat, fault berkembang, rusak → 60 set. 42.000 Hz, 10 s per set. Format CSV, XLSX, MAT |
| Yang diunduh | **Hanya 60 file MAT mentah** (folder `3_MatLab_Raw_Data_Files (.mat)`), 302.563.574 byte menurut API (`du -sh` lokal: 289 MB). Spektrogram PNG (1,0 GB + 0,78 GB) dan CSV/XLSX **tidak** diunduh |
| Verifikasi | SHA-256 tiap file dicocokkan dengan hash dari API Mendeley: 60/60 cocok. Manifest: `data/ottawa_uored_vafcls/manifest_mendeley_v5.tsv` |
| Lokasi lokal | `prototype/data/ottawa_uored_vafcls/mat/` (di-*gitignore*) |
| Cara unduh | API publik: `GET https://data.mendeley.com/public-api/datasets/y2px5tg92h/folders/5` → id folder; `GET .../files?folder_id=<id>&version=5` → `download_url` per file |

**Kolom file MAT** (matriks 420.000 × 5): kolom 0 = akselerometer, kolom 1 = mikrofon (menurut skrip penulis dataset, https://github.com/Mert-Sehri/1_Bearing_Spectrogram_Dataset_Creation). Kolom 2-3 hanya berisi satu nilai metadata di baris pertama. Kolom 4 tampak seperti kanal suhu. Purwarupa **hanya memakai kolom 0 (akselerometer)**.

**Pengamatan sendiri** (`results/data_survey.txt`, dihitung dari file):
- Garis putaran poros di ~29,7-29,8 Hz untuk bearing 1-15 dan 20. Bearing 16-19 (semua cage) berputar di ~19,5 Hz. Jadi kecepatan **tidak** sama di semua unit, walau tetap konstan di dalam satu unit.
- Kolom 4 (suhu?) naik dari sehat (median per file −0,2 s.d. 7,6) ke rusak (24-43). Kolom ini sengaja tidak dipakai supaya model tidak mengambil jalan pintas.
- Offset DC akselerometer sangat beragam (0,7 s.d. 178). Karena itu sinyal di-*high-pass* 10 Hz.

**Sitasi wajib (CC BY 4.0):**
> Sehri, M., & Dumond, P. (2023). University of Ottawa Rolling-element Dataset – Vibration and Acoustic Faults under Constant Load and Speed conditions (UORED-VAFCLS) (Version 5) [Data set]. Mendeley Data. https://doi.org/10.17632/y2px5tg92h.5

Artikel data terkait (dari `related_links` di metadata): https://www.sciencedirect.com/science/article/pii/S2352340923004456

Perubahan yang kami lakukan (syarat CC BY): file dipotong menjadi jendela 1 s, di-*high-pass* 10 Hz, lalu diekstrak fiturnya. Pada uji degradasi, derau Gaussian ditambahkan secara sintetis.

## 3. Cadangan yang tidak dipakai
- **Paderborn KAt** (CC BY-NC 4.0, punya arus motor): tidak diunduh karena Ottawa sudah memenuhi syarat (terbuka, ≤500 MB, tanpa login). Kekurangannya: Ottawa **tidak punya kanal arus motor**, jadi bagian "arus" dalam cerita DetakPompa belum diuji sama sekali.

## 4. Dataset lab pompa: SKAB (Skoltech Anomaly Benchmark) v0.9, dipakai 28 Okt 2026 malam
Unduhan disetujui user ("buktikan klaim dengan data lab nyata dari publikasi"). Tanpa login.

| Butir | Isi |
|---|---|
| Nama | SKAB: Skoltech Anomaly Benchmark, v0.9 |
| URL | https://github.com/waico/SKAB (juga Kaggle, DOI 10.34740/KAGGLE/DSV/1693952) |
| Lisensi | **GPL-3.0** (berkas `LICENSE` repo; GitHub API `spdx_id: GPL-3.0`) |
| Penulis | Iurii D. Katser, Vyacheslav O. Kozitsin (Skoltech) |
| Cara unduh | `git clone --depth 1 https://github.com/waico/SKAB.git data/skab` (28 Okt 2026 ±23:01 WIB), commit `b2c0d46c2971dcbfe71e26087b6d231998bb91c2` (11 Agu 2024) |
| Ukuran | Ukuran repo menurut GitHub API 34.084 KB; folder `data/` hasil klon 4,3 MB (35 CSV); seluruh klon tanpa `.git` ±13,9 MB |
| Yang dipakai | Hanya 35 CSV di `data/skab/data/`: `anomaly-free/anomaly-free.csv`, `valve1/0..15.csv`, `valve2/0..3.csv`, `other/1..14.csv`. Kode, notebook, dan hasil SKAB **tidak** dijalankan atau disalin |
| Verifikasi | SHA-256 tiap CSV: `results/skab/manifest_skab_csv.sha256` |
| Lokasi lokal | `prototype/data/skab/` (di-*gitignore*, tidak didistribusikan ulang) |
| Testbed | 1 testbed sirkulasi air di Skoltech: tangki, pompa air + motor listrik, 2 katup solenoid (inlet dan outlet pompa), sensor (gambar `docs/pictures/testbed.png`). Adanya inverter/VFD hanya dari makalah sekunder [cuplikan] dan gambar; tipe pompa dan rpm tidak disebut |
| Kolom (README) | `Accelerometer1RMS`, `Accelerometer2RMS` (g), `Current` (A), `Pressure` (bar, setelah pompa), `Temperature` (°C badan motor), `Thermocouple` (°C fluida), `Voltage` (V), `RateRMS` (L/min; **di header CSV bernama `Volume Flow RateRMS`**), `anomaly`, `changepoint` (0/1 per titik). `anomaly-free.csv` tidak punya kolom label |
| Laju sampel | 1 Hz (median selisih stempel waktu = 1,0 s di 35/35 berkas, dihitung dari data; README tidak menyebutkannya) |
| Kondisi (data/README.md) | valve1 = katup inlet ditutup; valve2 = katup outlet ditutup; other 1–4 bocor/penambahan fluida; 5–9 imbalance rotor (5 profil waktu); 10–11 penambahan volume air lambat/cepat; 12 kavitasi karena tangki dikuras; 13 kavitasi karena aliran dua fase di inlet; 14 air bersuhu tinggi |
| Paper | Belum ada paper posisi yang terbit (README: "currently submitted for publication"). Sitasi resmi = sitasi Kaggle di bawah |

**Sitasi wajib:**
> Katser, I. D., & Kozitsin, V. O. (2020). Skoltech Anomaly Benchmark (SKAB) [Data set]. Kaggle. https://doi.org/10.34740/KAGGLE/DSV/1693952 . Repositori: https://github.com/waico/SKAB (GPL-3.0).

**Perubahan yang kami lakukan (hanya di memori, berkas asli tidak diubah):** kolom `Volume Flow RateRMS` diganti nama menjadi `RateRMS`; kolom turunan `P_app = Voltage × Current`; z robust per sensor; residual model. **Implikasi GPL-3.0:** kami hanya membaca data; tidak ada kode SKAB yang disalin ke `detakpompa/`. Kalau data atau kode SKAB kelak ikut didistribusikan bersama kode tim (mis. dimasukkan ke repo publik), bagian itu tunduk pada GPL-3.0 dan atribusi di atas wajib.

**Sifat data yang penting untuk tafsiran** (dihitung dari data, `results/skab/posthoc_log.txt`): tekanan hanya 10 nilai unik (langkah ±0,33 bar); semua eksperimen katup berjalan di Q ≈ 32 L/min sepanjang berkas, eksperimen imbalance/kavitasi di Q ≈ 125 L/min; penutupan katup hanya menurunkan Q ±6 %.
