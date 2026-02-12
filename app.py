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
    st.markdown("<h1 style='color: #2E86C1;'>📝 Aktivitas Literasi Narasi</h1>", unsafe_allow_html=True)

    # --- 1. DATA DIRI ---
    st.markdown("### 👤 Identitas Penulis")
    c1, c2, c3 = st.columns([2, 1, 1])
    
    nama = c1.text_input("Nama Lengkap / Inisial", key="input_nama") 
    usia = c2.text_input("Usia", key="input_usia")
    kelas = c3.selectbox("Kelas", ["Pilih Kelas", "7", "8", "9"], key="select_kelas")

    st.markdown("---")
    st.info("🛡️ **Trauma Narrative Assessment**")
    st.write("Silakan pilih angka yang paling menggambarkan kondisi Anda (1: Tidak Pernah, 5: Sangat Sering)")

    # --- 10 PERTANYAAN SKALA ---
    col1, col2 = st.columns(2)
    with col1:
        p1 = st.select_slider("1. Bagaimana perasaanmu ketika membaca cerita yang mengandung konflik atau peristiwa sedih?", options=[1, 2, 3, 4, 5], key="t1")
        p2 = st.select_slider("2. Bagaimana reaksi emosimu setelah menulis narasi berdasarkan pengalaman pribadi?", options=[1, 2, 3, 4, 5], key="t2")
        p3 = st.select_slider("3. Bagaimana pengaruh isi cerita yang kamu baca terhadap suasana hatimu di kelas?", options=[1, 2, 3, 4, 5], key="t3")
        p4 = st.select_slider("4. Bagaimana caramu menghadapi tugas menulis narasi dengan tema yang sensitif?", options=[1, 2, 3, 4, 5], key="t4")
        p5 = st.select_slider("5. Bagaimana kondisi pikiran dan perasaanmu setelah menyelesaikan tugas membaca narasi?", options=[1, 2, 3, 4, 5], key="t5")

    with col2:
        p6 = st.select_slider("6. Apakah kegiatan membaca atau menulis narasi pernah membuatmu merasa tidak aman atau gelisah?", options=[1, 2, 3, 4, 5], key="t6")
        p7 = st.select_slider("7. Apakah kamu sering menyalahkan diri sendiri ketika tulisan narasimu menggambarkan perasaan negatif?", options=[1, 2, 3, 4, 5], key="t7")
        p8 = st.select_slider("8. Apakah kamu merasa terlalu tegang atau waspada saat mengikuti kegiatan menulis narasi di kelas?", options=[1, 2, 3, 4, 5], key="t8")
        p9 = st.select_slider("9. Apakah setelah membaca atau menulis cerita tertentu kamu menjadi mudah sedih, marah, atau sulit fokus?", options=[1, 2, 3, 4, 5], key="t9")
        p10 = st.select_slider("10. Apakah kegiatan menulis narasi pernah membuatmu merasa jauh atau asing dengan perasaan diri sendiri?", options=[1, 2, 3, 4, 5], key="t10")

    st.markdown("---")

    # --- TOMBOL ANALISIS & KIRIM ---
    if st.button("Analisis & Kirim Laporan 🚀", key="btn_final"):
        if nama and kelas != "Pilih Kelas":
            # 1. Hitung Total Skor
            total_skor = p1+p2+p3+p4+p5+p6+p7+p8+p9+p10
            
            # 2. Penentuan Hasil
            if total_skor >= 38:
                hasil = "Tinggi"
                st.error(f"Hasil Analisis: **Indikasi Trauma Tinggi** (Skor: {total_skor})")
            elif total_skor >= 22:
                hasil = "Sedang"
                st.warning(f"Hasil Analisis: **Indikasi Trauma Sedang** (Skor: {total_skor})")
            else:
                hasil = "Rendah"
                st.success(f"Hasil Analisis: **Indikasi Trauma Rendah** (Skor: {total_skor})")

            # 3. Siapkan Data
            new_data = pd.DataFrame([[nama, hasil, total_skor, "Analisis 10 Dimensi"]], 
                                    columns=["Nama", "Level_Trauma", "Skor", "Teks"])
            
            # 4. SIMPAN KE CSV (Baris ini yang WAJIB ada)
            header_status = not os.path.exists('data_tugas.csv')
            new_data.to_csv('data_tugas.csv', mode='a', index=False, header=header_status)
            
            st.balloons()
            st.info("✅ Data Anda telah berhasil dikirim ke Dashboard Guru.")

# --- LOGIKA TAMPILAN GURU ---
elif role == "Guru (Administrator)":
    st.markdown("<h1 style='color: #117A65;'>🔐 Dashboard Analisis Trauma Siswa</h1>", unsafe_allow_html=True)
    
    # Kotak password ditaruh di luar agar tetap terlihat
    password = st.text_input("Password Admin:", type="password")
    
    col_login, col_logout = st.columns([1, 4])
    with col_login:
        if st.button("Buka Dashboard 🔓"):
            if password == "kelompok4":
                st.session_state['authenticated'] = True
                st.success("Akses Diterima!")
            else:
                st.error("Password salah!")
                st.session_state['authenticated'] = False
    
    with col_logout:
        if st.button("Kunci Kembali 🔒"):
            st.session_state['authenticated'] = False
            st.rerun()

    st.markdown("---")

    # --- BAGIAN DATA (Hanya terbuka jika status True) ---
    if st.session_state.get('authenticated', False):
        if os.path.exists('data_tugas.csv'):
            df = pd.read_csv('data_tugas.csv')
            
            if 'Level_Trauma' in df.columns:
                # 1. PERHITUNGAN
                st.subheader("📊 Rekapitulasi & Statistik")
                counts = df['Level_Trauma'].value_counts()
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total Siswa", len(df))
                c2.metric("Tinggi 🔴", counts.get("Tinggi", 0))
                c3.metric("Sedang 🟡", counts.get("Sedang", 0))
                c4.metric("Rendah 🟢", counts.get("Rendah", 0))

                # 2. GRAFIK & KURVA
                col_kiri, col_kanan = st.columns(2)
                with col_kiri:
                    st.write("**Grafik Batang:**")
                    st.bar_chart(counts)
                with col_kanan:
                    st.write("**Kurva Sebaran:**")
                    st.area_chart(counts)

                # 3. TABEL DETAIL
                st.write("**Data Detail:**")
                def color_level(val):
                    color = 'red' if val == 'Tinggi' else 'orange' if val == 'Sedang' else 'green'
                    return f'color: {color}; font-weight: bold'
                
                st.dataframe(df.style.applymap(color_level, subset=['Level_Trauma']), use_container_width=True)
            else:
                st.error("Format data tidak sesuai.")
        else:
            st.info("Belum ada data dari siswa.")
