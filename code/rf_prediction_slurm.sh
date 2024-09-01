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

python -u << INNER_EOF


# use the trained model to predict on the testing data and save the results to prediction_rf.csv

import pandas as pd
import pickle
from pathlib import Path
from time import sleep
import os
from sklearn.metrics import r2_score, mean_squared_error
from cmaq_ai_utils import *
from pathlib import Path
import datetime as dt

# never delete the input folder. must have some copy.
# print("create and clean the prediction folder")
#create_and_clean_folder(f"{cmaq_folder}/prediction_files/")

# importing data
# final=pd.read_csv(f"{cmaq_folder}/testing_input_hourly/testing.csv")
testing_path = f'{cmaq_folder}/testing_input_hourly'
#all_hourly_files = glob.glob(os.path.join(testing_path, "test_data_*.csv"))
#df_from_each_hourly_file = (pd.read_csv(f) for f in all_hourly_files)

# load the model from disk
# filename = f'{cmaq_folder}/models/rf_pycaret.sav'

def parse_date_from_file_name(filename: str):
    # Extract date and time parts from the filename
    date_part = filename.split('_')[2]
    time_part = filename.split('_')[3].split('.')[0]

    # Convert the extracted parts to a datetime object
    date_time = dt.datetime.strptime(date_part + time_part, "%Y%m%d%H")

    # Convert the datetime object to the desired format (YYYYMMDDHH)
    formatted_date_time = date_time.strftime("%Y%m%d%H")

    # Print the formatted date and time
    # print("Formatted Date and Time:", formatted_date_time)
    return formatted_date_time

def do_prediction():

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
            file_dateTime = parse_date_from_file_name(file_name)

            final_file_path = f'{cmaq_folder}/prediction_files/prediction_rf_{file_dateTime}.csv'
            file_path = os.path.join(testing_path, file_name)

            if Path(final_file_path).is_file():
                print(f"The file {file_path} exists. Skipped.")
                continue

            print(f"adding {file_name}")
            testing_df = pd.read_csv(file_path)
            # Perform any desired data processing on 'df' here
            # dropping unnecessary variables
            #   print("adding month, day, and hours")
            testing_df['YYYYMMDDHH'] = testing_df['YYYYMMDDHH'].map(str)
            testing_df['month'] = pd.to_numeric(testing_df['YYYYMMDDHH'].str[4:6], errors='coerce', downcast='integer')
            testing_df['day'] = pd.to_numeric(testing_df['YYYYMMDDHH'].str[6:8], errors='coerce', downcast='integer')
            testing_df['hours'] = pd.to_numeric(testing_df['YYYYMMDDHH'].str[8:10], errors='coerce', downcast='integer')

            #   print(testing_df['YYYYMMDDHH'].values[0])
            #   print(testing_df['month'].values[0])
            # file_dateTime = testing_df['YYYYMMDDHH'].values[0]
            #   print(f"file_dateTime={file_dateTime}")

            

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
            print(f'Saving: {final_file_path}')
            testing_df.to_csv(final_file_path,index=False)
            
    print("Prediction is all done.")


if __name__ == "__main__":
    do_prediction()

INNER_EOF

EOF

# Submit the Slurm job and wait for it to finish
echo "sbatch ${SCRIPT_NAME}"

# Submit the Slurm job
job_id=$(sbatch ${SCRIPT_NAME} | awk '{print $4}')
echo "job_id="${job_id}

if [ -z "${job_id}" ]; then
    echo "job id is empty. something wrong with the slurm job submission."
    exit 1
fi

# Wait for the Slurm job to finish
file_name=$(find /scratch/zsun -name '*'${job_id}'.out' -print -quit)
previous_content=$(cat file_name)
exit_code=0
while true; do
    # Capture the current content
    file_name=$(find /scratch/zsun -name '*'${job_id}'.out' -print -quit)
    current_content=$(<"${file_name}")

    # Compare current content with previous content
    diff_result=$(diff <(echo "$previous_content") <(echo "$current_content"))
    # Check if there is new content
    if [ -n "$diff_result" ]; then
        # Print the newly added content
        echo "$diff_result"
    fi
    # Update previous content
    previous_content="$current_content"


    job_status=$(scontrol show job ${job_id} | awk '/JobState=/{print $1}')
    #echo "job_status "$job_status
    #if [[ $job_status == "JobState=COMPLETED" ]]; then
    #    break
    #fi
    if [[ $job_status == *"COMPLETED"* ]]; then
        echo "Job $job_id has finished with state: $job_status"
        break;
    elif [[ $job_status == *"CANCELLED"* || $job_status == *"FAILED"* || $job_status == *"TIMEOUT"* || $job_status == *"NODE_FAIL"* || $job_status == *"PREEMPTED"* || $job_status == *"OUT_OF_MEMORY"* ]]; then
        echo "Job $job_id has finished with state: $job_status"
        exit_code=1
        break;
    fi
    sleep 10  # Adjust the sleep interval as needed
done

echo "Slurm job ($job_id) has finished."

echo "Print the job's output logs"
sacct --format=JobID,JobName,State,ExitCode,MaxRSS,Start,End -j $job_id
find /scratch/zsun/ -type f -name "*${job_id}.out" -exec cat {} \;
cat /scratch/zsun/test_data_slurm-*-$job_id.out

echo "All slurm job for ${SCRIPT_NAME} finishes."

exit $exit_code

