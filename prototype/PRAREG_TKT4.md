# PRAREG-TKT4 v2: syarat klaim "AI di inti" DetakPompa

**Ditulis:** 28 Okt 2026, ±21:40 WIB, **sebelum** ada data baru apa pun: belum ada rekaman pompa lab, belum ada data PDAM, belum ada unduhan Paderborn atau dataset lain. Satu-satunya data yang pernah dilihat tim adalah Ottawa UORED-VAFCLS (20 bearing), dan data itu **tidak** boleh dipakai untuk uji konfirmasi di dokumen ini.

**Menggantikan:** PRAREG-TKT4 v1 (`05_BUKTI_TKT.md` §3, versi 28 Okt sore). Endpoint utama v1 adalah *recall waspada* 3-kelas. Panel juri (`JURI_90\SKOR.md` §3 butir 3, eksperimen E1) menunjukkan bahwa endpoint itu bisa naik hanya dengan menggeser batas waspada/rusak, tanpa menandai satu pompa pun lebih awal: di Ottawa, jendela waspada yang ditandai "perlu cek" 156/188 = 0,830 (usulan) vs 158/188 = 0,840 (RMS + gerbang), dihitung ulang tim dari `results\rmsgate_metrics.csv`. Endpoint v1 juga tidak menguji alasan AI yang kami pakai (memisahkan perubahan karena titik operasi dari keausan). v1 tidak pernah dijalankan pada data apa pun, jadi penggantian ini tidak melihat hasil.

