# combine cmaq and airnow into training.csv
from cmaq_ai_utils import *

# cmaq=pd.read_csv(home+"/cmaq/training_data.csv")
path = f'{cmaq_folder}/training_input_hourly'
all_hourly_files = sorted(glob.glob(os.path.join(path, "*.csv"))) 
df_from_each_hourly_file = (pd.read_csv(f) for f in all_hourly_files)
cmaq = pd.concat(df_from_each_hourly_file)

obs=pd.read_csv(f"{cmaq_folder}/observation/observation.csv")
ref_stations=pd.read_csv(f"{cmaq_folder}/station_cmaq_location.csv")

new_df = pd.merge(ref_stations, cmaq,  how='left', left_on=['Latitude_y','Longitude_y'], right_on = ['Latitude','Longitude'])
new_df.to_csv(f"{cmaq_folder}/subset.csv")
final = pd.merge(obs, new_df,  how='left', left_on=['Latitude','Longitude','YYYYMMDDHH'], right_on = ['Latitude_x','Longitude_x','YYYYMMDDHH'])

final=final.drop_duplicates(keep=False)
training_data = final.loc[:,~final.columns.duplicated()]

training_data['YYYYMMDDHH'] = training_data['YYYYMMDDHH'].map(str)
training_data['month'] = training_data['YYYYMMDDHH'].str[4:6]
training_data['day'] = training_data['YYYYMMDDHH'].str[6:8]
training_data['hours'] = training_data['YYYYMMDDHH'].str[8:10]

new_df=training_data.drop(['YYYYMMDDHH'],axis=1)
final_df = new_df[new_df.AirNOW_O3!= -999]
final_df.to_csv(f"{cmaq_folder}/trainingNew.csv",index=False)
print("All records should be incorporated into :", f"{cmaq_folder}/training.csv")



