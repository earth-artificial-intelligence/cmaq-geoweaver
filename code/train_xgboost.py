import pandas as pd
import pickle
from xgboost.sklearn import XGBRegressor
from sklearn.ensemble import VotingRegressor


final = pd.read_csv('/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/final.csv')

# Take the first 31 rows corresponding to the month of January as the training input (predictors)
X = final[:31].drop(['Date', 'AirNow_O3', 'Lat', 'Lon', 'latitude', 'longitude', 'date', 'O3_MDA8', 'O3_AVG'],axis=1)

# Take the first 31 rows corresponding to the month of January as the training target
y = final[:31]['AirNow_O3']




# define the base models
models = list()
models.append(('XGB1', XGBRegressor(max_depth=1)))
models.append(('XGB2', XGBRegressor(max_depth=2)))
models.append(('XGB3', XGBRegressor(max_depth=3)))
models.append(('XGB4', XGBRegressor(max_depth=4)))
models.append(('XGB5', XGBRegressor(max_depth=5)))
models.append(('XGB6', XGBRegressor(max_depth=6)))

# define the voting ensemble
ensemble = VotingRegressor(estimators=models)

# fit the model on all available data
ensemble.fit(X, y)


# save the model to disk
trainedModel = '/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/xgboost.sav'
listOfModels = '/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/xgboostModels.sav'

pickle.dump(ensemble, open(trainedModel, 'wb'))
pickle.dump(models, open(listOfModels, 'wb'))
print(f"Model is trained and saved to {trainedModel}")
