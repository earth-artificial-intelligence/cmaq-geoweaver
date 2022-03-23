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
new_df=data_frame.drop(['Station ID','CMAQ_NO(ppb)','AirNOW_NO2(ppb)','AirNOW_CO(ppm)'],axis=1)
final_df = new_df.rename(columns={new_df.columns[3]: 'AirNOW_O3'})
final_df = final_df[final_df.AirNOW_O3!= -999]
final_df.to_csv(home+'/cmaq/merged_2020_2021.csv',index=False)

