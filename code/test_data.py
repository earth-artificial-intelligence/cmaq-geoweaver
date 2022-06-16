import pandas as pd
from pathlib import Path

# home directory
home = str(Path.home())
cmaq=pd.read_csv("/groups/ESS/aalnaim/cmaq/test_data.csv")

# dropping unnecessary variables
cmaq['YYYYMMDDHH'] = cmaq['YYYYMMDDHH'].map(str)
cmaq['month'] = cmaq['YYYYMMDDHH'].str[4:6]
cmaq['day'] = cmaq['YYYYMMDDHH'].str[6:8]
cmaq['hours'] = cmaq['YYYYMMDDHH'].str[8:10]

#new_df=cmaq.drop(['YYYYMMDDHH'],axis=1)
cmaq.to_csv("/groups/ESS/aalnaim/cmaq/testing.csv",index=False)
