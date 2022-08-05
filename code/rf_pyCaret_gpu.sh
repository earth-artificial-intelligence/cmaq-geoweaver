# train the model using training.csv


echo "#!/bin/bash
#SBATCH --partition=gpuq                    # the DGX only belongs in the 'gpu'  partition
#SBATCH --qos=gpu                           # need to select 'gpu' QoS
#SBATCH --job-name=cmaq-gpu
#SBATCH --output=cmaq-gpu.%j.out
#SBATCH --error=cmaq-gpu.%j.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64                 # up to 128;
#SBATCH --gres=gpu:A100.40gb:4              # up to 8; only request what you need
#SBATCH --mem-per-cpu=3500M                 # memory per CORE; total memory is 1 TB (1,000,000 MB)
#SBATCH --export=ALL
#SBATCH --time=0-04:00:00                   # set to 1hr; please choose carefully
set echo
umask 0027
# to see ID and state of GPUs assigned
nvidia-smi

module load python
source /home/aalnaim/CMAQAI/bin/activate

cat <<EOF >>/groups/ESS/aalnaim/cmaq/rf_pyCaret.py
# Write first python in Geoweaver# NASA GEOWEAVER
# CMAQ-AI Model: Training Voting-XGBoost model

# Importing necessary libraries
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestRegressor
from xgboost.sklearn import XGBRegressor
import pickle
from pathlib import Path

# home directory
home = str(Path.home())

# importing data
final=pd.read_csv('/groups/ESS/aalnaim/cmaq/training.csv')
print(final.head())
final=final.dropna()

# Processing training  data
X = final.drop(['AirNOW_O3','Latitude_x','Longitude_x'],axis=1)
y = final['AirNOW_O3']

rf = RandomForestRegressor(bootstrap=True, ccp_alpha=0.0, criterion='mse',
                      max_depth=None, max_features='auto', max_leaf_nodes=None,
                      max_samples=None, min_impurity_decrease=0.0,
                      min_samples_leaf=1,
                      min_samples_split=2, min_weight_fraction_leaf=0.0,
                      n_estimators=100, n_jobs=-1, oob_score=False,
                      random_state=3086, verbose=0, warm_start=False)

rf.fit(X, y)

# save the model to disk
filename = '/groups/ESS/aalnaim/cmaq/models/rf_from_hourly_aug3.sav'
#filename = 'D:/Research/CMAQ/local_test/xgboost.sav'
pickle.dump(rf, open(filename, 'wb'))
EOF
python /groups/ESS/aalnaim/cmaq/rf_pyCaret.py" >> /groups/ESS/aalnaim/cmaq/cmaq_gpu.slurm

sbatch /groups/ESS/aalnaim/cmaq/cmaq_gpu.slurm

sleep 20
