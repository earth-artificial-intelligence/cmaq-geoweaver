# load the prediction_rf.csv into a NetCDF file for visualization
from cmaq_ai_utils import *

# end_date = datetime.today()
# base = end_date - timedelta(days=2)
sdate = date(2022, 8, 1)   # start date
edate = date(2022, 8, 2)   # end date
days = get_days_list(sdate, edate)

df_cdf = xr.open_dataset("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/CCTMout/12km/POST/COMBINE3D_ACONC_v531_gcc_AQF5X_"+days[0]+"_extracted.nc")

df_csv = pd.read_csv(f"{cmaq_folder}/prediction_files/prediction_rf.csv")

# df_csv['YYYYMMDDHH'] = df_csv['YYYYMMDDHH'].astype(str)
# print(df_csv['YYYYMMDDHH'].unique())
# df_filt = df_csv[df_csv['YYYYMMDDHH'].str.contains(days[1]+"|"+days[0]+"|"+days[2], case = False, regex=True)] #this line seems unnecessary
# df_filt = df_filt[(df_filt['YYYYMMDDHH'] > days[0]+'11') & (df_filt['YYYYMMDDHH'] < days[1]+'12')]
# print(df_filt['YYYYMMDDHH'].unique())

# Reshape "prediction/Latitude/Longitude" columns to (TSTEP, ROW, COL), these lines will reshape data into (24, 265, 442)
#reshaped_prediction = np.atleast_3d(df_filt['prediction']).reshape(-1, 265, 442)
reshaped_prediction = np.atleast_3d(df_csv['prediction']).reshape(-1, 265, 442)
print(reshaped_prediction.shape)

# Remove "LAY" Dimension in O3 variable already in nc file.
reduced_dim = df_cdf['O3'].sel(LAY=1, drop=True)

create_and_clean_folder(f"{cmaq_folder}/prediction_nc_files")

for i in range(len(days)-1):
  print(days[i])
  
  single_day_result = reshaped_prediction[i*24:(i+1)*24, :, :]
  print(single_day_result.shape)
  
  # Swap values from original nc file with new prediction data
  reduced_dim.values = single_day_result

  # Apply changes to data variable in nc file
  df_cdf['O3'] = (['TSTEP', 'ROW', 'COL'], single_day_result)

  
  df_cdf.to_netcdf(f'{cmaq_folder}/prediction_nc_files/COMBINE3D_ACONC_v531_gcc_AQF5X_'+days[i]+'_'+days[i+1]+'_ML_extracted.nc')

  print(f'Saved updated netCDF file: {cmaq_folder}/prediction_nc_files/COMBINE3D_ACONC_v531_gcc_AQF5X_'+days[i]+'_'+days[i+1]+'_ML_extracted.nc')


