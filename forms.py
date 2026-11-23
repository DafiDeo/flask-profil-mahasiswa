"""
FORMS.PY — TUGAS INDIVIDU 7
Definisi form class dengan Flask-WTF (Form class, validator, proteksi CSRF).
Nama : Dafi Deo Ananda Nurrokhim
NBI  : 1482500040

Dua form sesuai soal Tugas Individu 7:
1. KontakForm    -> form kontak/pemesanan untuk PUBLIK (halaman /kontak)
2. MatakuliahForm-> form TAMBAH DATA di DASHBOARD ADMIN (halaman /admin)

Jenis validator berbeda yang dipakai (minimal 4 sesuai soal):
- DataRequired : field wajib diisi
- Length       : batas panjang karakter (min/max)
- Email        : format email valid (butuh paket email-validator)
- Regexp       : pola teks untuk kode matakuliah
- NumberRange  : batas angka (SKS 1-6)

Setiap form FlaskForm otomatis menyisipkan token CSRF melalui
form.hidden_tag() di template, sehingga semua form terlindungi CSRF.
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, IntegerField, SelectField, SubmitField
)
from wtforms.validators import (
    DataRequired, Email, Length, NumberRange, Regexp
)

# pilihan nilai huruf untuk select di form admin
PILIHAN_NILAI = [
    ("A", "A"), ("AB", "AB"), ("B", "B"), ("BC", "BC"),
    ("C", "C"), ("D", "D"), ("E", "E"),
]


class KontakForm(FlaskForm):
    """Form kontak publik: pengunjung mengirim pesan ke mahasiswa."""

    nama = StringField("Nama", validators=[
        DataRequired(message="Nama wajib diisi"),
        Length(min=3, max=50,
               message="Nama minimal 3 dan maksimal 50 karakter"),
    ])
    email = StringField("Email", validators=[
        DataRequired(message="Email wajib diisi"),
        Email(message="Format email tidak valid, contoh: nama@domain.com"),
    ])
    pesan = TextAreaField("Pesan", validators=[
        DataRequired(message="Pesan wajib diisi"),
        Length(min=10, max=500,
               message="Pesan minimal 10 dan maksimal 500 karakter"),
    ])
    submit = SubmitField("Kirim Pesan")


class MatakuliahForm(FlaskForm):
    """Form tambah data matakuliah di dashboard admin (dari live coding PPT,
    diadaptasi ke studi kasus project: tambah matakuliah ke list Python)."""

    kode = StringField("Kode MK", validators=[
        DataRequired(message="Kode matakuliah wajib diisi"),
        Length(min=5, max=8,
               message="Kode harus 5-8 karakter, contoh: SIF107"),
        Regexp(r"^[A-Za-z]{2,4}\d{3}$",
               message="Format kode: 2-4 huruf diikuti 3 angka (contoh: SIF107)"),
    ])
    nama = StringField("Nama Matakuliah", validators=[
        DataRequired(message="Nama matakuliah wajib diisi"),
        Length(min=3, max=60,
               message="Nama matakuliah minimal 3 dan maksimal 60 karakter"),
    ])
    sks = IntegerField("SKS", validators=[
        DataRequired(message="SKS wajib diisi"),
        NumberRange(min=1, max=6,
                    message="SKS harus angka antara 1 sampai 6"),
    ])
    nilai = SelectField("Nilai Huruf",
                        choices=PILIHAN_NILAI,
                        validators=[DataRequired()])
    submit = SubmitField("Tambah Matakuliah")
