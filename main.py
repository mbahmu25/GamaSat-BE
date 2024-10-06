import rasterio
import matplotlib.pyplot as plt
import numpy as np

def calculate_lst(band10_path, band4_path, band5_path):
    # Baca band 10 (Thermal Infrared), band 4 (Red), dan band 5 (NIR)
    with rasterio.open(band10_path) as src:
        band10 = src.read(1).astype('float32')
        profile = src.profile

    with rasterio.open(band4_path) as src:
        band4 = src.read(1).astype('float32')

    with rasterio.open(band5_path) as src:
        band5 = src.read(1).astype('float32')

    # Konstanta dari metadata
    M_L = 3.8000e-04  # Gain
    A_L = 0.10000  # Offset
    K1 = 799.0284  # K1 band 10
    K2 = 1329.2405  # K2 band 10

    # Menghitung TOA Spectral Radiance
    L_lambda = M_L * band10 + A_L

    # Menghitung Brightness Temperature (BT)
    BT = (K2 / np.log((K1 / L_lambda) + 1)) - 273.15  # Konversi Kelvin ke Celsius

    # Menghitung NDVI (Normalized Difference Vegetation Index)
    # Masking untuk menghindari pembagian oleh nol
    valid_mask = (band4 != 0) & (band5 != 0)  # Buat masker untuk elemen yang valid
    # Hitung NDVI hanya untuk elemen yang valid
    NDVI = np.zeros_like(band4)  # Inisialisasi NDVI
    NDVI[valid_mask] = (band5[valid_mask] - band4[valid_mask]) / (band5[valid_mask] + band4[valid_mask])

    # Nilai minimum dan maksimum NDVI untuk estimasi emisivitas
    NDVI_min = 0.2
    NDVI_max = 0.5

    # Emisivitas vegetasi (ev) dan tanah (es)
    ev = 0.99  # Emisivitas vegetasi
    es = 0.97  # Emisivitas tanah
    m = 0.004  # Konstanta m
    n = 0.986  # Konstanta n

    emissivity = np.zeros_like(NDVI)

    # Kondisi 1: NDVI <= 0.2 (tanah kosong)
    emissivity[NDVI <= 0.2] = es

    # Kondisi 2: NDVI >= 0.5 (vegetasi rapat)
    emissivity[NDVI >= 0.5] = ev

    # Kondisi 3: 0.2 < NDVI < 0.5 (campuran tanah kosong dan vegetasi)
    mask = (NDVI > 0.2) & (NDVI < 0.5)
    PV = ((NDVI[mask] - NDVI_min) / (NDVI_max - NDVI_min)) ** 2
    emissivity[mask] = m * PV + n

    # Menghitung Land Surface Temperature (LST)
    lambda_ = 0.0010895  # Panjang gelombang band 10
    rho = 0.014388  # Konstanta Stefan-Boltzmann

    LST = BT / (1 + (lambda_ * BT / rho) * np.log(emissivity))

    # Masking 
    valid_mask = (BT > -50) & (NDVI >= -1) & (NDVI <= 1) & (band10 != 0) & (band4 != 0) & (band5 != 0)
    LST[~valid_mask] = np.nan

    # Tampilkan statistik
    print(f"Statistik TOA Spectral Radiance (L_lambda): Min: {np.min(L_lambda)}, Max: {np.max(L_lambda)}")
    print(f"Statistik Brightness Temperature (BT): Min: {np.min(BT)}, Max: {np.max(BT)}, Mean: {np.mean(BT)}")
    print(f"Statistik NDVI: Min: {np.min(NDVI)}, Max: {np.max(NDVI)}, Mean: {np.mean(NDVI)}")
    print(f"Statistik Emissivity: Min: {np.min(emissivity)}, Max: {np.max(emissivity)}, Mean: {np.mean(emissivity)}")
    print(f"Statistik LST: Min: {np.nanmin(LST)}, Max: {np.nanmax(LST)}, Mean: {np.nanmean(LST)}")

    return emissivity, LST, profile

# Path ke band yang diperlukan
band10_path = '/content/B10.TIF'
band4_path = '/content/B4.TIF'
band5_path = '/content/B5.TIF'

# Hitung emissivity dan LST
emissivity, LST, profile = calculate_lst(band10_path, band4_path, band5_path)

# Simpan hasil LST ke file GeoTIFF
profile.update(dtype=rasterio.float32, count=1, compress='lzw')  # Update profile dengan tipe float32

with rasterio.open('lst_output.tif', 'w', **profile) as dst:
    dst.write(LST.astype(rasterio.float32), 1)