#!/bin/bash

echo "start to run test_data_slurm_generated.sh"
pwd

echo "write the slurm script into test_data_slurm_generated.sh"
cat > test_data_slurm_generated.sh << EOF
#!/bin/bash
#SBATCH -J test_data_slurm       # Job name
#SBATCH --output=/scratch/%u/%x-%N-%j.out  # Output file`
#SBATCH --error=/scratch/%u/%x-%N-%j.err   # Error file`
#SBATCH -n 1               # Number of tasks
#SBATCH -c 4               # Number of CPUs per task (threads)
#SBATCH --mem=8G          # Memory per node (use units like G for gigabytes)
#SBATCH -t 0-01:00         # Runtime in D-HH:MM format

# Activate your customized virtual environment
source /home/zsun/anaconda3/bin/activate

python << INNER_EOF
# merge all hourly testing data into daily files

import pandas as pd
import glob
import os
from pathlib import Path
from cmaq_ai_utils import *

testing_path = f'{cmaq_folder}/testing_input_hourly'
print(f"testing_path: {testing_path}") 
# advisable to use os.path.join as this makes concatenation OS independent
# stupid move. why reading all files to concat a new file. Just append all the rows to the file!

combined_testing_csv_path = f"{testing_path}/testing.csv"
print(f"removed all file {combined_testing_csv_path}")
remove_file(f"{combined_testing_csv_path}")
#df_from_each_hourly_file = (pd.read_csv(f) for f in all_hourly_files)
file_list = os.listdir(testing_path)

# Initialize a flag to indicate if the final CSV file needs a header
write_header = True

for file_name in file_list:
    if file_name.endswith('.csv') and file_name.startswith('test_data_'):  # Adjust the file extension as needed
        print(f"adding {file_name}")
        file_path = os.path.join(testing_path, file_name)
        df = pd.read_csv(file_path)  # Read the CSV file into a dataframe
        # Perform any desired data processing on 'df' here
        # dropping unnecessary variables
        df['YYYYMMDDHH'] = df['YYYYMMDDHH'].map(str)
        df['month'] = df['YYYYMMDDHH'].str[4:6]
        df['day'] = df['YYYYMMDDHH'].str[6:8]
        df['hours'] = df['YYYYMMDDHH'].str[8:10]

        #cmaq.to_csv(f"{testing_path}/testing.csv",index=False)
        # Append or write the processed dataframe to the final CSV file
        mode = 'w' if write_header else 'a'
        header = True if write_header else False
        df.to_csv(combined_testing_csv_path, mode=mode, header=header, index=False)
        print(f"{combined_testing_csv_path} is updated")
        # After the first file, set the flag to False to avoid writing headers
        write_header = False

print(f'Combined data saved to {combined_testing_csv_path}')


INNER_EOF

EOF

# Submit the Slurm job and wait for it to finish
echo "sbatch test_data_slurm_generated.sh"
# should have another check. if there is another job running, should cancel it before submitting a new job.
# Specify the name of the script you want to submit
SCRIPT_NAME="test_data_slurm_generated.sh"

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
    else
        echo "Job $job_id is still running with state: $job_status"
fi
    sleep 10  # Adjust the sleep interval as needed
done

echo "Slurm job ($job_id) has finished."

echo "Print the job's output logs"
sacct --format=JobID,JobName,State,ExitCode,MaxRSS,Start,End -j $job_id
cat /scratch/zsun/test_data_slurm-hop046-$job_id.out

echo "All slurm job for test_data finishes."

