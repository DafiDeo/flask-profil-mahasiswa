import os

from flask import Flask, flash, redirect, render_template, url_for
from flask_wtf import CSRFProtect

from forms import KontakForm, MatakuliahForm

app = Flask(__name__)

csrf = CSRFProtect(app)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-kunci-rahasia-ganti-saat-production"
)


# DATA (list Python — sementara, diganti database di pertemuan 14)

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
    {"kode": "SIF104",   "nama": "ALGORITMA DAN STRUKTUR DATA",             "sks": 3, "nilai": "AB", "bobot": 3.50},
    {"kode": "SIF105",   "nama": "TEKNOLOGI INFORMASI DAN APLIKASI BISNIS BERKEMBANG", "sks": 3, "nilai": "AB", "bobot": 3.50},
    {"kode": "SIF106",   "nama": "SISTEM BASIS DATA",                        "sks": 2, "nilai": "B",  "bobot": 3.00},
    {"kode": "SIF106",   "nama": "ARSITEKTUR DAN ORGANISASI KOMPUTER",       "sks": 3, "nilai": "AB", "bobot": 3.50},
]

data_semester = [
    {"semester": "Semester 1", "sks": 18, "ip": 3.31, "ipk": 3.31},
    {"semester": "Semester 2", "sks": 20, "ip": 3.53, "ipk": 3.42},
    {"semester": "Semester 3", "sks": 23, "ip": None,  "ipk": 3.42},  # sedang berjalan
]

# bobot setiap nilai huruf (untuk form tambah matakuliah, Tugas 7)
BOBOT_NILAI = {
    "A": 4.00, "AB": 3.50, "B": 3.00, "BC": 2.50,
    "C": 2.00, "D": 1.00, "E": 0.00,
}


# FUNGSI pengolahan list Python

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


# ROUTE

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


# TUGAS INDIVIDU 7: FORM DAN SUBMIT DATA DENGAN FLASK-WTF

@app.route("/kontak", methods=["GET", "POST"])
def kontak():
    """Form kontak publik (KontakForm).

    Satu route menangani dua hal (sesuai materi Pertemuan 12):
    - GET  : menampilkan form kosong
    - POST : memvalidasi data; jika valid -> flash() + redirect (pola PRG),
             jika gagal -> form ditampilkan ulang dengan pesan error di
             bawah field dan input yang benar tetap terisi (WTForms otomatis
             mengisi ulang dari data yang dikirim).
    """
    form = KontakForm()
    if form.validate_on_submit():  # POST + semua validator lolos + token CSRF valid
        flash(
            "Terima kasih {}, pesanmu berhasil dikirim! "
            "Balasan akan dikirim ke {}.".format(form.nama.data, form.email.data),
            "success",
        )
        return redirect(url_for("kontak"))  # pola Post/Redirect/Get (PRG)
    return render_template("kontak.html", profil=profil, form=form)


@app.route("/admin", methods=["GET", "POST"])
def admin_dashboard():
    """Dashboard admin: sidebar + stat card + tabel data dari list Python.

    Tugas 7: route yang sama menerima POST dari MatakuliahForm. Jika data
    valid, matakuliah baru ditambahkan ke list data_matakuliah (bobot dihitung
    dari mapping BOBOT_NILAI), lalu redirect dengan flash sukses (PRG).
    Stat card dan tabel otomatis memakai data terbaru karena dihitung ulang
    setiap kali halaman dirender.
    """
    form = MatakuliahForm()
    if form.validate_on_submit():
        data_matakuliah.append({
            "kode": form.kode.data.upper(),
            "nama": form.nama.data.upper(),
            "sks": form.sks.data,
            "nilai": form.nilai.data,
            "bobot": BOBOT_NILAI[form.nilai.data],
        })
        flash(
            "Matakuliah {} - {} ({} SKS, nilai {}) berhasil ditambahkan!".format(
                form.kode.data.upper(), form.nama.data.upper(),
                form.sks.data, form.nilai.data,
            ),
            "success",
        )
        return redirect(url_for("admin_dashboard"))  # pola PRG
    return render_template(
        "admin/dashboard.html",
        profil=profil,
        statistik=hitung_statistik(),
        matakuliah=data_matakuliah,
        form=form,
    )


if __name__ == "__main__":
    app.run(debug=True)
