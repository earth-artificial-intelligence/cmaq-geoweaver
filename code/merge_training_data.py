# combine cmaq and airnow into training.csv
from cmaq_ai_utils import *


def append_large_data_to_file(all_files):
  
  CHUNK_SIZE = 50000
  output_file = f"{cmaq_folder}/merged_cmaq_one_year.csv"

  first_file = True

  for csv_file in all_hourly_files:
    if not first_file: # if it is not the first csv file then skip the header row to not repeat it for each file added. 
        skip_row = [0]
    else:
        skip_row = []
    
    chunks = pd.read_csv(csv_file, chunksize=CHUNK_SIZE, skiprows = skip_row)
    print('reading csv file: ', csv_file)
    for chunk in chunks:
        chunk.to_csv(output_file, mode="a", index=False)
    first_file = False


def match_large_csv(file_path, ref_stations):
  
  chunksize = 10000000 # 10M chunks per loop
  df_list = [] # holds all the chunks to concat later
  
  ref_stations[['Lat_cmaq','Lon_cmaq']] = ref_stations[['Lat_cmaq','Lon_cmaq']].astype(str)

  
  for chunk in pd.read_csv(file_path,  chunksize=chunksize, low_memory=False):

    chunk[['Latitude','Longitude']] =chunk[['Latitude','Longitude']].astype(str)
    print(f"Mergeing CMAQ Chunk #{len(df_list)} with ref_stations")
    df_list.append( pd.merge(ref_stations, chunk,  how='left', left_on=['Lat_cmaq','Lon_cmaq'], right_on = ['Latitude','Longitude']) )
    


  df = pd.concat(df_list)
  del df_list
  
  return df
    
    
# path = f'{cmaq_folder}/training_input_hourly'
# all_hourly_files = sorted(glob.glob(os.path.join(path, "*.csv"))) 
# df_from_each_hourly_file = (pd.read_csv(f) for f in all_hourly_files)
# cmaq = pd.concat(df_from_each_hourly_file)

# !!! Below line only needs to be run once! this will merge all hourly cmaq files.
# append_large_data_to_file(all_hourly_files)  

print("Started reading observation_20210801_20220801.csv")
obs=pd.read_csv(f"{cmaq_folder}/observation/observation_20210801_20220801.csv")
print("finished reading observation_20210801_20220801.csv")

print("Started reading updated_station_to_cell.csv")
ref_stations=pd.read_csv("/groups/ESS/zsun/cmaq/updated_station_to_cell.csv")
print("finished reading updated_station_to_cell.csv")

print("Started reading merged_cmaq_one_year.csv")
new_df = match_large_csv(f"{cmaq_folder}/merged_cmaq_one_year.csv", ref_stations)
print("finished reading merged_cmaq_one_year.csv")

# print("Starting to merge ref_stations/cmaq")
# new_df = pd.merge(ref_stations, cmaq,  how='left', left_on=['Lat_cmaq','Lon_cmaq'], right_on = ['Latitude','Longitude'])
# print("finished merging ref_stations/cmaq")

print("Saving subset.csv")
new_df.to_csv(f"{cmaq_folder}/subset.csv")
print("Done saving subset.csv")

print("Starting to merge obs/new_df")
final = pd.merge(obs, new_df,  how='left', left_on=['Latitude','Longitude','YYYYMMDDHH'], right_on = ['Lat_airnow','Lon_airnow','YYYYMMDDHH'])
print("finished merging obs/new_df")

print("Doing some df operations...")
final=final.drop_duplicates(keep=False)
training_data = final.loc[:,~final.columns.duplicated()]

training_data['YYYYMMDDHH'] = training_data['YYYYMMDDHH'].map(str)
training_data['month'] = training_data['YYYYMMDDHH'].str[4:6]
training_data['day'] = training_data['YYYYMMDDHH'].str[6:8]
training_data['hours'] = training_data['YYYYMMDDHH'].str[8:10]

new_df=training_data.drop(['YYYYMMDDHH'],axis=1)
final_df = new_df[new_df.AirNOW_O3!= -999]

print("Done df operations...Saving training_one_year.csv")
final_df.to_csv(f"{cmaq_folder}/training_one_year.csv",index=False)
print("All records should be incorporated into :", f"{cmaq_folder}/training.csv")



