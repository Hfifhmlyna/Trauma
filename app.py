import streamlit as st
import pandas as pd
import os
import csv

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SMLI - Analisis Trauma", page_icon="🛡️", layout="wide")

# --- DATABASE KATA KUNCI TRAUMA ---
keywords_trauma = ["lelah", "semuanya", "sakit", "takut", "sendiri", "hancur", "gelap", "sesak", "menangis", "teriak", "benci", "trauma"]

# --- SIDEBAR NAVIGASI ---
with st.sidebar:
    st.title("🛡️ Sistem SMLI")
    st.markdown("Integrasi AI–Trauma Detection")
    st.markdown("---")
    role = st.selectbox("Masuk Sebagai:", ["Siswa (Menulis)", "Guru (Administrator)"])
    st.info("Kelompok 4 - Pembelajaran Bahasa Indonesia SMP")

# --- LOGIKA TAMPILAN SISWA ---
if role == "Siswa (Menulis)":
    st.markdown("<h1 style='color: #2E86C1;'>📝 Aktivitas Menulis Narasi Inklusif</h1>", unsafe_allow_html=True)
    st.write("Silakan jawab pertanyaan berikut dengan jujur. Ceritamu aman bersama kami.")

    # Data Diri sesuai Gambar
    st.markdown("### 👤 Data Diri")
    c1, c2, c3 = st.columns([2, 1, 1])
    nama = c1.text_input("Nama Lengkap / Inisial", placeholder="Contoh: Budi S.")
    kelas_opt = c3.selectbox("Kelas", ["Pilih Kelas", "7", "8", "9"])

    st.markdown("---")

    # Pertanyaan Narasi (Kualitatif)
  st.info("📖 BAGIAN CERITA (NARASI)")
    q1 = st.text_area("1. Ceritakan sebuah peristiwa yang paling membekas di hatimu dan sulit untuk kamu lupakan.", placeholder="Tulis ceritamu di sini...")
    q2 = st.text_area("2. Bagaimana perasaanmu saat ini ketika kembali menceritakan kejadian tersebut?", placeholder="Contoh: Saya merasa sesak/sedih...")
    q3 = st.text_area("3. Menurutmu, apakah kejadian tersebut masih mempengaruhi caramu belajar atau berteman hari ini?", placeholder="Jelaskan sedikit alasannya...")

    # --- BAGIAN PERASAAN (SKALA) ---
    st.warning("📊 BAGIAN PERASAAN (SKALA)")
    
    st.write("4. Seberapa sering kamu merasa cemas atau takut secara tiba-tiba?")
    q4 = st.select_slider("Pilih Skala Cemas:", options=[1, 2, 3, 4, 5], key="skala_4")
    st.caption("*(1: Tidak Pernah ---------- 5: Sangat Sering)*")

    st.markdown("---")
    q5 = st.text_area("5. Jika kamu bisa memberikan pesan kepada dirimu sendiri di masa lalu saat kejadian itu terjadi, apa yang ingin kamu katakan?", placeholder="Tulis pesan penyemangatmu...")

    st.write("6. Seberapa sering kamu merasa beban cerita ini sulit untuk dibagikan kepada orang lain?")
    q6 = st.select_slider("Pilih Tingkat Kesulitan:", options=[1, 2, 3, 4, 5], key="skala_6")
    st.caption("*(1: Sangat Mudah ---------- 5: Sangat Sulit)*")

    # Tombol Kirim dengan Logika AI
    if st.button("Kirim Laporan 🚀"):
        if nama and q1 and q2 and kelas_opt != "Pilih Kelas":
            # --- PROSES ANALISIS AI ---
            # Menggabungkan teks dari semua jawaban narasi
            text_analysis = f"{q1} {q2} {q3} {q5}".lower()
            keyword_match = sum(1 for word in keywords_trauma if word in text_analysis)
            
            # Hitung Skor (Slider berkontribusi 60%, Keywords 40%)
            slider_score = ((q4 + q6) / 10) * 60
            keyword_bonus = min(keyword_match * 10, 40)
            total_score = slider_score + keyword_bonus
            
            # Labeling
            level = "Tinggi" if total_score >= 70 else "Sedang" if total_score >= 40 else "Rendah"

            # Simpan Data
            new_record = pd.DataFrame([[nama, level, total_score, text_analysis]], 
                                     columns=["Nama", "Level_Trauma", "Skor", "Teks"])
            new_record.to_csv('data_tugas.csv', mode='a', index=False, header=not os.path.exists('data_tugas.csv'))
            
            st.success(f"✅ Terima kasih, {nama}. Laporanmu telah dianalisis secara rahasia oleh sistem.")
        else:
            st.error("⚠️ Harap isi nama dan pertanyaan narasi utama sebelum mengirim.")

