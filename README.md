# Website Profil Mahasiswa — Versi Flask

**Tugas Individu 6 — Pengembangan Situs Web (PSBW)**
Pertemuan 11: Integrasi HTML & CSS dengan Flask
**Tugas Individu 7 — Pengembangan Situs Web (PSBW)**
Pertemuan 12: Forms di Flask (Flask-WTF, CSRF, PRG, Flash)
Lanjutan Tugas Individu 1–2 (Bootstrap + JavaScript DOM + jQuery)

| Identitas | |
|---|---|
| Nama | **Dafi Deo Ananda Nurrokhim** |
| NBI | **1482500040** |
| Program Studi | S1 Sistem dan Teknologi Informasi |
| Fakultas | Fakultas Teknologi Elektro dan Informatika Cerdas (FTEIC) |
| Kampus | Universitas 17 Agustus 1945 Surabaya |

---

## 1. Penjelasan Singkat Project

Pada Tugas Individu 1–2, website profil mahasiswa dibuat sebagai **satu file HTML statis**
(`Profile_Data_Diri.html`) dengan CSS Bootstrap, JavaScript DOM, dan jQuery. Pada tugas ini,
website yang sama **dipindahkan ke dalam aplikasi Flask** sehingga berubah dari kumpulan
file statis menjadi **aplikasi web dinamis** yang dijalankan oleh server Python:

1. Semua HTML dipindahkan ke folder `templates/` dan dipecah menjadi beberapa template
   yang saling mewarisi (**template inheritance** dengan `base.html`).
2. CSS, JavaScript, dan gambar dipindahkan ke folder `static/` dan dipanggil dengan
   **`url_for()`**, bukan path manual.
3. Data profil dan data matakuliah sekarang disimpan dalam **list/dict Python** di `app.py`
   dan dikirim ke template melalui `render_template()`.
4. Ditambahkan **halaman dashboard admin** (sidebar + 4 stat card + tabel data) yang datanya
   langsung dihitung dari list Python menggunakan loop Jinja2.
5. Seluruh fitur interaktif dari Tugas Individu 2 (pencarian, filter, hapus dengan jQuery,
   form tambah + validasi, mode gelap) **tetap berjalan**.
6. **(Tugas Individu 7)** Ditambahkan **form dan submit data dengan Flask-WTF**: halaman
   `/kontak` untuk pengunjung (form kontak publik) dan form **tambah matakuliah** di
   dashboard admin — lengkap dengan **token CSRF**, **5 jenis validator**, **pola PRG**
   (Post/Redirect/Get), **flash message**, dan **styling Bootstrap**.

Sesuai materi Pertemuan 11, integrasi dilakukan mengikuti **5 langkah pemindahan website
ke Flask**: pindahkan HTML ke `templates/` → pindahkan aset ke `static/` → buat `base.html`
→ ganti semua path menjadi `url_for` → buat route + `render_template` untuk setiap halaman.

---

## 2. Apa yang Berubah dari Tugas Individu 1–2?

| Aspek | Tugas Individu 1–2 (HTML statis) | Versi Flask (project ini) |
|---|---|---|
| File HTML | 1 file: `Profile_Data_Diri.html` | Pecahan template di `templates/` (`base.html` + 3 halaman + dashboard admin) |
| CSS & JS | `href="style.css"` (path manual) | `url_for('static', filename='css/style.css')` |
| Gambar | path manual `img/foto.jpg` | `url_for('static', filename='img/...')` |
| Data profil | ditulis langsung (hardcode) di HTML | disimpan di dict `profil` (Python), dikirim via `render_template` |
| Link antar halaman | tidak ada (satu halaman) | `url_for('nilai')`, `url_for('ipk')`, dst. (nama endpoint, bukan nama file) |
| Navbar | satu halaman, menu aktif tidak perlu | 4 halaman, menu aktif otomatis via `request.endpoint` |
| Dashboard admin | tidak ada | ada: sidebar + stat card + tabel data list Python |
| Form & submit data | modal kontak + validasi jQuery (client-side saja) | halaman `/kontak` + form admin dengan **Flask-WTF** (server-side, CSRF, PRG) — Tugas 7 |
| Notifikasi hasil aksi | pesan sukses jQuery (hanya halaman nilai) | `flash()` + alert Bootstrap di semua halaman — Tugas 7 |
| Cara menjalankan | buka file HTML langsung di browser | `python app.py` lalu buka `http://127.0.0.1:5000` |

Yang **tidak berubah**: tampilan, komponen Bootstrap, dan seluruh fitur JavaScript/jQuery
dari Tugas Individu 2 (lihat Bagian 11).

---

## 3. Struktur Folder Project

Struktur mengikuti pola standar Flask pada materi (folder `static/` dan `templates/`):

```text
flask-profil-mahasiswa/
│
├── app.py                      # Aplikasi Flask: data (list Python), fungsi hitung, 5 route (2 menerima POST)
├── forms.py                    # Tugas 7: class form Flask-WTF (KontakForm, MatakuliahForm) + validator
├── requirements.txt            # Dependensi: Flask, Flask-WTF, email-validator
├── README.md                   # File penjelasan ini
│
├── static/                     # File yang TIDAK diproses Python (CSS, JS, gambar)
│   ├── css/
│   │   └── style.css           # CSS website + mode gelap + sidebar admin
│   ├── js/
│   │   └── script.js           # DOM, event, validasi, jQuery (dipakai semua halaman)
│   └── img/
│       └── IMG_20260728_090150.jpg   # Foto profil (taruh di sini)
│
└── templates/                  # Semua file HTML (dirender oleh Jinja2)
    ├── base.html               # Template INDUK: <head>, navbar, flash message, footer, modal kontak, script
    ├── index.html              # Halaman Beranda : hero + kartu profil
    ├── nilai.html              # Halaman Nilai    : tabel interaktif + form tambah
    ├── ipk.html                # Halaman IPK     : kartu IPK + rekap semester
    ├── kontak.html             # Tugas 7         : form kontak publik (Flask-WTF, CSRF, error per field)
    ├── partials/
    │   └── navbar.html         # Navbar (partial) dengan menu aktif dinamis
    └── admin/
        ├── base_admin.html     # Layout dashboard: sidebar + topbar (mewarisi base.html)
        └── dashboard.html      # Stat card + tabel data + form tambah matakuliah (Tugas 7)
```

