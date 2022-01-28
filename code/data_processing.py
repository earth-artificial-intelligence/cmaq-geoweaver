# Write first python in Geoweaver
import pandas as pd
final=pd.read_csv('D:/Research/CMAQ/Geoweaver/merged_2020_2021.csv')

# defining training and testing variables
train=final.loc[final['year']==2020]
test=final.loc[final['year']==2021]
# processing training  data
X = train.drop(['AirNOW_O3','Station.ID','YYYYMMDDHH','year','date','dayofyear','datetime'],axis=1)
y = train['AirNOW_O3']

# processing est data
test_X = test.drop(['AirNOW_O3','Station.ID','YYYYMMDDHH','year','date','dayofyear','datetime'],axis=1)
test_y = test['AirNOW_O3']


