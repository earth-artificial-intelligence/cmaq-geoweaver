# NASA GEOWEAVER
# CMAQ-AI Model: Poocessing the data - shifting columns of NO2

## importing necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from time import sleep

# home directory
home = str(Path.home())

# importing data
final=pd.read_csv(home+'/cmaq/merged_2020_2021.csv')

# defining training variables
year_2020=final.loc[final['year']==2020]

# Processing training  data
selected_vars = year_2020.drop(['YYYYMMDDHH','year'],axis=1)

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
plt.savefig(home+'/cmaq/exploratory_analysis/correlation.png')
########################################################

# plotting r2 values of different variables vs AirNOW_O3
########################################################
columns=list(selected_vars)
for i in columns:
  try:
  	sns.lmplot(x=i, y="AirNOW_O3", data=selected_vars);
  	plt.savefig(home+'/cmaq/exploratory_analysis/'+i+'_AirNOW_O3.png')
  except FileNotFoundError:
    pass
    
########################################################