> Flask **otomatis** membuat route `/static/<path:filename>` untuk semua file di folder
> `static/`, sehingga CSS bisa diakses di `http://127.0.0.1:5000/static/css/style.css`.

---

## 4. Konsep Flask yang Dipakai (Penjelasan per Konsep)

### 4.1 Folder `static/` dan `url_for()`

File yang tidak diproses oleh Python (CSS, JavaScript, gambar, font) wajib berada di folder
`static/` dan dipanggil dengan `url_for('static', filename=...)`. Ini dipakai di `base.html`:

```html
<link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
<img src="{{ url_for('static', filename='img/IMG_20260728_090150.jpg') }}" alt="Foto Profil">
```

Mengapa tidak memakai path manual seperti `href="css/style.css"` (cara Tugas Individu 1–2)?

| Path manual | `url_for` |
|---|---|
| Path relatif berubah tergantung URL halaman yang sedang dibuka | Selalu menghasilkan path absolut `/static/...` yang benar |
| Rusak jika struktur folder berubah | Mengikuti struktur folder otomatis |
| Link halaman ditulis `nilai.html` | Link halaman ditulis nama endpoint: `url_for('nilai')` |

### 4.2 Route dan `render_template()`

Route adalah alamat URL yang ditangani sebuah fungsi Python (dekorator `@app.route`).
Fungsi tersebut mengembalikan template HTML lewat `render_template()`, sekaligus
**mengirim data Python ke template** sebagai parameter kata kunci:

```python
@app.route("/admin")
def admin_dashboard():
    return render_template(
        "admin/dashboard.html",
        profil=profil,                 # dict Python  -> variabel 'profil' di template
        statistik=hitung_statistik(),  # list of dict -> variabel 'statistik'
        matakuliah=data_matakuliah,    # list of dict -> variabel 'matakuliah'
    )
```

### 4.3 Template Inheritance (`base.html`, `{% extends %}`, `{% block %}`)

Bagian yang berulang di semua halaman (head, navbar, footer, modal kontak, pemanggilan
script) cukup ditulis **satu kali** di `base.html`. Template anak mewarisinya dengan
`{% extends %}` dan hanya mengisi "lubang" yang disediakan `{% block %}`:

```html
<!-- base.html : menyediakan lubang -->
<title>{% block title %}Profil Mahasiswa{% endblock %} — Dafi Deo Ananda Nurrokhim</title>
...
{% block content %}{% endblock %}
```

```html
<!-- index.html : mengisi lubang -->
{% extends "base.html" %}
{% block title %}Beranda{% endblock %}
{% block content %}
  ...isi khusus halaman beranda...
{% endblock %}
```

Hasilnya: mengganti navbar/footer cukup di satu tempat, dan ketiga halaman publik
serta dashboard admin otomatis ikut berubah (prinsip **konsistensi** pada materi
Prinsip Desain Web).

### 4.4 Partial Navbar + Menu Aktif Dinamis (`request.endpoint`)

Navbar disimpan terpisah di `templates/partials/navbar.html` lalu dimasukkan ke
`base.html` dengan `{% include "partials/navbar.html" %}`. Daftar menu dibuat dengan
`{% set %}` dan loop Jinja2, dan menu yang sedang dibuka otomatis diberi class `active`
karena **`request.endpoint` berisi nama fungsi route yang sedang diakses** — tidak perlu
dikirim dari Python:

```html
{% set menu = [
  ("index", "Beranda"),
  ("nilai", "Nilai Matakuliah"),
  ("ipk", "IPK"),
  ("admin_dashboard", "Dashboard")
] %}

{% for endpoint, label in menu %}
<li class="nav-item">
  <a class="nav-link {{ 'active' if request.endpoint == endpoint }}"
     href="{{ url_for(endpoint) }}">{{ label }}</a>
</li>
{% endfor %}
```

### 4.5 Nested Inheritance (Dashboard Admin)

Template boleh mewarisi template yang juga mewarisi template lain. Dashboard admin
menggunakan pola dari materi:

```text
base.html  →  admin/base_admin.html  →  admin/dashboard.html
```

- `base_admin.html` mewarisi `base.html`, lalu mengisi `content` dengan **layout dua kolom
  Bootstrap grid**: sidebar kiri (`col-md-3 col-lg-2 d-none d-md-block`) dan area konten kanan
  yang berisi `{% block judul %}` (topbar) serta `{% block admin_content %}`.
- `dashboard.html` mewarisi `base_admin.html` dan hanya mengisi kedua block tersebut.

Sidebar memakai `d-none d-md-block` sehingga **otomatis tersembunyi di layar HP**
(bagian dari uji responsif, requirement 5).

### 4.6 Data Python ke Template (Sintaks Jinja2 yang Dipakai)

