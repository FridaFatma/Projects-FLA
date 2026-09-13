import pandas as pd

def extract_shade_performance(path="data/PT_X_Pilot_Data_Pack.xlsx"):
    """Baca data shade group performance (stockout, overstock, return)."""
    df = pd.read_excel(path, sheet_name="4_Shade_Group_Perf", header=3)
    df = df.dropna(subset=["Shade Group"])  # buang baris judul/kosong
    return df

def extract_product_performance(path="data/PT_X_Pilot_Data_Pack.xlsx"):
    """Baca data per SKU (untuk nanti dipakai modul lain juga)."""
    df = pd.read_excel(path, sheet_name="2_Product_Foundation", header=3)
    df = df.dropna(subset=["SKU"])
    return df

if __name__ == "__main__":
    # cara cepat ngetes: jalankan `python extract.py` di terminal
    df = extract_shade_performance()
    print(df.head())
    print(df.columns.tolist())