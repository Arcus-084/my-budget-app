import streamlit as st
from supabase import create_client
import pandas as pd

# --- KONEKSI KE SUPABASE ---
# Masukkan data dari Notepad kamu di sini
SUPABASE_URL = "https://pjdvfdzmrwanbqxznixu.supabase.co"
SUPABASE_KEY = "sb_publishable_KbGny_svdRAyRSYvEL32iQ_RTLXfbNM"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Dani Budget Tracker", layout="wide")
st.title("📊 Personal & Business Budget Tracker")

# --- BAGIAN 1: FORM INPUT ---
with st.sidebar:
    st.header("Input Transaksi Baru")
    with st.form("input_form", clear_on_submit=True):
        tgl = st.date_input("Tanggal")
        kat = st.selectbox("Kategori", ["Pendapatan Rutin", "Pendapatan Usaha", "Pendapatan Sampingan", "Penerimaan Piutang", "Lain-lain", "F&B", "Transportasi", "Komunikasi & Digital", "Edukasi & Kuliah", "Organisasi", "Hobi", "Pemberian Piutang", "Operasional Bisnis"])
        ket = st.text_input("Keterangan")
        arus = st.radio("Arus Kas", ["Masuk", "Keluar"])
        nom = st.number_input("Nominal (Rp)", min_value=0)
        
        submitted = st.form_submit_button("Simpan Ke Supabase")
        
        if submitted:
            data = {
                "tanggal": str(tgl),
                "kategori": kat,
                "deskripsi": ket, # Pastikan nama kolom sama dengan di Supabase
                "arus_kas": arus,
                "nominal": nom
            }
            supabase.table("transaction").insert(data).execute()
            st.success("Data Berhasil Disimpan!")
            st.rerun()

# --- BAGIAN 2: TAMPILAN DATA ---
res = supabase.table("transaction").select("*").execute()
df = pd.DataFrame(res.data)

if not df.empty:
    # Logika Saldo (Hijau untuk Masuk, Merah untuk Keluar)
    df['Saldo_Visual'] = df.apply(lambda x: x['nominal'] if x['arus_kas'] == 'Masuk' else -x['nominal'], axis=1)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Ringkasan Saldo")
        total_saldo = df['Saldo_Visual'].sum()
        st.metric("Total Uang Saat Ini", f"Rp {total_saldo:,.0f}")
        st.dataframe(df[['tanggal', 'kategori', 'Saldo_Visual']])

    with col2:
        st.subheader("Grafik Arus Kas")
        # Menampilkan grafik batang seperti di Excel
        st.bar_chart(df.set_index('kategori')['Saldo_Visual'])
else:
    st.info("Belum ada data. Silakan input di menu samping!")