import geopandas as gpd
import rasterio
from shapely.geometry import shape
from rasterio.features import geometry_mask
import json
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from PIL import Image

patch_height = 512
patch_width = 512





def footprint_mask(geojson_file, tif_file, png_file, burn_value=255, out_type=np.uint8):
    # Read the GeoJSON file
    with open(geojson_file) as f:
        data = json.load(f)

    # Extract polygons and transform them into Shapely Polygon objects
    polygons = [shape(feature['geometry']) for feature in data['features']]

    # Read the reference image
    with rasterio.open(tif_file) as src:
        affine = src.transform

        # Get patch dimensions from the source image
        # patch_height, patch_width = src.height, src.width

        # Generate the mask using geometry_mask
        fp_mask = geometry_mask(polygons, out_shape=(patch_height, patch_width),
                                transform=affine, invert=True)


        # Set burn_value for pixels inside the polygon
        fp_mask = fp_mask.astype(out_type) * burn_value
        print(fp_mask)

        mask = fp_mask

        if (fp_mask.shape[0] < patch_height) or (fp_mask.shape[1] < patch_width):
            mask = np.zeros((patch_height, patch_width), dtype=np.float32)
            mask[0:fp_mask.shape[0], 0:fp_mask.shape[1]] = fp_mask


        # Save the mask as a PNG with the same dimensions as the TIFF
        # mask_img = Image.fromarray(mask)
        # mask_img.save(png_file)

# Create the mask
# footprint_mask(geojson_file, tif_file)

dir1 = './LandfillCoordPolygons_Pan'
dir2 = './HR_TIF_Files_Pan'


for i in os.listdir(dir1):
    # For each file in the second directory
    for j in os.listdir(dir2):
        if i[:5] == j[:5]:
            # Load CSVs into pandas
            geojson_file = os.path.join(dir1, i).replace("\\", "/")
            tif_file = os.path.join(dir2, j).replace("\\", "/")
            footprint_mask(geojson_file, tif_file, "Annotated_Pan/" + j[:-4] + ".png")

