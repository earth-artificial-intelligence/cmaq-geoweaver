# Write first python in Geoweaver

import sys
import subprocess
import pkg_resources

# Required packages to run this process.
required = {'pandas','sklearn','h2o','numpy','matplotlib','pathlib'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print("Packages missing and will be installed: ", missing)
    python = sys.executable
    subprocess.check_call(
        [python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

################################
#  END OF PACKAGES VALIDATION  #
# Importing data
import os
from pathlib import Path
import pandas as pd
home = str(Path.home())
final=pd.read_csv(f'{home}/Geoweaver/merged_2020_2021.csv')

# defining training and testing variables
train=final.loc[final['year']==2020]
test=final.loc[final['year']==2021]

# processing training  data
train = train.drop(['Station.ID','YYYYMMDDHH','year','date','dayofyear','CMAQ12KM_NO2'],axis=1)
test = test.drop(['Station.ID','YYYYMMDDHH','year','date','dayofyear','CMAQ12KM_NO2'],axis=1)

## AutoML
import h2o
from h2o.automl import H2OAutoML
# Start the H2O cluster (locally)
h2o.init()

# Converting training and test data into h2o data format
train = h2o.H2OFrame(train)
test = h2o.H2OFrame(test)

# Identify predictors and response in training data
x = train.columns
y = "AirNOW_O3"
x.remove(y)

# Identify predictors and response in test data

test_x = test.columns
test_y = "AirNOW_O3"
test_x.remove(test_y)

# Run AutoML for 20 base models
aml = H2OAutoML(max_models=2, seed=1)
aml.train(x=x, y=y, training_frame=train)

# Make prediction
preds = aml.leader.predict(test)
prd_=preds['predict']

# transforming back to pandas data frame
dat = h2o.as_list(prd_)
org = h2o.as_list(test)

# Merging the prediction with test dataset
prediction = pd.concat([org, dat], axis=1)
prediction.to_csv(f'{home}/Geoweaver/prediction_autoML.csv')