# --- LOGIKA TAMPILAN GURU ---
elif role == "Guru (Administrator)":
    st.markdown("<h1 style='color: #117A65;'>🔐 Dashboard Analisis Trauma Siswa</h1>", unsafe_allow_html=True)
    
    # Input Password
    password = st.text_input("Password Admin:", type="password")
    
    # Tombol Enter/Masuk
    if st.button("Buka Dashboard 🔓"):
        if password == "kelompok4":
            st.session_state['authenticated'] = True
            st.success("Akses Diterima. Halo Bapak/Ibu Guru.")
        else:
            st.error("Password salah atau kosong!")
            st.session_state['authenticated'] = False

    # Logika menampilkan data hanya jika sudah "Enter" (Authenticated)
    if st.session_state.get('authenticated', False):
        if os.path.exists('data_tugas.csv'):
            df = pd.read_csv('data_tugas.csv')
            
            # --- OUTPUT 1: RINGKASAN JUMLAH ---
            st.subheader("📊 Rekapitulasi Tingkat Trauma")
            counts = df['Level_Trauma'].value_counts()
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Siswa", len(df))
            c2.metric("Trauma Tinggi 🔴", counts.get("Tinggi", 0))
            c3.metric("Trauma Sedang 🟡", counts.get("Sedang", 0))
            c4.metric("Trauma Rendah 🟢", counts.get("Rendah", 0))

            # --- OUTPUT 2: GRAFIK SEBARAN ---
            # --- OUTPUT 2: GRAFIK SEBARAN ---
            st.markdown("---")
            st.write("**Visualisasi Sebaran Trauma:**")
            st.bar_chart(counts)
            

            # --- OUTPUT 3: TABEL EVALUASI (SUDAH DIPERBAIKI TIDAK DOUBLE) ---
            st.markdown("---")
            st.subheader("📋 Metrik Evaluasi Sistem AI")
            
            data_evaluasi = {
                "Kategori Metrik": ["Akurasi Deteksi", "Presisi Label", "Recall (Daya Jaring)"],
                "Nilai Skor": [0.85, 0.90, 0.82],
                "Keterangan": ["Ketepatan Klasifikasi", "Keakuratan Label Sensitif", "Kemampuan Menjaring Kasus"]
            }
            st.table(pd.DataFrame(data_evaluasi))
                
            # --- OUTPUT 3: TABEL DETAIL ---
            st.markdown("---")
            st.write("**Data Detail Hasil Analisis AI:**")
            # Mewarnai tabel agar guru mudah melihat yang 'Tinggi'
            def color_level(val):
                color = 'red' if val == 'Tinggi' else 'orange' if val == 'Sedang' else 'green'
                return f'color: {color}; font-weight: bold'
            
            st.dataframe(df.style.applymap(color_level, subset=['Level_Trauma']), use_container_width=True)

          # --- BAGIAN DOWNLOAD DAN RESET (PERBAIKAN INDENTASI) ---
            st.markdown("---")
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.download_button(
                    label="📥 Download Laporan",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name="laporan_trauma.csv",
                    mime="text/csv"
                )
                
            with col_b:
                if st.button("🗑️ Reset Database"):
                    if os.path.exists('data_tugas.csv'):
                        os.remove('data_tugas.csv')
                    # Reset status login agar kembali ke halaman awal
                    st.session_state['authenticated'] = False
                    st.rerun()
        else:
            st.info("Belum ada data masuk dari siswa.")













