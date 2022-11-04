import pandas as pd
import pickle
import math
import sklearn



final = pd.read_csv('/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/final.csv')


# Get the remaining rows after row 31 corresponding to the month of February as the testing set input.
X = final[31:].drop(['Date', 'AirNow_O3', 'Lat', 'Lon', 'latitude', 'longitude', 'date', 'O3_MDA8', 'O3_AVG'],axis=1)
# Get the remaining rows after row 31 corresponding to the month of February as the testing set target.
y = final[31:]['AirNow_O3']

filename = f'/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/xgboost.sav'
ensemble = pickle.load(open(filename, 'rb'))

pred = ensemble.predict(X)
dataset = final.iloc[31:].copy()
dataset['prediction'] = pred.tolist()

mse = sklearn.metrics.mean_squared_error(pred, y)
rmse = math.sqrt(mse)

print(mse, rmse)

dataset.to_csv("/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/prediction.csv", index=False)

