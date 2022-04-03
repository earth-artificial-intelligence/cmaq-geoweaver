## importing necessary libraries
import glob
import pandas as pd
from pathlib import Path
# home directory
home = str(Path.home())

days=[]
from datetime import date, timedelta

sdate = date(2021, 4, 5)   # start date
edate = date(2021, 4, 6)   # end date

delta = edate - sdate       # as timedelta

for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    list_day=day.strftime('%Y%m%d')
    days.append(list_day)
    
    
data_frame = pd.DataFrame()
merged=[]
time = ['12','13','14','15','16','17','18','19','20','21','22','23','00','01','02','03','04','05','06','07','08','09','10','11']
for d in days:
  for t in time:
    files=glob.glob(home+"/cmaq/observation/AQF5X_Hourly_"+d+t+".txt")
    for file in files:
      df=pd.read_csv(file, delimiter=" ",header=0,skiprows=1)
      df['YYYYMMDDHH']=d+t
      merged.append(df)
data_frame = pd.concat(merged)
data_frame = data_frame.replace(',','', regex=True)


# dropping unnecessary variables
data_frame.drop(data_frame.columns[[4, 5,6,7,8]], axis = 1, inplace = True)
# Changing columns name with index number
#mapping = {data_frame.columns[0]: 'StationID', data_frame.columns[1]: 'Latitude',data_frame.columns[2]: 'Longitude',data_frame.columns[3]: 'AirNOW_O3'}
mapping = {data_frame.columns[0]: 'StationID',data_frame.columns[1]: 'Latitude',data_frame.columns[2]: 'Longitude',data_frame.columns[3]: 'AirNOW_O3'}
df = data_frame.rename(columns=mapping)

df.to_csv(home+"/cmaq/observation.csv",index=False)

