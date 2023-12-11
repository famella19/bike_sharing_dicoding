from cgitb import text
from operator import index
from tkinter import HORIZONTAL
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# Buat Header
st.title('📊 Dashboard Sharing Bike ✨')

# Menampilkan kolom jumlah penyewa dan tanggal data terakhir diambil
st.subheader('Data Penyewa Per Minggu')

# Membaca DataFrame dari file CSV
df = pd.read_csv("days.csv")
# Mengonversi kolom 'dteday' ke dalam tipe data datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Menampilkan kolom jumlah penyewa dan tanggal data terakhir diambil
col1, col2 = st.columns(2)

# Kolom 1: Jumlah Penyewa
with col1:
    total_penyewa = df.cnt.sum()
    st.metric("Jumlah Penyewa 2011 - 2012", value=total_penyewa)

# Kolom 2: Tanggal Terakhir Record Data
with col2:
    tanggal_terakhir = df['dteday'].max()
    st.metric("Tanggal Terakhir Record Data", value=str(tanggal_terakhir))

# Data Perminggu
st.subheader('Data Penyewa Perminggu')

# Menambahkan kolom 'minggu' yang berisi informasi minggu dari tanggal
df['minggu'] = df['dteday'].dt.isocalendar().week

# Menghitung jumlah penyewa per minggu
jumlah_penyewa = df.groupby('minggu')['cnt'].sum().reset_index()

# Menampilkan grafik di Streamlit
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(jumlah_penyewa['minggu'], jumlah_penyewa['cnt'], marker='o')
ax.set_title('Jumlah Penyewa Per Minggu')
ax.set_xlabel('Minggu')
ax.set_ylabel('Jumlah Penyewa')
ax.grid(True)

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Menampilkan bulan yang memiliki jumlah penyewa terbanyak 
# Menambahkan kolom 'bulan_tahun' yang berisi informasi bulan dan tahun dari tanggal
df['bulan_tahun'] = df['dteday'].dt.to_period('M')

# Menghitung jumlah penyewa per bulan dan tahun
jumlah_penyewa_perbulan = df.groupby('bulan_tahun')['cnt'].sum().reset_index()

# Mengurutkan berdasarkan jumlah penyewa secara descending
jumlah_penyewa_perbulan = jumlah_penyewa_perbulan.sort_values(by='cnt', ascending=False)

# Mengambil 5 bulan dan tahun teratas
top_5_bulan = jumlah_penyewa_perbulan.head(5)

# Mengubah format kolom 'bulan_tahun' menjadi bulan dan tahun sebenarnya
top_5_bulan['bulan_tahun'] = top_5_bulan['bulan_tahun'].dt.strftime('%B %Y')

# Menampilkan tabel dengan 5 bulan dan tahun teratas
st.subheader('5 Bulan dan Tahun Terbanyak Penyewa Sepeda')
st.table(top_5_bulan.reset_index(drop=True))  # Menambahkan reset_index untuk menghapus indeks

# Menampilkan grafik per bulan dan tahun
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='bulan_tahun', 
    y='cnt', 
    data=top_5_bulan,
    palette='colorblind')
ax.set_title('Jumlah Penyewa Sepeda Top 5')
ax.set_xlabel('Bulan dan Tahun')
ax.set_ylabel('Jumlah Penyewa')
ax.set_xticklabels(top_5_bulan['bulan_tahun'], rotation=45, ha='right')
ax.grid(True)

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Menampilkan perbandingan penyewa casual dan registered
# Menampilkan subheader
st.subheader('Perbandingan Status Penyewa Sepeda')

# Menghitung rata-rata penyewa registered dan casual
rata_registered = df['registered'].mean()
rata_casual = df['casual'].mean()

# Membuat DataFrame baru
avg_sharing = pd.DataFrame({
    'User Type': ['Registered', 'Casual'],
    'Average Sharing': [rata_registered, rata_casual]
})

# Menampilkan pie chart dengan latar belakang tanpa warna
fig, ax = plt.subplots(figsize=(5, 5))
ax.pie(
    avg_sharing['Average Sharing'], 
    labels=avg_sharing['User Type'], 
    autopct='%1.1f%%', 
    startangle=90, 
    colors=['skyblue', 'lightcoral'])
ax.set_title('Rata-Rata Jumlah Penyewa Sepeda Registered dan Casual', color='white')  # Mengganti judul

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Buat Sidebar
with st.sidebar:
    st.image("images\logo.png")
# Menampilkan filter data
    st.subheader('Filter Data 📂')

    filter_category = st.sidebar.radio(
    label="Pilih Kategori !!!",
    options=('Cuaca', 'Musim', 'Hari Kerja', 'Akhir Pekan'),
    index=0
)

# Filter DataFrame berdasarkan kategori yang dipilih
if filter_category == 'Cuaca':
    cuaca_options = st.sidebar.multiselect("Pilih Kondisi Cuaca", df['weathersit'].unique())
    filtered_df = df[df['weathersit'].isin(cuaca_options)]

elif filter_category == 'Musim':
    musim_options = st.sidebar.multiselect("Pilih Musim", df['season'].unique())
    filtered_df = df[df['season'].isin(musim_options)]

elif filter_category == 'Hari Kerja':
    filtered_df = df[df['workingday'] == True]

elif filter_category == 'Akhir Pekan':
    filtered_df = df[df['workingday'] == False]

# Menampilkan data hasil filter
st.subheader(f"Data Setelah Filter Berdasarkan {filter_category}:")
st.write(filtered_df)

# Menampilkan grafik pengaruh
fig, ax = plt.subplots(figsize=(10, 6))

# Memplot jumlah penyewa
ax.bar(filtered_df['dteday'], filtered_df['cnt'], color='blue')
ax.set_title(f'Pengaruh {filter_category} Terhadap Jumlah Penyewa')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Jumlah Penyewa')
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Menampilkan kotak feedback
st.subheader('Feedback 🤩')
text = st.text_area('Feedback')
st.write('Feedback : ', text)

