# NASA GEOWEAVER
# CMAQ-AI Model: Poocessing the data - shifting columns of NO2

# Checking required packages are installed or not

import sys
import subprocess
print('running_preprocess')
#import pkg_resources

# Required packages to run this process.
#required = {'pandas','pathlib'}
#installed = {pkg.key for pkg in pkg_resources.working_set}
#missing = required - installed

#if missing:
 #   print("Packages missing and will be installed: ", missing)
 #   python = sys.executable
 #   subprocess.check_call(
    #    [python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

################################
#  END OF PACKAGES VALIDATION  #
################################

## importing necessary libraries
import glob
import pandas as pd
print('text_2021')
files=glob.glob(r'/groups/ESS/pmakkaro/az/2021/all/sep22/*.txt')
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
data_frame.to_csv('/home/mislam25/cmaq/2021.csv',index=False)
#data_frame.to_csv('D:/Research/CMAQ/local_test/2021.csv',index=False)
