# take all the airnow observations and merge into one observation.csv

import glob
import pandas as pd
from pathlib import Path
import numpy as np
from datetime import datetime, date, timedelta
# home directory
home = str(Path.home())

days=[]


sdate = date(2022, 7, 1)   # start date
edate = date(2022, 7, 2)   # end date

delta = edate - sdate       # as timedelta

for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    list_day=day.strftime('%Y%m%d')
    days.append(list_day)

    
data_frame = pd.DataFrame()
merged=[]
date_time=[]

time = ['12','13','14','15','16','17','18','19','20','21','22','23','00','01','02','03','04','05','06','07','08','09','10','11']

for d in days:
    for t in time:

        files=glob.glob("/groups/ESS/aalnaim/cmaq/observation/AQF5X_Hourly_"+d+t+".txt")
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
dff.to_csv("/groups/ESS/aalnaim/cmaq/observation/observation.csv",index=False)
