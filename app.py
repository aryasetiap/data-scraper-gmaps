from flask import Flask, render_template_string, request, send_file
import threading
import os
from code_scraper_test import main as run_scraper

app = Flask(__name__)

HTML_FORM = """
<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <title>Google Maps Scraper - BPS</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- Bootstrap CSS CDN -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background: #f7f7f7;
      font-family: 'Segoe UI', Arial, sans-serif;
      min-height: 100vh;
      margin: 0;
      display: flex;
      flex-direction: column;
    }
    .bps-header {
      background: #002b6a;
      color: #fff;
      padding: 24px 0 12px 0;
      margin-bottom: 32px;
      border-bottom: 4px solid #f9a825;
    }
    .center-container {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .bps-logo {
      height: 56px;
      margin-right: 16px;
      vertical-align: middle;
    }
    .bps-title {
      font-size: 2.2rem;
      font-weight: 700;
      letter-spacing: 1px;
      display: inline-block;
      vertical-align: middle;
    }
    .bps-form {
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.07);
      padding: 32px 28px;
      max-width: 480px;
      width: 100%;
      margin: 0 auto;
    }
    .bps-btn {
      background: #f9a825;
      color: #fff;
      font-weight: 600;
      border: none;
    }
    .bps-btn:hover {
      background: #fbc02d;
      color: #00796b;
    }
    .bps-footer {
      margin-top: 48px;
      color: #888;
      font-size: 0.95rem;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="bps-header text-center">
    <img src="/static/logo-bps.png" class="bps-logo" alt="Logo BPS">
    <span class="bps-title">Sewu Scrap<br><small style="font-size:1rem;font-weight:400;">Badan Pusat Statistik Kabupaten Pringsewu</small></span>
  </div>
  <div class="center-container">
    <div>
      <div class="bps-form">
        <form method="post">
          <div class="mb-3">
            <label for="search_query" class="form-label">Kata Kunci Pencarian</label>
            <input type="text" class="form-control" id="search_query" name="search_query" placeholder="Contoh: Pasar di Kabupaten Pringsewu" required>
          </div>
          <div class="mb-3">
            <label for="output_filename" class="form-label">Nama File Output</label>
            <input type="text" class="form-control" id="output_filename" name="output_filename" value="hasil_scrape.csv">
          </div>
          <button type="submit" class="btn bps-btn w-100">Mulai Scraping</button>
        </form>
        {% if message %}
          <div class="alert alert-info mt-4" role="alert">
            {{ message }}
            {% if file_ready %}
              <br>
              <a href="/download/{{ filename }}" class="btn btn-success mt-2">Download Hasil</a>
            {% endif %}
          </div>
        {% endif %}
      </div>
      <div class="bps-footer">
        &copy; {{ 2025 }} Badan Pusat Statistik | Tools Scraping Google Maps | Developed by <a href="https://github.com/aryasetiap">Arya Setia Pratama</a>
      </div>
    </div>
  </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    file_ready = False
    filename = ''
    if request.method == 'POST':
        search_query = request.form['search_query']
        output_filename = request.form['output_filename'] or 'hasil_scrape.csv'
        # Jalankan scraper di thread terpisah agar tidak blocking
        t = threading.Thread(target=run_scraper, args=(search_query, output_filename))
        t.start()
        t.join()
        if os.path.exists(output_filename):
            message = 'Scraping selesai!'
            file_ready = True
            filename = output_filename
        else:
            message = 'Terjadi kesalahan saat scraping.'
    return render_template_string(HTML_FORM, message=message, file_ready=file_ready, filename=filename)

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)