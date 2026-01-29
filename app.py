import streamlit as st
import pandas as pd
import os
import csv

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SMLI - Kelompok 4", page_icon="🔐", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #4A90E2;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #357ABD; border: none; color: white; }
    .footer { text-align: center; color: gray; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE KATA KUNCI ---
keywords_trauma = ["lelah", "semuanya", "sakit", "takut", "sendiri", "hancur", "gelap", "sesak", "menangis"]

# --- SIDEBAR NAVIGASI ---
with st.sidebar:
    st.title("🛡️ Sistem SMLI")
    st.markdown("---")
    role = st.selectbox("Masuk Sebagai:", ["Siswa (Menulis)", "Guru (Administrator)"])
    st.markdown("---")
    st.info("Kelompok 4 - Integrasi AI Trauma-Informed")

# --- LOGIKA TAMPILAN SISWA (VERSI SESUAI GAMBAR) ---
if role == "Siswa (Menulis)":
    st.markdown("<h1 style='color: #2E86C1;'>📝 Aktivitas Menulis Narasi Inklusif</h1>", unsafe_allow_html=True)
    st.write("Jawablah pertanyaan di bawah ini berdasarkan pengalaman dan perasaanmu.")

    # Data Diri Card
    with st.container():
        st.markdown("### 👤 Data Diri")
        col1, col2, col3 = st.columns(3)
        nama = col1.text_input("Nama Lengkap / Inisial", placeholder="Contoh: Budi S.")
        usia = col2.text_input("Usia", placeholder="Contoh: 14")
        kelas = col3.selectbox("Kelas", ["Pilih Kelas", "7", "8", "9"])

    st.markdown("---")

    # PERTANYAAN #1 (Cerita)
    st.info("CERITA")
    q1 = st.text_area("**#1** Ceritakan pengalaman paling menyedihkan atau menakutkan yang pernah kamu alami baru-baru ini.", placeholder="Tulis jawabanmu di sini...", height=150)

    # PERTANYAAN #2 (Cerita)
    st.info("CERITA")
    q2 = st.text_area("**#2** Bagaimana perasaanmu ketika mengingat kejadian tersebut?", placeholder="Tulis jawabanmu di sini...", height=150)

    # PERTANYAAN #3 (Cerita)
    st.info("CERITA")
    q3 = st.text_area("**#3** Apa yang biasanya kamu lakukan ketika merasa sedih atau takut?", placeholder="Tulis jawabanmu di sini...", height=150)

    st.markdown("---")

    # PERTANYAAN #4 (Perasaan - Skala)
    st.warning("PERASAAN")
    st.write("**#4** Saya sering merasa cemas tanpa alasan yang jelas.")
    q4 = st.radio("Skala Kecemasan:", [1, 2, 3, 4, 5], horizontal=True, key="q4", help="1: Tidak Pernah, 5: Sering")

    # PERTANYAAN #5 (Cerita)
    st.info("CERITA")
    q5 = st.text_area("**#5** Ceritakan tentang hubunganmu dengan orang-orang di sekitarmu (keluarga/teman) akhir-akhir ini.", height=150)

    # PERTANYAAN #6 (Perasaan - Skala)
    st.warning("PERASAAN")
    st.write("**#6** Saya merasa sulit tidur atau sering mimpi buruk.")
    q6 = st.radio("Skala Gangguan Tidur:", [1, 2, 3, 4, 5], horizontal=True, key="q6", help="1: Tidak Pernah, 5: Sering")

    if st.button("Kirim Laporan Narasi"):
        if nama and q1 and q2:
            # Gabungkan input teks untuk deteksi AI
            teks_gabungan = f"{q1} {q2} {q3} {q5} (Skala Cemas: {q4}, Skala Tidur: {q6})"
            
            # Analisis AI sederhana (Keyword Matching)
            found = [w for w in keywords_trauma if w in teks_gabungan.lower()]
            # Tambahan logika: Jika skala 4 atau 5, otomatis dianggap sensitif
            is_sensitif = len(found) >= 1 or q4 >= 4 or q6 >= 4
            label = "1 (Sensitif)" if is_sensitif else "0 (Normal)"
            
            # Simpan ke CSV
            new_data = pd.DataFrame([[nama, teks_gabungan, label, ", ".join(found)]], 
                                    columns=["Nama", "Teks", "Label", "Keywords"])
            new_data.to_csv('data_tugas.csv', mode='a', index=False, header=not os.path.exists('data_tugas.csv'))
            
            st.success("✅ Data berhasil dikirim. Terima kasih sudah berbagi cerita dengan jujur.")
            if is_sensitif:
                st.info("❤️ Kamu adalah siswa yang berani. Jangan ragu untuk berbicara dengan guru jika merasa berat.")
        else:
            st.error("Mohon isi Nama dan minimal pertanyaan cerita #1 dan #2.")

# --- LOGIKA TAMPILAN GURU ---
elif role == "Guru (Administrator)":
    st.markdown("<h1 style='color: #117A65;'>🔐 Dashboard Monitoring Guru</h1>", unsafe_allow_html=True)
    password = st.text_input("Masukkan Password Admin:", type="password")
    
    if password == "kelompok4":
        st.success("Akses Diterima. Halo Bapak/Ibu Guru.")
        
        if os.path.exists('data_tugas.csv'):
            df_master = pd.read_csv('data_tugas.csv')
            total_data = len(df_master)
            jml_sensitif = len(df_master[df_master['Label'] == "1 (Sensitif)"])
            jml_normal = len(df_master[df_master['Label'] == "0 (Normal)"])

            c1, c2, c3 = st.columns(3)
            c1.metric("Total Tugas", f"{total_data} Siswa")
            c2.metric("Sensitif", f"{jml_sensitif}")
            c3.metric("Normal", f"{jml_normal}")

            st.markdown("---")
            st.write("**Daftar Tulisan Siswa:**")
            st.dataframe(df_master, use_container_width=True)

            if total_data > 0:
                st.subheader("📈 Analisis Sebaran Data Real-Time")
                persen_sensitif = (jml_sensitif / total_data) * 100
                persen_normal = (jml_normal / total_data) * 100

                rekap_data = {
                    "Kategori Klasifikasi": ["1 (Sensitif)", "0 (Normal)", "TOTAL"],
                    "Jumlah Data": [jml_sensitif, jml_normal, total_data],
                    "Persentase": [f"{persen_sensitif:.1f}%", f"{persen_normal:.1f}%", "100%"]
                }
                st.table(pd.DataFrame(rekap_data))

                st.markdown("---")
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    csv_data = df_master.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Download CSV", csv_data, "laporan_smli.csv", "text/csv")
                with col_btn2:
                    if st.button("🗑️ Hapus Semua Data"):
                        with open('data_tugas.csv', mode='w', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow(["Nama", "Teks", "Label", "Keywords"])
                        st.rerun()
        else:
            st.info("Belum ada data masuk.")
    elif password != "":
        st.error("Password salah!")

st.markdown("<div class='footer'>Sistem Monitoring Literasi Inklusif © 2026 Kelompok 4</div>", unsafe_allow_html=True)

