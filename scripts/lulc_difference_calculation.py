import rasterio
import numpy as np

# Mapping of my esri tif file
URBAN = 7 # Built area value
NODATA = 0 # Nothing value

# Load Senegal-clipped rasters
with rasterio.open("data/lulc/senegal_esri_lulc_2019.tif") as src19:
    lulc19 = src19.read(1)


# with rasterio.open("data/lulc/senegal_esri_lulc_2024.tif") as src24:
with rasterio.open("data/lulc/senegal_esri_lulc_2024_aligned.tif") as src24:
    lulc24 = src24.read(1)

print("Making masks.")
# Mask for valid data
valid = (lulc19 != NODATA) & (lulc24 != NODATA)

# Mask for class of interest
urban19 = (lulc19 == URBAN)
urban24 = (lulc24 == URBAN)

print("Counting transitions.")
# Count transitions between urban and non-urban
urban_to_nonurban = np.sum(urban19 & (~urban24) & valid)
nonurban_to_urban = np.sum((~urban19) & urban24 & valid)
urban_to_urban = np.sum(urban19 & urban24 & valid)
nonurban_to_nonurban = np.sum((~urban19) & (~urban24) & valid)

# Display results
print("Urban -> Non-urban:", urban_to_nonurban)
print("Non-urban -> Urban:", nonurban_to_urban)
print("Urban -> Urban:", urban_to_urban)
print("Non-urban -> Non-urban:", nonurban_to_nonurban)

# Area conversion (WorldCover = 10m resolution)
pixel_area_km2 = (10 * 10) / 1e6  # 100 m² = 0.0001 km²

print("\nUrban growth (km squared):", nonurban_to_urban * pixel_area_km2)
print("Urban loss (km squared):", urban_to_nonurban * pixel_area_km2)
