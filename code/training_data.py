import pandas as pd
from pathlib import Path

# home directory
home = str(Path.home())
cmaq=pd.read_csv(home+"/cmaq/training_data.csv")
obs=pd.read_csv(home+"/cmaq/observation.csv")
ref_stations=pd.read_csv(home+"/station_cmaq_location.csv")

new_df = pd.merge(ref_stations, cmaq,  how='left', left_on=['Latitude_y','Longitude_y'], right_on = ['Latitude','Longitude'])
new_df.to_csv(home+"/cmaq/subset.csv")
final = pd.merge(obs, new_df,  how='left', left_on=['Latitude','Longitude','YYYYMMDDHH'], right_on = ['Latitude_x','Longitude_x','YYYYMMDDHH'])
final.to_csv(home+"/cmaq/subset.csv",index=False)
final=final.drop_duplicates(keep=False)
training_data = final.loc[:,~final.columns.duplicated()]
# dropping unnecessary variables
training_data['YYYYMMDDHH'] = training_data['YYYYMMDDHH'].map(str)
training_data['month'] = training_data['YYYYMMDDHH'].str[4:6]
training_data['day'] = training_data['YYYYMMDDHH'].str[6:8]
training_data['hours'] = training_data['YYYYMMDDHH'].str[8:10]

new_df=training_data.drop(['StationID','Latitude_y','Longitude_y','YYYYMMDDHH'],axis=1)
final_df = new_df[new_df.AirNOW_O3!= -999]
final_df.to_csv(home+"/cmaq/training.csv",index=False)
