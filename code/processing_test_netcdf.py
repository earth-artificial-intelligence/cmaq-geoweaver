import xarray as xr
import pandas as pd
import glob, os
import numpy as np
from pathlib import Path
import datetime
from datetime import timedelta
# home directory
home = str(Path.home())

# nc file need to correspond to the same prediction date in "/groups/ESS/aalnaim/cmaq/prediction_files/prediction_rf_Jun13.csv"
df_cdf = xr.open_dataset("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/CCTMout/12km/POST/COMBINE3D_ACONC_v531_gcc_AQF5X_20220612_extracted.nc")

df_csv = pd.read_csv("/groups/ESS/aalnaim/cmaq/prediction_files/prediction_rf_Jun13.csv")
df_csv['YYYYMMDDHH'] = df_csv['YYYYMMDDHH'].astype(str)
df_filt = df_csv[df_csv['YYYYMMDDHH'].str.contains("20220613")]

# Reshape "prediction/Latitude/Longitude" columns to (TSTEP, ROW, COL), these lines will reshape data into (24, 265, 442)
reshaped_prediction = np.atleast_3d(df_filt['prediction']).reshape(-1, 265, 442)
reshaped_lat = np.atleast_3d(df_filt['Latitude']).reshape(-1, 265, 442)
reshaped_lon = np.atleast_3d(df_filt['Longitude']).reshape(-1, 265, 442)

# Remove "LAY" Dimension in O3 variable already in nc file.
reduced_dim = df_cdf['O3'].sel(LAY=1, drop=True)
# Swap values from original nc file with new prediction data
reduced_dim.values = reshaped_prediction

# Apply changes to data variable in nc file
df_cdf['O3'] = (['TSTEP', 'ROW', 'COL'], reshaped_prediction)
df_cdf['LAT'] = (['TSTEP', 'ROW', 'COL'], reshaped_lat)
df_cdf['LON'] = (['TSTEP', 'ROW', 'COL'], reshaped_lon)

df_cdf.to_netcdf('/groups/ESS/aalnaim/cmaq/prediction_nc_files/COMBINE3D_ACONC_v531_gcc_AQF5X_20220612_extracted.nc')
