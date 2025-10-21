# ChatBot (Gemini / Replicate)

**Project:** avpn-hacktiv8-ai-for-ds  
**Isi:** `app-01.py` (CLI) dan `app-02.py` (Streamlit UI)  
**Tujuan README:** langkah-langkah install, konfigurasi API key, menjalankan lokal, tips debugging, dan cara push ke GitHub / deploy.

---

## Ringkasan singkat

Project ini berisi dua demo chatbot:

* `app-01.py` — chatbot via terminal (CLI) memakai Google Gemini (default saat ini).
* `app-02.py` — chatbot via Streamlit (web UI) memakai Google Gemini (default saat ini).

> Catatan: README ini juga menyediakan opsi **mengganti provider ke Replicate (IBM Granite)** jika kamu mau pakai model Granite di Replicate.com.

---

## Prasyarat

* Python 3.11 / 3.13 (disarankan gunakan satu versi dan virtual environment)
* pip (manajer paket Python)
* Akun Google + API key Gemini **atau** akun Replicate + `REPLICATE_API_TOKEN` jika ingin pakai IBM Granite
* Koneksi internet

---

## Struktur file

```
avpn-hacktiv8-ai-for-ds-2025-10/
├─ app-01.py        # CLI chatbot
├─ app-02.py        # Streamlit chatbot
├─ requirements.txt # (direkomendasikan dibuat)
├─ .gitignore
└─ README.md
```

---

## 1) Setup environment (Windows contoh)

Buka terminal (PowerShell / CMD) di folder project.

1. Buat virtual environment:

```powershell
# pakai python launcher (sesuaikan versi)
py -3.13 -m venv .venv
# aktifkan
.venv\Scripts\Activate.ps1   # PowerShell
# atau untuk cmd:
.venv\Scripts\activate.bat
```

2. Upgrade pip dan install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Contoh `requirements.txt` (rekomendasi):**

```
streamlit>=1.20
replicate>=0.9.0    # jika mau pake Replicate (opsional)
langchain>=0.1.0    # kalau masih pakai langchain (opsional)
langchain-core>=1.0.0
langchain-google-genai>=0.1.0
google-genai>=0.1.0
```

> Sesuaikan versi bila ada konflik. Jika kamu *tidak* ingin pakai Google Gemini, hapus paket Google-related; jika mau pakai Replicate, pastikan `replicate` terinstal.

---

## 2) Dapatkan API Key

### A. Google Gemini (via Google AI Studio)

1. Kunjungi: `https://aistudio.google.com/apikey`
2. Login dengan akun Google.
3. Klik **Create API key** → pilih `Create API key in new project`.
4. Salin API key (format biasanya `AIza...`) → jangan di-commit ke GitHub.

### B. Replicate (untuk IBM Granite)

1. Daftar / login ke `https://replicate.com`.
2. Buka `https://replicate.com/account/api-tokens`.
3. Generate API token → salin (contoh `r8_...`).

Simpan key di tempat aman. Jangan commit ke repo publik.

---

## 3) Menjalankan lokal

### A. Jalankan CLI (app-01.py)

Konfigurasi environment variable (Windows PowerShell contoh):

**Untuk Google Gemini (saat ini script minta input via getpass):**

```bash
python app-01.py
# script akan minta input API key via prompt (hidden)
```

**Jika kamu ingin set env var dulu (opsional):**

```powershell
setx GOOGLE_API_KEY "YOUR_GOOGLE_API_KEY"
# lalu restart terminal
python app-01.py
```

**Jika memakai Replicate (versi yang diganti):**

* Script harus diubah agar meminta `REPLICATE_API_TOKEN` (atau kamu bisa set env var):

```powershell
setx REPLICATE_API_TOKEN "your_replicate_token"
python app-01.py
```

### B. Jalankan Streamlit (app-02.py)

Jalankan:

```bash
streamlit run app-02.py
```

Buka browser ke `http://localhost:8501`.

**Perhatikan:**

* Script `app-02.py` versi default meminta Google API Key lewat UI. Jika ingin pakai Replicate, ubah input label jadi `REPLICATE_API_TOKEN` dan ubah pemanggilan LLM di bagian `load_llm()` / invoke.

---

## 4) Mengganti dari Google Gemini ke Replicate (IBM Granite)

