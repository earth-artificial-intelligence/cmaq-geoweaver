# importing necessary libraries
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path
import geopandas as gpd
import cmaps
from datetime import datetime

import imageio
import glob


matplotlib.rcParams['font.size'] = 25
norm= matplotlib.colors.Normalize(vmin=0,vmax=80)


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

time_ = df['YYYYMMDDHH'].unique()
dfs = dict(tuple(df.groupby('YYYYMMDDHH')))  # grouping the data by YYMMDDHH



for t in time_:
    
    df = dfs[t]
    
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
    #gdf = gdf.set_crs("EPSG:3762", allow_override=True)
    #gdf = gdf.set_crs("EPSG:4326")
    gdf.plot(column='prediction', legend=True, figsize=(20, 25),
         cmap=cmaps.WhiteBlueGreenYellowRed, legend_kwds={'orientation': "horizontal", "pad": 0.05}, vmin=0, vmax=80 )
    
    # Add individual AirNow stations in US with color representation.
    
    # gdfAirnow = gpd.GeoDataFrame(
        # AirnowObs, geometry=gpd.points_from_xy(AirnowObs.Longitude, AirnowObs.Latitude))
    # gdfAirnow.plot(ax=predDF, column='AirNOW_O3', marker='o', cmap=cmaps.WhiteBlueGreenYellowRed, figsize=(20, 20))
    
    # Add US states boundries.
    
    # states = gpd.read_file('usStates/cb_2018_us_state_500k.shp')
	# states = states.to_crs("EPSG:4326")
	# states.boundary.plot(ax=ax)
    
    dateObj = datetime.strptime(str(t), "%Y%m%d%H")
    plotTitle = datetime.strftime(dateObj, "%Y-%m-%d (Time: %-H)")
    plt.title(plotTitle, fontdict={'fontsize': 35})
    plt.savefig(home + "/cmaq/prediction_maps/" + str(t) + ".tif")

    
files=glob.glob(home + "/cmaq/prediction_maps/*.tif")
images=[]

for i in files:
    print(i)
    img=imageio.imread(i)
    images.append(img)
    
imageio.mimsave(home+'/prediction.gif', images)
