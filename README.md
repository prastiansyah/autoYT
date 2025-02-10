 YouTube Automation Script 🤖

Skrip ini digunakan untuk mengotomatisasi berbagai aksi di YouTube, seperti:
- **Login manual dan menyimpan sesi cookies** (untuk Gmail & YouTube)
- **Auto Like Video/Live Streaming YouTube** (menggunakan link dari `video.txt`)
- **Auto Comment Video YouTube**
- **Auto Like Video Short**
- **Auto Comment Video Short**
- **Auto Subscribe Channel** (menggunakan link dari `channel.txt`)

Selain itu, skrip mendukung pemilihan akun dari file cookies yang tersimpan dalam folder `cookies` dengan dua mode:
- **Pernama:** Hanya menjalankan akun tertentu berdasarkan nama.
- **Perbaris:** Menjalankan akun-akun berdasarkan range nomor urut file cookies.

## Fitur Utama

1. **Login Manual dan Simpan Cookies**  
   Melakukan login secara manual di Gmail (dalam mode incognito) dan menyimpan cookies di folder `cookies` dengan format `cookies_(accountname).pkl`.

2. **Auto Like & Comment**  
   Otomatis melakukan aksi like dan comment pada video YouTube dan Shorts, dengan file input berupa link video (`video.txt` dan `short.txt`) dan file komentar (`commentvideo.txt` dan `commentshort.txt`).

3. **Auto Subscribe Channel**  
   Membaca link channel dari `channel.txt` dan mengklik tombol subscribe menggunakan XPath `//*[@id="page-header"]`.

4. **Dukungan Multi-akun**  
   Jalankan aksi otomatis pada beberapa akun sekaligus, dengan opsi memilih akun berdasarkan nama atau berdasarkan range (perbaris) dari file cookies yang ada.

5. **Mode Headless**  
   Mendukung mode headless sehingga cocok dijalankan di VPS tanpa tampilan GUI.

## Prasyarat 🛠️

- **Python 3.6+**
- **Google Chrome**  
  Pastikan Google Chrome telah terinstall pada sistem atau VPS Anda.
- **Koneksi Internet**  
  Untuk mendownload ChromeDriver menggunakan `webdriver_manager` (pada eksekusi pertama) dan untuk login.

## Instalasi 📦

1. **Clone repository**
   git clone https://github.com/prastiansyah/autoYT.git

2. **Buat Virtual Environment** (opsional, tapi direkomendasikan):
   ```bash
   cd autoYT
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/MacOS
   # Pada Windows:
   # venv\Scripts\activate
   pip install -r requirements.txt
   python bot.py

