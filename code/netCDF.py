# load the prediction_rf.csv into a NetCDF file for visualization
from cmaq_ai_utils import *


# end_date = datetime.today()
# base = end_date - timedelta(days=2)
sdate = date(2022, 8, 5)   # start date
edate = date(2022, 8, 6)   # end date
days = get_days_list(sdate, edate)

prediction_path = f"{cmaq_folder}/prediction_files/"
create_and_clean_folder(f"{cmaq_folder}/prediction_nc_files/")

# df_csv['YYYYMMDDHH'] = df_csv['YYYYMMDDHH'].astype(str)
# print(df_csv['YYYYMMDDHH'].unique())
# df_filt = df_csv[df_csv['YYYYMMDDHH'].str.contains(days[1]+"|"+days[0]+"|"+days[2], case = False, regex=True)] #this line seems unnecessary
# df_filt = df_filt[(df_filt['YYYYMMDDHH'] > days[0]+'11') & (df_filt['YYYYMMDDHH'] < days[1]+'12')]
# print(df_filt['YYYYMMDDHH'].unique())

# Reshape "prediction/Latitude/Longitude" columns to (TSTEP, ROW, COL), these lines will reshape data into (24, 265, 442)
#reshaped_prediction = np.atleast_3d(df_filt['prediction']).reshape(-1, 265, 442)
print(prediction_path)
all_hourly_files = sorted(glob.glob(os.path.join(prediction_path, "*.csv")))
print("overall hourly files: ", all_hourly_files)

for i in range(1):
    print(days[i])

#     df_cdf = xr.open_dataset(
#         "/groups/ESS/share/projects/SWUS3km/data/cmaqdata/CCTMout/12km/POST/COMBINE3D_ACONC_v531_gcc_AQF5X_" + days[i + 1] + "_extracted.nc")
    df_cdf = xr.open_dataset(
        "/Users/uhhmed/localCMAQ/COMBINE3D_ACONC_v531_gcc_AQF5X_20220806_extracted.nc")

    print("single day hourly files: ", all_hourly_files[i * 24:(i + 1) * 24])
    df_from_each_hourly_file = (pd.read_csv(f)
                                for f in all_hourly_files[i * 24:(i + 1) * 24])

    df_csv = pd.concat(df_from_each_hourly_file, ignore_index=True)

    reshaped_prediction = df_csv['prediction'].to_numpy().reshape(24, 265, 442)
    print(reshaped_prediction.shape)

    # Remove "LAY" Dimension in O3 variable already in nc file.
    reduced_dim = df_cdf['O3'].sel(LAY=1, drop=True)

    # Swap values from original nc file with new prediction data
    reduced_dim.values = reshaped_prediction

    # Apply changes to data variable in nc file
    df_cdf['O3'] = (['TSTEP', 'ROW', 'COL'], reshaped_prediction)
    df_cdf = df_cdf[['O3', 'TFLAG']]
    
#   create_and_clean_folder(f"{cmaq_folder}/prediction_nc_files")
    df_cdf.to_netcdf(
        f'{cmaq_folder}/prediction_nc_files/COMBINE3D_ACONC_v531_gcc_AQF5X_' + days[i] + '_ML_extracted.nc')

    print(
        f'Saved updated netCDF file: {cmaq_folder}/prediction_nc_files/COMBINE3D_ACONC_v531_gcc_AQF5X_' + days[i] + '_ML_extracted.nc')

