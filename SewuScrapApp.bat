@echo off

REM ===========================
REM Menjalankan Google Maps Scraper Web App
REM ===========================

REM ---------------------------------------------------------------------------
REM Mengecek apakah Python sudah terinstall di komputer dan sudah ada di PATH.
REM Jika belum, tampilkan pesan error dan instruksi instalasi Python.
REM ---------------------------------------------------------------------------
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python belum terinstall atau tidak ada di PATH.
    echo Silakan install Python dari https://www.python.org/downloads/
    pause
    exit /b
)

REM ---------------------------------------------------------------------------
REM Mengecek apakah pip (alat untuk mengelola library Python) sudah terinstall.
REM Jika belum, tampilkan pesan error dan instruksi instalasi pip.
REM ---------------------------------------------------------------------------
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] pip belum terinstall.
    echo Silakan install pip dengan mengikuti petunjuk di https://pip.pypa.io/en/stable/installation/
    pause
    exit /b
)

REM ---------------------------------------------------------------------------
REM Mengecek apakah semua library/dependencies yang dibutuhkan sudah terinstall.
REM Jika belum, maka akan mencoba menginstall semua dependencies yang ada di file requirements.txt.
REM Jika gagal, tampilkan pesan error dan instruksi pengecekan.
REM ---------------------------------------------------------------------------
python -m pip check >nul 2>nul
if %errorlevel% neq 0 (
    echo Menginstal dependencies...
    pip install -r requirements.txt >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Gagal menginstal dependencies. Silakan cek requirements.txt dan koneksi internet.
        pause
        exit /b
    )
    echo Dependencies berhasil diinstal.
) else (
    echo Semua dependencies sudah terinstall.
)

REM ---------------------------------------------------------------------------
REM Membuka browser secara otomatis ke alamat aplikasi web (localhost:5000).
REM Tujuannya agar pengguna langsung diarahkan ke aplikasi setelah dijalankan.
REM ---------------------------------------------------------------------------
start "" http://127.0.0.1:5000

REM ---------------------------------------------------------------------------
REM Menjalankan aplikasi utama (Flask) dengan menjalankan file app.py.
REM Pengguna dapat mengakses aplikasi melalui browser yang sudah terbuka.
REM ---------------------------------------------------------------------------
echo Menjalankan aplikasi Flask...
python app.py

pause