# Website Profil Mahasiswa — Versi Flask

**Tugas Individu 6 — Pengembangan Situs Web (PSBW)**

Pertemuan 11: Integrasi HTML & CSS dengan Flask.

## Profil

| Keterangan | Data |
|---|---|
| Nama | Dafi Deo |
| NBI | 0040 |
| Program Studi | S1 Sistem dan Teknologi Informasi |
| Fakultas | FTEIC |
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
| Cara menjalankan | buka file HTML langsung di browser | `python app.py` lalu buka `http://127.0.0.1:5000` |

Yang **tidak berubah**: tampilan, komponen Bootstrap, dan seluruh fitur JavaScript/jQuery
dari Tugas Individu 2 (lihat Bagian 9).

---

## 3. Struktur Folder Project

Struktur mengikuti pola standar Flask pada materi (folder `static/` dan `templates/`):

```text
flask-profil-mahasiswa/
│
├── app.py                      # Aplikasi Flask: data (list Python), fungsi hitung, 4 route
├── requirements.txt            # Dependensi: Flask
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
    ├── base.html               # Template INDUK: <head>, navbar, footer, modal kontak, script
    ├── index.html              # Halaman Beranda : hero + kartu profil
    ├── nilai.html              # Halaman Nilai    : tabel interaktif + form tambah
    ├── ipk.html                # Halaman IPK     : kartu IPK + rekap semester
    ├── partials/
    │   └── navbar.html         # Navbar (partial) dengan menu aktif dinamis
    └── admin/
        ├── base_admin.html     # Layout dashboard: sidebar + topbar (mewarisi base.html)
        └── dashboard.html      # Stat card + tabel data dari list Python
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

## 5. Penjelasan `app.py`

### 5.1 Data (list Python — sementara, diganti database di pertemuan 14)

| Variabel | Tipe | Isi |
|---|---|---|
| `profil` | `dict` | nama, NBI, prodi, fakultas, kampus, IPK, predikat |
| `data_matakuliah` | `list of dict` | 7 matakuliah: `kode`, `nama`, `sks`, `nilai`, `bobot` |
| `data_semester` | `list of dict` | rekap 3 semester: `sks`, `ip` (semester 3 `None` karena sedang berjalan), `ipk` |

### 5.2 Fungsi Bantu (pengolahan list Python)

| Fungsi | Penjelasan |
|---|---|
| `hitung_total_sks(daftar)` | Menjumlahkan seluruh SKS dengan perulangan `for` |
| `hitung_ip(daftar)` | IP = total (bobot × SKS) dibagi total SKS (rata-rata tertimbang) |
| `hitung_statistik()` | Menyusun 4 stat card dashboard langsung dari list Python: jumlah matakuliah (`len()`), total SKS, IP semester ini (`"{:.2f}".format()`), IPK kumulatif (diambil dari semester terakhir `data_semester[-1]`) |

Ketiga fungsi ini adalah **versi Python** dari fungsi JavaScript yang lama
(`hitungTotalSks`, `hitungIP` di `script.js`) — datanya kini diolah di sisi server.

### 5.3 Daftar Route

| Route | Fungsi Python | Template yang dirender | Data dikirim |
|---|---|---|---|
| `/` | `index()` | `index.html` | `profil` |
| `/nilai` | `nilai()` | `nilai.html` | — (tabel dirender JavaScript) |
| `/ipk` | `ipk()` | `ipk.html` | `profil` |
| `/admin` | `admin_dashboard()` | `admin/dashboard.html` | `profil`, `statistik`, `matakuliah` |

Menjalankan `python app.py` dengan `debug=True` membuat server otomatis reload
setiap kali `app.py` diubah.

---

## 6. Penjelasan Tiap Template

| File | Isi & Peran |
|---|---|
| `templates/base.html` | Kerangka induk: `<head>` (Bootstrap CSS CDN → Bootstrap Icons → CSS sendiri via `url_for`), `{% include %}` navbar, `{% block content %}`, footer sosial media, **modal kontak** (validasi form), lalu urutan script: Bootstrap bundle → **jQuery 3.7.1** → `script.js` |
| `templates/partials/navbar.html` | Navbar `sticky-top` dengan menu dinamis + tombol Kontak (membuka modal) + tombol Mode Gelap (`#tombolMode`) |
| `templates/index.html` | Beranda: hero (foto profil, nama, NBI, badge prodi & fakultas dari `{{ profil }}`) + 3 kartu info (Nama & NBI, Program Studi, Prestasi Akademik) dengan animasi `.reveal` |
| `templates/nilai.html` | Halaman nilai: input pencarian `#inputCari`, filter `#pilihNilai`, tabel dengan `<tbody id="isiTabelNilai">` yang **kosong** (baris dirender `script.js` dari array of object), ringkasan `#infoStatistik`, dan form tambah matakuliah dengan validasi `.is-invalid` |
| `templates/ipk.html` | Kartu IPK besar (angka dari `{{ profil.ipk }}` + progress bar) + tabel rekap semester `<tbody id="isiTabelSemester">` (dirender `script.js`) |
| `templates/admin/base_admin.html` | Layout dashboard: sidebar navigasi (menggunakan `url_for` + class `active` dari `request.endpoint`), topbar berisi `{% block judul %}` + badge nama admin |
| `templates/admin/dashboard.html` | 4 stat card via `{% for s in statistik %}` (jumlah MK, total SKS, IP, IPK) + tabel data matakuliah via `{% for mk in matakuliah %}` dengan `loop.index`, badge warna nilai, dan kolom keterangan (ekspresi kondisional) |

