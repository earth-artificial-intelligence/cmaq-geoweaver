# importing necessary libraries
import os
import pandas as pd
import matplotlib as m
import matplotlib.pyplot as plt
from pathlib import Path
import geopandas as gpd
import cmaps
from datetime import datetime

import imageio
import glob

import random
import string


# printing lowercase
letters = string.ascii_lowercase
folder_name =  ''.join(random.choice(letters) for i in range(5))


#m.rcParams['font.size'] = 25
#norm= m.colors.Normalize(vmin=0,vmax=80)
cdict = {
  'red'  :  ( (0.0, 0.25, .25), (0.02, .59, .59), (1., 1., 1.)),
  'green':  ( (0.0, 0.0, 0.0), (0.02, .45, .45), (1., .97, .97)),
  'blue' :  ( (0.0, 1.0, 1.0), (0.02, .75, .75), (1., 0.45, 0.45))
}

cm = m.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)


# home directory
home = "D:/data/"#str(Path.home())
cmaq_folder = f"{home}/cmaq/"
input_folder = f"{home}/cmaq/prediction_files/"
result_folder = f"{home}/cmaq/prediction_maps_{folder_name}/"
os.makedirs(cmaq_folder, exist_ok=True)
os.makedirs(input_folder, exist_ok=True)
os.makedirs(result_folder, exist_ok=True)

# importing data
df = pd.read_csv(f'D:/data/prediction_rf.csv')
AirnowObs = pd.read_csv(f"D:/data/observation.csv")

time_ = df['YYYYMMDDHH'].unique()
dfs = dict(tuple(df.groupby('YYYYMMDDHH')))  # grouping the data by YYMMDDHH

time_ = time_[:5]

for t in time_:
    
    df = dfs[t]
    
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
    #gdf = gdf.set_crs("EPSG:3762", allow_override=True)
    #gdf = gdf.set_crs("EPSG:4326")
    #print(cmaps.WhiteBlueGreenYellowRed())
    
    gdf.plot(column='prediction', 
             legend=True, 
             figsize=(20, 25),
             cmap=cm,
             categorical=True,
             #cmap=cmaps.WhiteBlueGreenYellowRed, 
             #legend_kwds={'orientation': "horizontal", "pad": 0.05}, 
             vmin=0, 
             vmax=80 )
    
    # Add individual AirNow stations in US with color representation.
    
    # gdfAirnow = gpd.GeoDataFrame(
        # AirnowObs, geometry=gpd.points_from_xy(AirnowObs.Longitude, AirnowObs.Latitude))
    # gdfAirnow.plot(ax=predDF, column='AirNOW_O3', marker='o', cmap=cmaps.WhiteBlueGreenYellowRed, figsize=(20, 20))
    
    # Add US states boundries.
    
    # states = gpd.read_file('usStates/cb_2018_us_state_500k.shp')
	# states = states.to_crs("EPSG:4326")
	# states.boundary.plot(ax=ax)
    print(t)
    dateObj = datetime.strptime(str(t), "%Y%m%d%H")
    plotTitle = datetime.strftime(dateObj, "%Y-%m-%d (Time: %H)")
    plt.title(plotTitle, fontdict={'fontsize': 35})
    plt.savefig(f"{result_folder}/{str(t)}.tif")

    
files=glob.glob(f"{result_folder}/*.tif")
images=[]

for i in files:
    print(i)
    img=imageio.imread(i)
    images.append(img)
    
imageio.mimsave(f'{cmaq_folder}/prediction_{folder_name}.gif', images)
