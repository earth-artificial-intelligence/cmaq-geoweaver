# combine cmaq and airnow into training.csv
from cmaq_ai_utils import *

obs=pd.read_csv(f"{cmaq_folder}/observation_one_year.csv")
obs['Latitude'] = obs['Latitude'].astype(float)
obs['Longitude'] = obs['Longitude'].astype(float)
obs['YYYYMMDDHH'] = obs['YYYYMMDDHH'].astype(str)
print("obs head: ", obs.columns, obs.head())
ref_stations=pd.read_csv(f"{cmaq_folder}/updated_station_to_cell.csv")
ref_stations = ref_stations.astype(float)
print("ref_stations head: ", ref_stations.columns, ref_stations.head())

print("obs shape: ", obs.shape)
print("ref_station shape: ", ref_stations.shape)

chunksize = 10000
count = 0
with pd.read_csv("/groups/ESS3/aalnaim/cmaq/merged_cmaq_one_year.csv", chunksize=chunksize) as reader:
  for chunk in reader:
    chunk = chunk[pd.to_numeric(chunk['Latitude'], errors='coerce').notnull()]
    chunk = chunk[pd.to_numeric(chunk['Longitude'], errors='coerce').notnull()]
    chunk['Latitude'] = chunk['Latitude'].astype(float)
    chunk['Longitude'] = chunk['Longitude'].astype(float)
    new_df = pd.merge(chunk,  ref_stations, how='left', left_on=['Latitude','Longitude'], right_on = ['Lat_cmaq','Lon_cmaq'])
    new_df = new_df[new_df.Lat_cmaq.notnull()][new_df.Lat_airnow!=-999]
    new_df['Lat_airnow'] = new_df['Lat_airnow'].astype(float)
    new_df['Lon_airnow'] = new_df['Lon_airnow'].astype(float)
    new_df['YYYYMMDDHH'] = new_df['YYYYMMDDHH'].astype(str)
    chunk_final = pd.merge(new_df, obs, how='left', left_on=['Lat_airnow','Lon_airnow','YYYYMMDDHH'], right_on = ['Latitude','Longitude','YYYYMMDDHH'])
    chunk_final['month'] = chunk_final['YYYYMMDDHH'].str[4:6]
    chunk_final['day'] = chunk_final['YYYYMMDDHH'].str[6:8]
    chunk_final['hours'] = chunk_final['YYYYMMDDHH'].str[8:10]
    new_chunk_df=chunk_final.drop(['YYYYMMDDHH'],axis=1)
    final_chunk_df = new_chunk_df[new_chunk_df.AirNOW_O3.notnull()][new_chunk_df.AirNOW_O3!=-999]
    #print("final_chunk_df", final_chunk_df)
    #count += 1
    #if count == 10:
    final_chunk_df.to_csv(f"{cmaq_folder}/training_new_one_year_valid_test.csv",mode='a',index=False)
    break


print("All records should be incorporated into :", f"{cmaq_folder}/training_new_one_year_valid_test.csv")
