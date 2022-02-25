stdout=subprocess.DEVNULL)

################################
#  END OF PACKAGES VALIDATION  #
################################

## importing necessary libraries
import glob
import pandas as pd
print('running text_2020')
file=open
files=glob.glob(r'/groups/ESS/pmakkaro/az/2020/all/sep22/*.txt')
#files=glob.glob(r'D:/Research/CMAQ/2020/text/*.txt')
data_frame = pd.DataFrame()
merged=[]
for file in files:
  with open(file,'r') as f:
    	df=pd.read_csv(f)
    	merged.append(df)
data_frame = pd.concat(merged)
data_frame['YYYYMMDDHH'] = data_frame['YYYYMMDDHH'].map(str)
data_frame['year'] = data_frame['YYYYMMDDHH'].str[:4]
data_frame['month'] = data_frame['YYYYMMDDHH'].str[4:6]
data_frame['day'] = data_frame['YYYYMMDDHH'].str[6:8]
data_frame['hours'] = data_frame['YYYYMMDDHH'].str[8:10]
data_frame.to_csv('/home/mislam25/cmaq/2020.csv',index=False)
