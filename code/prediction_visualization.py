
## importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import glob
from pathlib import Path

# home directory
home = str(Path.home())

# importing data
pred=pd.read_csv(home+'/cmaq/prediction_files/prediction_xgboost.csv')
time_=pred['YYYYMMDDHH'].unique()
dfs = dict(tuple(pred.groupby('YYYYMMDDHH'))) # grouping the data by YYMMDDHH

for t in time_:
  subset=dfs[t]
  fig = px.density_mapbox(subset, lat='Latitude', lon='Longitude', z='prediction', radius=10,
                        center=dict(lat=32.777701, lon=-111.358871), zoom=6.5,
                        mapbox_style="stamen-terrain")
  # Set figure title
  fig.update_layout(title_text="Date-time: "+str(t)+"(YY:MM:DD:HH)", title_x=0.5)
  # saving figures
  fig.write_image(home+"/cmaq/prediction_maps/"+"pred"+str(t)+".png")

