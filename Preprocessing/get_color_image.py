import geopandas as gpd
import rasterio
from rasterio.plot import show
from rasterio.windows import Window
from shapely.geometry import shape
from rasterio.features import geometry_mask
import json
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from PIL import Image
import earthpy.plot as ep
import io

dir1 = './LandfillCoordPolygons_Pan'
dir2 = './HR_TIF_Files_Pan'



for j in os.listdir(dir2):
    tif_file = os.path.join(dir2, j).replace("\\", "/")
    raster_image = rasterio.open(tif_file).read()
    raster_channels, width, height = raster_image.shape

    if raster_channels == 8:
        rgb = (4, 2, 1)  # R, G, B bands
    elif raster_channels == 4:
        rgb = (2, 1, 0)  # R, G, B bands

    w = 5.12
    h = 5.12


    fig = plt.figure(frameon=False)
    fig.set_size_inches(w, h)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax1 = ep.plot_rgb(raster_image, rgb=rgb,stretch=True, ax=ax)
    # Set the figure size and dpi to achieve the desired resolution (512x512)
    # fig = ax.get_figure()
    # # fig.set_size_inches(512 / dpi, 512 / dpi)
    fig.savefig(
        "ColorImage_Pan/" + j[:-4] + ".png",
        pad_inches=0

    )
    #
    plt.show()