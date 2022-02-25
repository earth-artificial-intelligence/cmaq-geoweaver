
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
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# importing data
final=pd.read_csv('/home/mislam25/cmaq/merged_2020_2021.csv')
#final=pd.read_csv('D:/Research/CMAQ/local_test/merged_2020_2021.csv')

# defining training variables
year_2020=final.loc[final['year']==2020]

# Processing training  data
selected_vars = year_2020.drop(['Station.ID','YYYYMMDDHH','year','date','dayofyear'],axis=1)

########################################################
## Correlation matrix heatmap
# Correlation between different variables
corr = selected_vars.corr()
# Set up the matplotlib plot configuration
f, ax = plt.subplots(figsize=(18, 10))
# Generate a mask for upper traingle
mask = np.triu(np.ones_like(corr, dtype=bool))
# Configure a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)
# Draw the heatmap
sns.heatmap(corr, annot=True, mask = mask, cmap=cmap)
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top + 0.5)
#ax.set(xlim=(0, 12))
plt.savefig('/home/mislam25/cmaq/EDA/correlation.png')
########################################################

# plotting r2 values of different variables vs AirNOW_O3
########################################################
columns=list(selected_vars)
for i in columns:
  try:
  	sns.lmplot(x=i, y="AirNOW_O3", data=selected_vars);
  	plt.savefig('/home/mislam25/cmaq/EDA/'+i+'_AirNOW_O3.png')
  except FileNotFoundError:
    pass
    
########################################################
