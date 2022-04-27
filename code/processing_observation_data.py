## importing necessary libraries
import glob
import pandas as pd
from pathlib import Path
import numpy as np
# home directory
home = str(Path.home())

days=[]
from datetime import date, timedelta

sdate = date(2021, 10, 30)   # start date
edate = date(2022, 1, 1)   # end date

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

    files=glob.glob(home+"/cmaq/observation/AQF5X_Hourly_"+d+t+".txt")
    for file in files:
      print(file)

      data = np.loadtxt(file, skiprows=1,dtype='str')
      dt=d+t
      print(dt)
      dt=np.tile(dt,len(data)) # 2822 total station number
      date_time.append(dt)
      merged.append(data)
data_frame = np.concatenate(merged)
data_frame =np.delete(data_frame, np.s_[4:9], axis=1) 
#data_frame.drop(data_frame.columns[[4, 5,6,7,8]], axis = 1, inplace = True)
df = pd.DataFrame(data_frame, columns = ['StationID','Latitude','Longitude','AirNOW_O3'])
print(len(days))
print(df.shape)
dt = np.concatenate(date_time)
print(dt.shape)
#dt = np.concatenate(date_time)
#print(len(dt))
dff=df.replace(',','', regex=True)
dff['YYYYMMDDHH'] = dt.tolist()
dff.to_csv(home+"/cmaq/observation.csv",index=False)