| Sintaks | Kegunaan | Contoh di project |
|---|---|---|
| `{{ variabel }}` | Menampilkan nilai | `{{ profil.nama }}`, `{{ profil.ipk }}` di hero & kartu IPK |
| `{% for x in list %}` | Perulangan | `{% for mk in matakuliah %}` (baris tabel dashboard) |
| `{{ loop.index }}` | Nomor urut loop | Kolom "No" pada tabel dashboard |
| `{% if %} ... {% else %} ... {% endif %}` | Percabangan | `{% else %}` pada loop: pesan "Belum ada data" jika list kosong |
| Ekspresi kondisional inline | Nilai bergantung syarat | `{{ "Predikat Tertinggi" if mk.bobot == 4.0 else ("Baik Sekali" if mk.bobot >= 3.5 else "Baik") }}` |
| Filter `|lower` | Mengubah ke huruf kecil | `bg-nilai-{{ mk.nilai|lower }}` untuk warna badge nilai |
| `"{:.2f}".format()` | Format 2 angka desimal | `{{ "{:.2f}".format(mk.bobot) }}` |
| `{# komentar #}` | Komentar Jinja2 | Penjelasan di navbar & dashboard |

Potongan tabel dashboard (`admin/dashboard.html`) yang datanya dari list Python:

```html
{% for mk in matakuliah %}
<tr>
  <td>{{ loop.index }}</td>
  <td>{{ mk.kode }}</td>
  <td class="text-start">{{ mk.nama }}</td>
  <td>{{ mk.sks }}</td>
  <td><span class="badge badge-nilai bg-nilai-{{ mk.nilai|lower }}">{{ mk.nilai }}</span></td>
  <td>{{ "{:.2f}".format(mk.bobot) }}</td>
  <td>{{ "Predikat Tertinggi" if mk.bobot == 4.0 else ("Baik Sekali" if mk.bobot >= 3.5 else "Baik") }}</td>
</tr>
{% else %}
<tr><td colspan="7" class="text-center text-muted py-4">Belum ada data matakuliah.</td></tr>
{% endfor %}
```

### 4.7 Urutan CSS: Bootstrap Dulu, CSS Sendiri Sesudahnya

Di `<head>` `base.html`, Bootstrap CDN dipanggil **lebih dulu**, kemudian CSS milik
project sendiri. Jika urutannya terbalik, style custom akan **tertimpa Bootstrap**
(sesuai peringatan materi). Warna tema dipusatkan dengan **CSS variable** di `:root`:

```css
:root {
  --warna-utama: #1a1a2e;   /* navbar, footer, sidebar */
  --warna-aksen: #00b4d8;   /* hover, angka IPK, badge */
  --warna-teks: #1f2933;
}
```

---

## 5. Rangkuman Materi Pertemuan 12 — Forms di Flask

Bagian ini merangkum isi PPT *Pertemuan 12 — Forms di Flask* (Abdullah Faqih Septiyanto, S.Kom., M.Kom):
cara menerima data dari pengguna, memvalidasinya, dan menjawabnya dengan aman.

### 5.1 Anatomi Form HTML — Jembatan Browser ke Server

Form adalah cara utama pengguna mengirim data ke server. Empat atribut kuncinya:

| Atribut | Peran | Contoh |
|---|---|---|
| `action` | URL tujuan pengiriman data | `action="{{ url_for('kontak') }}"` |
| `method` | cara pengiriman: `GET` atau `POST` | `method="POST"` |
| `name` | **kunci** data yang dibaca Flask — **wajib ada** | `<input name="nama">` |
| `type` | jenis input | `text`, `email`, `password`, `number`, … |

> Poin penting materi: **tanpa atribut `name`, nilai input tidak ikut terkirim** ke server.

### 5.2 GET vs POST

| Aspek | GET | POST |
|---|---|---|
| Lokasi data | query string di URL (`/cari?q=kopi&hal=2`) | body request (tidak tampil di URL) |
| Terlihat / bisa di-bookmark | ya | tidak |
| Ukuran data | terbatas | bisa besar + file |
| Dibaca di Flask | `request.args` | `request.form` |
| Cocok untuk | pencarian, filter, pagination | login, pendaftaran, tambah/ubah data |

> Catatan materi: POST **tidak** berarti terenkripsi — data tetap terbaca bila tidak memakai
> HTTPS. Gunakan HTTPS saat deployment (dibahas pertemuan 13).

### 5.3 Objek `request`

Semua data yang dikirim browser dibaca lewat objek `request` dari Flask:

```python
from flask import request

nama = request.form["nama"]          # KeyError -> 400 jika tidak ada
nama = request.form.get("nama", "")  # aman: nilai default jika kosong
hobi = request.form.getlist("hobi")  # checkbox dengan banyak nilai
```

### 5.4 Satu Route, Dua Tugas (GET & POST)

Satu route menangani dua hal: **GET menampilkan form, POST memproses data**:

```python
@app.route("/kontak", methods=["GET", "POST"])
def kontak():
    if request.method == "POST":
        # baca request.form -> proses -> tampilkan hasil
        return render_template("terima_kasih.html", nama=nama)
    return render_template("kontak.html")
```

### 5.5 Pola Post/Redirect/Get (PRG)

Jika halaman hasil POST di-refresh, browser mengirim ulang data (pesanan bisa tercatat dua
kali). Pola PRG memecah alurnya:

```text
POST /kontak  →  form disubmit  →  proses data  →  redirect() 302  →  GET /kontak (aman di-refresh)
```

```python
if request.method == "POST":
    simpan_pesan(request.form)
    flash("Pesan berhasil dikirim!", "success")
    return redirect(url_for("kontak"))   # PRG
```

### 5.6 Flash Message

Pesan disimpan sementara di session dan **tampil sekali** di request berikutnya. Memerlukan
`SECRET_KEY` — untuk production jangan ditulis langsung di kode, simpan di environment variable:

```python
app.config["SECRET_KEY"] = "ganti-dengan-kunci-acak"
flash("Data berhasil disimpan", "success")
flash("Email sudah terdaftar", "danger")
```

Menampilkan semua pesan flash (kategori -> warna alert Bootstrap):

```html
{% with pesan = get_flashed_messages(with_categories=true) %}
  {% for kategori, isi in pesan %}
    <div class="alert alert-{{ kategori }}">{{ isi }}</div>
  {% endfor %}
{% endwith %}
```

