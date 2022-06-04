# importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path
import geopandas as gpd
import cmaps
from datetime import datetime

import imageio
import glob
import os


mpl.rcParams['font.size'] = 25
#os.system('module load ffmpeg') # Uncomment if running on HOPPER

# home directory
home = str(Path.home())

# Delete previous .tif images only (not folder) to reduce space if folder and files exist already.
if Path(home + "/cmaq/prediction_maps/"):
    for file in Path(home + "/cmaq/prediction_maps/").glob("*"):
        if file.is_file():
          [f.unlink() for f in Path(home + "/cmaq/prediction_maps/").glob("*") if f.is_file()] 

# importing data
df = raw_df = pd.read_csv(home + '/cmaq/prediction_files/prediction_rf.csv')

time_ = df['YYYYMMDDHH'].unique()
dfs = dict(tuple(df.groupby('YYYYMMDDHH')))  # grouping the data by YYMMDDHH

cmap = cmaps.WhiteBlueGreenYellowRed[0:262:12]

count = 0

for t in time_:
  
    dateObj = datetime.strptime(str(t), "%Y%m%d%H")
    print(t)
    
    single_hour_df = raw_df.loc[raw_df['YYYYMMDDHH']==t]
    #print(single_hour_df)
    print("max: ", single_hour_df["prediction"].max())
    print("min: ", single_hour_df["prediction"].min())
    print("median: ", single_hour_df["prediction"].median())
    print("mean: ", single_hour_df["prediction"].mean())
    
    count += 1
    
    df = dfs[t]
    
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
    gdf = gdf.set_crs("EPSG:4326")
    #gdf = gdf.to_crs("+proj=lcc +lat_1=2 +lat_2=33.000 +lat_0=45.000 +lon_0=-97.000 +x_0=-97.000 +y_0=40.000 +datum=NAD83 +units=m +no_defs")

    gdf.plot(column='prediction', legend=True, figsize=(20, 18),
         cmap=cmap, vmin=0,vmax=80,)
    
    plotTitle = datetime.strftime(dateObj, "%Y-%m-%d (Time: %H)")
    plt.title(plotTitle, fontdict={'fontsize': 35})
    plt.savefig(home + "/cmaq/prediction_maps/CMAQ_" + str(t) + ".tif")
    
    if count > 5:
         break;

