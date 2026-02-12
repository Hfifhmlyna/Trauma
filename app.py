import streamlit as st
import pandas as pd
import os
import plotly.figure_factory as ff

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SMLI - Analisis Trauma", page_icon="🛡️", layout="wide")

# --- DATABASE KATA KUNCI TRAUMA (NLP Dasar) ---
keywords_trauma = ["lelah", "sakit", "takut", "sendiri", "hancur", "gelap", "sesak", "menangis", "teriak", "benci", "trauma", "mati", "putus asa", "cemas", "sedih", "kecewa", "pusing", "stress", "beban"]

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
    q_nlp2 = st.text_area("2. Dari cerita tadi, bagian mana yang membuatmu merasa tidak nyaman? Apa yang kamu rasakan?", key="nlp2")
    q_nlp3 = st.text_area("3. Bagaimana perasaanmu sekarang setelah menuangkan pengalaman tersebut ke dalam tulisan?", key="nlp3")
    q_nlp4 = st.text_area("4. Jika kamu adalah tokoh utama, kata apa yang paling tepat menggambarkan rasa sakitmu?", key="nlp4")
    q_nlp5 = st.text_area("5. Saat menulis tadi, jika dihubungkan dengan tema keluarga, pikiran apa yang muncul?", key="nlp5")

    # BAGIAN B: SOAL OPSI (STATISTIK)
    st.markdown("---")
    st.markdown("### 🛡️ Penilaian Mandiri (Skala 1-5)")
    st.write("1: Tidak Pernah, 5: Sangat Sering")
    
    col_kiri, col_kanan = st.columns(2)
    with col_kiri:
        o1 = st.select_slider("1.Apakah kamu merasa ingin berhenti menulis atau membaca saat alur ceritanya mulai mengingatkanmu pada kejadian yang menyakitkan di hidupmu?", options=[1, 2, 3, 4, 5], key="o1")
        o2 = st.select_slider("2.Apakah kamu merasa detak jantungmu bertambah cepat atau tanganmu bergetar saat sedang menuliskan bagian narasi yang paling emosional?", options=[1, 2, 3, 4, 5], key="o2")
        o3 = st.select_slider("3.Apakah kamu merasa pikiranmu mendadak menjadi 'kosong' atau sulit fokus karena teringat kembali pada kejadian sedih di masa lalu?", options=[1, 2, 3, 4, 5], key="o3")
        o4 = st.select_slider("4.Apakah kamu merasa bahwa penderitaan yang dialami tokoh dalam cerita tersebut merupakan cerminan nyata dari apa yang kamu rasakan sendiri?", options=[1, 2, 3, 4, 5], key="o4")
        o5 = st.select_slider("5.Apakah kamu merasa lelah secara fisik atau kehilangan energi setelah menyelesaikan seluruh tugas menulis narasi yang menguras perasaan ini?", options=[1, 2, 3, 4, 5], key="o5")
    
    with col_kanan:
        o6 = st.select_slider("6.Seberapa sering kamu merasa sedih atau terganggu secara emosional setelah membaca cerita yang mengandung konflik?", options=[1, 2, 3, 4, 5], key="o6")
        o7 = st.select_slider("7.Seberapa sering kamu merasa gelisah atau tidak aman saat melakukan kegiatan membaca atau menulis narasi?", options=[1, 2, 3, 4, 5], key="o7")
        o8 = st.select_slider("8.Seberapa sering kamu merasa tegang atau terlalu waspada saat sedang mengerjakan tugas menulis di kelas?", options=[1, 2, 3, 4, 5], key="o8")
        o9 = st.select_slider("9.Seberapa sering kamu menyalahkan diri sendiri atau merasa menyesal setelah menuliskan perasaan negatif ke dalam narasi?", options=[1, 2, 3, 4, 5], key="o9")
        o10 = st.select_slider("10.Seberapa sering kamu merasa sulit fokus atau merasa asing dengan perasaanmu sendiri setelah menyelesaikan tugas literasi?", options=[1, 2, 3, 4, 5], key="o10")
    
    if st.button("Analisis & Kirim Laporan 🚀"):
        if nama and kelas != "Pilih Kelas" and q_nlp1:
            teks_lengkap = f"{q_nlp1} {q_nlp2} {q_nlp3} {q_nlp4} {q_nlp5}".lower()
            kata_terdeteksi = [k for k in keywords_trauma if k in teks_lengkap]
            bonus_nlp = len(kata_terdeteksi) * 2 

            # Memberi nilai lebih tinggi untuk kata kunci yang sangat berat
            bobot_kata = {"mati": 5, "hancur": 3, "trauma": 3, "lelah": 1, "putus asa": 4}
            # Jika kata tidak ada di daftar bobot_kata, nilai defaultnya adalah 2
            bonus_nlp = sum([bobot_kata.get(k, 2) for k in kata_terdeteksi])
            
            skor_slider = o1 + o2 + o3 + o4 + o5
            total_akhir = skor_slider + bonus_nlp
            
            if total_akhir >= 25: hasil = "Tinggi"
            elif total_akhir >= 15: hasil = "Sedang"
            else: hasil = "Rendah"
            
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
    
    c_log, c_out = st.columns([1, 4])
    if c_log.button("Buka Dashboard 🔓"):
        if password == "kelompok4":
            st.session_state['authenticated'] = True
            st.success("Akses Diterima!")
        else:
            st.error("Password salah!")
            st.session_state['authenticated'] = False
            
    if c_out.button("Kunci Kembali 🔒"):
        st.session_state['authenticated'] = False
        st.rerun()

    st.markdown("---")

    if st.session_state.get('authenticated', False) and password == "kelompok4":
        if os.path.exists('data_tugas.csv'):
            df = pd.read_csv('data_tugas.csv')
            
            # Statistik Utama
            st.subheader("📊 Rekapitulasi & Statistik")
            counts = df['Level_Trauma'].value_counts()
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Siswa", len(df))
            m2.metric("Tinggi 🔴", counts.get("Tinggi", 0))
            m3.metric("Sedang 🟡", counts.get("Sedang", 0))
            m4.metric("Rendah 🟢", counts.get("Rendah", 0))

            # Grafik
            col_kiri, col_kanan = st.columns(2)
            with col_kiri:
                st.write("**Grafik Batang:**")
                st.bar_chart(counts)
            with col_kanan:
                st.write("**Sebaran Skor:**")
                if len(df) > 1:
                    fig = ff.create_distplot([df['Skor']], ['Skor'], bin_size=2, show_hist=False)
                    st.plotly_chart(fig, use_container_width=True)
            

            # Fitur NLP Word Analysis
            if 'Keywords_NLP' in df.columns:
                st.subheader("🔍 Kata Kunci Dominan (Hasil NLP)")
                # Menghapus baris kosong dan menggabungkan kata
                valid_keywords = df['Keywords_NLP'].dropna()
                if not valid_keywords.empty:
                    all_keywords = ", ".join(valid_keywords)
                    st.info(f"Kata-kata emosional yang sering muncul: {all_keywords}")

            # Tabel Detail
            st.write("**Data Detail Siswa:**")
            st.dataframe(df, use_container_width=True)

            # --- FITUR HAPUS DATA SATU PER SATU (NEW) ---
            st.markdown("---")
            st.subheader("🗑️ Kelola Data (Hapus Salah Satu)")
            list_siswa = df['Nama'].tolist()
            pilih_siswa = st.selectbox("Pilih nama siswa yang ingin dihapus:", ["-- Pilih Siswa --"] + list_siswa)

            if pilih_siswa != "-- Pilih Siswa --":
                index_to_drop = df[df['Nama'] == pilih_siswa].index
                if st.button(f"Konfirmasi Hapus Data: {pilih_siswa} ❌"):
                    df = df.drop(index_to_drop)
                    df.to_csv('data_tugas.csv', index=False)
                    st.success(f"Data {pilih_siswa} berhasil dihapus!")
                    st.rerun()

            # Download & Reset
            st.markdown("---")
            dl, rs = st.columns(2)
            dl.download_button("📥 Download Laporan", df.to_csv(index=False).encode('utf-8'), "laporan_trauma.csv", "text/csv")
            if rs.button("🗑️ Reset Database"):
                os.remove('data_tugas.csv')
                st.rerun()
        else:
            st.info("Belum ada data masuk.")








