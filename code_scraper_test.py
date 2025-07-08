"""
code_scraper_test.py (Versi 3.1 - Perbaikan Ekstraksi Lat/Lon)

Sewu Scrap - Google Maps Scraper v3.1 (Polished Build)

Deskripsi:
Script ini digunakan untuk mengambil (scrape) data tempat dari Google Maps berdasarkan kata kunci pencarian.
Data yang diambil meliputi nama tempat, rating, jumlah ulasan, alamat, situs web, nomor telepon, URL Google Maps, latitude, dan longitude.
Hasil data akan disimpan dalam file CSV yang dapat dibuka dengan Excel.

Catatan:
- Script ini menggunakan Selenium untuk mengotomasi browser Google Chrome.
- Gunakan script ini hanya untuk keperluan riset internal dan non-komersial.

Developer: Arya Setia Pratama | BPS Kabupaten Pringgiran
"""

import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def print_banner():
    """
    Menampilkan banner informasi dan peringatan di awal program.
    Banner ini berisi nama aplikasi, versi, dan peringatan penggunaan.
    """
    print("="*70)
    print("\nSewu Scrap - Google Maps Scraper v3.1 (Polished Build)")
    print("="*70)
    print("PERINGATAN: Gunakan secara bijak untuk riset internal & non-komersial.")

