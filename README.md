Baimluaa

«Python-based file uploader for Baim Market.»

Baimluaa adalah tool Python untuk mengunggah file melalui SFile.co dengan dukungan chunk upload, MD5 hash checking, duplicate detection, dan resume upload.

✨ Features

- 🚀 File upload
- 📦 Chunk-based upload
- 🔄 Resume upload
- 🔍 MD5 hash checking
- ♻️ Duplicate detection
- 🔗 Automatic URL extraction
- 📝 Custom file description
- 📱 Support Termux / Android
- 💻 Support Windows, Linux, dan macOS
- 📏 Maximum file size: 250 MB

📁 Project Structure

Baimluaa/
├── main.py
└── README.md

🛠️ Requirements

- Python 3.10+
- "requests"

Install dependency:

pip install requests

Linux:

pip3 install requests

🚀 Installation

Windows

Clone repository:

git clone https://github.com/baimlekk7-design/Baimluaa.git
cd Baimluaa

Install dependency:

pip install requests

Linux

git clone https://github.com/baimlekk7-design/Baimluaa.git
cd Baimluaa
pip3 install requests

Android — Termux

Install Python dan Git:

pkg update
pkg install python git

Clone repository:

git clone https://github.com/baimlekk7-design/Baimluaa.git
cd Baimluaa

Install Requests:

pip install requests

▶️ Usage

Format:

python main.py <file>

Contoh:

python main.py file.zip

Dengan deskripsi:

python main.py file.zip "Baim Market Release"

📱 Termux

Berikan akses storage:

termux-setup-storage

Contoh upload file dari folder Download:

python main.py ~/storage/downloads/file.zip

Dengan deskripsi:

python main.py ~/storage/downloads/file.zip "Baim Market"

📦 Upload Process

Baimluaa menggunakan chunk upload sehingga file besar tidak dikirim sebagai satu request.

Default chunk size:

1 MB

Alur upload:

File
  ↓
MD5 Hash
  ↓
Check Duplicate
  ↓
Split Into Chunks
  ↓
Upload Chunks
  ↓
Resume Existing Chunks
  ↓
Extract URL
  ↓
Done

🔄 Resume Upload

Jika chunk tertentu sudah tersedia di server, uploader dapat melewati chunk tersebut dan melanjutkan chunk berikutnya.

Contoh:

Chunk 1/5 → existing → skip
Chunk 2/5 → existing → skip
Chunk 3/5 → upload
Chunk 4/5 → upload
Chunk 5/5 → upload

♻️ Duplicate Detection

Sebelum proses upload, file dihitung menggunakan MD5.

MD5 → Check server → Duplicate?
                     ├─ Yes → Get existing URL
                     └─ No  → Start upload

Jika file yang sama sudah tersedia, tool mencoba mengambil URL yang tersedia daripada mengupload ulang file tersebut.

📏 File Limit

Maximum file size yang dikonfigurasi:

250 MB

File yang melebihi limit akan ditolak sebelum proses upload dimulai.

⚙️ Configuration

Konfigurasi utama tersedia di bagian atas "main.py".

Base URL

BASE_URL = "https://sfile.co"

Chunk Size

CHUNK_SIZE = 1024 * 1024

Nilai tersebut berarti:

1 MB

Maximum File Size

MAX_FILE_SIZE = 250 * 1024 * 1024

Nilai tersebut berarti:

250 MB

🧪 Examples

ZIP

python main.py BaimTools.zip

APK

python main.py aplikasi.apk

File dengan description

python main.py aplikasi.apk "Baim Market Release"

Full path

Windows:

python main.py "C:\Users\User\Downloads\file.zip"

Linux:

python main.py "/home/user/Downloads/file.zip"

Termux:

python main.py "/sdcard/Download/file.zip"

❗ Troubleshooting

"ModuleNotFoundError: No module named 'requests'"

Install Requests:

pip install requests

"File tidak ada"

Pastikan path file benar.

Cek isi directory:

ls

Kemudian:

python main.py nama-file.zip

HTTP 5xx

Server sedang memberikan server error. Tool memiliki retry untuk error server tertentu.

Jika masih gagal, jalankan kembali proses upload setelah beberapa saat.

URL tidak terbaca

Jika seluruh chunk berhasil tetapi URL tidak ditemukan pada response server, tool akan menampilkan pesan bahwa URL tidak terbaca.

🔐 Security

Jangan upload file yang berisi informasi sensitif seperti:

- Password
- API key
- Access token
- Private key
- Data pribadi
- Credential

Tool tidak membutuhkan username atau password SFile untuk proses upload.

⚠️ Disclaimer

Baimluaa merupakan project pihak ketiga dan tidak berafiliasi secara resmi dengan SFile.co.

Gunakan tool ini hanya untuk file yang memang berhak kamu upload dan sesuai dengan aturan layanan platform yang digunakan.

👤 Author

Baim Market

GitHub:

"baimlekk7-design"

Repository:

"Baimluaa"

---

⭐ Support

Jika project ini membantu, kamu bisa memberikan Star pada repository GitHub.

Made with 🐍 Python
