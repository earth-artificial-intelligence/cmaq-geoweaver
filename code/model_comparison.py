# Write first python in Geoweaver
import pandas as pd
from sklearn.metrics import mean_squared_error
import glob
from time import sleep
from pathlib import Path

# home directory
home = str(Path.home())

df=glob.glob(home+'/cmaq/prediction_files/*.csv')
for i in df:
  file=pd.read_csv(i)
  mse=mean_squared_error(file['AirNOW_O3'],file['prediction'])
  print(i+"- "+"MSE: ",mse)

sleep(10)