**Pembekuan:** SHA-256 berkas ini disimpan di `prototype\PRAREG_TKT4.sha256` bersama timestamp. Folder `ITSHackathon2026\` saat ini **tidak terlacak git** (`.gitignore` repo `barengpoggy` berisi `*/`), jadi tidak ada hash commit. Penggantinya adalah manifes SHA-256 kode di §2 (bagian dari berkas ini, jadi ikut terkunci oleh hash berkas). Disarankan: manusia menjalankan `git add -f` untuk `prototype\` + berkas ini dan commit lokal, lalu mencatat hash commit di addendum; hash berkas ini tidak berubah karena itu.

---

## 1. Pertanyaan yang diuji

Kami memakai model ML (bukan aturan) dengan dua alasan. Prareg ini menguji **kedua alasan itu langsung**, bukan metrik pengganti:

- **H-AI1 (generalisasi ke unit baru).** Pada unit fisik (pompa/bantalan/rakitan motor-pompa) yang **tidak pernah dilihat** saat latihan, model usulan mengklasifikasikan kondisi lebih tepat daripada ambang RMS yang diberi gerbang sinyal yang sama.
- **H-AI2 (titik operasi bukan keausan).** Bila data memuat variasi titik operasi mekanis-sehat (throttling katup, perubahan permintaan/beban), model usulan lebih mampu membedakan "sehat dengan titik operasi berubah" dari "fault" daripada ambang RMS + gerbang yang sama. Ini alasan AI yang kami sebut di `10_QNA.md` Q20 dan `07_BISNIS_DAMPAK.md` R3.

Kalau keduanya tidak lulus, kami tidak punya bukti bahwa AI diperlukan (lihat §8).

## 2. Yang dikunci (sama dengan versi purwarupa saat ini)

**Model usulan:** `detakpompa.models.proposed_rf()` = `RFModel(SPEC_COLS)` dengan `RF_PARAMS = dict(n_estimators=300, min_samples_leaf=2, class_weight="balanced", random_state=0, n_jobs=-1)`. Daftar fitur = `features.SPEC_COLS` (fitur statistik + energi pita + centroid/spread/flatness/entropy + frekuensi poros terlacak Viterbi + SNR garis poros + harmonik 1×/2×/3× + envelope). Bobot model **tidak** dikunci: model dilatih ulang di unit latih data baru dengan resep yang sama. Yang dikunci adalah resep (fitur, hiperparameter, cara memilih ambang).

**Pembanding utama:** `detakpompa.models.RMSGateBaseline(col="rms")` (tingkat jendela) dan `detakpompa.triage.RMSRecordingTriage(col="rms")` (tingkat rekaman): `ThresholdRule` dua ambang dipilih di unit latih (grid kuantil, maksimalkan balanced accuracy), skor keyakinan `rule_margin` (jarak log10 ke ambang terdekat), τ dari CV dalam grouped 5-fold di unit latih, cakupan target 0,9.

**Pembanding sekunder (hanya bila ada data daya):** ambang kW = kelas yang sama dengan pembanding utama, `col` = kolom daya rata-rata per jendela (nama kolom ditetapkan di addendum sebelum data dibuka). Gerbang sinyal sama.

**Gerbang sinyal (identik untuk semua model):** `AbstainGate.quality_ok`: SNR garis poros ≥ ambang CFAR (`pipeline.snr_cfar_threshold`, pfa 0,01, derau putih, tanpa label, dihitung ulang untuk laju sampel sensor baru dengan resep yang sama), `clip_max = 0,01`, `flat_max = 0,2`. Tingkat rekaman: `triage.MIN_OK_SHARE = 0,5`, prioritas usulan = 0,5·P(waspada) + P(rusak), kapasitas audit k = 3.

**Satu-satunya penyesuaian yang diizinkan, semuanya tanpa label dan dicatat di addendum sebelum rekaman pertama:**
1. `features.SHAFT_BAND` diset dari pelat nama (rpm nominal ± 25 %, dalam Hz). Nilai Ottawa (15–35 Hz) hanya cocok untuk rig itu; pompa 2 kutub (±48 Hz) di luar pita tersebut.
2. Laju sampel sensor dan konstanta laju sampel di `__init__.py`. Pita `SPEC_BANDS` di atas Nyquist dibiarkan seperti perilaku kode sekarang; **tidak** diganti dengan pita baru.
3. `io.py`: penambahan fungsi pembaca format berkas baru (tanpa mengubah fungsi lama).
4. Skrip evaluasi baru untuk §4–§5 (ditulis dan di-hash **sebelum** label dibuka; tidak boleh mengimpor apa pun yang mengubah model).

Perubahan di luar empat butir ini = model baru = prareg baru. Menambah fitur arus motor (MCSA) atau kW ke model usulan juga termasuk model baru.

**Manifes kode terkunci** (SHA-256, dihitung 28 Okt 2026 21:39:53 +0700; Python 3.11.9, scikit-learn 1.9.1, numpy 2.4.6, scipy 1.17.1, pandas 3.1.0; jalur relatif terhadap `prototype\`):

```
1c18c86c1e79f2f68ad617648067c11322930e53a8d86c4230c03f6f5dc80fe2  detakpompa/__init__.py
abc13c3a46867b69f12b8f3e34e28e2237675979d30ec933f8d6d8340f8f2530  detakpompa/deviation.py
e7dc308fe3ca88f7b3bee16d99faae817940f46d75f6c59db6e4662acc9ddd44  detakpompa/features.py
b083a19c417f659cbe6c4a262315fcd610a3ea40e5c6d8684bc87b200d6d9ad6  detakpompa/io.py
ba6a5d885d5d9e05e382e9983ec86d4e94829c1cd6128f41c35761589dd73c46  detakpompa/metrics.py
c015ad854b03c5774b85178afbc97aaa9fa4c19df985437c5a6555d177fcc63d  detakpompa/models.py
423e5c3f2b4f8d6838a38979bb13b56b131c7e3813ee778b01f11bf575496e40  detakpompa/pipeline.py
0921be759cefac582c4d8151628dddb5d54fae231ccbdc60ffe2a5b17764c9ff  detakpompa/report.py
a532e147413533805f9f25618b2b0d66c6a3f293477cc226f72b31292f1ce1bd  detakpompa/spectral.py
6b6fe41e3ec30df89536cd8b1a2a4d5f9637a443c57642bd72b70053422bfb2a  detakpompa/splits.py
833d4e41f4ffaa4aaeb437ab0780f8518c710d5178379c023e9289efcc53a52f  detakpompa/triage.py
c6ebed5172ae8ce40da0f05ca7e4094d1d41ac2a31918f163b1a68734a7abee1  run_eval.py
b0d542e44c6d444e13bfdda00df9de9a91e8d8f2cbd9de5f8bd7ce522ed5ef3c  run_eval_rms_gate.py
e64b11ecf08aed27c3ea1b3abcd5ae469d446e058bad5102250a5c514ee806d2  triase.py
1651343e0fd98491d9f3adacf7641ca98e7f13d1c124d7fd382d4188fcef05bd  demo.py
```

Cara cek: dari `prototype\`, `sha256sum -c` atas blok di atas. Berkas yang hash-nya berbeda harus bisa dijelaskan dengan butir 1–3 di atas (diff dilampirkan di addendum).

## 3. Data dan split

**Data yang memenuhi syarat** (salah satu, ditetapkan di addendum sebelum label dibuka):
- (a) rekaman pompa lab sendiri (TKT 4): pompa sentrifugal, akselerometer sensor BOM, clamp arus, power meter, flowmeter/manometer;
- (b) dataset publik bantalan/pompa dengan beberapa unit fisik dan, untuk H-AI2, variasi titik operasi (unduhan hanya dengan izin user, lisensi dicatat);
- (c) data PDAM (on-prem, dengan izin tertulis).

**Label** ditetapkan per kondisi **sebelum** rekaman: `sehat` (termasuk titik operasi berubah dengan mekanis sehat, mis. bukaan katup throttling; label kelas 0 "tidak perlu cek"); `waspada` = tingkat ringan yang diinduksi; `rusak` = tingkat berat. Definisi fisik tiap tingkat (massa imbalance, offset misalignment, bukaan katup) ditulis di addendum. Kedua model dilatih dengan label yang sama persis.

**Unit split = unit fisik** (satu pompa, satu bantalan, atau satu rakitan yang tidak pernah muncul di data latih). Leave-one-physical-unit-out bila ≤ 20 unit; grouped 10-fold bila > 20. `assert_no_leakage` di tiap fold. Semua jendela dan semua sesi satu unit selalu di sisi yang sama. Split per sesi pemasangan pada **satu** unit tidak memenuhi syarat H-AI1 (itu generalisasi antar-sesi, bukan antar-unit).

**Ukuran minimum** (di bawah ini hasilnya TIDAK KONKLUSIF, §7):
- H-AI1: ≥ 8 unit fisik, masing-masing punya kelas `sehat` dan minimal satu kelas fault; ≥ 5 sesi × 30 s per kondisi per unit untuk data lab.
- H-AI2: ≥ 3 unit fisik dengan rekaman titik-operasi-berubah **dan** fault; ≥ 5 sesi × 30 s per kondisi per unit; sensor dilepas-pasang antarsesi.

**Pembutaan:** berkas rekaman diberi ID acak; peta ID → label disimpan oleh anggota yang tidak menjalankan analisis (usul: Aziz) sampai fitur, keputusan gerbang sinyal, dan daftar sesi yang dibuang karena kualitas sinyal sudah dihitung dan dicatat.

## 4. Endpoint primer (keluarga primer, koreksi Holm)

Semua dihitung pada **jendela yang lolos gerbang sinyal** (himpunan sama untuk kedua model, karena gerbangnya identik), **tanpa** gerbang ragu tahap 2, dengan prediksi out-of-fold dari split §3. Selisih = usulan − RMS + gerbang. Interval = bootstrap berpasangan per unit fisik (unit diambil ulang dengan pengembalian, metrik dihitung dari semua jendela unit terambil), B = 10.000, seed 0.

| # | Endpoint | Berlaku bila | Metrik |
|---|---|---|---|
| **P1** (H-AI1) | Klasifikasi kondisi di unit baru | Selalu (bila syarat minimum H-AI1 terpenuhi) | Balanced accuracy 3-kelas (sehat / waspada / rusak) |
| **P2** (H-AI2) | Titik operasi vs fault | Data punya kondisi titik-operasi-berubah dengan mekanis sehat | Balanced accuracy keputusan biner "perlu cek" (prediksi waspada atau rusak) pada himpunan {jendela titik-operasi-berubah-sehat} ∪ {jendela fault}; kelas "tidak perlu cek" = titik operasi berubah, kelas "perlu cek" = fault |

**Uji:** H0: selisih ≤ 0 vs H1: selisih > 0. p satu sisi = (1 + #{selisih bootstrap ≤ 0}) / (B + 1). Jumlah uji primer m = 1 (hanya P1) atau m = 2 (P1 dan P2); nilai m ditetapkan di addendum sebelum label dibuka, berdasarkan kondisi yang **direkam**, bukan hasil. Koreksi **Holm** pada α satu sisi = 0,025 (setara dengan "batas bawah CI 95 % dua sisi > 0" bila m = 1). Untuk m = 2: p terkecil harus < 0,0125 (setara batas bawah CI 97,5 % dua sisi > 0), lalu p berikutnya < 0,025.

**Endpoint primer P_k LULUS** bila ditolak oleh Holm **dan** semua pengaman di §5 terpenuhi.

## 5. Pengaman (wajib terpenuhi agar endpoint primer dihitung LULUS)

Dihitung pada data dan split yang sama:
- **G1 tidak kehilangan fault:** proporsi jendela fault (waspada + rusak) yang diprediksi "perlu cek", selisih usulan − RMS: batas bawah CI 95 % > −0,10. (Di Ottawa: 325/373 = 0,871 vs 335/373 = 0,898, dihitung dari `rmsgate_metrics.csv`; bukan bagian uji.)
- **G2 tidak menambah alarm palsu:** proporsi jendela `sehat` (termasuk titik-operasi-berubah) yang diprediksi "perlu cek": usulan ≤ RMS + 0,05 (estimasi titik).
- **G3 nilai triase pada prevalensi realistis:** presisi@3 tingkat rekaman pada armada simulasi 22 pompa dengan 3 dan 5 pompa bermasalah (prosedur sama dengan `run_triase_eval.py --prevalensi`): usulan ≥ RMS − 0,05 (estimasi titik) di kedua skenario.

## 6. Endpoint sekunder (dilaporkan semua; tidak bisa mengubah status LULUS/GAGAL)

Keluarga sekunder, Holm dua sisi α = 0,05, dilaporkan bersama CI 95 %:
1. Macro-F1 3-kelas.
2. Recall per kelas (sehat, waspada, rusak). **Recall waspada adalah metrik label tahap, bukan deteksi dini**, dan tidak boleh dipromosikan menjadi bukti deteksi lebih awal.
3. Proporsi jendela waspada yang ditandai "perlu cek" (metrik E1). Hanya metrik ini yang boleh dipakai untuk bicara "menandai tahap awal", dan hanya bila selisihnya signifikan setelah Holm.
4. AURC galat dengan gerbang (`metrics.gated_score`).
5. Balanced accuracy di titik operasi dua tahap (gerbang sinyal + gerbang ragu), dengan cakupan masing-masing.
6. Presisi@3 armada 22 pompa, 3/22 dan 5/22 bermasalah, dengan dasar acak.
7. P2 terhadap ambang kW (bila ada data daya).
8. P1 terhadap aturan envelope + kurtosis (`EnvelopeKurtosisRule`), bila label adalah jenis fault nominal, bukan tingkat.

Jumlah uji sekunder maksimum 10. Semua dilaporkan, termasuk yang merugikan usulan.

## 7. Aturan berhenti dan TIDAK KONKLUSIF

- **Satu analisis konfirmasi per dataset.** Tidak ada intip di tengah. Pengumpulan data selesai saat semua sesi di daftar addendum terekam, atau saat akses lab berakhir; analisis dijalankan sekali setelah label dikunci.
- **Tidak boleh menambah data setelah melihat hasil.** Kalau data kurang, hasilnya TIDAK KONKLUSIF. Pengumpulan tambahan hanya lewat prareg v3, dengan hasil v2 tetap dilaporkan.
- **TIDAK KONKLUSIF** (dilaporkan "belum teruji", **bukan** lulus) bila: syarat minimum §3 tidak terpenuhi; gerbang sinyal menolak > 30 % jendela `sehat`; kode terkunci tidak bisa dijalankan pada laju sampel/format data tanpa perubahan di luar §2 butir 1–4; atau ditemukan kebocoran (gagal `assert_no_leakage`). Kebocoran diperbaiki hanya di kode split, dicatat, lalu analisis diulang sekali.
- **Membuang sesi** hanya karena kualitas sinyal yang dicatat di log sensor **sebelum** label dibuka.

## 8. Keputusan dan apa yang dilaporkan

| Hasil | Arti | Yang kami tulis di 05/08/09/10 dan pitch |
|---|---|---|
| ≥ 1 endpoint primer LULUS | Bukti pertama bahwa AI diperlukan, untuk alasan yang lulus saja (H-AI1 dan/atau H-AI2), di domain data itu | Angka primer + CI, p Holm, pengaman, semua sekunder. Domain disebut eksplisit (mis. "bantalan publik, bukan pompa"). |
| Semua primer GAGAL (tidak ditolak Holm, atau pengaman dilanggar) | AI belum diperlukan | Kata "AI" dicabut dari klaim inti di semua materi. Produk dijual sebagai gerbang sinyal + ambang RMS + antrean triase. Semua angka primer dan sekunder tetap dilaporkan apa adanya, termasuk arah selisih. Metrik sekunder (recall waspada, AURC, dll.) **tidak boleh** dipakai sebagai "hiburan". AI hanya boleh diklaim lagi lewat prareg baru pada data baru. |
| TIDAK KONKLUSIF | Belum teruji | "Belum teruji", alasannya, dan apa yang kurang. Status klaim AI tetap "hipotesis". |

Hasil apa pun ditambahkan di bawah berkas ini sebagai **bagian hasil terpisah** (berkas ini sendiri tidak diubah; hash-nya tetap) dan dirujuk dari `05_BUKTI_TKT.md`.

## 9. Addendum yang wajib ditulis sebelum label dibuka

Berkas terpisah `prototype\PRAREG_TKT4_addendum_<tanggal>.md` dengan SHA-256 sendiri, berisi: dataset terpilih dan lisensinya; definisi fisik tiap kondisi dan tingkat; daftar unit dan sesi yang direncanakan; nilai m (1 atau 2); `SHAFT_BAND`, laju sampel, dan nama kolom daya; diff kode terhadap manifes §2; hash skrip evaluasi; nama orang yang memegang peta label. Addendum **tidak boleh** mengubah endpoint, ambang lulus, pengaman, atau aturan di berkas ini.
