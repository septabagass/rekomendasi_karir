# 🎓 Dashboard Analitik MatchStep AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]([https://namalinkdeploymentanda.streamlit.app](https://rekomendasi-karir-mahasiswa.streamlit.app/))
*(Klik tombol di atas untuk mengakses dashboard secara langsung)*

Sebuah *dashboard* interaktif yang dibangun menggunakan **Streamlit** untuk mengeksplorasi dan menganalisis korelasi antara pola keterampilan mahasiswa (berdasarkan *self-assessment*) dengan target spesialisasi karier mereka di bidang Teknologi Informasi (TI).

Dashboard ini merupakan bagian dari proyek **MatchStep AI**, sebuah sistem rekomendasi karier berbasis *Deep Learning* yang dirancang untuk membantu mahasiswa memetakan potensi diri mereka secara presisi.

---

## ✨ Fitur Utama

Dashboard ini memvisualisasikan data ke dalam 4 bagian analitik utama:
1. **Overview Demografi & Kepemimpinan:** Menampilkan sebaran target karier mahasiswa dan proporsi pengalaman kepemimpinan mereka (dalam bentuk *Bar Chart* dan *Pie Chart*).
2. **Profil Bahasa Pemrograman:** *Heatmap* interaktif yang memetakan korelasi antara penguasaan 10 bahasa pemrograman (Python, Java, C++, dll.) terhadap probabilitas target karier tertentu.
3. **Pemetaan Hard Skill:** Visualisasi menggunakan *Heatmap* untuk membandingkan 4 kompetensi inti (*Software Dev, Database, Networking, Web Dev*) pada masing-masing spesialisasi karier.
4. **Distribusi Soft Skill Utama:** *Boxplot* yang membandingkan secara langsung tingkat kecakapan *soft skill* kunci (Komunikasi, *Problem Solving*, dan *Teamwork*) antara mahasiswa di jalur **Manajerial & Analis** melawan jalur **Teknis Murni**.

**Fitur Interaktif:**
- ⚙️ **Filter Dinamis:** Pengguna dapat memfilter data berdasarkan kombinasi "Target Karier" secara bebas melalui panel *sidebar*.
- 📊 **Grafik Responsif:** Tinggi grafik akan menyesuaikan secara otomatis (*auto-scaling*) berdasarkan jumlah data yang difilter agar visualisasi tidak bertumpuk dan teks tetap terbaca dengan jelas.

---

## 🛠️ Teknologi yang Digunakan

- **Python 3.x**
- **[Streamlit](https://streamlit.io/):** Framework untuk membangun antarmuka *dashboard* web secara cepat.
- **[Pandas](https://pandas.pydata.org/):** Pustaka andalan untuk manipulasi, prapemrosesan, dan agregasi data (*Data Wrangling*).
- **[Plotly Express](https://plotly.com/python/):** Pembuatan visualisasi grafik analitik yang modern, dinamis, dan interaktif.

---

## 📂 Struktur File

```text
📁 rekomendasi_karir/
│
├── 📁 dashboard/
|   ├── Logo.png                 # Aset gambar logo untuk sidebar
|   ├── dashboard.py             # File kode utama program Streamlit
|   ├── dataset.csv              # Dataset mentah awal
│   └── dataset_bersih.csv       # Dataset bersih (format separator ';')
│
├── README.md                    # Dokumentasi proyek
└── requirements.txt             # Daftar library yang dibutuhkan (streamlit, pandas, plotly)
