# general purpose data manipulation and analysis
import numpy as np

# packages for working with raster datasets
import rasterio
from rasterio.mask import mask
from rasterio.plot import show
from rasterio.enums import Resampling

import xarray # allows us to work with raster data as arrays

# packages for working with geospatial data
import geopandas as gpd
import pycrs

from shapely.geometry import box

# import packages for viewing the data
import matplotlib.pyplot as pyplot

