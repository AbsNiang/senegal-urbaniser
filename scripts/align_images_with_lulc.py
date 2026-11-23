import rasterio
from rasterio.warp import reproject, Resampling

def align_to_lulc_grid(src_path, ref_path, dst_path):

    # Read reference (only metadata)
    with rasterio.open(ref_path) as ref_src:
        ref_profile = ref_src.profile.copy()
        dst_transform = ref_profile["transform"]
        dst_crs = ref_profile["crs"]

    # Read source metadata
    with rasterio.open(src_path) as src:
        band_count = src.count
        dtype = src.dtypes[0]

    # Update before opening destination to allow for all bands
    dst_profile = ref_profile.copy()
    dst_profile.update(
        count=band_count,
        dtype=dtype,
        nodata=None,
    )

    # Now open src and dst together
    with rasterio.open(src_path) as src, rasterio.open(dst_path, "w", **dst_profile) as dst:
        print(f"Aligning {band_count} bands...")

        for b in range(1, band_count + 1):
            print(f"Reprojecting band {b}/{band_count}...")

            reproject(
                source=rasterio.band(src, b),
                destination=rasterio.band(dst, b),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=dst_transform,
                dst_crs=dst_crs,
                resampling=Resampling.bilinear
            )

    print("Saved aligned raster:", dst_path)

align_to_lulc_grid(
    src_path="data/images/sar_all.tif",
    ref_path="data/lulc/senegal_esri_lulc_2019.tif",
    dst_path="data/realigned_images/2019_S1_SAR_VV_VH.tif"
)