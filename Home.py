
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
        filepath = os.path.join(folder, file.name)
        with open(filepath, "wb") as f:
            f.write(file.getbuffer())
        st.success(f"File {file.name} berhasil diunggah dan disimpan di {folder}")
        return filepath
    return None

if menu == "Pelanggan Prabayar":
    st.header("📥 Upload Data Harian Prabayar")
    file = st.file_uploader("Unggah File Data Harian Prabayar", type=["csv", "xlsx"])
    path = upload_and_save(file, os.path.join(data_dir, "prabayar"))
    if path:
        df = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
        st.dataframe(df)

elif menu == "Pelanggan Paskabayar":
    st.header("📥 Upload Data Bulanan OLAP Paskabayar")
    file = st.file_uploader("Unggah File Data Bulanan OLAP Paskabayar", type=["csv", "xlsx"])
    path = upload_and_save(file, os.path.join(data_dir, "paskabayar"))
    if path:
        df = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
        st.dataframe(df)


elif menu == "Pelanggan AMR":
    st.header("📥 Upload Data Instant AMR")
    file = st.file_uploader("Unggah File Data Instant AMR", type=["csv", "xlsx"])
    path = upload_and_save(file, os.path.join(data_dir, "amr"))
    if path:
        df = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
        st.dataframe(df)

        st.markdown("### ⚙️ Pengaturan Threshold Anomali")

        with st.expander("1. Tegangan Drop"):
            st.write("**Penjelasan:** Tegangan drop terjadi ketika salah satu L1, L2, L3 bertegangan kecil, bernilai positif, dan arusnya besar.")
            v_drop_threshold = st.number_input("Ambang Tegangan Drop (Volt)", value=180)

        with st.expander("2. Tegangan Hilang"):
            st.write("**Penjelasan:** Tegangan hilang terjadi pada data PHASE 3, salah satu tegangan L1, L2, atau L3 = 0, dan arusnya lebih besar dari ambang.")
            v_lost_threshold_i = st.number_input("Ambang Arus untuk Tegangan Hilang (Ampere)", value=5)

        with st.expander("3. Cos Phi Kecil"):
            st.write("**Penjelasan:** Cos phi kecil menunjukkan pemakaian daya aktif yang rendah pada pelanggan tak langsung.")
            cos_phi_threshold = st.number_input("Ambang Cos Phi", value=0.5)

        with st.expander("4. Arus Hilang"):
            st.write("**Penjelasan:** Arus hilang jika arus saat ini kecil tetapi sebelumnya pernah besar.")
            i_hilang_threshold = st.number_input("Ambang Arus Hilang (Ampere)", value=3)

        with st.expander("5. Arus Netral > 130% Arus Maksimum"):
            st.write("**Penjelasan:** Arus netral melebihi 130% dari arus maksimum dan melebihi nilai ambang.")
            in_more_imax_threshold = st.number_input("Ambang Arus Netral (Ampere)", value=20)

        with st.expander("6. Over Current"):
            st.write("**Penjelasan:** Arus maksimum lebih besar dari nilai standar (berdasarkan daya) + nilai ambang.")
            over_current_threshold = st.number_input("Ambang Over Current (Ampere)", value=30)

        with st.expander("7. Over Voltage"):
            st.write("**Penjelasan:** Tegangan maksimum melebihi nilai ambang batas.")
            over_voltage_threshold = st.number_input("Ambang Tegangan Maksimum (Volt)", value=240)

        with st.expander("8. Reverse Power"):
            st.write("**Penjelasan:** Daya aktif rendah tapi arus cukup tinggi. Termasuk pembobotan billing dan waktu.")
            reverse_power_threshold_p = st.number_input("Ambang Daya Aktif (Watt)", value=50)
            reverse_power_threshold_i = st.number_input("Ambang Arus (Ampere)", value=5)

        with st.expander("9. Arus Inbalance"):
            st.write("**Penjelasan:** Deviasi arus terhadap rata-rata melebihi batas toleransi (khusus tak langsung).")
            unbalance_i_threshold_pct = st.number_input("Batas Deviasi Arus (%)", value=20)

        with st.expander("10. Active Power Lost"):
            st.write("**Penjelasan:** Daya aktif = 0 dan arus masih besar pada salah satu L1, L2, L3.")
            active_p_lost_threshold_i = st.number_input("Ambang Arus (Ampere)", value=3)

        st.success("✅ Semua threshold anomali telah disiapkan.")
