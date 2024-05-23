# load the prediction_rf.csv into a NetCDF file for visualization
from cmaq_ai_utils import *

# end_date = datetime.today()
# base = end_date - timedelta(days=2)
#sdate = date(2022, 8, 6)   # start date
#edate = date(2022, 8, 8)   # end date
today = datetime.today()
edate = today
sdate = today - timedelta(days=7)
days = get_days_list_for_prediction(sdate, edate)

prediction_path = f"{cmaq_folder}/prediction_files/"

all_hourly_files = sorted(glob.glob(os.path.join(prediction_path, "*.csv")))
# print("overall hourly files: ", all_hourly_files)
real_hour_list = [12,13,14,15,16,17,18,19,20,21,22,23,0,1,2,3,4,5,6,7,8,9,10,11]
time_step_in_netcdf_list = range(0,24)

for i in range(len(days)-1):
  print(days[i])
  current_day = days[i]
  next_day = days[i+1]
  
  cmaq_cdf_file = "/scratch/yli74/forecast/12km/POST/COMBINE3D_ACONC_v531_gcc_AQF5X_"+current_day+".nc"
  
  target_cdf_file = f'{cmaq_folder}/prediction_nc_files/COMBINE3D_ACONC_v531_gcc_AQF5X_'+current_day+'_ML_extracted.nc'
  
  if not os.path.exists(cmaq_cdf_file):
    print(f"{cmaq_cdf_file} doesn't exist")
    continue
    
  if os.path.exists(target_cdf_file):
    print(f"{target_cdf_file} already exists")
    continue
  
  df_cdf = xr.open_dataset(cmaq_cdf_file)
  daily_hourly_files = []
  for k in real_hour_list:
    real_hour_value = real_hour_list[k]
    if real_hour_value<12:
      day = next_day
    else:
      day = current_day
    #daily_hourly_files.append(f'{test_folder}/test_data_{day}_{turn_2_digits(real_hour_value)}.csv')
    daily_hourly_files.append(f'{cmaq_folder}/prediction_files/prediction_rf_{day}{turn_2_digits(real_hour_value)}.csv')
  
  daily_hourly_files = sorted(daily_hourly_files)
  #print("single day hourly files: ", all_hourly_files[i*24:(i+1)*24])
  print("single day hourly files: ", daily_hourly_files)
  df_from_each_hourly_file = (pd.read_csv(f) for f in daily_hourly_files)
  
  df_csv = pd.concat(df_from_each_hourly_file, ignore_index=True)

  reshaped_prediction = df_csv['prediction'].to_numpy().reshape(24, 1, 265, 442).astype(np.float32)
  print(reshaped_prediction.shape)
  
  # retain only two essential variables
  clean_df_cdf = df_cdf[['O3', 'TFLAG']]
  print("O3 attrs is: ", df_cdf.O3.attrs)
  
  # reduce VAR dim to 1
  new_tflag = df_cdf['TFLAG'].to_numpy()
  new_tflag = new_tflag[:, 0, :].reshape(24, 1, 2)
  
  # Apply changes to data variable in nc file
  clean_df_cdf['O3'] = (['TSTEP', 'LAY', 'ROW', 'COL'], reshaped_prediction)
  clean_df_cdf['TFLAG'] = (['TSTEP', 'VAR', 'DATE-TIME'], new_tflag)

  clean_df_cdf.O3.attrs = df_cdf.O3.attrs
  clean_df_cdf.TFLAG.attrs = df_cdf.TFLAG.attrs
  clean_df_cdf.attrs['VGLVLS'] = "1.f, 0.9941f"
  clean_df_cdf.attrs['VAR-LIST'] = "O3              "
#   create_and_clean_folder(f"{cmaq_folder}/prediction_nc_files")
  clean_df_cdf.to_netcdf(target_cdf_file,)

  print(f'Saved updated netCDF file: {target_cdf_file}')
  
