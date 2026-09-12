# Proyek Akhir: Menyelesaikan Permasalahan Dropout Siswa - Jaya Jaya Institut

## Business Understanding

Jaya Jaya Institut adalah institusi pendidikan perguruan tinggi yang telah berdiri sejak tahun 2000 dan telah mencetak banyak lulusan berkualitas. Namun, institusi ini menghadapi masalah **tingkat dropout siswa yang tinggi**, yang berdampak pada reputasi, efisiensi operasional, dan keberhasilan misi pendidikan institusi.

### Permasalahan Bisnis
1. Berapa proporsi siswa yang dropout, masih aktif (enrolled), dan lulus (graduate)?
2. Faktor apa saja (akademik, finansial, demografis) yang paling memengaruhi risiko dropout?
3. Bagaimana mendeteksi siswa berisiko dropout sedini mungkin agar dapat diberikan bimbingan khusus?

### Cakupan Proyek
- Data understanding & exploratory data analysis (EDA) atas data performa siswa.
- Data preparation (encoding target biner, split train/test, standardisasi).
- Pemodelan machine learning (Logistic Regression sebagai baseline, Random Forest sebagai model final) untuk memprediksi risiko dropout.
- Evaluasi model (accuracy, F1-score, ROC-AUC, feature importance).
- Business dashboard untuk memonitor performa siswa (Metabase).
- Prototype sistem prediksi berbasis Streamlit, di-deploy ke Streamlit Community Cloud.
- Rekomendasi action items berbasis data.

### Persiapan