---

## 7. Penjelasan Folder `static/`

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

## 8. Alur Kerja Aplikasi (satu request)

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

---

## 9. Fitur Interaktif Tugas Individu 2 yang Tetap Berjalan

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

## 10. Cara Menjalankan

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

> Jangan lupa menaruh foto profil di `static/img/IMG_20260728_090150.jpg`.

**Masalah yang sering terjadi:**

| Gejala | Penyebab & solusi |
|---|---|
| `$ is not defined` di console | jQuery belum termuat sebelum `script.js` — urutan di `base.html` sudah benar: Bootstrap → jQuery → `script.js` |
| Style custom tidak muncul / tertimpa Bootstrap | CSS sendiri harus dipanggil **setelah** Bootstrap CDN |
| CSS/JS 404 | File tidak ada di `static/`, atau path ditulis manual — selalu pakai `url_for` |
| Port 5000 dipakai | Matikan proses lain, atau ubah `app.run(debug=True, port=5001)` |
| Mengubah template tidak berubah | Tekan Ctrl+F5 (cache browser); dengan `debug=True` template otomatis reload |

---

## 11. Uji Responsif (Requirement 5)

1. Jalankan aplikasi, tekan `F12` (DevTools).
2. Tekan `Ctrl + Shift + M` (device toolbar / mode layar HP).
3. Pilih perangkat, misalnya *iPhone SE* atau *Samsung Galaxy*.
4. Periksa: navbar menyusut menjadi tombol hamburger, sidebar admin **tersembunyi**
   (`d-none d-md-block`), stat card menjadi 2 kolom (`col-6 col-lg-3`), tabel bisa
   digeser (`table-responsive`).
5. Screenshot tampilan **desktop** dan **mobile** untuk dikumpulkan ke LMS Elitag.

---

## 12. Push ke GitHub & Pengumpulan

```bash
git init
git add .
git commit -m "Tugas Individu 6: integrasi website profil ke Flask"
git branch -M main
git remote add origin https://github.com/DafiDeo/<nama-repo>.git
git push -u origin main
```

Dikumpulkan ke LMS Elitag: **link repository** + **screenshot tampilan desktop & mobile**.

> Catatan: aplikasi Flask **tidak bisa dijalankan di GitHub Pages** (Pages hanya hosting
> file statis). Yang dikumpulkan adalah link repository-nya, bukan link Pages.

---

## 13. Checklist Pemenuhan Soal (Tugas Individu 6)

| No | Requirement (sesuai soal) | Implementasi | File bukti |
|----|---------------------------|--------------|------------|
| 1 | Semua HTML di `templates/` + template inheritance (`base.html`) | 7 template, semua `extends "base.html"`; dashboard memakai nested inheritance `base.html → admin/base_admin.html → admin/dashboard.html` | `templates/` |
| 2 | CSS, JS, gambar di `static/` + dipanggil dengan `url_for` | CSS, JS, foto profil dipanggil via `url_for('static', filename=...)` di `base.html` dan `index.html` | `base.html`, `index.html`, `static/` |
| 3 | Navbar dengan menu aktif dinamis | Partial `navbar.html` + `{% include %}`, menu dari `{% set %}` + loop, class `active` dari `request.endpoint` | `templates/partials/navbar.html` |
| 4 | Dashboard admin: sidebar, minimal 3 stat card, tabel data dari list Python | Sidebar (`d-none d-md-block`), **4 stat card** dihitung fungsi `hitung_statistik()` dari list Python, tabel `data_matakuliah` dengan loop Jinja2 + `loop.index` + ekspresi kondisional | `app.py`, `templates/admin/` |
| 5 | Tampilan responsif (uji di layar HP) | Bootstrap grid + `d-none d-md-block`, `col-6 col-lg-3`, `table-responsive` — uji via DevTools device toolbar (Bagian 11) | `admin/base_admin.html`, `dashboard.html` |

Tambahannya sesuai instruksi soal: push ke GitHub dan kumpulkan link + screenshot
desktop & mobile di LMS Elitag, serta dikerjakan **secara mandiri** (kesamaan kode/desain
antarmahasiswa menyebabkan nilai dibagi 2).

---

## 14. Catatan Pembelajaran

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

---

© 2026 — Dafi Deo · NBI 0040 · PSBW / FTEIC / Untag Surabaya