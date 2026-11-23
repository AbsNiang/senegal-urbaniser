import rasterio
from rasterio.warp import reproject, Resampling
import numpy as np

# Align the 2024 lulc to the 2019 lulc

# Load 2019 (reference grid)
with rasterio.open("data/lulc/senegal_esri_lulc_2019.tif") as ref_src:
    ref_profile = ref_src.profile
    lulc19 = ref_src.read(1)

# Load 2024 (to be aligned)
with rasterio.open("data/lulc/senegal_esri_lulc_2024.tif") as src24:
    lulc24_raw = src24.read(1)
    src24_transform = src24.transform
    src24_crs = src24.crs

# Prepare aligned output array (same shape as 2019)
lulc24 = np.zeros_like(lulc19, dtype=np.uint8)

# Reproject 2024 to 2019
print("Reprojection started.")
reproject(
    source=lulc24_raw,
    destination=lulc24,
    src_transform=src24_transform,
    src_crs=src24_crs,
    dst_transform=ref_profile["transform"],
    dst_crs=ref_profile["crs"],
    resampling=Resampling.nearest
)

print("Reprojection completed.")

# Optional: save aligned file
aligned_path = "data/lulc/senegal_esri_lulc_2024_aligned.tif"
profile = ref_profile.copy()
profile.update(dtype="uint8", count=1)

with rasterio.open(aligned_path, "w", **profile) as dst:
    dst.write(lulc24, 1)

print("Aligned 2024 raster saved:", aligned_path)
