#!/bin/bash

echo "start to run test_data_slurm_generated.sh"
pwd

# Specify the name of the script you want to submit
SCRIPT_NAME="rf_prediction_slurm_generated.sh"
echo "write the slurm script into ${SCRIPT_NAME}"
cat > ${SCRIPT_NAME} << EOF
#!/bin/bash
#SBATCH -J rf_prediction       # Job name
#SBATCH --output=/scratch/%u/%x-%N-%j.out  # Output file`
#SBATCH --error=/scratch/%u/%x-%N-%j.err   # Error file`
#SBATCH -n 1               # Number of tasks
#SBATCH -c 8               # Number of CPUs per task (threads)
#SBATCH --mem=150G          # Memory per node (use units like G for gigabytes) - this job must need 200GB lol
#SBATCH -t 0-01:00         # Runtime in D-HH:MM format
## Slurm can send you updates via email
#SBATCH --mail-type=FAIL  # BEGIN,END,FAIL         # ALL,NONE,BEGIN,END,FAIL,REQUEUE,..
#SBATCH --mail-user=zsun@gmu.edu     # Put your GMU email address here

# Activate your customized virtual environment
source /home/zsun/anaconda3/bin/activate

python << INNER_EOF


# use the trained model to predict on the testing data and save the results to prediction_rf.csv

import pandas as pd
import pickle
from pathlib import Path
from time import sleep
import os
from sklearn.metrics import r2_score, mean_squared_error
from cmaq_ai_utils import *

print("create and clean the prediction folder")
create_and_clean_folder(f"{cmaq_folder}/prediction_files/")

# importing data
# final=pd.read_csv(f"{cmaq_folder}/testing_input_hourly/testing.csv")
testing_path = f'{cmaq_folder}/testing_input_hourly'
#all_hourly_files = glob.glob(os.path.join(testing_path, "test_data_*.csv"))
#df_from_each_hourly_file = (pd.read_csv(f) for f in all_hourly_files)

# load the model from disk
# filename = f'{cmaq_folder}/models/rf_pycaret.sav'

print("start to load model")

filename = f'{model_folder}/rf_pycaret_o3_one_year_good.sav'
loaded_model = pickle.load(open(filename, 'rb'))

print("model is loaded")

#for testing_df in df_from_each_hourly_file:
file_list = os.listdir(testing_path)

# Initialize a flag to indicate if the final CSV file needs a header
write_header = True

for file_name in file_list:
    if file_name.endswith('.csv') and file_name.startswith('test_data_'):  # Adjust the file extension as needed
      print(f"adding {file_name}")
      file_path = os.path.join(testing_path, file_name)
      testing_df = pd.read_csv(file_path)
      # Perform any desired data processing on 'df' here
      # dropping unnecessary variables
      print("adding month, day, and hours")
      testing_df['YYYYMMDDHH'] = testing_df['YYYYMMDDHH'].map(str)
      testing_df['month'] = pd.to_numeric(testing_df['YYYYMMDDHH'].str[4:6], errors='coerce', downcast='integer')
      testing_df['day'] = pd.to_numeric(testing_df['YYYYMMDDHH'].str[6:8], errors='coerce', downcast='integer')
      testing_df['hours'] = pd.to_numeric(testing_df['YYYYMMDDHH'].str[8:10], errors='coerce', downcast='integer')

      print(testing_df['YYYYMMDDHH'].values[0])
      print(testing_df['month'].values[0])
      file_dateTime = testing_df['YYYYMMDDHH'].values[0]
      print(f"file_dateTime={file_dateTime}")
      #X = testing_df.drop(['YYYYMMDDHH','Latitude','Longitude'],axis=1)
      testing_df['time_of_day'] = (testing_df['hours'] % 24 + 4) // 4

      # Make coords even more coarse by rounding to closest multiple of 5 
      # (e.g., 40, 45, 85, 55)
      #testing_df['Latitude_ExtraCoarse'] = 0.1 * round(testing_df['Latitude']/0.1)
      #testing_df['Longitude_ExtraCoarse'] = 0.1 * round(testing_df['Longitude']/0.1)
      X = testing_df.drop(['YYYYMMDDHH','Latitude','Longitude', 'CO(moles/s)'],axis=1)

      print(X.columns)

      # # making prediction
      pred = loaded_model.predict(X)

      # adding prediction values to test dataset
      #testing_df['prediction'] = testing_df['CMAQ12KM_O3(ppb)'].tolist()
      testing_df['prediction'] = pred

      testing_df = testing_df[['Latitude', 'Longitude','YYYYMMDDHH','prediction']]
      # saving the dataset into local drive
      print(f'Saving: {cmaq_folder}/prediction_files/prediction_rf_{file_dateTime}.csv')
      testing_df.to_csv(f'{cmaq_folder}/prediction_files/prediction_rf_{file_dateTime}.csv',index=False)
        
print("Prediction is all done.")

INNER_EOF

EOF

# Submit the Slurm job and wait for it to finish
echo "sbatch ${SCRIPT_NAME}"
# should have another check. if there is another job running, should cancel it before submitting a new job.

# Find and cancel existing running jobs with the same script name
#existing_jobs=$(squeue -h -o "%A %j" -u $(whoami) | awk -v script="$SCRIPT_NAME" '$2 == script {print $1}')

# if [ -n "$existing_jobs" ]; then
#     echo "Canceling existing jobs with the script name '$SCRIPT_NAME'..."
#     for job_id in $existing_jobs; do
#         scancel $job_id
#     done
# else
#     echo "No existing jobs with the script name '$SCRIPT_NAME' found."
# fi

# Submit the Slurm job
job_id=$(sbatch ${SCRIPT_NAME} | awk '{print $4}')
echo "job_id="${job_id}

if [ -z "${job_id}" ]; then
    echo "job id is empty. something wrong with the slurm job submission."
    exit 1
fi

# Wait for the Slurm job to finish
while true; do
    job_status=$(scontrol show job ${job_id} | awk '/JobState=/{print $1}')
    #echo "job_status "$job_status
    #if [[ $job_status == "JobState=COMPLETED" ]]; then
    #    break
    #fi
    if [[ $job_status == *"COMPLETED"* || $job_status == *"CANCELLED"* || $job_status == *"FAILED"* || $job_status == *"TIMEOUT"* || $job_status == *"NODE_FAIL"* || $job_status == *"PREEMPTED"* || $job_status == *"OUT_OF_MEMORY"* ]]; then
        echo "Job $job_id has finished with state: $job_status"
        break;
    fi
    sleep 10  # Adjust the sleep interval as needed
done

echo "Slurm job ($job_id) has finished."

echo "Print the job's output logs"
sacct --format=JobID,JobName,State,ExitCode,MaxRSS,Start,End -j $job_id
find /scratch/zsun/ -type f -name "*${job_id}.out" -exec cat {} \;

#cat /scratch/zsun/test_data_slurm-*-$job_id.out

echo "All slurm job for ${SCRIPT_NAME} finishes."