Jika kamu ingin **sepenuhnya** pindah ke Replicate / IBM Granite, langkah yang disarankan:

1. Install `replicate`:

```bash
pip install replicate
```

2. Ubah `app-01.py` / `app-02.py`:

* Ganti input env var dari `GOOGLE_API_KEY` menjadi `REPLICATE_API_TOKEN`.
* Ganti pemanggilan `ChatGoogleGenerativeAI(...)` dengan `replicate.run("ibm-granite/MODEL_ID", input={...})`.
* Perhatikan: beberapa model menerima `prompt` string; model lain memakai `messages` array. Cek doc model di replicate.com untuk format input.

**Contoh pemanggilan sederhana (synchronous):**

```python
import os
import replicate

os.environ["REPLICATE_API_TOKEN"] = "PASTE_TOKEN_HERE"

output = replicate.run(
    "ibm-granite/granite-3.1-8b-instruct",
    input={"prompt": "Halo, perkenalkan diri"}
)
print(output)
```

**Di Streamlit**, gunakan spinner agar UI tidak terlihat “muter”:

```python
with st.spinner("IBM Granite sedang berpikir..."):
    output = replicate.run(MODEL_ID, input={"prompt": prompt})
```

Jika model sering *hang*, tambahkan timeout atau gunakan model cadangan.

---

## 5) Debugging umum

* `ModuleNotFoundError: No module named 'langchain_core'`
  → Pastikan `langchain-core`/`langchain` terinstal di environment yang sama dengan yang menjalankan Streamlit (`python -m pip install langchain-core`).

* `ModuleNotFoundError: No module named 'replicate'`
  → `pip install replicate` di environment yang sama.

* Streamlit menampilkan warning: `label got an empty value`
  → Pastikan `st.text_input()` memiliki label (bisa disembunyikan dengan `label_visibility="collapsed"`).

* Jika Streamlit muter terus saat `replicate.run(...)`
  → Periksa:
    * Token valid?
    * Model tersedia/public?
    * Koneksi internet?
    * Coba panggil dari REPL/terminal untuk test:

    ```python
    import replicate
    print(replicate.run("ibm-granite/granite-3.1-8b-instruct", input={"prompt": "test"}))
    ```

---

## 6) .gitignore (saran)

Buat `.gitignore` untuk mencegah commit file sensitif:

```
# Python
__pycache__/
*.pyc
.venv/
env/
venv/

# Streamlit
.streamlit/

# Secrets
.env
*.env
secrets.json

# OS
Thumbs.db
.DS_Store
```

---

## 7) Upload ke GitHub — langkah demi langkah

1. Inisialisasi repo lokal:

```bash
git init
git add .
git commit -m "Initial commit - chatbot demo"
```

2. Buat repo di GitHub (via website) — misal `avpn-hacktiv8-ai-for-ds`.

3. Tambahkan remote & push:

```bash
git remote add origin https://github.com/USERNAME/avpn-hacktiv8-ai-for-ds.git
git branch -M main
git push -u origin main
```

4. **JANGAN** commit API keys. Pastikan `.gitignore` termasuk `.env`.

---

## 8) Deployment (opsi)

### A. Streamlit Community Cloud (cepat)

1. Buat account di [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Tambah repo GitHub project.
3. Atur `requirements.txt` di repo.
4. Di Streamlit cloud, tambah Secret: `REPLICATE_API_TOKEN` (atau `GOOGLE_API_KEY`) di Settings → Secrets.
5. Deploy — Streamlit akan menjalankan `streamlit run app-02.py` otomatis.

### B. Render / Railway / Heroku (alternatif)

* Buat service baru, link GitHub repo, atur `start` command:

  ```
  streamlit run app-02.py --server.port $PORT
  ```
* Set environment variables (secrets) di portal provider.

---

## 9) Tips keamanan & biaya

* Jangan memasukkan API key ke dalam kode atau commit.
* Simpan key sebagai **secret environment variable** di hosting / CI.
* Replicate dan Google dapat menagih penggunaan — cek halaman pricing.
* Gunakan model dengan resource sesuai kebutuhan (small/medium for testing).

---

## 10) Contoh: `README` singkat untuk GitHub

Gunakan file `README.md` ini sebagai basis. Di GitHub, tambahkan badge (opsional) dan instruksi singkat.

---
