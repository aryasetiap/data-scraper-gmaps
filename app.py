# app.py (Pop-up Selalu Muncul)

from flask import Flask, render_template_string, request, send_file, jsonify
import threading
import os
from code_scraper_test import main as run_scraper

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <title>Sewu Scrap - Google Maps Scraper BPS</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary-color: #0d47a1;
      --secondary-color: #f9a825;
      --background-color: #eef2f9;
      --form-background: #ffffff;
      --text-color: #333;
      --border-radius: 12px;
      --shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    body {
      background: var(--background-color);
      font-family: 'Poppins', 'Segoe UI', sans-serif;
      display: flex;
      flex-direction: column;
      min-height: 100vh;
      color: var(--text-color);
    }
    .main-container {
      flex: 1; display: flex; align-items: center; justify-content: center; padding: 20px;
    }
    .card-scraper {
      background: var(--form-background);
      border-radius: var(--border-radius);
      box-shadow: var(--shadow);
      padding: 2.5rem;
      width: 100%;
      max-width: 500px;
      text-align: center;
    }
    .header-logo { width: 70px; margin-bottom: 1rem; }
    .header-title h1 { color: var(--primary-color); font-weight: 700; font-size: 2rem; margin: 0; }
    .header-title p { font-weight: 500; color: #6c757d; margin-bottom: 2rem; }
    .form-label { font-weight: 500; color: #555; }
    .form-control { border-radius: 8px; border: 1px solid #ddd; padding: 0.75rem 1rem; }
    .form-control:focus { border-color: var(--primary-color); box-shadow: 0 0 0 0.25rem rgba(13, 71, 161, 0.2); }
    .btn-submit {
      background-color: var(--primary-color); color: white; font-weight: 600;
      padding: 0.8rem; border-radius: 8px; transition: all 0.3s ease; border: none;
    }
    .btn-submit:hover { background-color: #0b3a82; transform: translateY(-2px); box-shadow: 0 4px 15px rgba(13, 71, 161, 0.3); }
    .btn-submit:disabled { opacity: 0.7; cursor: not-allowed; }
    #status-area { margin-top: 1.5rem; font-weight: 500; }
    .spinner-border { width: 1.5rem; height: 1.5rem; vertical-align: text-bottom; margin-right: 0.5rem; }
    .alert-custom-success { background-color: #d1e7dd; border-color: #badbcc; color: #0f5132; }
    .btn-download { background-color: #198754; color: white; font-weight: 600; transition: background-color 0.2s; }
    .btn-download:hover { background-color: #157347; color: white; }
    .footer { padding: 1.5rem 0; text-align: center; font-size: 0.9rem; color: #777; }
    #disclaimer-overlay {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.75);
        display: flex; justify-content: center; align-items: center;
        z-index: 2000;
        visibility: visible; opacity: 1;
        transition: visibility 0s, opacity 0.3s linear;
    }
    #disclaimer-box {
        background-color: white; padding: 25px 30px; border-radius: var(--border-radius);
        width: 90%; max-width: 550px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        text-align: left;
    }
    #disclaimer-box h2 { margin-top: 0; color: var(--primary-color); font-weight: 600; }
    #disclaimer-box p, #disclaimer-box ul { color: #555; line-height: 1.7; }
    #disclaimer-box ul { padding-left: 20px; }
    #agree-button {
        display: block; width: 100%; padding: 12px; margin-top: 20px;
        border: none; background-color: #4285F4; color: white;
        font-size: 16px; font-weight: bold; border-radius: 8px;
        cursor: pointer; transition: background-color 0.2s;
    }
    #agree-button:hover { background-color: #357ae8; }
    #disclaimer-overlay.hidden { visibility: hidden; opacity: 0; }
  </style>
</head>
<body>
  <div id="disclaimer-overlay">
      <div id="disclaimer-box">
          <h2>Pemberitahuan Penggunaan Data</h2>
          <p>Alat ini ditujukan untuk membantu pengumpulan data awal untuk keperluan riset internal BPS Kabupaten Pringsewu.</p>
          <p>Dengan melanjutkan, Anda memahami dan menyetujui poin-poin berikut:</p>
          <ul>
              <li>Data yang dikumpulkan hanya akan digunakan untuk tujuan <strong>riset internal dan non-komersial</strong>.</li>
              <li>Keakuratan data <strong>wajib divalidasi ulang</strong> sebelum digunakan dalam analisis atau laporan resmi.</li>
              <li>Alat ini bersifat otomatis, dan hasilnya mungkin tidak selalu 100% lengkap atau akurat.</li>
          </ul>
          <button id="agree-button">Saya Mengerti dan Setuju</button>
      </div>
  </div>
  <div class="main-container">
    <div class="card-scraper">
      <img src="/static/logo-bps.png" alt="Logo BPS" class="header-logo">
      <div class="header-title">
        <h1>Sewu Scrap</h1>
        <p>Google Maps Data Scraper</p>
      </div>
      <form id="scraper-form">
        <div class="mb-3 text-start">
          <label for="search_query" class="form-label">Kata Kunci Pencarian</label>
          <input type="text" class="form-control" id="search_query" name="search_query" placeholder="Contoh: Bank di Pringsewu" required>
        </div>
        <div class="mb-4 text-start">
          <label for="output_filename" class="form-label">Nama File Output</label>
          <input type="text" class="form-control" id="output_filename" name="output_filename" value="hasil_scrape.csv">
        </div>
        <button type="submit" id="submit-button" class="btn btn-submit w-100">
          <span id="button-text">Mulai Scraping</span>
          <div id="loading-spinner" class="spinner-border spinner-border-sm text-light" role="status" style="display: none;"></div>
        </button>
      </form>
      <div id="status-area"></div>
    </div>
  </div>
  <footer class="footer">
    &copy; 2025 Badan Pusat Statistik | Developed by <a href="https://github.com/aryasetiap">Arya Setia Pratama</a>
  </footer>

  <script>
    // JAVASCRIPT UNTUK DISCLAIMER POP-UP
    document.addEventListener('DOMContentLoaded', function() {
        const overlay = document.getElementById('disclaimer-overlay');
        const agreeButton = document.getElementById('agree-button');
        
        // [DIHAPUS] Bagian kode yang memeriksa sessionStorage dihapus agar pop-up selalu muncul
        // if (sessionStorage.getItem('disclaimerAgreed') === 'true') {
        //     overlay.classList.add('hidden');
        // }
        
        agreeButton.addEventListener('click', function() {
            overlay.classList.add('hidden');
            // [DIHAPUS] Bagian kode yang menyimpan ke sessionStorage dihapus
            // sessionStorage.setItem('disclaimerAgreed', 'true');
        });
    });

    // JAVASCRIPT UNTUK FORM SUBMISSION
    document.getElementById('scraper-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const submitButton = document.getElementById('submit-button');
        const buttonText = document.getElementById('button-text');
        const loadingSpinner = document.getElementById('loading-spinner');
        const statusArea = document.getElementById('status-area');

        statusArea.innerHTML = '';
        submitButton.disabled = true;
        buttonText.textContent = 'Memproses...';
        loadingSpinner.style.display = 'inline-block';

        fetch('/start-scraping', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                statusArea.innerHTML = `
                    <div class="alert alert-custom-success" role="alert">
                        <strong>Berhasil!</strong> Scraping selesai.
                        <a href="/download/${data.filename}" class="btn btn-sm btn-download mt-2 d-block">Download ${data.filename}</a>
                    </div>
                `;
            } else {
                statusArea.innerHTML = `<div class="alert alert-danger" role="alert"><strong>Gagal:</strong> ${data.message}</div>`;
            }
        })
        .catch(error => {
            statusArea.innerHTML = `<div class="alert alert-danger" role="alert"><strong>Error:</strong> Terjadi kesalahan komunikasi.</div>`;
            console.error('Error:', error);
        })
        .finally(() => {
            submitButton.disabled = false;
            buttonText.textContent = 'Mulai Scraping';
            loadingSpinner.style.display = 'none';
        });
    });
  </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/start-scraping', methods=['POST'])
def start_scraping():
    try:
        search_query = request.form['search_query']
        output_filename = request.form['output_filename'] or 'hasil_scrape.csv'
        if not search_query:
            return jsonify({'status': 'error', 'message': 'Kata kunci pencarian tidak boleh kosong.'})
        if os.path.exists(output_filename):
            os.remove(output_filename)
        scraper_thread = threading.Thread(target=run_scraper, args=(search_query, output_filename))
        scraper_thread.start()
        scraper_thread.join()
        if os.path.exists(output_filename):
            return jsonify({'status': 'success', 'filename': output_filename})
        else:
            return jsonify({'status': 'error', 'message': 'Scraper selesai namun tidak ada data yang dihasilkan atau disimpan.'})
    except Exception as e:
        print(f"Error pada endpoint /start-scraping: {e}")
        return jsonify({'status': 'error', 'message': f'Terjadi kesalahan internal: {e}'})

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)