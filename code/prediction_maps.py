
## importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path
import geopandas as gpd
import shapely
from osgeo import gdal
# home directory
home = str(Path.home())

# importing data
df=pd.read_csv(home+'/cmaq/prediction_files/prediction_xgboost.csv')

time_=df['YYYYMMDDHH'].unique()
dfs = dict(tuple(df.groupby('YYYYMMDDHH'))) # grouping the data by YYMMDDHH

for t in time_:
  df=dfs[t]
  gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
  gdf = gdf.set_crs("EPSG:4326",allow_override=True)
  #gdf = gdf.set_crs("EPSG:4326")
  gdf.plot(column='prediction',cmap='bwr')
  plt.savefig(home+"/cmaq/prediction_maps/"+str(t)+".tif")
  

  
  
  
  

# total area for the grid
#  xmin, ymin, xmax, ymax= gdf.geometry.total_bounds
#  gdf=gdal.OpenEx(gdf.to_json(), gdal.OF_VECTOR)
# how many cells across and down
#  xsize=422
#  ysize=265
#  gdal.Grid(home+"/cmaq/prediction_maps/"+str(t)+".tif", gdf, zfield="prediction",outputSRS ="EPSG:4326",    algorithm="linear", outputBounds=[xmax,ymax,xmin,ymin], width=xsize, height=ysize)

