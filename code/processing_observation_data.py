# take all the airnow observation csvs and merge into one observation.csv

import glob
import pandas as pd
from pathlib import Path
import numpy as np
from cmaq_ai_utils import *

sdate = date(2021, 8, 1)   # start date
edate = date(2022, 8, 2)   # end date
days = get_days_list(sdate, edate)
    
data_frame = pd.DataFrame()
merged=[]
date_time=[]

time = ['12','13','14','15','16','17','18','19','20','21','22','23','00','01','02','03','04','05','06','07','08','09','10','11']

for x in range(len(days)-1):
  current_day = days[x]
  next_day = days[x+1]
  for y in range(len(time)):
    t = time[y]
    if y>=12:
      d = next_day
    else:
      d = current_day
    files=glob.glob(f"{cmaq_folder}/observation/AQF5X_Hourly_{d}{t}.txt")
    for file in files:
      print(file)
      data = np.loadtxt(file, skiprows=1,dtype='str')
      dt=d+t
      print(dt)
      dt=np.tile(dt,len(data)) # constructs an array for each hour of each day with length of data from total stations available
      date_time.append(dt)
      merged.append(data)
            
data_frame = np.concatenate(merged)

# This gets the first 4 columns in the observation file (AQSID, Latitude, Longitude, OZONE(ppb))
data_frame = np.delete(data_frame, np.s_[4:9], axis=1) 

df = pd.DataFrame(data_frame, columns = ['StationID','Latitude','Longitude','AirNOW_O3'])
dff=df.replace(',','', regex=True)

dt = np.concatenate(date_time)
dff['YYYYMMDDHH'] = dt.tolist()
dff.to_csv(f"{cmaq_folder}/observation_one_year.csv",index=False)