def main(search_query=None, output_filename=None):
    """
    Fungsi utama untuk menjalankan proses scraping Google Maps.

    Args:
        search_query (str, optional): Kata kunci pencarian tempat di Google Maps.
        output_filename (str, optional): Nama file output hasil scraping (format CSV).

    Langkah-langkah utama:
    1. Membuka browser Chrome secara otomatis (bisa mode headless/tanpa tampilan).
    2. Melakukan pencarian berdasarkan kata kunci yang diberikan.
    3. Mengumpulkan semua URL tempat dari hasil pencarian.
    4. Mengunjungi setiap URL untuk mengambil detail informasi tempat.
    5. Menyimpan hasil data ke file CSV.
    """
    HEADLESS_MODE = True  # Jika True, browser berjalan di background tanpa tampilan

    print_banner()
    if search_query is None:
        search_query = input("Masukkan kata kunci pencarian: ").strip()
    if output_filename is None:
        output_filename = input("Nama file output CSV [hasil_scrape.csv]: ").strip() or "hasil_scrape.csv"

    print(f"\n[INFO] Memulai Scraper untuk: '{search_query}'")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--lang=id-ID")
    if HEADLESS_MODE:
        options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    scraped_data = []
    try:
        # LANGKAH 1: Kumpulkan semua URL tempat dari hasil pencarian
        search_url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
        driver.get(search_url)
        wait = WebDriverWait(driver, 20)

        # Mencoba menutup pop-up persetujuan cookie jika muncul
        try:
            print("[INFO] Mencari pop-up persetujuan cookie...")
            consent_button_selector = 'button[aria-label*="Accept all"], button[aria-label*="Setuju semua"]'
            consent_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, consent_button_selector)))
            consent_button.click()
            print("[INFO] Pop-up persetujuan diklik.")
        except TimeoutException:
            print("[INFO] Tidak ada pop-up persetujuan yang ditemukan.")

        print("[INFO] Menunggu panel hasil pencarian...")
        scroll_panel_selector = 'div[role="feed"]'
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, scroll_panel_selector)))
        print("[INFO] Panel ditemukan. Memberi jeda...")
        time.sleep(2)

        RESULTS_SELECTOR = 'a.hfpxzc'
        print("[INFO] Memulai scroll untuk mengumpulkan semua URL...")
        patience_counter = 0
        patience_threshold = 3
        last_known_count = 0

        # Melakukan scroll pada panel hasil pencarian untuk memunculkan semua tempat
        while patience_counter < patience_threshold:
            try:
                scrollable_div = driver.find_element(By.CSS_SELECTOR, scroll_panel_selector)
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                time.sleep(3)
                current_card_count = len(driver.find_elements(By.CSS_SELECTOR, RESULTS_SELECTOR))
                if current_card_count > last_known_count:
                    last_known_count = current_card_count
                    patience_counter = 0
                    print(f"  -> Menemukan {last_known_count} URL... (Kesabaran direset)")
                else:
                    patience_counter += 1
                    print(f"  -> Jumlah URL tidak bertambah. (Kesabaran: {patience_counter}/{patience_threshold})")
            except Exception as e:
                print(f"[ERROR] Error saat scroll: {e}, menghentikan scroll.")
                break

        place_links = driver.find_elements(By.CSS_SELECTOR, RESULTS_SELECTOR)
        urls = [link.get_attribute('href') for link in place_links if link.get_attribute('href')]
        unique_urls = list(dict.fromkeys(urls))  # Menghapus duplikat sambil menjaga urutan
        print(f"[INFO] Scroll selesai. Ditemukan {len(unique_urls)} URL unik.")

        # LANGKAH 2: Kunjungi setiap URL untuk ekstraksi detail tempat
        print(f"[INFO] Memulai ekstraksi detail dari {len(unique_urls)} URL...")
        for i, url in enumerate(unique_urls):
            try:
                driver.get(url)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.DUwDvf')))
                time.sleep(1.5)

                # Mengambil nama tempat
                nama = driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf').text

                # Mengambil rating dan jumlah ulasan
                rating, ulasan = "N/A", 0
                try:
                    rating_text = driver.find_element(By.CSS_SELECTOR, 'div.F7nice').text.strip()
                    parts = rating_text.split('(')
                    rating = parts[0].strip()
                    ulasan_match = re.search(r'(\d[\d,.]*)', parts[1])
                    if ulasan_match:
                        ulasan = int(re.sub(r'[.,]', '', ulasan_match.group(1)))
                except NoSuchElementException:
                    pass

                # Mengambil alamat, website, dan nomor telepon
                alamat, website, telepon = "N/A", "N/A", "N/A"
                try:
                    address_element = driver.find_element(By.CSS_SELECTOR, '[data-item-id="address"]')
                    alamat = address_element.find_element(By.CSS_SELECTOR, 'div.Io6YTe').text
                except NoSuchElementException:
                    pass
                try:
                    website_element = driver.find_element(By.CSS_SELECTOR, '[data-item-id="authority"]')
                    website = website_element.find_element(By.CSS_SELECTOR, 'div.Io6YTe').text
                except NoSuchElementException:
                    pass
                try:
                    phone_element = driver.find_element(By.CSS_SELECTOR, '[data-item-id*="phone:tel:"]')
                    telepon = phone_element.find_element(By.CSS_SELECTOR, 'div.Io6YTe').text
                except NoSuchElementException:
                    pass

                # Mengambil latitude dan longitude dari URL
                current_url = driver.current_url
                lat, lon = "N/A", "N/A"
                if "@" in current_url:
                    try:
                        coords_part = current_url.split('@')[1]
                        coords_array = coords_part.split(',')
                        lat = coords_array[0]
                        lon = coords_array[1]
                    except (IndexError, Exception):
                        pass
                else:
                    match = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', current_url)
                    if match:
                        lat = match.group(1)
                        lon = match.group(2)

                data = {
                    "Nama Tempat": nama,
                    "Rating": rating,
                    "Jumlah Ulasan": ulasan,
                    "Alamat": alamat,
                    "Situs Web": website,
                    "Nomor Telepon": telepon,
                    "URL Google Maps": current_url,
                    "Latitude": lat,
                    "Longitude": lon,
                }
                scraped_data.append(data)
                print(f"  [OK] {i + 1}/{len(unique_urls)} - {nama} | Data lengkap: {alamat != 'N/A' and website != 'N/A' and telepon != 'N/A'}")

            except TimeoutException:
                print(f"  [GAGAL] {i + 1}/{len(unique_urls)} - Timeout saat memuat URL: {url}")
            except Exception as e:
                print(f"  [ERROR] {i + 1}/{len(unique_urls)} - Terjadi error pada URL {url}: {e}")

    finally:
        driver.quit()

    # Menyimpan hasil data ke file CSV jika ada data yang berhasil diambil
    if scraped_data:
        print(f"\n[INFO] Berhasil mengekstrak {len(scraped_data)} data. Menyimpan ke {output_filename}...")
        df = pd.DataFrame(scraped_data)
        df = df.drop_duplicates(subset=["Nama Tempat", "Alamat"])
        df.to_csv(output_filename, index=False, encoding='utf-8-sig')
        print("==============================================")
        print("  ✅ PROYEK SELESAI DAN BERHASIL! ✅")
        print("==============================================")
    else:
        print("[INFO] Tidak ada data yang berhasil diekstrak.")

if __name__ == '__main__':
    main()