# importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import gridspec
from pathlib import Path
import geopandas as gpd
import cmaps
from datetime import datetime
import subprocess

import imageio
import glob
import os


mpl.rcParams['font.size'] = 65
mpl.rcParams['axes.linewidth'] = 2

# home directory
home = str(Path.home())

# Delete previous .tif images only (not folder) to reduce space if folder and files exist already.
if Path("/groups/ESS/aalnaim/cmaq/prediction_maps/"):
    for file in Path("/groups/ESS/aalnaim/cmaq/prediction_maps/").glob("*"):
        if file.is_file():
          [f.unlink() for f in Path("/groups/ESS/aalnaim/cmaq/prediction_maps/").glob("*") if f.is_file()] 

# importing data
df = pd.read_csv('/groups/ESS/aalnaim/cmaq/prediction_files/prediction_rf_Jun13.csv')
cmaq_actual = pd.read_csv("/groups/ESS/aalnaim/cmaq/testing.csv")
AirnowObs = pd.read_csv("/groups/ESS/aalnaim/cmaq/observation.csv")
AirnowObs = AirnowObs.loc[AirnowObs['AirNOW_O3'] != -999]

time_ = df['YYYYMMDDHH'].unique()
dfs = dict(tuple(df.groupby('YYYYMMDDHH')))  # grouping the data by YYMMDDHH

time_Airnow = AirnowObs['YYYYMMDDHH'].unique()
dfs_Airnow = dict(tuple(AirnowObs.groupby('YYYYMMDDHH')))  # grouping the data by YYMMDDHH

time_actual = cmaq_actual['YYYYMMDDHH'].unique()
dfs_actual = dict(tuple(cmaq_actual.groupby('YYYYMMDDHH')))  # grouping the data by YYMMDDHH

def add_colorbar(fig, axes):
  
    norm = mpl.colors.Normalize(vmin=0,vmax=80)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    
    cb = fig.colorbar(sm, ticks=list(range(0, 84, 4)), 	location='bottom', format='%.0f', boundaries=np.arange(0,84,4),       
                      spacing='uniform', drawedges=True, pad=0.05, ax=axes)


    cb.outline.set_linewidth(2)
    cb.dividers.set_color('black')
    cb.dividers.set_linewidth(2)

cmap = cmaps.WhiteBlueGreenYellowRed[0:262:12]
    
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize=(80, 50))
    
add_colorbar(fig, ax1)
add_colorbar(fig, ax2)
add_colorbar(fig, ax3)
add_colorbar(fig, ax4) 
    
    
for t in time_:
    
    print("Plotting... ", t)
    
    # CMAQ prediction dataframe    
    df = dfs[t]
    
    # AirNow observation dataframe
    df_Airnow = dfs_Airnow[t]

    # CMAQ actual dataframe
    df_actual = dfs_actual[t]
    
    # Setting up GeoPandas df from [CMAQ prediction dataframe]    
    predictionMapData = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
    predictionMapData = predictionMapData.set_crs("EPSG:4326")

    # Setting up GeoPandas df from [AirNow observation dataframe]
    predictionAirnowData = gpd.GeoDataFrame(
        df_Airnow, geometry=gpd.points_from_xy(df_Airnow.Longitude,df_Airnow.Latitude))
    predictionAirnowData = predictionAirnowData.set_crs("EPSG:4326")
    
    # Setting up GeoPandas df from [CMAQ actual dataframe]
    cmaqActualData = gpd.GeoDataFrame(
        df_actual, geometry=gpd.points_from_xy(df_actual.Longitude, df_actual.Latitude))
    cmaqActualData = cmaqActualData.set_crs("EPSG:4326")


    ###### Plots ROW 1 ######
    
    # Plotting CMAQ prediction Map     
    predictionMapData.plot(column='prediction', legend=False,
         cmap=cmap, vmin=0,vmax=80, ax=ax1)

    # Plotting CMAQ predictions base layer for AirNow observations     
    predictionMap = predictionMapData.plot(column='prediction', legend=False,
         cmap=cmap, vmin=0,vmax=80, ax=ax2)
    
    # Plotting AirNow observation layer
    predictionAirnowData.plot(ax=predictionMap, column='AirNOW_O3', 
                   marker='o', markersize=400, cmap=cmap, 
                   linewidths=3, edgecolors="black")
    
    
    ###### Plots ROW 2 ######
    
    # Plotting Actual CMAQ Map     
    cmaqActualData.plot(column='CMAQ12KM_O3(ppb)', legend=False,
        cmap=cmap, vmin=0,vmax=80, ax=ax3)
    
    # Plotting Actual CMAQ base layer for AirNow observations     
    actualCmaqMap = cmaqActualData.plot(column='CMAQ12KM_O3(ppb)', legend=False,
         cmap=cmap, vmin=0,vmax=80, ax=ax4)
    

    # Plotting AirNow observation layer
    predictionAirnowData.plot(ax=actualCmaqMap, column='AirNOW_O3', 
                   marker='o', markersize=400, cmap=cmap, 
                   linewidths=3, edgecolors="black")
       
    # Add US states boundries.
    
    # states = gpd.read_file('usStates/cb_2018_us_state_500k.shp')
	# states = states.to_crs("EPSG:4326")
	# states.boundary.plot(ax=ax)
    
    dateObj = datetime.strptime(str(t), "%Y%m%d%H")
    predictionMapPlotTitle = datetime.strftime(dateObj, "%Y-%m-%d (Time: %-H)")
    AirNowPlotTitle = datetime.strftime(dateObj, "AirNow Stations: %Y-%m-%d (Time: %-H)")
    cmaqActualPlotTitle = datetime.strftime(dateObj, "Actual CMAQ: %Y-%m-%d (Time: %-H)")
    AirNowActualPlotTitle = datetime.strftime(dateObj, "Actual AirNow Stations: %Y-%m-%d (Time: %-H)")
    ax1.set_title(predictionMapPlotTitle)
    ax2.set_title(AirNowPlotTitle)
    ax3.set_title(cmaqActualPlotTitle)
    ax4.set_title(AirNowActualPlotTitle)
    print("Saving Prediction Map: ", predictionMapPlotTitle)
    
    plt.tight_layout()
    plt.savefig("/groups/ESS/aalnaim/cmaq/prediction_maps/Plots_" + str(t) + ".tif")
    


files=glob.glob("/groups/ESS/aalnaim/cmaq/prediction_maps/Plots_*.tif")
#files = sorted(files)
files = sorted(files)
images=[]

for i in files:
    print(i)
    img=imageio.imread(i)
    images.append(img)
    
imageio.mimsave('/groups/ESS/aalnaim/cmaq/prediction.mp4', images, fps=10)


print("Generating prediction.gif ...")
# create .gif from .mp4 using FFmpeg
os.system('module load ffmpeg; ffmpeg -i /groups/ESS/aalnaim/cmaq/prediction.mp4 -vf "scale=2000:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse, fps=10" /groups/ESS/aalnaim/cmaq/prediction.gif')

# remove the created .mp4 file
os.system('rm /groups/ESS/aalnaim/cmaq/prediction.mp4')
print("Done prediction.gif !!!")

    