### 5.7 Validasi Client-side vs Server-side

Aturan materi: **validasi client-side untuk kenyamanan, validasi server-side untuk keamanan —
gunakan keduanya**.

- **Client-side** (HTML5 / JavaScript): atribut `required`, `minlength`, `type="email"`,
  `pattern` — umpan balik cepat, tetapi **mudah dilewati** lewat DevTools, Postman, atau curl.
- **Server-side** (Flask): **wajib ada**, satu-satunya yang tidak bisa dilewati — menjaga
  keamanan dan integritas data, mencegah data rusak, SQL injection, dan XSS.

Teknik validasi manual: `strip()` (hapus spasi), `isdigit()` (cek angka), `re.match()` (pola teks).
Pola error dict: `errors` kosong → data valid; `errors` terisi → tampilkan ulang form + pesan.

### 5.8 Menampilkan Error & Mempertahankan Input

Saat validasi gagal: pesan tampil **di bawah field** (class Bootstrap `is-invalid` +
`invalid-feedback`) dan nilai yang sudah diketik diisi kembali agar pengguna tidak mengulang
dari awal:

```html
<input name="nama"
       class="form-control {{ 'is-invalid' if errors.nama }}"
       value="{{ request.form.get('nama', '') }}">
{% if errors.nama %}
  <div class="invalid-feedback">{{ errors.nama }}</div>
{% endif %}
```

### 5.9 Flask-WTF: Form Class, Validator, dan Proteksi CSRF

Flask-WTF mengintegrasikan library WTForms dengan Flask: form didefinisikan sebagai
**class Python**, validator siap pakai, proteksi CSRF otomatis, dan route menjadi lebih
ringkas. Instalasi (paket `email-validator` dibutuhkan agar validator `Email()` berfungsi):

```bash
pip install flask-wtf email-validator
pip freeze > requirements.txt
```

