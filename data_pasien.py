import requests
import pandas as pd

def get_global_ncd_data():
    # Endpoint API dengan parameter lengkap
    indicator = "SH.DYN.NCOM.ZS"
    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}?format=json&per_page=500&date=2010:2023"
    
    try:
        print("Mengambil data global dari World Bank API...")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Pastikan data tersedia
        if len(data) < 2 or not data[1]:
            print("Tidak ada data yang tersedia")
            return pd.DataFrame()
            
        records = data[1]
        df = pd.DataFrame(records)
        
        # Filter kolom
        df = df[['country', 'value', 'date']]
        df.columns = ['Negara', 'Persentase Kematian NCD', 'Tahun']
        
        # Hapus nilai kosong dan konversi tipe data
        df = df.dropna(subset=['Persentase Kematian NCD'])
        df['Persentase Kematian NCD'] = df['Persentase Kematian NCD'].astype(float)
        
        # Urutkan berdasarkan persentase tertinggi
        df = df.sort_values(by='Persentase Kematian NCD', ascending=False)
        
        print(f"Data berhasil diambil ({len(df)} negara)")
        return df
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return pd.DataFrame()

# Simpan ke CSV
df = get_global_ncd_data()
if not df.empty:
    df.to_csv("global_ncd_deaths.csv", index=False)
    print("Data disimpan ke global_ncd_deaths.csv")
    print("\n10 Negara dengan Persentase Kematian NCD Tertinggi:")
    print(df.head(10))
else:
    print("Gagal mendapatkan data")