import rasterio
import numpy as np
import shapely
from rasterio.warp import transform
from rasterio.windows import from_bounds
import os

def getRasterStats(path, lat, lon):
    base = "raster/"
    try:
        listBand = [i for i in os.listdir(base + path) if i.endswith(".TIF") and "B" in i]
        dat = []

        # Set point of interest
        point = shapely.geometry.Point(lon, lat)    
        # Process only the first band for now
        for j in range(len(listBand)):
            print(f"Processing: {listBand[j]}",f"{base}{path}/{listBand[j]}")
            
            
            with rasterio.open(f"{base}{path}/{listBand[j]}") as src:
                # Get the CRS of the raster and reproject lat/lon to the raster's CRS (UTM)
                lon_utm, lat_utm = transform('EPSG:4326', src.crs, [lon], [lat])
                print(lon_utm,lat_utm)
                # Get the bounding box (window) around the point (small area for faster reading)
                window = from_bounds(lon_utm[0] - 50, lat_utm[0] - 50, 
                                    lon_utm[0] + 50, lat_utm[0] + 50, src.transform)
                print(window)
                # Read the data within this window
                data = src.read(1, window=window)
                
                # Get the window transform (coordinates for this specific window)
                win_transform = src.window_transform(window)

                # Compute lat/lon for this window
                rows, cols = np.meshgrid(np.arange(data.shape[1]), np.arange(data.shape[0]))
                xs, ys = rasterio.transform.xy(win_transform, rows, cols)
                lons_window = np.array(xs)
                lats_window = np.array(ys)
                # print(lats_window,lons_window)
                # Find the closest pixel to the input lat/lon
                dist = np.sqrt((lons_window - lon)**2 + (lats_window - lat)**2)
                min_idx = np.unravel_index(np.argmin(dist), dist.shape)
                # print(data,min_idx)
                # value = data[min_idx]
                dat.append([[float(j) for j in i] for i in data]
        )
                # dat.append(value)
                # print(f"Value at ({lat}, {lon}): {value}")
        
        return dat
    except:
        return 0
        
# Example usage
# path = "your_raster_directory"
# lat = -7.2575  # Example latitude
# lon = 112.7521  # Example longitude
# getRasterStats(path, lat, lon)
