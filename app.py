from flask import Flask, render_template

app = Flask(__name__)


# ==================== DATA (list Python — sementara, diganti database di pertemuan 14) ====================

profil = {
    "nama": "Dafi Deo Ananda Nurrokhim",
    "nbi": "1482500040",
    "prodi": "S1 Sistem dan Teknologi Informasi",
    "fakultas": "Fakultas Teknologi Elektro dan Informatika Cerdas (FTEIC)",
    "kampus": "Universitas 17 Agustus 1945 Surabaya",
    "ipk": 3.42,
    "predikat": "Sangat Memuaskan",
}

data_matakuliah = [
    {"kode": "14823372", "nama": "STATISTIKA DAN PROBABILITAS",              "sks": 2, "nilai": "AB", "bobot": 3.50},
    {"kode": "SIF102",   "nama": "PEMROGRAMAN BERORIENTASI OBJEK",           "sks": 4, "nilai": "A",  "bobot": 4.00},
    {"kode": "SIF103",   "nama": "INTERAKSI MANUSIA KOMPUTER",               "sks": 3, "nilai": "AB", "bobot": 3.50},
    {"kode": "SIF104",   "nama": "ALGORITMA DAN STRUKTUR DATA",              "sks": 3, "nilai": "AB", "bobot": 3.50},
    {"kode": "SIF105",   "nama": "TEKNOLOGI INFORMASI DAN APLIKASI BISNIS BERKEMBANG", "sks": 3, "nilai": "AB", "bobot": 3.50},
    {"kode": "SIF106",   "nama": "SISTEM BASIS DATA",                        "sks": 2, "nilai": "B",  "bobot": 3.00},
    {"kode": "SIF106",   "nama": "ARSITEKTUR DAN ORGANISASI KOMPUTER",       "sks": 3, "nilai": "AB", "bobot": 3.50},
]

data_semester = [
    {"semester": "Semester 1", "sks": 18, "ip": 3.31, "ipk": 3.31},
    {"semester": "Semester 2", "sks": 20, "ip": 3.53, "ipk": 3.42},
    {"semester": "Semester 3", "sks": 23, "ip": None,  "ipk": 3.42},  # sedang berjalan
]


# ==================== FUNGSI BANTU (pengolahan list Python) ====================

def hitung_total_sks(daftar):
    """Menjumlahkan seluruh SKS dengan perulangan for."""
    total = 0
    for mk in daftar:
        total += mk["sks"]
    return total


def hitung_ip(daftar):
    """Menghitung IP = total (bobot x SKS) dibagi total SKS."""
    total_poin = 0
    for mk in daftar:
        total_poin += mk["bobot"] * mk["sks"]
    return total_poin / hitung_total_sks(daftar)


def hitung_statistik():
    """Menyusun data stat card dashboard langsung dari list Python."""
    total_sks = hitung_total_sks(data_matakuliah)
    ip_semester = hitung_ip(data_matakuliah)
    ipk_terakhir = data_semester[-1]["ipk"]  # ambil IPK terakhir dari list semester

    return [
        {"label": "Matakuliah",      "nilai": len(data_matakuliah), "ikon": "bi-journal-bookmark-fill", "warna": "primary"},
        {"label": "Total SKS",       "nilai": total_sks,            "ikon": "bi-clock-history",         "warna": "success"},
        {"label": "IP Semester Ini", "nilai": "{:.2f}".format(ip_semester), "ikon": "bi-graph-up-arrow", "warna": "info"},
        {"label": "IPK Kumulatif",   "nilai": "{:.2f}".format(ipk_terakhir), "ikon": "bi-award-fill",    "warna": "warning"},
    ]


# ==================== ROUTE ====================

@app.route("/")
def index():
    """Halaman beranda: hero + kartu profil (data dikirim dari Python)."""
    return render_template("index.html", profil=profil)


@app.route("/nilai")
def nilai():
    """Halaman nilai matakuliah: tabel interaktif (render oleh JavaScript)."""
    return render_template("nilai.html")


@app.route("/ipk")
def ipk():
    """Halaman IPK: kartu IPK + rekap semester (dirender JavaScript)."""
    return render_template("ipk.html", profil=profil)


@app.route("/admin")
def admin_dashboard():
    """Dashboard admin: sidebar + stat card + tabel data dari list Python."""
    return render_template(
        "admin/dashboard.html",
        profil=profil,
        statistik=hitung_statistik(),
        matakuliah=data_matakuliah,
    )


if __name__ == "__main__":
    app.run(debug=True)
