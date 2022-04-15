# NASA GEOWEAVER
# CMAQ-AI Model: Poocessing the data - shifting columns of NO2

# importing necessary libraries
import glob
import pandas as pd
from pathlib import Path
from time import sleep

# home directory
home = str(Path.home())
print(home+'*.txt')
files=glob.glob(home+'/*.txt')
print(files)
merged=[]
for file in files:
	df=pd.read_csv(file)
	merged.append(df)
data_frame = pd.concat(merged)
data_frame['YYYYMMDDHH'] = data_frame['YYYYMMDDHH'].map(str)
data_frame['year'] = data_frame['YYYYMMDDHH'].str[:4]
data_frame['month'] = data_frame['YYYYMMDDHH'].str[4:6]
data_frame['day'] = data_frame['YYYYMMDDHH'].str[6:8]
data_frame['hours'] = data_frame['YYYYMMDDHH'].str[8:10]
data_frame.to_csv(home+'/cmaq/daily_cmaq.csv',index=False)

sleep(5) # Sleep for 5 secs to give time for .csv file to save and ensure next node picks it up
