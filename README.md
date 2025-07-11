﻿# 🚀 Sewu Scrap - Google Maps Scraper Web App

<p align="left">
    <img src="static/logo-bps.png" alt="Logo BPS" width="120">
</p>

**Sewu Scrap** adalah aplikasi web berbasis Flask untuk melakukan scraping data tempat dari Google Maps secara otomatis dan menyimpannya ke file CSV. Dikembangkan oleh Badan Pusat Statistik Kabupaten Pringsewu untuk mendukung pengumpulan data spasial secara efisien.

---

## ✨ Fitur Utama

- **Antarmuka Web Modern**: Input kata kunci pencarian dan nama file output dengan tampilan profesional.
- **Scraping Otomatis**: Mengambil data nama tempat, rating, jumlah ulasan, alamat, situs web, nomor telepon, URL Google Maps, latitude, dan longitude.
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
git clone https://github.com/aryasetiap/sewuscrap-gmaps.git
cd sewuscrap-gmaps
```

### 2. **Jalankan Batch File (Windows)**

Cukup **double-click** file [`app.exe`](SewuScrap/app.exe)  

### 3. **Akses Aplikasi**

Buka browser ke [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📝 Penggunaan

1. Masukkan **kata kunci pencarian** (misal: `Bank di Pringsewu`)
2. Tentukan **nama file output** (opsional, default: `hasil_scrape.csv`)
3. Klik **Mulai Scraping**
4. Setelah selesai, klik **Download Hasil** untuk mengunduh file CSV

---

## 🛠️ Struktur Project

```
.
├── app.py                # Aplikasi web utama (Flask)
├── scraper.py            # Script utama untuk scraping Google Maps
├── requirements.txt      # Daftar dependencies Python
├── SewuScrapApp.bat      # Batch file untuk menjalankan aplikasi (Windows)
├── favicon.ico           # Favicon aplikasi
├── SewuScrap
│   └── app.exe           # Aplikasi desktop (Windows)
├── static/
│   ├── logo-bps.png      # Logo BPS
│   └── tampilan.png      # Gambar tampilan aplikasi
├── hasil_scrape.csv      # Contoh hasil scraping (opsional)
└── README.md             # Dokumentasi proyek
```

---

## 📦 Dependencies

- Flask
- Selenium
- BeautifulSoup4
- Pandas
- webdriver_manager

Semua dependencies akan terinstall otomatis saat menjalankan batch file.

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

> &copy; 2025 Badan Pusat Statistik Kabupaten Pringsewu | Arya Setia Pratama
