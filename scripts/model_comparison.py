# Write first python in Geoweaver
import pandas as pd
from sklearn.metrics import mean_squared_error
import glob
df=glob.glob('/home/mislam25/cmaq/prediction/*.csv')
print(df)
for i in df:
  file=pd.read_csv(i)
  mse=mean_squared_error(file['AirNOW_O3'],file['prediction'])
  print("MSE: ",mse)
# acceracy assisment 
# MSE
#mse = sklearn.metrics.mean_squared_error(pred, test_y)