**Sumber data:** [Students' Performance Dataset](https://github.com/dicodingacademy/dicoding_dataset/tree/main/students_performance) — UCI Machine Learning Repository (Realinho, Vieira Martins, Machado, Baptista, 2021), berisi 4.424 baris data siswa dengan 36 fitur dan target `Status` (Dropout / Enrolled / Graduate).

**Setup environment:**
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Menjalankan notebook:**
```bash
jupyter notebook notebook.ipynb
```

---

## Business Dashboard

Dashboard dibuat menggunakan **Metabase** untuk membantu tim manajemen Jaya Jaya Institut memonitor performa siswa secara berkelanjutan. Dashboard menampilkan:
- Distribusi status siswa (Dropout / Enrolled / Graduate).
- Tren dropout berdasarkan program studi (Course).
- Hubungan status pembayaran SPP (Tuition fees) dan status Debtor terhadap tingkat dropout.
- Hubungan performa akademik semester 1 & 2 (jumlah mata kuliah lulus, rata-rata nilai) terhadap status dropout.
- Distribusi dropout berdasarkan kepemilikan beasiswa dan usia saat mendaftar.

**Cara mengakses:**
1. Jalankan Metabase melalui Docker:
   ```bash
   docker run -d -p 3000:3000 --name metabase metabase/metabase
   ```
2. Salin berkas `metabase.db.mv.db` yang disertakan pada submission ini ke folder `metabase-data` container, atau restore database instance sesuai dokumentasi Metabase, lalu jalankan ulang container agar dashboard yang sudah dibuat langsung termuat.
3. Buka `http://localhost:3000` pada browser.
4. Login menggunakan kredensial berikut:
   - **Email:** root@mail.com
   - **Password:** root123

> Catatan: File screenshot dashboard tersedia pada folder `username_dicoding-dashboard/`.

---

## Menjalankan Sistem Machine Learning (Prototype)

Prototype prediksi risiko dropout dibangun dengan **Streamlit**, memanfaatkan model `RandomForestClassifier` yang telah dilatih pada `notebook.ipynb` dan disimpan pada folder `model/`.

### Menjalankan secara lokal
```bash
pip install -r requirements.txt
streamlit run app.py
```
Aplikasi akan terbuka otomatis di `http://localhost:8501`.

### Menjalankan di Streamlit Community Cloud
1. Push seluruh isi folder submission (`app.py`, `model/`, `requirements.txt`) ke repository GitHub.
2. Buka [share.streamlit.io](https://share.streamlit.io), hubungkan akun GitHub.
3. Pilih repository, branch, dan file utama `app.py`, lalu klik **Deploy**.
4. Setelah proses build selesai, aplikasi dapat diakses secara publik.

**Link prototype (Streamlit Community Cloud):**
`<isi dengan URL hasil deployment Anda, contoh: https://username-jayajaya-dropout.streamlit.app>`

---

## Conclusion

Berdasarkan analisis data dan pemodelan pada `notebook.ipynb`:

1. **Tingkat dropout Jaya Jaya Institut cukup tinggi (±32%)** dari total siswa pada dataset — menjadi masalah prioritas yang perlu ditangani serius.
2. **Performa akademik di semester-semester awal** (jumlah mata kuliah yang berhasil diselesaikan dan rata-rata nilai semester 1 & 2) adalah faktor paling dominan dalam memprediksi dropout. Siswa yang kesulitan sejak awal perkuliahan berisiko tinggi untuk dropout.
3. **Faktor finansial** — status tunggakan (Debtor) dan status pembayaran SPP yang belum lunas — terbukti berkorelasi kuat dengan dropout.
4. **Beasiswa membantu retensi siswa**; siswa penerima beasiswa memiliki tingkat dropout yang lebih rendah.
5. Model **Random Forest** yang dikembangkan mencapai **akurasi ±89%** dan **F1-score ±0.81** dalam memprediksi risiko dropout, sehingga layak dijadikan alat bantu deteksi dini (early warning system) bagi tim akademik, meskipun keputusan akhir tetap perlu ditinjau manusia.

Solusi dashboard dan model prediksi pada proyek ini menjawab kebutuhan Jaya Jaya Institut untuk mendeteksi siswa berisiko dropout secara lebih cepat dan berbasis data, sehingga bimbingan khusus dapat diberikan secara lebih tepat sasaran dan tepat waktu.

---

## Rekomendasi Action Items

1. **Bangun sistem early-warning berbasis model prediksi.** Integrasikan model ke dalam sistem akademik agar setiap akhir semester 1, siswa dengan probabilitas dropout tinggi (>50%) otomatis ditandai untuk ditindaklanjuti oleh bagian bimbingan konseling (BK).
2. **Perkuat monitoring performa akademik di semester awal.** Karena jumlah mata kuliah lulus dan nilai semester 1–2 adalah prediktor terkuat, lakukan evaluasi akademik lebih sering (mid-semester check-in), bukan hanya di akhir semester.
3. **Perluas dukungan finansial.** Siswa dengan tunggakan SPP (Debtor) atau pembayaran belum lunas berisiko dropout tinggi — pertimbangkan skema cicilan SPP, dana darurat, atau perluasan program beasiswa berbasis kebutuhan (need-based) bagi siswa berisiko.
4. **Program pendampingan khusus untuk siswa non-tradisional** (usia masuk lebih tua, pindahan/transfer, kelas malam) karena kelompok ini menunjukkan kecenderungan risiko dropout yang berbeda dari siswa reguler.
5. **Pantau dashboard secara rutin (mingguan/bulanan)** oleh manajemen dan BK untuk melihat tren dropout per program studi, sehingga intervensi dapat difokuskan pada program studi dengan tingkat dropout tertinggi.
6. **Lakukan evaluasi ulang model secara berkala** (misalnya setiap tahun ajaran) dengan data terbaru, agar model tetap relevan mengikuti perubahan pola siswa dan kebijakan institusi.

---

## Struktur Direktori

```
submission
├── model/
│   ├── model.joblib              # Model Random Forest terlatih
│   ├── scaler.joblib             # StandardScaler
│   └── feature_names.json        # Urutan nama fitur
├── notebook.ipynb                # Notebook analisis end-to-end (sudah dijalankan)
├── app.py                        # Prototype Streamlit
├── data.csv                      # Dataset mentah
├── README.md                     # Dokumentasi proyek (berkas ini)
├── username_dicoding-dashboard/  # Screenshot dashboard Metabase
├── metabase.db.mv.db             # Database instance Metabase (isi setelah dashboard dibuat)
└── requirements.txt              # Daftar dependencies
```
