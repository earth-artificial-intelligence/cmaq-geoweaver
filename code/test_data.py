# merge all hourly testing data into daily files

import pandas as pd
import glob
import os
from pathlib import Path

# home directory
# home = str(Path.home())

path = '/groups/ESS/aalnaim/cmaq/input_hourly'
all_hourly_files = glob.glob(os.path.join(path, "test_data_*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent

df_from_each_hourly_file = (pd.read_csv(f) for f in all_hourly_files)
cmaq = pd.concat(df_from_each_hourly_file, ignore_index=True)

# dropping unnecessary variables
cmaq['YYYYMMDDHH'] = cmaq['YYYYMMDDHH'].map(str)
cmaq['month'] = cmaq['YYYYMMDDHH'].str[4:6]
cmaq['day'] = cmaq['YYYYMMDDHH'].str[6:8]
cmaq['hours'] = cmaq['YYYYMMDDHH'].str[8:10]

#new_df=cmaq.drop(['YYYYMMDDHH'],axis=1)
cmaq.to_csv("/groups/ESS/aalnaim/cmaq/input_hourly/testing.csv",index=False)

print('Done!')