Form disimpan di file terpisah (misalnya `forms.py`) agar `app.py` tetap rapi:

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class DaftarForm(FlaskForm):
    nama = StringField("Nama", validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    umur = IntegerField("Umur", validators=[NumberRange(min=17, max=99)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    konfirmasi = PasswordField("Ulangi Password", validators=[
        EqualTo("password", message="Password tidak sama")])
    submit = SubmitField("Daftar")
```

Validator yang sering digunakan: `DataRequired` (wajib diisi), `Length` (batas karakter),
`Email` (format email), `NumberRange` (batas angka), `EqualTo` (kesamaan dua field),
`Regexp` (pola teks) — plus **validator kustom** lewat metode `validate_username(self, field)`
yang melempar `ValidationError`.

Di route, `validate_on_submit()` bernilai `True` **hanya jika request adalah POST dan semua
validator lolos, termasuk pengecekan token CSRF**:

```python
form = DaftarForm()
if form.validate_on_submit():
    flash(f"Selamat datang, {form.nama.data}!", "success")
    return redirect(url_for("index"))
return render_template("daftar.html", form=form)
```

Di template: `form.hidden_tag()` menyisipkan token CSRF, field dirender dengan class
Bootstrap (`form.nama(class="form-control")`), dan pesan error di-loop dari `form.nama.errors`.

### 5.10 CSRF: Cross-Site Request Forgery

CSRF adalah serangan yang **memanfaatkan sesi login korban** untuk mengirim request tanpa
sepengetahuannya (korban login di situs tujuan → membuka situs jahat berisi form tersembunyi →
request otomatis POST ke situs tujuan). Solusinya **token acak di setiap form**:

- Flask-WTF menyisipkan token melalui `form.hidden_tag()` atau `{{ form.csrf_token }}`.
- Server memeriksa token saat POST — situs lain tidak mengetahui token tersebut sehingga
  request palsu **ditolak (400 Bad Request)**.
- Untuk form HTML biasa tanpa FlaskForm, aktifkan `CSRFProtect(app)` dan tambahkan
  `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`.

### 5.11 Upload File dengan Form

Form upload wajib memiliki `enctype="multipart/form-data"`. Keamanannya: batasi ekstensi yang
diizinkan, bersihkan nama file dengan `secure_filename()`, dan batasi ukuran dengan
`MAX_CONTENT_LENGTH`:

```python
from werkzeug.utils import secure_filename
import os

app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB
IZIN = {"png", "jpg", "jpeg"}

f = request.files.get("foto")
if f and f.filename.rsplit(".", 1)[-1].lower() in IZIN:
    nama = secure_filename(f.filename)
    f.save(os.path.join("static/img/produk", nama))
    flash("Foto berhasil di-upload", "success")
```

---

## 6. Implementasi Tugas Individu 7 pada Project Ini

### 6.1 Dua Form Sesuai Soal (Requirement 1)

| Form | Lokasi | Untuk siapa | Field |
|---|---|---|---|
| **KontakForm** | halaman `/kontak` (menu navbar "Kontak") | **publik** — pengunjung mengirim pesan | nama, email, pesan |
| **MatakuliahForm** | dashboard `/admin` (kartu "Tambah Matakuliah") | **admin** — menambah data | kode, nama, sks, nilai (select) |

### 6.2 Validator (Requirement 2 — 5 jenis berbeda, melebihi minimal 4)

Jenis validator yang dipakai: **DataRequired, Length, Email, Regexp, NumberRange**:

| Field | Validator | Aturan |
|---|---|---|
| Kontak: nama | `DataRequired` + `Length(3, 50)` | wajib, 3–50 karakter |
| Kontak: email | `DataRequired` + `Email` | wajib, format email valid |
| Kontak: pesan | `DataRequired` + `Length(10, 500)` | wajib, 10–500 karakter |
| Admin: kode | `DataRequired` + `Length(5, 8)` + `Regexp` | wajib, 5–8 karakter, pola huruf+angka (contoh `SIF107`) |
| Admin: nama | `DataRequired` + `Length(3, 60)` | wajib, 3–60 karakter |
| Admin: sks | `DataRequired` + `NumberRange(1, 6)` | wajib, angka 1–6 |
| Admin: nilai | `DataRequired` (SelectField) | pilihan A/AB/B/BC/C/D/E |

### 6.3 CSRF Aktif di Semua Form (Requirement 3)

Proteksinya **dua lapis**: (1) setiap FlaskForm menyisipkan token lewat `form.hidden_tag()`;
(2) `CSRFProtect(app)` menolak **semua** request POST tanpa token valid dengan **400 Bad
Request** — dibuktikan uji otomatis (Bagian 6.8). `SECRET_KEY` diambil dari environment
variable dengan fallback nilai dev, sesuai peringatan materi untuk production.

### 6.4 Error di Bawah Field + Input Tetap Terisi (Requirement 4)

Template menambahkan class `is-invalid` pada field yang bermasalah dan menampilkan pesan di
`<div class="invalid-feedback">` tepat di bawahnya. WTForms otomatis mengisi ulang nilai yang
dikirim, sehingga **input yang benar tetap terisi** — bukti: screenshot `kontak-error.png`
(nama "B" dan pesan "pendek" tetap tampil di field ketika validasi gagal).

> Jebakan yang ditemui: `{{ }}` **tidak boleh disarangkan di dalam string argumen Jinja**.
> Menulis `class="form-control{{ ' is-invalid' if ... }}"` membuat teks Jinja dirender apa
> adanya. Solusinya konkatenasi: `class="form-control" + (" is-invalid" if form.nama.errors else "")`.

### 6.5 Pola PRG + Flash Message (Requirement 5)

Kedua route memakai pola yang sama:

```text
POST (valid)  →  flash("... berhasil ...")  →  redirect() 302  →  GET  →  alert hijau tampil sekali
POST (gagal)  →  form tampil ulang + error di bawah field + input tetap terisi (tanpa redirect)
```

Blok flash dirender di `base.html` sehingga muncul di semua halaman; kategori flash menentukan
warna alert (`success` hijau, `danger` merah, dst.). Untuk form admin, matakuliah baru
ditambahkan ke list `data_matakuliah` dengan bobot dari mapping `BOBOT_NILAI`, sehingga
**stat card dan tabel terhitung ulang otomatis** (contoh uji: 7 → 8 matakuliah, 20 → 23 SKS,
IP 3.55 → 3.54).

### 6.6 Bootstrap Form Styling (Requirement 6)

Semua input memakai `form-control`, select memakai `form-select`, label `form-label`, error
`is-invalid` + `invalid-feedback`, tombol `btn-primary` / `btn-success`, dibungkus `card` —
tampilan form konsisten dengan tema website dan tetap responsif di layar HP.

### 6.7 Perbandingan Form Tugas 2 (jQuery) vs Form Tugas 7 (Flask-WTF)

| Aspek | Form Tugas 2 (halaman `/nilai`) | Form Tugas 7 (`/kontak` & `/admin`) |
|---|---|---|
| Validasi | JavaScript client-side | Flask-WTF **server-side** |
| Keamanan | tanpa token (dapat dilewati) | **token CSRF + validator server** |
| Penyimpanan data | array JavaScript (hilang saat refresh) | list Python di `app.py` (milik server) |
| Setelah submit | tetap di halaman (`preventDefault`) | **redirect PRG + flash** |
| Pesan error | class ditambahkan JavaScript | ditentukan validator, dirender Jinja2 |

### 6.8 Hasil Uji Otomatis (34 cek, lolos semua)

Uji menggunakan Flask test client membuktikan: GET semua halaman berstatus 200; POST tanpa
token CSRF → **400**; POST isian salah → form tampil ulang dengan error di bawah field dan
input tetap terisi; POST valid → **302 redirect** lalu flash tampil **sekali**; matakuliah
baru (SIF107) masuk tabel dan stat card terhitung ulang; panjang/kode/SKS di luar batas
ditolak pesan validator yang sesuai.

---

## 7. Penjelasan `app.py`

### 7.1 Data (list Python — sementara, diganti database di pertemuan 14)

| Variabel | Tipe | Isi |
|---|---|---|
| `profil` | `dict` | nama, NBI, prodi, fakultas, kampus, IPK, predikat |
| `data_matakuliah` | `list of dict` | 7 matakuliah: `kode`, `nama`, `sks`, `nilai`, `bobot` |
| `data_semester` | `list of dict` | rekap 3 semester: `sks`, `ip` (semester 3 `None` karena sedang berjalan), `ipk` |
| `BOBOT_NILAI` | `dict` | mapping nilai huruf → bobot (A=4.00, AB=3.50, B=3.00, BC=2.50, C=2.00, D=1.00, E=0.00) — dipakai form tambah matakuliah (Tugas 7) |

### 7.2 Fungsi Bantu (pengolahan list Python)

| Fungsi | Penjelasan |
|---|---|
| `hitung_total_sks(daftar)` | Menjumlahkan seluruh SKS dengan perulangan `for` |
| `hitung_ip(daftar)` | IP = total (bobot × SKS) dibagi total SKS (rata-rata tertimbang) |
| `hitung_statistik()` | Menyusun 4 stat card dashboard langsung dari list Python: jumlah matakuliah (`len()`), total SKS, IP semester ini (`"{:.2f}".format()`), IPK kumulatif (diambil dari semester terakhir `data_semester[-1]`) |

Ketiga fungsi ini adalah **versi Python** dari fungsi JavaScript yang lama
(`hitungTotalSks`, `hitungIP` di `script.js`) — datanya kini diolah di sisi server.

### 7.3 Daftar Route

| Route | Fungsi Python | Method | Template yang dirender | Data dikirim |
|---|---|---|---|---|
| `/` | `index()` | GET | `index.html` | `profil` |
| `/nilai` | `nilai()` | GET | `nilai.html` | — (tabel dirender JavaScript) |
| `/ipk` | `ipk()` | GET | `ipk.html` | `profil` |
| `/kontak` | `kontak()` | **GET + POST** | `kontak.html` | `profil`, `form` (KontakForm) — Tugas 7 |
| `/admin` | `admin_dashboard()` | **GET + POST** | `admin/dashboard.html` | `profil`, `statistik`, `matakuliah`, `form` (MatakuliahForm) — Tugas 7 |

Menjalankan `python app.py` dengan `debug=True` membuat server otomatis reload
setiap kali `app.py` diubah.

---

## 8. Penjelasan Tiap Template

| File | Isi & Peran |
|---|---|
| `templates/base.html` | Kerangka induk: `<head>` (Bootstrap CSS CDN → Bootstrap Icons → CSS sendiri via `url_for`), `{% include %}` navbar, **blok flash message** (Tugas 7 — `get_flashed_messages`), `{% block content %}`, footer sosial media, **modal kontak** (validasi form), lalu urutan script: Bootstrap bundle → **jQuery 3.7.1** → `script.js` |
| `templates/partials/navbar.html` | Navbar `sticky-top` dengan menu dinamis (termasuk menu **Kontak** ke halaman `/kontak`) + tombol Kirim Pesan (membuka modal) + tombol Mode Gelap (`#tombolMode`) |
| `templates/kontak.html` | **Tugas 7**: form kontak publik (KontakForm) — `form.hidden_tag()` (token CSRF), label + `form-control` per field, error di `invalid-feedback` di bawah field, catatan proteksi CSRF di footer kartu |
| `templates/index.html` | Beranda: hero (foto profil, nama, NBI, badge prodi & fakultas dari `{{ profil }}`) + 3 kartu info (Nama & NBI, Program Studi, Prestasi Akademik) dengan animasi `.reveal` |
| `templates/nilai.html` | Halaman nilai: input pencarian `#inputCari`, filter `#pilihNilai`, tabel dengan `<tbody id="isiTabelNilai">` yang **kosong** (baris dirender `script.js` dari array of object), ringkasan `#infoStatistik`, dan form tambah matakuliah dengan validasi `.is-invalid` |
| `templates/ipk.html` | Kartu IPK besar (angka dari `{{ profil.ipk }}` + progress bar) + tabel rekap semester `<tbody id="isiTabelSemester">` (dirender `script.js`) |
| `templates/admin/base_admin.html` | Layout dashboard: sidebar navigasi (menggunakan `url_for` + class `active` dari `request.endpoint`), topbar berisi `{% block judul %}` + badge nama admin |
| `templates/admin/dashboard.html` | 4 stat card via `{% for s in statistik %}` + **grid dua kolom**: tabel data matakuliah (kiri) dan **form tambah matakuliah MatakuliahForm** (kanan, Tugas 7) dengan `hidden_tag`, error per field, dan select nilai huruf |

---

## 9. Penjelasan Folder `static/`

### `static/css/style.css`

- CSS variable tema (`:root`), styling navbar, hero + foto profil, ikon kartu gradien
  (`ikon-biru`, `ikon-cyan`, `ikon-hijau`), `judul-section`, `tabel-custom`,
  `badge-nilai` + warna per huruf nilai (`bg-nilai-a`, `bg-nilai-ab`, `bg-nilai-b`),
  `kartu-ipk` + `angka-ipk`, `badge-custom`, animasi `.reveal` / `.reveal.aktif`.
- **Mode gelap**: seluruh varian `body.dark-mode ...` (kartu, tabel, form, sidebar).
- **Dashboard admin**: `.sidebar`, `.sidebar a.active`, `.sidebar .sidebar-judul`,
  dan efek hover `.card.stat-hover`.

### `static/js/script.js`

Satu file JS dipakai **empat halaman Flask sekaligus**, sehingga setiap fitur dipasang
hanya jika elemennya ada di halaman itu (cek dengan fungsi bantu `ada(id)`).

- **Bagian 1 (vanilla JS)**: array of object `dataMatakuliah` (7 MK + `id` unik) dan
  `dataSemester`, fungsi `hitungTotalSks`, `hitungIP`, `cariMatakuliah` (filter +
  `includes`), `filterNilai`, `tentukanPredikat`, serta output `console.table()` untuk
  screenshot Bagian 1.
- **Bagian 2 (DOM + jQuery)** di dalam `$(function () { ... })` (document ready):
  `renderTabel()` dengan `createElement`, `perbaruiStatistik()` dan `renderSemester()`
  dengan template literal, pencarian/filter realtime (event `input` dan `change`),
  form tambah (`preventDefault()` + validasi `classList.add("is-invalid")`),
  mode gelap (`classList.toggle` + `localStorage` agar tema konsisten antar halaman
  Flask), validasi modal kontak, dan animasi reveal `IntersectionObserver`.

### `static/img/`

Foto profil dengan nama file `IMG_20260728_090150.jpg` (sesuai pemanggilan
`url_for` di `index.html`). Jika foto belum ada, folder berisi petunjuk
`_TARUH_FOTO_DISINI.txt`.

---

## 10. Alur Kerja Aplikasi (satu request)

```text
BROWSER                     FLASK (app.py)                    JINJA2
  |                                                                |
  | GET http://127.0.0.1:5000/admin                                |
  |----------------------------------------------------------->    |
  |                            @app.route("/admin") cocok          |
  |                            hitung_statistik() menghitung       |
  |                            render_template("admin/dashboard")  |
  |                                       |                        |
  |                                       |-- gabungkan base.html  |
  |                                       |   + base_admin.html    |
  |                                       |   + dashboard.html,    |
  |                                       |   ganti semua {{ }}    |
  |                                       |   dan {% %} jadi HTML  |
  |<-----------------------------------------------------------|   |
  | HTML utuh ditampilkan                                           |
  | lalu browser memuat:                                            |
  |   /static/css/style.css   (via url_for)                         |
  |   /static/js/script.js    (via url_for)                         |
  | script.js memasang event: cari, filter, hapus (jQuery),         |
  | form tambah, mode gelap, reveal                                 |
```

Jadi pembagian tugasnya jelas: **Python/Flask** menyiapkan data dan merangkai HTML
di server; **JavaScript/jQuery** mengambil alih setelah halaman sampai ke browser
(interaktivitas), persis seperti materi "Static Files" dan pola dashboard admin.

Untuk halaman form (Tugas 7), alurnya diperpanjang satu langkah: browser mengirim
**POST** berisi data form + token CSRF → Flask memvalidasi lewat `validate_on_submit()` →
berhasil: `flash()` + `redirect()` (PRG) → gagal: form tampil ulang dengan error
(lihat Bagian 6.5).

---

## 11. Fitur Interaktif Tugas Individu 2 yang Tetap Berjalan

| No | Fitur | Konsep | Lokasi |
|---|---|---|---|
| 1 | Pencarian matakuliah realtime | event `input` + `filter` + `includes` | `script.js` (halaman `/nilai`) |
| 2 | Filter nilai huruf (A / AB / B) | event `change` + fungsi `filterNilai` | `script.js` |
| 3 | Hapus baris dengan dialog konfirmasi | **jQuery event delegation** `$("#isiTabelNilai").on("click", ".btn-hapus", ...)`, `confirm()`, traversing `closest("tr")`, efek `fadeOut` lalu render ulang | `script.js` |
| 4 | Form tambah matakuliah + validasi | `preventDefault()`, `classList.add("is-invalid")` (tanpa style inline), push ke array of object | `script.js` |
| 5 | Pesan sukses animasi | **jQuery chaining** `removeClass().hide().fadeIn().delay().fadeOut()` | `script.js` |
| 6 | Mode gelap | `classList.toggle` + `localStorage` (konsisten antar halaman Flask) | `script.js` + `style.css` |
| 7 | Modal kontak + validasi email | Bootstrap modal + validasi manual (`@` dan `.`) | `base.html` + `script.js` |
| 8 | Animasi reveal saat scroll | `IntersectionObserver` | `script.js` + `style.css` |

> Catatan: karena website kini **multi-halaman**, satu `script.js` harus cek dulu apakah
> elemen targetnya ada di halaman tersebut (fungsi `ada()`), agar tidak error saat dibuka
> di halaman yang tidak punya tabel nilai.

---

## 12. Cara Menjalankan

```bash
# 1. Masuk folder project
cd flask-profil-mahasiswa

# 2. (Opsional tapi disarankan) buat & aktifkan virtual environment
python -m venv venv
venv\Scripts\activate          # Windows (PowerShell)
# source venv/bin/activate     # Linux / macOS

# 3. Install dependensi
pip install -r requirements.txt

# 4. Jalankan aplikasi
python app.py
```

Lalu buka **http://127.0.0.1:5000** di browser. Halaman yang tersedia:

| Halaman | Alamat |
|---|---|
| Beranda | http://127.0.0.1:5000/ |
| Nilai Matakuliah | http://127.0.0.1:5000/nilai |
| IPK | http://127.0.0.1:5000/ipk |
| Dashboard Admin | http://127.0.0.1:5000/admin |
| Kontak (form publik) | http://127.0.0.1:5000/kontak |

> Jangan lupa menaruh foto profil di `static/img/IMG_20260728_090150.jpg`.

**Masalah yang sering terjadi:**

| Gejala | Penyebab & solusi |
|---|---|
| `$ is not defined` di console | jQuery belum termuat sebelum `script.js` — urutan di `base.html` sudah benar: Bootstrap → jQuery → `script.js` |
| Style custom tidak muncul / tertimpa Bootstrap | CSS sendiri harus dipanggil **setelah** Bootstrap CDN |
| CSS/JS 404 | File tidak ada di `static/`, atau path ditulis manual — selalu pakai `url_for` |
| Port 5000 dipakai | Matikan proses lain, atau ubah `app.run(debug=True, port=5001)` |
| Mengubah template tidak berubah | Tekan Ctrl+F5 (cache browser); dengan `debug=True` template otomatis reload |
| **400 Bad Request saat submit form** | Token CSRF hilang/kadaluarsa — tekan F5 agar token baru dibuat, pastikan `form.hidden_tag()` masih ada di form |

---

## 13. Uji Responsif (Requirement 5)

1. Jalankan aplikasi, tekan `F12` (DevTools).
2. Tekan `Ctrl + Shift + M` (device toolbar / mode layar HP).
3. Pilih perangkat, misalnya *iPhone SE* atau *Samsung Galaxy*.
4. Periksa: navbar menyusut menjadi tombol hamburger, sidebar admin **tersembunyi**
   (`d-none d-md-block`), stat card menjadi 2 kolom (`col-6 col-lg-3`), tabel bisa
   digeser (`table-responsive`).
5. Screenshot tampilan **desktop** dan **mobile** untuk dikumpulkan ke LMS Elitag.

---

## 14. Push ke GitHub & Pengumpulan

```bash
git init
git add .
git commit -m "Tugas Individu 6 & 7: integrasi Flask + form Flask-WTF (CSRF, PRG, flash)"
git branch -M main
git remote add origin https://github.com/DafiDeo/<nama-repo>.git
git push -u origin main
```

Dikumpulkan ke LMS Elitag: **link repository** + **laporan Word Tugas Individu 7 sebagai
pengganti video demo (maks. 3 menit)** + **screenshot tampilan desktop & mobile**.

> Catatan: aplikasi Flask **tidak bisa dijalankan di GitHub Pages** (Pages hanya hosting
> file statis). Yang dikumpulkan adalah link repository-nya, bukan link Pages.

---

## 15. Checklist Pemenuhan Soal (Tugas Individu 6 & 7)

| No | Requirement (sesuai soal) | Implementasi | File bukti |
|----|---------------------------|--------------|------------|
| 1 | Semua HTML di `templates/` + template inheritance (`base.html`) | 7 template, semua `extends "base.html"`; dashboard memakai nested inheritance `base.html → admin/base_admin.html → admin/dashboard.html` | `templates/` |
| 2 | CSS, JS, gambar di `static/` + dipanggil dengan `url_for` | CSS, JS, foto profil dipanggil via `url_for('static', filename=...)` di `base.html` dan `index.html` | `base.html`, `index.html`, `static/` |
| 3 | Navbar dengan menu aktif dinamis | Partial `navbar.html` + `{% include %}`, menu dari `{% set %}` + loop, class `active` dari `request.endpoint` | `templates/partials/navbar.html` |
| 4 | Dashboard admin: sidebar, minimal 3 stat card, tabel data dari list Python | Sidebar (`d-none d-md-block`), **4 stat card** dihitung fungsi `hitung_statistik()` dari list Python, tabel `data_matakuliah` dengan loop Jinja2 + `loop.index` + ekspresi kondisional | `app.py`, `templates/admin/` |
| 5 | Tampilan responsif (uji di layar HP) | Bootstrap grid + `d-none d-md-block`, `col-6 col-lg-3`, `table-responsive` — uji via DevTools device toolbar (Bagian 13) | `admin/base_admin.html`, `dashboard.html` |

Tambahannya sesuai instruksi soal: push ke GitHub dan kumpulkan link + screenshot
desktop & mobile di LMS Elitag, serta dikerjakan **secara mandiri** (kesamaan kode/desain
antarmahasiswa menyebabkan nilai dibagi 2).

**Checklist Tugas Individu 7 (Pertemuan 12):**

| No | Requirement (sesuai soal) | Implementasi | File bukti |
|----|---------------------------|--------------|------------|
| 1 | Minimal 2 form: kontak/pemesanan (publik) + tambah data (dashboard admin) | **KontakForm** di `/kontak` (publik) + **MatakuliahForm** di `/admin` | `forms.py`, `kontak.html`, `admin/dashboard.html` |
| 2 | Flask-WTF dengan minimal 4 jenis validator berbeda | **5 jenis**: `DataRequired`, `Length`, `Email`, `Regexp`, `NumberRange` | `forms.py` |
| 3 | Token CSRF aktif pada semua form | `form.hidden_tag()` + `CSRFProtect(app)`; POST tanpa token ditolak **400** (uji otomatis) | `app.py`, kedua template form |
| 4 | Error di bawah field, input yang benar tetap terisi | `is-invalid` + `invalid-feedback` per field; WTForms mengisi ulang nilai yang dikirim | `kontak.html`, `admin/dashboard.html`, screenshot `kontak-error.png` |
| 5 | Pola PRG dan flash message | `flash()` + `redirect()` di kedua route; alert Bootstrap di `base.html`; matakuliah baru langsung masuk tabel + stat card | `app.py`, screenshot `kontak-sukses.png`, `admin-sukses.png` |
| 6 | Form ditata dengan Bootstrap | `form-control`, `form-select`, `form-label`, `is-invalid`, `btn`, dibungkus `card` | `kontak.html`, `admin/dashboard.html` |

Sesuai instruksi penutup soal: push ke GitHub, lalu kumpulkan link repository dan
**laporan hasil pekerjaan (pengganti video demo maks. 3 menit)** ke LMS Elitag.

---

## 16. Catatan Pembelajaran

- **Pemisahan peran**: Python (server) mengurus data dan perhitungan IP/SKS;
  JavaScript (browser) mengurus interaktivitas. Keduanya tidak saling menggantikan.
- **`url_for` dengan nama endpoint** membuat link tidak rusak walau URL route diubah.
- **Template inheritance** menghilangkan duplikasi head/navbar/footer/modal —
  mengganti satu bagian cukup di `base.html`.
- **Satu JS untuk banyak halaman**: wajib cek ketersediaan elemen (`ada()`) sebelum
  memasang event, karena Flask mengirim satu halaman per request.
- **Mode gelap antar halaman**: tanpa `localStorage`, tema kembali terang setiap pindah
  halaman Flask (karena tiap halaman = request baru); dengan `localStorage` preferensi
  tetap tersimpan.
- Data masih berupa **list Python** dan dashboard masih tanpa proteksi login — sesuai
  materi, akan ditingkatkan dengan **database (pertemuan 14)** dan **otorisasi
  (pertemuan 13)**.
- **Rantai validator berhenti di error pertama**: `sks=0` gagal di `DataRequired`
  (nilai 0 dianggap kosong) sehingga pesan `NumberRange` tidak sempat muncul — untuk
  memaksa NumberRange berjalan, nilai harus "ada" dulu (misal 99).
- **PRG mencegah submit ganda**: tanpa `redirect()`, menekan F5 setelah submit mengirim
  ulang POST; dengan redirect 302, refresh hanya mengulang GET yang aman.
- **Flash = sekali tampil**: `get_flashed_messages()` mengonsumsi pesan; setelah dirender,
  request berikutnya sudah tidak memuatnya — cocok untuk notifikasi hasil aksi.

---

© 2026 — Dafi Deo Ananda Nurrokhim · NBI 1482500040 · PSBW / FTEIC / Untag Surabaya
