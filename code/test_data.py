# merge all hourly testing data into daily files

import pandas as pd
import glob
import os
from pathlib import Path
from cmaq_ai_utils import *

testing_path = f'{cmaq_folder}/testing_input_hourly'
all_hourly_files = glob.glob(os.path.join(testing_path, "test_data_*.csv"))   
# advisable to use os.path.join as this makes concatenation OS independent

df_from_each_hourly_file = (pd.read_csv(f) for f in all_hourly_files)
cmaq = pd.concat(df_from_each_hourly_file, ignore_index=True)

# dropping unnecessary variables
cmaq['YYYYMMDDHH'] = cmaq['YYYYMMDDHH'].map(str)
cmaq['month'] = cmaq['YYYYMMDDHH'].str[4:6]
cmaq['day'] = cmaq['YYYYMMDDHH'].str[6:8]
cmaq['hours'] = cmaq['YYYYMMDDHH'].str[8:10]

cmaq.to_csv(f"{testing_path}/testing.csv",index=False)

print('Done with generating testing.csv!')