elif menu == "Intra kWh P2TL":
    st.header("📥 Upload Data Intra kWh P2TL")
    file = st.file_uploader("Unggah File Data Intra kWh P2TL", type=["csv", "xlsx"])
    path = upload_and_save(file, os.path.join(data_dir, "intra_kwh_p2tl"))
    if path:
        df = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
        st.dataframe(df)
        st.markdown("🛠️ Data bisa dimodifikasi sesuai kebutuhan:")
        edited_df = st.experimental_data_editor(df)
        st.write("🔄 Data setelah diedit:")
        st.dataframe(edited_df)

def gabungan_analisa_scoring():
    st.header("🔍 Analisa Gabungan & Scoring")

    # Load data dari semua kategori
    df_prabayar, df_paskabayar, df_amr = None, None, None

    try:
        prabayar_files = os.listdir(os.path.join(data_dir, "prabayar"))
        if prabayar_files:
            path = os.path.join(data_dir, "prabayar", prabayar_files[-1])
            df_prabayar = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
    except: pass

    try:
        paskabayar_files = os.listdir(os.path.join(data_dir, "paskabayar"))
        if paskabayar_files:
            path = os.path.join(data_dir, "paskabayar", paskabayar_files[-1])
            df_paskabayar = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
    except: pass

    try:
        amr_files = os.listdir(os.path.join(data_dir, "amr"))
        if amr_files:
            path = os.path.join(data_dir, "amr", amr_files[-1])
            df_amr = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
    except: pass

    # Gabungkan berdasarkan ID pelanggan
    if df_prabayar is not None and df_paskabayar is not None and df_amr is not None:
        try:
            df_prabayar["IDPEL"] = df_prabayar["IDPEL"].astype(str)
            df_paskabayar["IDPEL"] = df_paskabayar["IDPEL"].astype(str)
            df_amr["IDPEL"] = df_amr["IDPEL"].astype(str)

            df_gabungan = df_prabayar.merge(df_paskabayar, on="IDPEL", how="outer", suffixes=("_pra", "_pas"))
            df_gabungan = df_gabungan.merge(df_amr, on="IDPEL", how="outer", suffixes=("", "_amr"))

            st.success("✅ Data berhasil digabungkan berdasarkan IDPEL")
            st.dataframe(df_gabungan)

            # Contoh scoring sederhana
            st.subheader("📈 Scoring Potensi Pelanggaran")
            def scoring(row):
                score = 0
                if "KWH_pra" in row and row["KWH_pra"] < 10: score += 1
                if "KWH_pas" in row and row["KWH_pas"] > 500: score += 1
                if "Daya" in row and row["Daya"] > 10000: score += 1
                return score

            df_gabungan["Skor_Pelanggaran"] = df_gabungan.apply(scoring, axis=1)
            st.dataframe(df_gabungan[["IDPEL", "Skor_Pelanggaran"]].sort_values(by="Skor_Pelanggaran", ascending=False))

        except Exception as e:
            st.error(f"Gagal memproses gabungan data: {e}")
    else:
        st.warning("🔄 Pastikan semua data (Prabayar, Paskabayar, AMR) sudah tersedia untuk analisa gabungan.")

# Tambahkan tombol menu analisa gabungan
if menu == "Analisa Gabungan":
    gabungan_analisa_scoring()
