@echo off
REM filepath: d:\1. SANDBOX\Project\Project 2025\data-scraper-gmaps\run_all.bat
echo ===========================
echo Menjalankan Google Maps Scraper Web App
echo ===========================

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python belum terinstall atau tidak ada di PATH.
    echo Silakan install Python dari https://www.python.org/downloads/
    pause
    exit /b
)

python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] pip belum terinstall.
    echo Silakan install pip dengan mengikuti petunjuk di https://pip.pypa.io/en/stable/installation/
    pause
    exit /b
)

REM Cek apakah semua dependencies sudah terinstall
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

REM Membuka browser ke localhost:5000
start "" http://127.0.0.1:5000

echo Menjalankan aplikasi Flask...
python app.py

pause