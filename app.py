import streamlit as st
import pandas as pd
import os
import plotly.figure_factory as ff

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SMLI - Analisis Trauma", page_icon="🛡️", layout="wide")

# --- DATABASE KATA KUNCI TRAUMA (NLP Dasar) ---
# Tambahkan kata kunci di sini agar AI bisa mendeteksinya
keywords_trauma = ["lelah", "sakit", "takut", "sendiri", "hancur", "gelap", "sesak", "menangis", "teriak", "benci", "trauma", "mati", "putus asa", "cemas"]

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
    
    # BAGIAN A: SOAL NARASI (NLP)
    st.markdown("### ✍️ Menulis Narasi Sesuai Perasaan")
    st.info("Tuliskan jawabanmu dalam bentuk kalimat.")
    
    q_nlp1 = st.text_area("1. Tuliskan secara singkat sebuah pengalaman pribadi atau cerita sedih yang pernah kamu alami.", key="nlp1")
    q_nlp2 = st.text_area("2. Dari cerita yang baru saja kamu tulis, bagian mana yang paling membuatmu merasa tidak nyaman? Apa yang kamu rasakan saat mengingatnya?", key="nlp2")
    q_nlp3 = st.text_area("3. Bagaimana perasaanmu sekarang setelah berhasil menuangkan pengalaman sedih tersebut ke dalam bentuk tulisan?", key="nlp3")
    q_nlp4 = st.text_area("4. Jika kamu adalah tokoh utama dalam cerita yang baru saja kamu tulis, kata apa yang paling tepat untuk menggambarkan rasa sakitmu?", key="nlp4")
    q_nlp5 = st.text_area("5. Saat menuliskan cerita tadi, jika dihubungkan dengan tema keluarga, pikiran atau kenangan apa yang tiba-tiba muncul di kepalamu?", key="nlp5")

    # BAGIAN B: SOAL OPSI (STATISTIK)
    st.markdown("---")
    st.markdown("### 🛡️ Penilaian Mandiri (Skala 1-5)")
    st.write("1: Tidak Pernah, 5: Sangat Sering")
    
    col_kiri, col_kanan = st.columns(2)
    with col_kiri:
        o1 = st.select_slider("1. Ingin berhenti membaca saat cerita mulai menyakitkan?", options=[1, 2, 3, 4, 5], key="o1")
        o2 = st.select_slider("2. Detak jantung bertambah cepat saat menulis diri sendiri?", options=[1, 2, 3, 4, 5], key="o2")
        o3 = st.select_slider("3. Pikiran mendadak 'kosong' karena teringat hal sedih?", options=[1, 2, 3, 4, 5], key="o3")
    
    with col_kanan:
        o4 = st.select_slider("4. Merasa tokoh cerita sedih adalah cerminan dirimu?", options=[1, 2, 3, 4, 5], key="o4")
        o5 = st.select_slider("5. Merasa lelah fisik setelah tugas menulis emosional?", options=[1, 2, 3, 4, 5], key="o5")

    # --- PROSES GABUNGAN (Hanya 1 Tombol Utama) ---
    if st.button("Analisis & Kirim Laporan 🚀"):
        if nama and kelas != "Pilih Kelas" and q_nlp1:
            # 1. Gabungkan semua narasi untuk dianalisis NLP
            teks_lengkap = f"{q_nlp1} {q_nlp2} {q_nlp3} {q_nlp4} {q_nlp5}".lower()
            
            # 2. Logika NLP: Mencari kata kunci
            kata_terdeteksi = [k for k in keywords_trauma if k in teks_lengkap]
            bonus_nlp = len(kata_terdeteksi) * 2 
            
            # 3. Hitung skor total
            skor_slider = o1 + o2 + o3 + o4 + o5
            total_akhir = skor_slider + bonus_nlp
            
            # 4. Penentuan Level
            if total_akhir >= 25: hasil = "Tinggi"
            elif total_akhir >= 15: hasil = "Sedang"
            else: hasil = "Rendah"
            
            # 5. Simpan ke CSV
            new_row = pd.DataFrame([[nama, kelas, hasil, total_akhir, teks_lengkap, ", ".join(kata_terdeteksi)]], 
                                    columns=["Nama", "Kelas", "Level_Trauma", "Skor", "Narasi", "Keywords_NLP"])
            
            new_row.to_csv('data_tugas.csv', mode='a', index=False, header=not os.path.exists('data_tugas.csv'))
            
            st.success(f"Analisis Selesai! Skor Total: {total_akhir} ({hasil})")
            if kata_terdeteksi:
                st.warning(f"AI Mendeteksi emosi: {', '.join(kata_terdeteksi)}")
            st.balloons()
        else:
            st.error("Mohon lengkapi Nama, Kelas, dan minimal soal narasi nomor 1.")
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
    if 'Keywords_NLP' in df.columns:
                st.subheader("🔍 Kata Kunci Dominan (Hasil NLP)")
                all_keywords = df['Keywords_NLP'].str.cat(sep=', ')
                st.write(f"Siswa paling banyak menyebutkan: **{all_keywords}**")
        
    if st.session_state.get('authenticated', False) and password == "kelompok4":
        if os.path.exists('data_tugas.csv'):
            df = pd.read_csv('data_tugas.csv')
            
            if 'Level_Trauma' in df.columns:
                st.subheader("📊 Rekapitulasi & Statistik")
                counts = df['Level_Trauma'].value_counts()
                
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Siswa", len(df))
                m2.metric("Tinggi 🔴", counts.get("Tinggi", 0))
                m3.metric("Sedang 🟡", counts.get("Sedang", 0))
                m4.metric("Rendah 🟢", counts.get("Rendah", 0))

                # 2. GRAFIK
                col_kiri, col_kanan = st.columns(2)
                with col_kiri:
                    st.write("**Grafik Batang:**")
                    st.bar_chart(counts)
                
                with col_kanan:
                    st.write("**Kurva Sebaran Halus (Trend):**")
                    if len(df) > 1: 
                        try:
                            # Menggunakan fig_factory untuk kurva distribusi
                            fig = ff.create_distplot([df['Skor']], ['Skor Siswa'], bin_size=2, show_hist=False)
                            st.plotly_chart(fig, use_container_width=True)
                        except:
                            st.warning("Data belum cukup bervariasi untuk membentuk kurva.")
                    else:
                        st.info("Butuh minimal 2 data siswa untuk membentuk kurva.")

               # 3. TABEL DETAIL
                st.write("**Data Detail:**")
                def color_level(val):
                    color = 'red' if val == 'Tinggi' else 'orange' if val == 'Sedang' else 'green'
                    return f'color: {color}; font-weight: bold'
                
                st.dataframe(df.style.map(color_level, subset=['Level_Trauma']), use_container_width=True)

                # --- TAMBAHKAN BAGIAN DOWNLOAD DI SINI ---
                st.markdown("---")
                col_dl, col_rs = st.columns(2)
                
                with col_dl:
                    # Konversi dataframe ke CSV untuk didownload
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Laporan (CSV)",
                        data=csv_data,
                        file_name='laporan_analisis_trauma.csv',
                        mime='text/csv',
                    )
                
                with col_rs:
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










