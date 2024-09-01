#!/bin/bash
# Specify the name of the script you want to submit
SCRIPT_NAME="preprocessing_test_netcdf.sh"
echo "write the slurm script into ${SCRIPT_NAME}"
cat > ${SCRIPT_NAME} << EOF
#!/bin/bash
#SBATCH -J preprocessing_test_netcdf       # Job name
#SBATCH --output=/scratch/%u/%x-%N-%j.out  # Output file`
#SBATCH --error=/scratch/%u/%x-%N-%j.err   # Error file`
#SBATCH -n 1               # Number of tasks
#SBATCH -c 4               # Number of CPUs per task (threads)
#SBATCH --mem=20G          # Memory per node (use units like G for gigabytes) - this job must need 200GB lol
#SBATCH -t 0-01:00         # Runtime in D-HH:MM format

# Activate your customized virtual environment
source /home/zsun/anaconda3/bin/activate

python -u << INNER_EOF


# load the prediction_rf.csv into a NetCDF file for visualization
from cmaq_ai_utils import *

today = datetime.today()
edate = today
sdate = today - timedelta(days=days_back)
days = get_days_list_for_prediction(sdate, edate)

prediction_path = f"{cmaq_folder}/prediction_files/"

all_hourly_files = sorted(glob.glob(os.path.join(prediction_path, "*.csv")))
# print("overall hourly files: ", all_hourly_files)
real_hour_list = [12,13,14,15,16,17,18,19,20,21,22,23,0,1,2,3,4,5,6,7,8,9,10,11]
time_step_in_netcdf_list = range(0,24)

for i in range(len(days)-1):
  print(days[i])
  current_day = days[i]
  next_day = days[i+1]
  
  cmaq_cdf_file = "/scratch/sma8/forecast/12km/POST/COMBINE3D_ACONC_v531_gcc_AQF5X_"+current_day+".nc"
  
  target_cdf_file = f'{cmaq_folder}/prediction_nc_files/COMBINE3D_ACONC_v531_gcc_AQF5X_'+current_day+'_ML_extracted.nc'
  
  if not os.path.exists(cmaq_cdf_file):
    print(f"{cmaq_cdf_file} doesn't exist")
    continue
    
  if os.path.exists(target_cdf_file):
    print(f"{target_cdf_file} already exists")
    continue
  
  df_cdf = xr.open_dataset(cmaq_cdf_file, engine='netcdf4')
  daily_hourly_files = []
  for k in real_hour_list:
    real_hour_value = real_hour_list[k]
    if real_hour_value<12:
      day = next_day
    else:
      day = current_day
    #daily_hourly_files.append(f'{test_folder}/test_data_{day}_{turn_2_digits(real_hour_value)}.csv')
    daily_hourly_files.append(f'{cmaq_folder}/prediction_files/prediction_rf_{day}{turn_2_digits(real_hour_value)}.csv')
  
  daily_hourly_files = sorted(daily_hourly_files)
  #print("single day hourly files: ", all_hourly_files[i*24:(i+1)*24])
  print("single day hourly files: ", daily_hourly_files)
  df_from_each_hourly_file = (pd.read_csv(f) for f in daily_hourly_files)
  
  df_csv = pd.concat(df_from_each_hourly_file, ignore_index=True)

  reshaped_prediction = df_csv['prediction'].to_numpy().reshape(24, 1, 265, 442).astype(np.float32)
  print(reshaped_prediction.shape)
  
  # retain only two essential variables
  clean_df_cdf = df_cdf[['O3', 'TFLAG']]
  print("O3 attrs is: ", df_cdf.O3.attrs)
  
  # reduce VAR dim to 1
  new_tflag = df_cdf['TFLAG'].to_numpy()
  new_tflag = new_tflag[:, 0, :].reshape(24, 1, 2)
  
  # Apply changes to data variable in nc file
  clean_df_cdf['O3'] = (['TSTEP', 'LAY', 'ROW', 'COL'], reshaped_prediction)
  clean_df_cdf['TFLAG'] = (['TSTEP', 'VAR', 'DATE-TIME'], new_tflag)

  clean_df_cdf.O3.attrs = df_cdf.O3.attrs
  clean_df_cdf.TFLAG.attrs = df_cdf.TFLAG.attrs
  clean_df_cdf.attrs['VGLVLS'] = "1.f, 0.9941f"
  clean_df_cdf.attrs['VAR-LIST'] = "O3              "
#   create_and_clean_folder(f"{cmaq_folder}/prediction_nc_files")
  clean_df_cdf.to_netcdf(target_cdf_file,)

  print(f'Saved updated netCDF file: {target_cdf_file}')


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

