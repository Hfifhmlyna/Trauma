import streamlit as st
import pandas as pd
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SMLI - Analisis Trauma", page_icon="🛡️", layout="wide")

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

    st.markdown("### 👤 Identitas Penulis")
    c1, c2, c3 = st.columns([2, 1, 1])
    nama = c1.text_input("Nama Lengkap / Inisial", key="input_nama") 
    kelas = c3.selectbox("Kelas", ["Pilih Kelas", "7", "8", "9"], key="select_kelas")

    st.markdown("---")
    st.info("🛡️ **Trauma Narrative Assessment**")
    st.write("Silakan pilih angka yang paling menggambarkan kondisi Anda (1: Tidak Pernah, 5: Sangat Sering)")

    col1, col2 = st.columns(2)
    with col1:
        p1 = st.select_slider("1. Merasa sedih/terganggu saat membaca konflik?", options=[1, 2, 3, 4, 5], key="t1")
        p2 = st.select_slider("2. Gejolak emosi kuat setelah menulis narasi?", options=[1, 2, 3, 4, 5], key="t2")
        p3 = st.select_slider("3. Suasana hati berubah buruk saat di kelas?", options=[1, 2, 3, 4, 5], key="t3")
        p4 = st.select_slider("4. Terbebani tugas menulis tema sensitif?", options=[1, 2, 3, 4, 5], key="t4")
        p5 = st.select_slider("5. Pikiran gelisah setelah membaca narasi?", options=[1, 2, 3, 4, 5], key="t5")
    with col2:
        p6 = st.select_slider("6. Merasa tidak aman atau cemas?", options=[1, 2, 3, 4, 5], key="t6")
        p7 = st.select_slider("7. Menyalahkan diri sendiri atas perasaan negatif?", options=[1, 2, 3, 4, 5], key="t7")
        p8 = st.select_slider("8. Merasa tegang atau kaku saat menulis?", options=[1, 2, 3, 4, 5], key="t8")
        p9 = st.select_slider("9. Mudah marah atau sulit fokus?", options=[1, 2, 3, 4, 5], key="t9")
        p10 = st.select_slider("10. Merasa asing dari perasaan sendiri?", options=[1, 2, 3, 4, 5], key="t10")

    if st.button("Analisis & Kirim Laporan 🚀"):
        if nama and kelas != "Pilih Kelas":
            total_skor = p1+p2+p3+p4+p5+p6+p7+p8+p9+p10
            if total_skor >= 38: hasil = "Tinggi"
            elif total_skor >= 22: hasil = "Sedang"
            else: hasil = "Rendah"

            new_data = pd.DataFrame([[nama, hasil, total_skor]], columns=["Nama", "Level_Trauma", "Skor"])
            header_status = not os.path.exists('data_tugas.csv')
            new_data.to_csv('data_tugas.csv', mode='a', index=False, header=header_status)
            
            st.success(f"Berhasil dikirim! Skor Anda: {total_skor} ({hasil})")
            st.balloons()
        else:
            st.warning("Mohon isi nama dan pilih kelas!")

# --- LOGIKA TAMPILAN GURU ---
elif role == "Guru (Administrator)":
    st.markdown("<h1 style='color: #117A65;'>🔐 Dashboard Analisis Trauma Siswa</h1>", unsafe_allow_html=True)
    
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

    # Kunci Keamanan: Data HANYA muncul jika password benar DAN tombol login diklik
    if st.session_state.get('authenticated', False) and password == "kelompok4":
        if os.path.exists('data_tugas.csv'):
            df = pd.read_csv('data_tugas.csv')
            
            if 'Level_Trauma' in df.columns:
                st.subheader("📊 Rekapitulasi & Statistik")
                counts = df['Level_Trauma'].value_counts()
                
                # Metric
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Siswa", len(df))
                m2.metric("Tinggi 🔴", counts.get("Tinggi", 0))
                m3.metric("Sedang 🟡", counts.get("Sedang", 0))
                m4.metric("Rendah 🟢", counts.get("Rendah", 0))

                # 2. GRAFIK (Batang & Kurva Halus)
                col_kiri, col_kanan = st.columns(2)
                with col_kiri:
                    st.write("**Grafik Batang:**")
                    st.bar_chart(counts)
                
                with col_kanan:
                    st.write("**Kurva Sebaran Halus (Trend):**")
                    if len(df) > 1: # Kurva hanya muncul jika data lebih dari 1
                        # Membuat kurva distribusi (Smooth Curve)
                        fig = ff.create_distplot([df['Skor']], ['Skor Siswa'], bin_size=2, show_hist=False)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Butuh minimal 2 data siswa untuk membentuk kurva.")

                # Tabel
                st.write("**Data Detail:**")
                st.dataframe(df, use_container_width=True)

                # Tombol Reset
                if st.button("🗑️ Reset Database"):
                    os.remove('data_tugas.csv')
                    st.session_state['authenticated'] = False
                    st.rerun()
            else:
                st.error("Data CSV tidak valid.")
        else:
            st.info("Belum ada data masuk dari siswa.")
    else:
        st.info("Masukkan password dan klik 'Buka Dashboard' untuk mengakses data.")

