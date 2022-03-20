## importing necessary libraries
import glob
import pandas as pd
from pathlib import Path
# home directory
home = str(Path.home())
files=glob.glob(r'/groups/ESS/mislam25/cmaq_results_2020_2021/*.txt')
#files=glob.glob(r'D:/Research/CMAQ/2021/text/*.txt')
data_frame = pd.DataFrame()
merged=[]
for file in files:
    df=pd.read_csv(file)
    merged.append(df)
data_frame = pd.concat(merged)
data_frame['YYYYMMDDHH'] = data_frame['YYYYMMDDHH'].map(str)
data_frame['year'] = data_frame['YYYYMMDDHH'].str[:4]
data_frame['month'] = data_frame['YYYYMMDDHH'].str[4:6]
data_frame['day'] = data_frame['YYYYMMDDHH'].str[6:8]
data_frame['hours'] = data_frame['YYYYMMDDHH'].str[8:10]
data_frame.to_csv(home+'/cmaq/cmaq_2020_2021.csv',index=False)
#data_frame.to_csv('D:/Research/CMAQ/local_test/2021.csv',index=False)
