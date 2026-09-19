Baim Market Uploader

Uploader file berbasis Python untuk mengunggah file ke SFile.co menggunakan sistem chunk upload, pengecekan hash, dan resume upload.

✨ Features

- 🚀 Upload file ke SFile.co
- 📦 Chunk upload untuk file besar
- 🔄 Resume chunk yang sebelumnya sudah ter-upload
- 🔍 MD5 hash verification
- ♻️ Deteksi file duplikat
- 🔗 Otomatis mengambil download URL
- 📝 Support deskripsi file
- 📱 Bisa digunakan di Android melalui Termux
- 💻 Bisa digunakan di Windows, Linux, dan macOS
- 🛡️ Maximum file size: 250 MB

---

📁 Struktur Project

Baim-Market/
├── uploader.py
├── README.md
└── requirements.txt

«Jika file Python kamu memiliki nama berbeda, sesuaikan "uploader.py" dengan nama file tersebut.»

---

🛠️ Installation

Windows

Pastikan Python 3.10+ sudah terinstall.

Clone repository:

git clone https://github.com/USERNAME/Baim-Market.git
cd Baim-Market

Install dependency:

pip install -r requirements.txt

Atau langsung:

pip install requests

---

Linux

git clone https://github.com/USERNAME/Baim-Market.git
cd Baim-Market

Install dependency:

pip3 install -r requirements.txt

---

Android — Termux

Install Python:

pkg update
pkg upgrade
pkg install python git

Clone repository:

git clone https://github.com/USERNAME/Baim-Market.git
cd Baim-Market

Install dependency:

pip install requests

---

📦 Requirements

Project ini membutuhkan:

Python 3.10+
requests

Contoh "requirements.txt":

requests>=2.31.0

Install dengan:

pip install -r requirements.txt

---

🚀 Usage

Format dasar:

python uploader.py FILE

Contoh:

python uploader.py file.zip

Dengan deskripsi:

python uploader.py file.zip "Baim Market Tools"

---

📱 Contoh di Termux

Misalnya file berada di folder Download Android.

Berikan akses storage:

termux-setup-storage

Kemudian:

cd ~/storage/downloads

Upload file:

python ~/Baim-Market/uploader.py script.zip

Dengan deskripsi:

python ~/Baim-Market/uploader.py script.zip "Baim Market Release"

---

🔗 Output

Jika upload berhasil, program akan menampilkan informasi seperti:

[author : Baim Market] Target: script.zip (5242880 bytes)
[author : Baim Market] MD5 hash: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
[author : Baim Market] Mulai upload 5 chunk...
[author : Baim Market] Chunk 1/5 terkirim (HTTP 200)
[author : Baim Market] Chunk 2/5 terkirim (HTTP 200)
[author : Baim Market] Chunk 3/5 terkirim (HTTP 200)
[author : Baim Market] Chunk 4/5 terkirim (HTTP 200)
[author : Baim Market] Chunk 5/5 terkirim (HTTP 200)
[author : Baim Market] Upload selesai: https://sfile.co/xxxxxx

URL terakhir dapat digunakan untuk mengakses file yang sudah di-upload.

---

🔄 Resume Upload

Uploader menggunakan sistem chunk.

File dibagi menjadi beberapa bagian dengan ukuran:

1 MB / chunk

Jika sebagian chunk sudah tersedia di server, uploader akan melewati chunk tersebut:

Chunk 1/10 dilewati (sudah ada)
Chunk 2/10 dilewati (sudah ada)
Chunk 3/10 terkirim

Hal ini membantu melanjutkan proses upload tanpa harus mengirim ulang seluruh file.

---

♻️ Duplicate Detection

Sebelum upload, program menghitung MD5 hash file.

Contoh:

MD5 hash: 4f7c2f8bxxxxxxxxxxxxxxxxxxxxxxxx

Hash tersebut digunakan untuk mengecek apakah file yang sama sudah tersedia di server.

Jika terdeteksi:

File duplikat terdeteksi di server.

Uploader akan mencoba mengambil URL file yang sudah ada.

---

📏 File Size Limit

Maximum file size:

250 MB

Jika file melebihi batas:

Ukuran file ... bytes melampaui limit 250 MB.

Upload akan dihentikan.

---

⚙️ Configuration

Beberapa konfigurasi utama terdapat di bagian atas "uploader.py":

BASE_URL = "https://sfile.co"

CHUNK_SIZE = 1024 * 1024

MAX_FILE_SIZE = 250 * 1024 * 1024

Chunk Size

Default:

1 MB

Secara Python:

CHUNK_SIZE = 1024 * 1024

Maximum File Size

Default:

250 MB

Secara Python:

MAX_FILE_SIZE = 250 * 1024 * 1024

---

🧪 Examples

Upload ZIP

python uploader.py BaimTools.zip

Upload APK

python uploader.py aplikasi.apk

Upload dengan deskripsi

python uploader.py aplikasi.apk "Baim Market Android Release"

Upload file dari path

Windows:

python uploader.py "C:\Users\User\Downloads\file.zip"

Linux:

python uploader.py "/home/user/Downloads/file.zip"

Termux:

python uploader.py "/sdcard/Download/file.zip"

---

❗ Troubleshooting

"ModuleNotFoundError: No module named 'requests'"

Install Requests:

pip install requests

Jika menggunakan Linux:

pip3 install requests

---

"File tidak ada"

Pastikan path file benar.

Contoh:

ls

Kemudian jalankan:

python uploader.py nama-file.zip

---

Upload gagal dengan HTTP 5xx

Server sedang mengembalikan server error.

Uploader otomatis mencoba melakukan 1x retry untuk error HTTP 5xx.

Jika tetap gagal, coba upload kembali beberapa saat kemudian.

---

URL tidak terbaca

Jika semua chunk berhasil tetapi response server tidak memberikan URL yang dikenali, program akan menampilkan:

Upload selesai, URL tidak terbaca di response.

Dalam kondisi ini file mungkin sudah diproses oleh server, tetapi endpoint tidak memberikan format response yang dikenali oleh uploader.

---

🔐 Privacy

Program ini tidak meminta username atau password SFile.

File dikirim langsung ke endpoint upload SFile menggunakan HTTP request.

Jangan upload file yang berisi:

- Password
- API key
- Token
- Private key
- Data pribadi
- Informasi rahasia

---

⚠️ Disclaimer

Baim Market Uploader adalah project pihak ketiga untuk mempermudah proses upload file.

Project ini tidak berafiliasi secara resmi dengan SFile.co.

Pastikan file yang kamu upload tidak melanggar hukum, hak cipta, atau aturan layanan platform tujuan.

---

📜 License

Gunakan dan modifikasi project ini sesuai kebutuhan kamu.

Jika melakukan redistribusi atau modifikasi, disarankan tetap mencantumkan credit asli project.

---

👤 Author

Baim Market

Project:

Baim Market Uploader

Made with Python 🐍
