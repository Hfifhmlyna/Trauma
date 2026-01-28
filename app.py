import streamlit as st
import pandas as pd
import os
import csv  # WAJIB ADA untuk tombol hapus

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

# --- LOGIKA TAMPILAN SISWA ---
if role == "Siswa (Menulis)":
    st.markdown("<h1 style='color: #2E86C1;'>📝 Ruang Ekspresi Siswa</h1>", unsafe_allow_html=True)
    st.write("Silakan tuangkan ceritamu. AI akan memberikan apresiasi untuk setiap karyamu.")

    nama = st.text_input("Nama Lengkap:")
    teks = st.text_area("Ceritakan perasaan atau pengalamanmu hari ini:", height=200)
    
    if st.button("Kirim Tulisan"):
        if nama and teks:
            found = [w for w in keywords_trauma if w in teks.lower()]
            is_sensitif = len(found) >= 1
            label = "1 (Sensitif)" if is_sensitif else "0 (Normal)"
            rekomendasi = "Suportif & Validatif" if is_sensitif else "Apresiasi Literasi"

            # Tampilan Analisis
            st.subheader("📊 Analisis Hasil Tulisan")
            df_siswa = pd.DataFrame({
                "Nama": [nama],
                "Status": [label],
                "Rekomendasi": [rekomendasi]
            })
            st.table(df_siswa)

            if is_sensitif:
                st.info(f"❤️ **Pesan Suportif:** Terima kasih sudah berbagi, {nama}. Tulisanmu sangat kuat dan berani!")
            else:
                st.success(f"✨ **Pesan Apresiasi:** Luar biasa, {nama}! Teruslah berkarya.")

            # Simpan ke CSV
            new_data = pd.DataFrame([[nama, teks, label, ", ".join(found)]], 
                                    columns=["Nama", "Teks", "Label", "Keywords"])
            new_data.to_csv('data_tugas.csv', mode='a', index=False, header=not os.path.exists('data_tugas.csv'))
        else:
            st.error("Nama dan teks tidak boleh kosong.")

# --- LOGIKA TAMPILAN GURU ---
elif role == "Guru (Administrator)":
    st.markdown("<h1 style='color: #117A65;'>🔐 Dashboard Monitoring Guru</h1>", unsafe_allow_html=True)
    password = st.text_input("Masukkan Password Admin:", type="password")
    
    if password == "kelompok4":
        st.success("Akses Diterima. Halo Bapak/Ibu Guru.")
        
        if os.path.exists('data_tugas.csv'):
            df_master = pd.read_csv('data_tugas.csv')
            
            # --- 1. STATISTIK RINGKAS ---
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

            # --- 2. ANALISIS REAL-TIME ---
            if total_data > 0:
                st.subheader("📈 Analisis Sebaran Data Real-Time")
                persen_sensitif = (jml_sensitif / total_data) * 100
                persen_normal = (jml_normal / total_data) * 100

                # Tabel Rekapitulasi
                rekap_data = {
                    "Kategori Klasifikasi": ["1 (Sensitif)", "0 (Normal)", "TOTAL"],
                    "Jumlah Data": [jml_sensitif, jml_normal, total_data],
                    "Persentase": [f"{persen_sensitif:.1f}%", f"{persen_normal:.1f}%", "100%"]
                }
                st.table(pd.DataFrame(rekap_data))

                # Tombol Download & Hapus
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

            with st.expander("📚 Catatan untuk Dosen"):
                st.write(f"Sistem menggunakan *Keyword Spotting* untuk mendeteksi {len(keywords_trauma)} kata kunci emosional secara otomatis.")
        else:
            st.info("Belum ada data masuk.")
            
    elif password != "":
        st.error("Password salah!")

# --- FOOTER ---
st.markdown("<div class='footer'>Sistem Monitoring Literasi Inklusif © 2026 Kelompok 4</div>", unsafe_allow_html=True)
