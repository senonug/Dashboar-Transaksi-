
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Dashboard Monitoring Pelanggan", layout="wide")

st.title("📊 Dashboard Monitoring Pelanggan")

menu = st.sidebar.radio("Pilih Menu Utama:", [
    "Analisa Gabungan",
    "Pelanggan Prabayar", "Pelanggan Paskabayar", 
    "Pelanggan AMR", "Intra kWh P2TL"
])

data_dir = "data"

def upload_and_save(file, folder):
    if file is not None:
        os.makedirs(folder, exist_ok=True)  # Pastikan folder ada
        filepath = os.path.join(folder, file.name)
        with open(filepath, "wb") as f:
            f.write(file.getbuffer())
        st.success(f"File {file.name} berhasil diunggah dan disimpan di {folder}")
        return filepath
    return None

elif menu == "Pelanggan AMR":
    st.header("📥 Upload Data Instant AMR")
    file = st.file_uploader("Unggah File Data Instant AMR", type=["csv", "xlsx"])
    path = upload_and_save(file, os.path.join(data_dir, "amr"))
    if path:
        df = pd.read_excel(path)
        df = df[df['LOCATION_TYPE'] == 'COSTUMER']  # Filter hanya pelanggan COSTUMER
        st.dataframe(df)

        # Threshold + Deteksi otomatis diikuti visual summary
        # -- kode threshold dan hasil_analisa_code akan masuk di sini dalam aplikasi penuh
