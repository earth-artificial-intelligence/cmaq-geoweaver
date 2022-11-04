from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from numpy import mean
from numpy import std
import matplotlib.pyplot as plt
import pandas as pd
import pickle


final = pd.read_csv('/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/final.csv')

filename = f'/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/xgboostModels.sav'
models = pickle.load(open(filename, 'rb'))

# evaluate a given model or set of models using cross-validation
def evaluate_model(model, X, y):
    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    scores = cross_val_score(model, X, y, scoring='neg_root_mean_squared_error', cv=cv, n_jobs=-1, error_score='raise')
    return scores

# Get the remaining rows after row 31 corresponding to the month of February as the testing set input.
X = final[31:].drop(['Date', 'AirNow_O3', 'Lat', 'Lon', 'latitude', 'longitude', 'date', 'O3_MDA8', 'O3_AVG'],axis=1)
# Get the remaining rows after row 31 corresponding to the month of February as the testing set target.
y = final[31:]['AirNow_O3']
# evaluate the models and store results
results, names = list(), list()
for name, model in models:
    scores = evaluate_model(model, X, y)
    results.append(scores)
    names.append(name)
    print('>%s %.3f (%.3f)' % (name, mean(scores), std(scores)))
    

# plot model performance for comparison
plt.rc('font', size=12)
fig, ax = plt.subplots(figsize=(20, 13))
plt.boxplot(results, labels=names, showmeans=True)
plt.suptitle("Voting-XGBoost", size=16)
plt.xlabel("XGBoost models")
plt.ylabel("neg_RMSE")
plt.grid()

fig.savefig('/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/boxPlot.png')
