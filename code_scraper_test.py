"""
Scraper Google Maps untuk mengambil data Puskesmas di Bandar Lampung.

Fitur:
- Mengambil nama tempat, rating, jumlah ulasan, alamat, URL Google Maps, latitude, dan longitude.
- Menyimpan hasil dalam file CSV.
- Tidak mengambil kategori tempat.
- Alamat sudah dibersihkan dan disimpan dalam satu kolom.

Cara kerja:
1. Membuka Google Maps dengan query pencarian.
2. Melakukan scroll otomatis untuk memuat semua hasil.
3. Mengekstrak data dari setiap kartu hasil pencarian.
4. Menyimpan data ke file CSV.

Dibuat menggunakan Selenium, BeautifulSoup, dan Pandas.
"""

import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

SEARCH_QUERY = "Puskesmas di Bandar Lampung"
OUTPUT_FILENAME = "hasil_scrape_test.csv"

def parse_card_final(card_html_string):
    """
    Mengekstrak informasi dari satu kartu hasil pencarian Google Maps.

    Parameter:
        card_html_string (str): HTML dari satu kartu hasil pencarian.

    Return:
        dict: Data hasil ekstraksi (nama tempat, rating, ulasan, alamat, URL, latitude, longitude).
    """
    card_soup = BeautifulSoup(card_html_string, 'html.parser')
    data = {
        "Nama Tempat": "N/A", "Rating": "N/A", "Jumlah Ulasan": 0,
        "Alamat": "N/A", "URL Google Maps": "N/A",
        "Latitude": "N/A", "Longitude": "N/A"
    }

    try:
        nama_element = card_soup.select_one('div.qBF1Pd, div.font-medium')
        if not nama_element: return None
        data['Nama Tempat'] = nama_element.text.strip()

        rating_container = card_soup.select_one('span.ZkP5Je')
        if rating_container:
            rating_element = rating_container.select_one('span.MW4etd')
            if rating_element:
                data['Rating'] = float(rating_element.text.strip().replace(',', '.'))
            ulasan_element = rating_container.select_one('span.UY7F9')
            if ulasan_element:
                ulasan_text = ulasan_element.text.strip()
                ulasan_match = re.search(r'(\d+)', ulasan_text)
                if ulasan_match:
                    data['Jumlah Ulasan'] = int(ulasan_match.group(1))

        link_element = card_soup.select_one('a')
        if link_element: data['URL Google Maps'] = link_element.get('href')
        if link_element:
            url = link_element.get('href')
            data['URL Google Maps'] = url
            coord_match = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', url)
            if coord_match:
                data['Latitude'] = float(coord_match.group(1))
                data['Longitude'] = float(coord_match.group(2))

        address_found = False
        all_lines = card_soup.get_text(separator='\n', strip=True).split('\n')
        address_keywords = ['Jl.', 'Jalan', 'Gg.', 'No.', 'Kec.', 'Kel.']

        def get_clean_address(line):
            if '·' in line:
                return line.split('·', 1)[1].strip()
            else:
                return line.strip()

        for line in all_lines:
            if any(keyword in line for keyword in address_keywords):
                data['Alamat'] = get_clean_address(line)
                address_found = True
                break

        if not address_found:
            for line in all_lines:
                if '·' in line and data['Nama Tempat'] not in line:
                    data['Alamat'] = get_clean_address(line)
                    break

        return data
    except Exception as e:
        print(f"Error parsing satu kartu: {e}")
        return None

def main():
    """
    Fungsi utama untuk menjalankan proses scraping Google Maps dan menyimpan hasil ke file CSV.
    """
    print(f"Memulai Scraper Final untuk: '{SEARCH_QUERY}'")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--lang=id-ID")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    try:
        url = f"https://www.google.com/maps/search/{SEARCH_QUERY.replace(' ', '+')}"
        driver.get(url)
        scroll_panel_xpath = "//div[contains(@aria-label, 'Hasil untuk')]"
        wait = WebDriverWait(driver, 30)
        scrollable_div = wait.until(EC.presence_of_element_located((By.XPATH, scroll_panel_xpath)))
        print("Memulai scroll otomatis...")
        last_height = -1
        while True:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(3)
            new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
            if new_height == last_height: break
            last_height = new_height
        print("Scroll selesai.")
        card_selector_css = "div[jsaction*='mouseover:pane']"
        cards_elements = driver.find_elements(By.CSS_SELECTOR, card_selector_css)
        print(f"Ditemukan {len(cards_elements)} kartu. Memulai ekstraksi...")
        scraped_data = []
        for card_element in cards_elements:
            card_html = card_element.get_attribute('outerHTML')
            card_data = parse_card_final(card_html)
            if card_data:
                scraped_data.append(card_data)
        if scraped_data:
            print(f"Berhasil mengekstrak {len(scraped_data)} data. Menyimpan ke '{OUTPUT_FILENAME}'...")
            df = pd.DataFrame(scraped_data)
            df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
            print("Proses Selesai.")
        else:
            print("Tidak ada data yang berhasil diekstrak.")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()