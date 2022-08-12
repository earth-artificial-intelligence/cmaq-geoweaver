# load the prediction_rf.csv into a NetCDF file for visualization
from cmaq_ai_utils import *

# end_date = datetime.today()
# base = end_date - timedelta(days=2)
sdate = date(2022, 7, 1)   # start date
edate = date(2022, 7, 2)   # end date
days = get_days_list(sdate, edate)

df_cdf = xr.open_dataset("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/CCTMout/12km/POST/COMBINE3D_ACONC_v531_gcc_AQF5X_"+days[0]+"_extracted.nc")

df_csv = pd.read_csv(f"{cmaq_folder}/prediction_files/prediction_rf.csv")

df_csv['YYYYMMDDHH'] = df_csv['YYYYMMDDHH'].astype(str)
df_filt = df_csv[df_csv['YYYYMMDDHH'].str.contains(days[1]+"|"+days[0]+"|"+days[2], case = False, regex=True)]
print(df_filt['YYYYMMDDHH'].unique())
df_filt = df_filt[(df_filt['YYYYMMDDHH'] > days[0]+'11') & (df_filt['YYYYMMDDHH'] < days[1]+'12')]


# Reshape "prediction/Latitude/Longitude" columns to (TSTEP, ROW, COL), these lines will reshape data into (24, 265, 442)
reshaped_prediction = np.atleast_3d(df_filt['prediction']).reshape(-1, 265, 442)

# Remove "LAY" Dimension in O3 variable already in nc file.
reduced_dim = df_cdf['O3'].sel(LAY=1, drop=True)
# Swap values from original nc file with new prediction data
reduced_dim.values = reshaped_prediction

# Apply changes to data variable in nc file
df_cdf['O3'] = (['TSTEP', 'ROW', 'COL'], reshaped_prediction)

create_and_clean_folder(f"{cmaq_folder}/prediction_nc_files")
df_cdf.to_netcdf(f'{cmaq_folder}/prediction_nc_files/COMBINE3D_ACONC_v531_gcc_AQF5X_'+days[0]+'_'+days[1]+'_ML_extracted.nc')

print(f'Saved updated netCDF file: {cmaq_folder}/prediction_nc_files/COMBINE3D_ACONC_v531_gcc_AQF5X_'+days[0]+'_'+days[1]+'_ML_extracted.nc')


