# 🚀 Sewu Scrap - Google Maps Scraper Web App

<p align="left">
    <img src="static/logo-bps.png" alt="Logo BPS" width="120">
</p>

**Sewu Scrap** adalah aplikasi web berbasis Flask untuk melakukan scraping data tempat dari Google Maps secara otomatis dan menyimpannya ke file CSV. Dikembangkan oleh Badan Pusat Statistik Kabupaten Pringsewu untuk mendukung pengumpulan data spasial secara efisien.

---

## ✨ Fitur Utama

- **Antarmuka Web Modern**: Input kata kunci pencarian dan nama file output dengan tampilan profesional.
- **Scraping Otomatis**: Mengambil data nama tempat, rating, jumlah ulasan, alamat, URL Google Maps, latitude, dan longitude.
- **Ekspor ke CSV**: Hasil scraping langsung dapat diunduh dalam format CSV.
- **Dukungan Bahasa Indonesia**: UI dan output berbahasa Indonesia.
- **Mudah Digunakan**: Cukup jalankan satu perintah/batch file, aplikasi siap digunakan!

---

## 📸 Tampilan Aplikasi

![Tampilan Web App](static/tampilan.png)

---

## ⚡️ Cara Instalasi & Menjalankan

### 1. **Clone Repository**

```sh
git clone https://github.com/aryasetiap/data-scraper-gmaps.git
cd data-scraper-gmaps
```

### 2. **Jalankan Batch File (Windows)**

Cukup **double-click** file [`(app)_Scraper.bat`](<./(app)_Scraper.bat>)  
atau jalankan lewat terminal/cmd:

```sh
(app)_Scraper.bat
```

Batch file ini akan:

- Mengecek Python & pip
- Menginstal dependencies otomatis
- Membuka aplikasi di browser

### 3. **Akses Aplikasi**

Buka browser ke [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📝 Penggunaan

1. Masukkan **kata kunci pencarian** (misal: `Pasar di Kabupaten Pringsewu`)
2. Tentukan **nama file output** (opsional, default: `hasil_scrape.csv`)
3. Klik **Mulai Scraping**
4. Setelah selesai, klik **Download Hasil** untuk mengunduh file CSV

---

## 🛠️ Struktur Project

```
.
├── app.py                  # Aplikasi web utama (Flask)
├── code_scraper_test.py    # Script untuk scraping Google Maps
├── requirements.txt        # Daftar dependencies Python
├── (app)_Scraper.bat       # Batch file untuk menjalankan aplikasi (Windows)
├── static/
│   ├── logo-bps.png        # Logo BPS
│   └── tampilan.png        # Gambar tampilan aplikasi
├── hasil_scrape.csv        # Contoh hasil scraping (opsional)
└── README.md               # Dokumentasi proyek
```

---

## 📦 Dependencies

- Flask
- Selenium
- BeautifulSoup4
- Pandas
- webdriver_manager

Instalasi otomatis saat menjalankan batch file.

---

## ⚠️ Disclaimer

> **PERINGATAN:**  
> Script ini hanya untuk kebutuhan riset dan ilmu pengetahuan.  
> Penggunaan data hasil scraping harus mematuhi kebijakan dan hukum yang berlaku.

---

## 👨‍💻 Pengembang

- **Arya Setia Pratama**  
   [GitHub](https://github.com/aryasetiap) | [Badan Pusat Statistik Kabupaten Pringsewu](https://pringsewukab.bps.go.id/)

---

## ⭐️ Lisensi

MIT License

---

> &copy; 2025 Badan Pusat Statistik Kabupaten | Arya Setia Pratama
