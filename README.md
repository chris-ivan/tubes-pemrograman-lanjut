# Prediksi Harga Tiket Cinema
## Tugas Besar ET3107 Pemrograman Lanjut

### Anggota Kelompok
- [18119025] Christopher Ivan Gunardi
- [18119026] Farhan Krishna

### Latar Belakang
Untuk memberi dampak positif pada produsen dan penonton film, sebaiknya harga untuk setiap film tidak diatur sama rata seperti di bioskop, namun diatur berdasarkan faktor-faktor seperti: waktu pemesanan, supply-demand, ketertarikan publik, waktu menonton, dan lain-lain. Dari korelasi-korelasi ini dapat diprediksi harga yang sesuai untuk sebuah judul film.

### Instalasi
1. Install `Python` dan `pip` (jika belum ada)
2. Install library yang dibutuhkan dalam `requirements.txt` dengan menjalankan `pip install -r requirements.txt`
3. Karena adanya keterbatasan ukuran file di Github, file model hasil training perlu ditambahkan manual dengan menjalankan script pada file [Google Colab ini](ttps://colab.research.google.com/drive/1hxfp7g_F0HbCBJRoUrY2oBEL8IDINwTc?usp=sharing). Akan didapatkan berkas `cinema_ticket_regression_model.pkl` yang perlu dimasukkan ke root folder. 
4. Untuk kebutuhan development, modifikasi `main.py`. Ubah value `port` pada baris 64 menjadi `5050` atau port yang anda inginkan.
5. Jalankan `main.py`. Pada Windows, dapat digunakan perintah `python main.py` di root folder. Silakan akses `http://localhost:5050` untuk melihat hasil eksekusi program.


### Informasi Tambahan
- Website telah dideploy menggunakan Heroku dan dapat diakses melalui [link ini](https://tubes-pemlan.herokuapp.com/)
- Informasi tambahan terkait aplikasi Machine Learning dan Analisis Data pada project ini dapat dilihat pada berkas .ipynb di [link ini](https://colab.research.google.com/drive/1hxfp7g_F0HbCBJRoUrY2oBEL8IDINwTc?usp=sharing).