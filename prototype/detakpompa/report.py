"""Human-readable "laporan kesehatan pompa" (triage report).

Posisi: TRIASE (pompa mana yang perlu dicek/diaudit duluan), bukan pengukur efisiensi.
Efisiensi pompa butuh debit + head + daya listrik; getaran saja tidak cukup.
Catatan energi hanya memakai angka bersumber (03_RISET.md S6, S10), berlabel skenario.
"""

from __future__ import annotations

STATUS_LABEL = {0: "SEHAT", 1: "WASPADA", 2: "RUSAK", -1: "TIDAK TAHU"}

ACTION = {
    0: "Tidak perlu tindakan khusus. Rekam ulang sesuai jadwal rutin.",
    1: "Masukkan ke daftar cek minggu ini: inspeksi bearing/pelumasan, bandingkan dengan rekaman baseline unit ini.",
    2: "Prioritas cek: jadwalkan inspeksi bearing dan audit energi pompa ini (flowmeter portable + manometer + power meter).",
}

NEXT_STEP = {
    "sinyal": ("Ukur ulang 30 detik dengan sensor dipasang kencang di bearing housing (magnet/baut, bukan selotip), "
               "arah radial; pastikan pompa berjalan pada putaran normal dan kabel sensor tidak longgar."),
    "ragu": ("Ukur ulang 30 detik di titik yang sama, lalu bandingkan dengan rekaman baseline unit ini "
             "(mode --baseline). Bila tetap ragu: cek dengan flowmeter portable + manometer untuk melihat "
             "apakah kinerja hidrolik pompa turun."),
    "pendek": "Rekaman terlalu pendek. Rekam minimal 10 detik (disarankan 30 detik).",
}

# Sourced scenario numbers (03_RISET.md). DO NOT replace with model output.
S6 = {"biaya_energi_rp": 147_654_439_569, "tahun": 2021, "porsi_opex_pct": 24.37,
      "efisiensi_pompa_T1_pct": 49.77,
      "sumber": "S6: Indra dkk., JIST 5(2) 2024, IPA Ngagel I, PDAM Surya Sembada (audit manual)"}
S10 = {"eff_awal_pct": 65.2, "eff_aus_pct": 53.6, "daya_awal_hp": 270, "daya_aus_hp": 285,
       "debit_awal_gpm": 4100, "debit_aus_gpm": 3900,
       "sumber": "S10: Nelik, Pumps & Systems, 3 Okt 2016 (satu kasus lapangan, celah wear-ring)"}


def energy_note() -> list[str]:
    daya = S10["daya_aus_hp"] / S10["daya_awal_hp"] - 1
    per_vol = (S10["daya_aus_hp"] / S10["debit_aus_gpm"]) / (S10["daya_awal_hp"] / S10["debit_awal_gpm"]) - 1
    rp = f"{S6['biaya_energi_rp']:,}".replace(",", ".")
    return [
        "CATATAN ENERGI [SKENARIO, BUKAN PENGUKURAN]",
        f"- Konteks: biaya energi PDAM Surya Sembada {S6['tahun']} Rp{rp} "
        f"({S6['porsi_opex_pct']:.2f} % opex); pompa distribusi T1 IPA Ngagel I terukur "
        f"{S6['efisiensi_pompa_T1_pct']:.2f} % lewat audit manual. [{S6['sumber']}]",
        f"- Skenario: bila pompa yang ditandai ternyata aus seperti kasus S10 (efisiensi "
        f"{S10['eff_awal_pct']} % -> {S10['eff_aus_pct']} %), daya naik {S10['daya_awal_hp']} -> "
        f"{S10['daya_aus_hp']} hp (+{100 * daya:.1f} %) sambil debit turun {S10['debit_awal_gpm']} -> "
        f"{S10['debit_aus_gpm']} gpm, yaitu energi per volume +{100 * per_vol:.1f} % (aritmetika dari "
        f"angka S10). [{S10['sumber']}]",
        "- Status di atas TIDAK mengukur efisiensi atau kWh. Efisiensi butuh debit + head + daya "
        "listrik (flowmeter, manometer, power meter). Fungsi alat ini: memilih pompa mana yang diaudit duluan.",
    ]


