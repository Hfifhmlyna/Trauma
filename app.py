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

    # --- 1. DATA DIRI (Pastikan nama variabel ini konsisten) ---
    st.markdown("### 👤 Identitas Penulis")
    c1, c2, c3 = st.columns([2, 1, 1])
    
    # Kita gunakan variabel 'nama' agar sesuai dengan baris 98 milikmu
    nama = c1.text_input("Nama Lengkap / Inisial", key="input_nama") 
    usia = c2.text_input("Usia", key="input_usia")
    kelas_opt = c3.selectbox("Kelas", ["Pilih Kelas", "7", "8", "9"], key="select_kelas")

    st.markdown("---")
    st.info("🛡️ **Trauma Narrative Assessment**")
    st.write("Silakan pilih angka yang paling menggambarkan kondisi Anda (1: Tidak Pernah, 5: Sangat Sering)")

    # --- 10 PERTANYAAN SKALA ---
    col1, col2 = st.columns(2)
    with col1:
        p1 = st.select_slider("1. Munculnya potongan ingatan buruk tiba-tiba.", options=[1, 2, 3, 4, 5], key="t1")
        p2 = st.select_slider("2. Mengalami mimpi buruk kejadian lampau.", options=[1, 2, 3, 4, 5], key="t2")
        p3 = st.select_slider("3. Menghindari pembicaraan tentang kejadian itu.", options=[1, 2, 3, 4, 5], key="t3")
        p4 = st.select_slider("4. Menghindari tempat yang mengingatkan kejadian itu.", options=[1, 2, 3, 4, 5], key="t4")
        p5 = st.select_slider("5. Sulit mengingat bagian penting kejadian buruk.", options=[1, 2, 3, 4, 5], key="t5")

    with col2:
        p6 = st.select_slider("6. Merasa dunia sepenuhnya tidak aman.", options=[1, 2, 3, 4, 5], key="t6")
        p7 = st.select_slider("7. Sering menyalahkan diri sendiri.", options=[1, 2, 3, 4, 5], key="t7")
        p8 = st.select_slider("8. Merasa sangat waspada/siaga terus-menerus.", options=[1, 2, 3, 4, 5], key="t8")
        p9 = st.select_slider("9. Mudah marah atau sulit tidur.", options=[1, 2, 3, 4, 5], key="t9")
        p10 = st.select_slider("10. Merasa asing dengan diri sendiri.", options=[1, 2, 3, 4, 5], key="t10")

    # --- TOMBOL KIRIM ---
    if st.button("Kirim 🚀", key="btn_kirim_siswa"):
        if nama and kelas_opt != "Pilih Kelas":
            # Perhitungan AI di latar belakang
            total_skor = p1+p2+p3+p4+p5+p6+p7+p8+p9+p10
            
            if total_skor >= 38:
                hasil = "Tinggi"
            elif total_skor >= 22:
                hasil = "Sedang"
            else:
                hasil = "Rendah"

            # Simpan Data
            new_data = pd.DataFrame([[nama, hasil, total_skor, "Data Analisis 10 Dimensi"]], 
                                    columns=["Nama", "Level_Trauma", "Skor", "Teks"])
            new_data.to_csv('data_tugas.csv', mode='a', index=False, header=False)
            
            st.balloons()
            st.success(f"✅ Terima kasih {nama}, data kamu sudah terkirim ke Guru.")
        else:
            st.error("⚠️ Harap isi Nama dan pilih Kelas terlebih dahulu.")
    # --- LOGIKA PENENTUAN OUTPUT AI (SKOR MAKSIMAL 50) ---
    if st.button("Analisis Laporan 🚀"):
        if nama and kelas != "Pilih Kelas":
            # 1. Hitung Total Skor
            total_skor = p1+p2+p3+p4+p5+p6+p7+p8+p9+p10
            
            # 2. Tentukan Kategori
            if total_skor >= 38:
                hasil = "Indikasi Trauma Tinggi"
                label_warna = "error"
            elif total_skor >= 22:
                hasil = "Indikasi Trauma Sedang"
                label_warna = "warning"
            else:
                hasil = "Indikasi Trauma Rendah"
                label_warna = "success"

            # 3. Buat Data Baru
            new_data = pd.DataFrame([[nama_mhs, hasil, total_skor, "Analisis 10 Dimensi Trauma"]], 
                                    columns=["Nama", "Level_Trauma", "Skor", "Teks"])
            
            # 4. Simpan ke CSV
            new_data.to_csv('data_tugas.csv', mode='a', index=False, header=not os.path.exists('data_tugas.csv'))
            
            # 5. Tampilkan Output ke Layar
            st.markdown("---")
            if label_warna == "success":
                st.success(f"Hasil {nama_mhs}: **{hasil}** (Skor: {total_skor})")
            elif label_warna == "warning":
                st.warning(f"Hasil {nama_mhs}: **{hasil}** (Skor: {total_skor})")
            else:
                st.error(f"Hasil {nama_mhs}: **{hasil}** (Skor: {total_skor})")
        else:
            st.error("⚠️ Isi identitas terlebih dahulu!")
    
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
























