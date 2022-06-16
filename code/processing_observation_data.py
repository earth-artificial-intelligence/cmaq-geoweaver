## importing necessary libraries
import glob
import pandas as pd
from pathlib import Path
import numpy as np
from datetime import datetime, date, timedelta
# home directory
home = str(Path.home())

days=[]

base = datetime.today() - timedelta(days=2)
date_list = [base - timedelta(days=x) for x in range(3)]
days = [date.strftime('%Y%m%d') for date in date_list]

    
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
dff.to_csv("/groups/ESS/aalnaim/cmaq/observation.csv",index=False)




