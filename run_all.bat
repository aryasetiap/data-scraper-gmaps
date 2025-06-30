@echo off

echo ===========================
echo Google Maps Scraper v1.0 by Arya Setia Pratama ---- Help: github.com/aryasetiap
echo ===========================
echo Pastikan Python, pip, dan Google Chrome terbaru sudah terinstal.
echo Menginstal paket yang diperlukan...

pip install pandas selenium webdriver-manager beautifulsoup4 >nul 2>&1

python code_scraper_test.py

pause