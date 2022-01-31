# Write first python in Geoweaver
import sys
import subprocess
import pkg_resources

# Required packages to run this process.
required = {'pandas','pathlib'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print("Packages missing and will be installed: ", missing)
    python = sys.executable
    subprocess.check_call(
        [python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

################################
#  END OF PACKAGES VALIDATION  #
################################

## importing necessary libraries

import pandas as pd
import datetime
import os
from pathlib import Path
home = str(Path.home())

# defining function for shifting data
month_i=[1,2,3,4,5,6,7,8,9,10,11,12]
def shift(file):
    station=file['Station.ID'].unique()
    file['date']=pd.to_datetime(file[["year", "month", "day","hours"]]) # creating date
    file['dayofyear'] = pd.to_datetime(file['date']).dt.dayofyear # converting monthly days to yearly dasy
    dfs = dict(tuple(file.groupby('Station.ID'))) # grouping the data by station
#    print(dfs)
    list_final=[]
    for site in station:
        list1=dfs[site]  # selecting dataset for each station
        o3_max=list1.loc[list1.groupby("dayofyear")["AirNOW_O3"].idxmax()] # daily max values
        o3_month=pd.DataFrame(o3_max.groupby('month',as_index=False)['hours'].mean()) # monthly average hour
        no2_max=list1.loc[list1.groupby("dayofyear")["CMAQ12KM_NO2"].idxmax()] # daily amx values
        no2_month=pd.DataFrame(no2_max.groupby('month',as_index=False)['hours'].mean()) # montly average hour
        merge_hour=pd.concat([o3_month,no2_month],axis = 1) # merging two table
        merge_hour.columns = ['month1','hours1', 'month2','hours2'] # renaming column name
        merge_hour['hours_diff']=merge_hour['hours1']-merge_hour['hours2']
        merge_hour.hours_diff = merge_hour.hours_diff.astype(int) # converting hours_diff to int
        months = dict(tuple(list1.groupby('month')))   # grouping the data by month
        diff=merge_hour['hours_diff'] # extracting hours difference field
        mon=merge_hour['month1'] # extracting month field

        for (m,n) in zip(mon,diff):
            list2= months[m] # selecting dataset for each month and for each station
            list3=list2.loc[list2['month'] == m] # subsetting dataset for each month
            list3['CMAQ12KM_NO2_new'] = list3['CMAQ12KM_NO2'].shift(n) # shifting rows for each month
            list_final.append(list3)
    return list_final


  
# Importing and merging 2020 and 2021 dataset
df1 = pd.read_csv(f'{home}/Geoweaver/full_20_lstm.csv')
df2 = pd.read_csv(f'{home}/Geoweaver/full_21_lstm.csv')
#merging two dataframe vertically
mrg=df1.append(df2, ignore_index=True)
df3_rs=pd.read_csv(f'{home}/Geoweaver/merged_rs.csv')
# merging
final=pd.merge(mrg,df3_rs, on=['year', 'month','day','hours','Station.ID'])

#shifting CMAQ NO2
shift_df=shift(final)
data_frame = pd.concat(shift_df) # concatening the list

# droping no data from all column and AirNOW_O3
data_new1 = data_frame.drop(['Unnamed: 0'],axis=1)
data_new=data_new1.dropna() 
final_df = data_new[data_new.AirNOW_O3!= -999]
final_df.to_csv(f'{home}/Geoweaver/merged_2020_2021.csv')
