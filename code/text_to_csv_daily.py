# NASA GEOWEAVER
# CMAQ-AI Model: Poocessing the data - shifting columns of NO2

# importing necessary libraries
import glob
import pandas as pd
from pathlib import Path
from time import sleep

# home directory
home = str(Path.home())
data_frame=pd.read_csv(home+'/cmaq/test_data.csv')

data_frame['YYYYMMDDHH'] = data_frame['YYYYMMDDHH'].map(str)
data_frame['year'] = data_frame['YYYYMMDDHH'].str[:4]
data_frame['month'] = data_frame['YYYYMMDDHH'].str[4:6]
data_frame['day'] = data_frame['YYYYMMDDHH'].str[6:8]
data_frame['hours'] = data_frame['YYYYMMDDHH'].str[8:10]
data_frame.to_csv(home+'/cmaq/daily_cmaq.csv',index=False)


