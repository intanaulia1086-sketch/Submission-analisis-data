import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard E-Commerce Intan", layout="wide")

# Gaya CSS Custom
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    div[data-testid="stMetricValue"] {
        font-size: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df1 = pd.read_csv("main_df_q1.csv")
    df2 = pd.read_csv("main_df_q2.csv")
    rfm = pd.read_csv("rfm_data.csv")
    return df1, df2, rfm

try:
    main_df_q1, main_df_q2, rfm_df = load_data()
except Exception as e:
    st.error("Pastikan file CSV hasil colab sudah ada di folder dashboard!")
    st.stop()

st.title("Proyek Analisis Data: E-commerce Public Dataset 🛍️")
st.markdown("Oleh: **Intan Aulia Agustina**")

# --- PERTANYAAN 1: KATEGORI PRODUK ---
st.header("1. Analisis Kategori Produk Terlaris (2017)")

col1, col2 = st.columns([2, 1])

with col1:
    # Visualisasi Bar Chart Colorful
    top_product_df = main_df_q1.groupby("product_category_name_english").agg({
        "order_item_id": "count",
        "price": "sum" 
    }).sort_values(by="order_item_id", ascending=False).head(10).reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette("rocket", 10) 
    sns.barplot(x="order_item_id", y="product_category_name_english", data=top_product_df, palette=colors, ax=ax)
    ax.set_title("10 Kategori Produk dengan Penjualan Tertinggi", fontsize=15)
    st.pyplot(fig)

with col2:
    st.write("### Ringkasan Penjualan")
    summary_q1 = top_product_df.copy()
    
    # Merapikan Format Angka Revenue agar tidak terlalu rinci
    summary_q1['price'] = summary_q1['price'].map("{:,.2f}".format)
    
    summary_q1 = summary_q1.rename(columns={
        "product_category_name_english": "Kategori",
        "order_item_id": "Pesanan",
        "price": "Revenue (R$)"
    })
    st.dataframe(summary_q1, hide_index=True, use_container_width=True)

# Insight 1 (Langsung muncul tanpa expander)
st.info("""
**Insight Pertanyaan 1:** Berdasarkan visualisasi di atas, kategori produk **Bed Bath Table** (cama_mesa_banho) menjadi kategori yang paling banyak terjual sepanjang tahun 2017. Hal ini menunjukkan tingginya permintaan pada perlengkapan rumah tangga dibandingkan kategori lainnya.
""")

st.divider()

# --- PERTANYAAN 2: METODE PEMBAYARAN ---
st.header("2. Distribusi Metode Pembayaran")

payment_counts = main_df_q2['payment_type'].value_counts()
    
col_pie, col_ins = st.columns([1, 1])

with col_pie:
    fig, ax = plt.subplots()
    ax.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%', 
           startangle=140, colors=sns.color_palette("pastel"))
    ax.axis('equal') 
    st.pyplot(fig)

with col_ins:
    st.success("""
    **Insight Pertanyaan 2:** Mayoritas pelanggan (lebih dari 70%) lebih memilih menggunakan **Credit Card** sebagai metode pembayaran utama. Hal ini kemungkinan dipicu oleh adanya fitur cicilan yang memudahkan pelanggan dalam bertransaksi dalam jumlah besar tanpa mengganggu arus kas mereka.
    """)

st.divider()

# --- ANALISIS RFM ---
st.header("3. Analisis RFM (Best Customer)")
st.write("Menampilkan 5 pelanggan terbaik berdasarkan parameter Recency, Frequency, dan Monetary.")

col_r, col_f, col_m = st.columns(3)

with col_r:
    st.subheader("Recency (Hari)")
    fig, ax = plt.subplots()
    sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency").head(5), palette="YlOrBr")
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col_f:
    st.subheader("Frequency")
    fig, ax = plt.subplots()
    sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette="GnBu")
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col_m:
    st.subheader("Monetary")
    fig, ax = plt.subplots()
    sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette="Purples")
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.divider()

# --- CONCLUSION & RECOMMENDATION (With Background Color) ---
st.header("Conclusion & Recommendation 💡")

# Menggunakan st.success dan st.info sebagai background warna
st.success("""
**Conclusion:**
1. **Dominasi Produk:** Kategori *Bed Bath Table* merupakan kontributor volume pesanan terbesar, menandakan fokus pasar pada kebutuhan rumah tangga.
2. **Preferensi Pembayaran:** Ketergantungan tinggi pada kartu kredit menunjukkan bahwa kemudahan pembayaran/cicilan adalah faktor kunci keputusan pembelian.
3. **Loyalitas Pelanggan:** Melalui RFM, kita telah mengidentifikasi pelanggan spesifik yang memberikan nilai ekonomi tertinggi bagi bisnis.
""")

st.info("""
**Recommendation:**
1. **Marketing Campaign:** Fokuskan promosi pada kategori *Bed Bath Table* dan berikan opsi cicilan yang lebih fleksibel untuk menarik pelanggan baru.
2. **Customer Retention:** Berikan reward khusus atau poin loyalitas kepada pelanggan yang berada di deretan Top RFM untuk mencegah mereka beralih ke kompetitor.
3. **Optimasi Inventory:** Pastikan ketersediaan stok produk unggulan selalu terjaga, terutama pada periode promosi besar.
""")

st.caption('Copyright (c) Intan Aulia Agustina 2026')