def priority_text(r: dict) -> str:
    """Signal-gated / too-short recordings get NO priority (they must never outrank a pump that
    was actually assessed); an unsure ('ragu') one shows a provisional value, not used for ranking."""
    reason = r.get("abstain_reason")
    if reason in ("sinyal", "pendek"):
        return ("- (tidak diurutkan; masuk antrean UKUR ULANG. Sinyal tidak bisa dipercaya, "
                "jadi tidak ada prioritas sampai diukur ulang)")
    if reason == "ragu":
        pv = r.get("priority_provisional")
        pv_txt = "-" if pv is None else f"{pv:.2f}"
        return (f"{pv_txt} SEMENTARA (model ragu; masuk antrean UKUR ULANG, "
                "tidak ikut urutan audit sampai diukur ulang)")
    if r.get("priority") is None:
        return "-"
    return f"{r['priority']:.2f} (0 = sehat ... 1 = rusak; untuk mengurutkan pompa)"


def format_report(r: dict) -> str:
    L = []
    L.append("=" * 72)
    L.append("LAPORAN KESEHATAN POMPA (DetakPompa, purwarupa TKT 3, triase)")
    L.append("=" * 72)
    L.append(f"Berkas       : {r['file']}")
    if r.get("unit_note"):
        L.append(f"Catatan unit : {r['unit_note']}")
    L.append(f"Durasi       : {r['duration_s']:.1f} s, {r['n_windows']} jendela x 1 s, fs = {r['fs']:.0f} Hz")
    L.append(f"STATUS       : {STATUS_LABEL[r['status']]}")
    if r["status"] == -1:
        L.append(f"Alasan abstain: {r['abstain_reason_text']}")
        L.append(f"LANGKAH BERIKUTNYA: {r['next_step']}")
        L.append("Catatan      : TIDAK TAHU bukan berarti aman. Di uji leave-one-bearing-out, 69 dari 76 "
                 "jendela TIDAK TAHU (91 %) berasal dari bantalan berkembang/rusak.")
    else:
        L.append(f"Tindakan     : {ACTION[r['status']]}")
    L.append(f"Antrean      : {r.get('queue', '-')}")
    L.append("Prioritas cek: " + priority_text(r))
    p = r["proba"]
    tag = " [TIDAK DIPAKAI: sinyal ditolak]" if r.get("abstain_reason") in ("sinyal", "pendek") else ""
    L.append(f"Probabilitas : sehat {p[0]:.2f} | waspada {p[1]:.2f} | rusak {p[2]:.2f} "
             f"(ambang yakin {r['tau_conf']:.2f}){tag}")
    L.append(f"Kualitas sinyal: SNR garis poros {r['snr_db']:.1f} dB (ambang {r['snr_min']:.1f} dB), "
             f"frekuensi poros terlacak {r['shaft_hz']:.2f} Hz (~{60 * r['shaft_hz']:.0f} rpm), "
             f"{r['n_ok']}/{r['n_windows']} jendela lolos gerbang sinyal")
    L.append("Fitur dominan (nilai rekaman ini vs median unit sehat di data latih):")
    for name, val, ref in r["top_features"]:
        L.append(f"   - {name:14s} = {val:10.3f}   (median sehat {ref:10.3f})")
    if r.get("deviation") is not None:
        d = r["deviation"]
        L.append(f"Deviasi dari baseline unit sendiri: skor {d['score']:.2f} "
                 f"(acuan: median jendela baseline = {d['ref_score']:.2f}); fitur paling bergeser: "
                 + ", ".join(f"{n} (z={z:+.1f})" for n, z in d["top"]))
    L.append("")
    L.extend(energy_note())
    L.append("")
    L.append("Batas klaim: model dilatih di rig bantalan Ottawa (bukan pompa PDAM). Validasi lab sendiri "
             "(TKT 4) dan data pompa PDAM (TKT 5) belum dilakukan.")
    return "\n".join(L)
