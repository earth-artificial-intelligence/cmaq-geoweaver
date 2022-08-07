# combine cmaq and airnow into training.csv

import pandas as pd
from pathlib import Path
import glob, os

# home directory

# cmaq=pd.read_csv(home+"/cmaq/training_data.csv")
path = '/groups/ESS/aalnaim/cmaq/training_input_hourly'
all_hourly_files = sorted(glob.glob(os.path.join(path, "*.csv"))) 
df_from_each_hourly_file = (pd.read_csv(f) for f in all_hourly_files)
cmaq = pd.concat(df_from_each_hourly_file)

obs=pd.read_csv("/groups/ESS/aalnaim/cmaq/observation/observation.csv")
ref_stations=pd.read_csv("/groups/ESS/mislam25/station_cmaq_location.csv")

new_df = pd.merge(ref_stations, cmaq,  how='left', left_on=['Latitude_y','Longitude_y'], right_on = ['Latitude','Longitude'])
new_df.to_csv("/groups/ESS/aalnaim/cmaq/subset.csv")
final = pd.merge(obs, new_df,  how='left', left_on=['Latitude','Longitude','YYYYMMDDHH'], right_on = ['Latitude_x','Longitude_x','YYYYMMDDHH'])

final=final.drop_duplicates(keep=False)
training_data = final.loc[:,~final.columns.duplicated()]

training_data['YYYYMMDDHH'] = training_data['YYYYMMDDHH'].map(str)
training_data['month'] = training_data['YYYYMMDDHH'].str[4:6]
training_data['day'] = training_data['YYYYMMDDHH'].str[6:8]
training_data['hours'] = training_data['YYYYMMDDHH'].str[8:10]

new_df=training_data.drop(['StationID','Latitude_y','Longitude_y','YYYYMMDDHH'],axis=1)
final_df = new_df[new_df.AirNOW_O3!= -999]
final_df.to_csv("/groups/ESS/aalnaim/cmaq/training.csv",index=False)



