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
df = pd.read_csv(home + '/cmaq/prediction_files/prediction_rf.csv')
AirnowObs = pd.read_csv(home + "/cmaq/observation.csv")
AirnowObs = AirnowObs.loc[AirnowObs['AirNOW_O3'] != -999]

time_ = df['YYYYMMDDHH'].unique()
dfs = dict(tuple(df.groupby('YYYYMMDDHH')))  # grouping the data by YYMMDDHH

time_Airnow = AirnowObs['YYYYMMDDHH'].unique()
dfs_Airnow = dict(tuple(AirnowObs.groupby('YYYYMMDDHH')))  # grouping the data by YYMMDDHH

cmap = cmaps.WhiteBlueGreenYellowRed[0:262:12]



for t in time_:
    
    df = dfs[t]
    
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
    gdf = gdf.set_crs("EPSG:4326")
    #gdf = gdf.to_crs("+proj=lcc +lat_1=2 +lat_2=33.000 +lat_0=45.000 +lon_0=-97.000 +x_0=-97.000 +y_0=40.000 +datum=NAD83 +units=m +no_defs")

    gdf.plot(column='prediction', legend=False, figsize=(20, 18),
         cmap=cmap, vmin=0,vmax=80 )
    #cb = plt.colorbar(sm, ticks=list(range(0, 84, 4)), location='bottom', 	
    #                  format='%.0f', boundaries=np.arange(0,84,4),       
    #                  spacing='uniform', drawedges=True, pad=0.05)

    #cb.outline.set_linewidth(2)
    #cb.dividers.set_color('black')
    #cb.dividers.set_linewidth(2)
    
    # Add US states boundries.
    
    # states = gpd.read_file('usStates/cb_2018_us_state_500k.shp')
	# states = states.to_crs("EPSG:4326")
	# states.boundary.plot(ax=ax)
    
    dateObj = datetime.strptime(str(t), "%Y%m%d%H")
    plotTitle = datetime.strftime(dateObj, "%Y-%m-%d (Time: %-H)")
    plt.title(plotTitle, fontdict={'fontsize': 35})
    plt.savefig(home + "/cmaq/prediction_maps/CMAQ_" + str(t) + ".tif")

    
for t_Airnow, t in zip(time_Airnow, time_):
    
    df = dfs[t]
    
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
    gdf = gdf.set_crs("EPSG:4326")
    
    
    predDf = gdf.plot(column='prediction', legend=False, figsize=(20, 18),
                      cmap=cmap, vmin=0,vmax=84  )
    
    df_Airnow = dfs_Airnow[t_Airnow]
    # Add individual AirNow stations in US with color representation.
    
    gdfAirnow = gpd.GeoDataFrame(df_Airnow, geometry=gpd.points_from_xy(df_Airnow.Longitude,df_Airnow.Latitude))

    gdfAirnow = gdfAirnow.set_crs("EPSG:4326")
    gdfAirnow.plot(ax=predDf, column='AirNOW_O3', marker='o', markersize=65, cmap=cmap, figsize=(20, 15), linewidths=1, edgecolors="black")
    
    
    dateObj = datetime.strptime(str(t), "%Y%m%d%H")
    plotTitle = datetime.strftime(dateObj, "%Y-%m-%d (Time: %-H)")
    plt.title("AirNow Stations: "+plotTitle, fontdict={'fontsize': 35})
    plt.savefig(home + "/cmaq/prediction_maps/AirNow_" + str(t) + ".tif")
    
files=glob.glob(home + "/cmaq/prediction_maps/CMAQ_*.tif")
#files = sorted(files)
files = sorted(files)
images=[]

for i in files:
    print(i)
    img=imageio.imread(i)
    images.append(img)
    
imageio.mimsave(home+'/prediction.mp4', images, fps=10)


files=glob.glob("/Users/uhhmed/prediction_maps/Airnow_*.tif")
#files = sorted(files)
files = sorted(files)
images=[]

for i in files:
    print(i)
    img=imageio.imread(i)
    images.append(img)
    
imageio.mimsave("/Users/uhhmed/predctionAirNow.mp4", images, fps=10)

# create .gif from .mp4 using FFmpeg
os.system('ffmpeg -i '+ home + '/prediction.mp4 -vf "scale=2000:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse, fps=10" '+ home + '/prediction.gif')

# remove the created .mp4 file
os.system('rm '+ home + '/prediction.mp4')


# create .gif from .mp4 using FFmpeg
os.system('ffmpeg -i '+ home + '/predctionAirNow.mp4 -vf "scale=2000:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse, fps=10" '+ home + '/predctionAirNow.gif')

# remove the created .mp4 file
os.system('rm '+ home + '/predctionAirNow.mp4')

