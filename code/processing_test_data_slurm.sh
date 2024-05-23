#!/bin/bash


echo "start to run processing_test_data_generated.sh"
pwd

# Specify the name of the script you want to submit
SCRIPT_NAME="processing_test_data_generated.sh"
echo "write the slurm script into ${SCRIPT_NAME}"
cat > ${SCRIPT_NAME} << EOF
#!/bin/bash
#SBATCH -J processing_test_data       # Job name
#SBATCH --output=/scratch/%u/%x-%N-%j.out  # Output file`
#SBATCH --error=/scratch/%u/%x-%N-%j.err   # Error file`
#SBATCH -n 1               # Number of tasks
#SBATCH -c 4               # Number of CPUs per task (threads)
#SBATCH --mem=50G          # Memory per node (use units like G for gigabytes) - this job must need 200GB lol
#SBATCH -t 0-01:00         # Runtime in D-HH:MM format

# Activate your customized virtual environment
source /home/zsun/anaconda3/bin/activate

python << INNER_EOF

# get hourly CMAQ data into csv for prediction

from cmaq_ai_utils import *


#edate = datetime.today()
#sdate = edate - timedelta(days=1)
# today = datetime.today()
# edate = today
# sdate = today - timedelta(days=days_back)

#sdate = date(2022, 8, 6)   # start date
#edate = date(2022, 8, 8)   # end date
# days = get_days_list_for_prediction(sdate, edate)

real_hour_list = [12,13,14,15,16,17,18,19,20,21,22,23,0,1,2,3,4,5,6,7,8,9,10,11]
time_step_in_netcdf_list = range(0,24)

test_folder = f"{cmaq_folder}/testing_input_hourly/"
create_and_clean_folder(test_folder)  # don't clean folder anymore
#os.makedirs(test_folder, exist_ok=True)

for x in range(len(days)-1):
  current_day = days[x]
  next_day = days[x+1]
  print("Getting data for: "+current_day)
  
  # read cmaq results
  cmaq_file = "/scratch/yli74/forecast/12km/POST/COMBINE3D_ACONC_v531_gcc_AQF5X_"+current_day+".nc"
  if not os.path.exists(cmaq_file):
    print(f"CMAQ file {cmaq_file} doesn't exist")
    continue
  
  target_cdf_file = f'{cmaq_folder}/prediction_nc_files/COMBINE3D_ACONC_v531_gcc_AQF5X_'+current_day+'_ML_extracted.nc'
    
  if os.path.exists(target_cdf_file):
    print(f"{target_cdf_file} already exists")
    continue
  
  df_cmaq = xr.open_dataset(cmaq_file, engine='netcdf4')
  
  # read mcip results 
  mcip_file = "/groups/ESS/share/projects/SWUS3km/data/cmaqdata/mcip/12km/METCRO2D_"+current_day+".nc"
  df_mcip = xr.open_dataset(mcip_file, engine='netcdf4')
  
  # read emissions results 
  df_emis = xr.open_dataset("/groups/ESS/share/projects/SWUS3km/data/cmaqdata/emis2021/12km/all/emis_mole_all_"+current_day+"_AQF5X_cmaq_cb6ae7_2017gb_17j.ncf", engine='netcdf4')
  
  for k in time_step_in_netcdf_list:
    
    real_hour_value = real_hour_list[k]
    
    if real_hour_value<12:
      day = next_day
    else:
      day = current_day
    
    hourly_target_file = f'{test_folder}/test_data_{day}_{turn_2_digits(real_hour_value)}.csv'
    if os.path.exists(hourly_target_file):
      print(f"Hourly csv file {hourly_target_file} already exist")
      continue
    
    df_hourly = pd.DataFrame()
    
    #print("df_cmaq.variables['O3'] shape: ", df_cmaq.variables['O3'].shape)
    #print("df_cmaq.variables['O3'][:] shape: ", df_cmaq.variables['O3'][:].shape)
    #print("df_cmaq.variables['O3'][:].values[k, 0].shape", df_cmaq.variables['O3'][:].values[k, 0].shape)
    # CMAQ data
    # O3 variable
    o3=df_cmaq.variables['O3'][:].values[k, 0]
    cmaq_O3=list(np.ravel(o3).transpose())
    #print("o3 shape: ", o3.shape)
    #print("cmaq_O3 shape: ", np.ravel(o3).transpose().shape)
    
    # NO2
    no2=df_cmaq.variables['NO2'][:].values[k, 0]
    cmaq_NO2=list(np.ravel(no2).transpose())
    
    # CO
    co=df_cmaq.variables['CO'][:].values[k, 0]
    cmaq_CO=list(np.ravel(co).transpose())
    
    # PM25_CO
    pm25=df_cmaq.variables['PM25_OC'][:].values[k, 0]
    cmaq_PM25_CO=list(np.ravel(pm25).transpose())
    
    # EMIS data
    co_emis=df_emis.variables['CO'][:].values[k, 0]
    CO_emi=list(np.ravel(co_emis).transpose())    
    
    # MCIP data
    # CO variable
    prsfc=df_mcip.variables['PRSFC'][:].values[k, 0]
    PRSFC=list(np.ravel(prsfc).transpose())
    
    # NO2
    pbl=df_mcip.variables['PBL'][:].values[k, 0]
    PBL=list(np.ravel(pbl).transpose())
    
    # TEMP2
    temp2=df_mcip.variables['TEMP2'][:].values[k, 0]
    TEMP2=list(np.ravel(temp2).transpose())
    
    # WSPD10
    wspd10=df_mcip.variables['WSPD10'][:].values[k, 0]
    WSPD10=list(np.ravel(wspd10).transpose())
    
    # WDIR10
    wdir10=df_mcip.variables['WDIR10'][:].values[k, 0]
    WDIR10=list(np.ravel(wdir10).transpose())
    
    # RGRND
    rgrnd=df_mcip.variables['RGRND'][:].values[k, 0]
    RGRND=list(np.ravel(rgrnd).transpose())
    
    # CFRAC
    cfrac=df_mcip.variables['CFRAC'][:].values[k, 0]
    CFRAC=list(np.ravel(cfrac).transpose())
    
    ## LAT/LON data
    df_coords = xr.open_dataset('/home/yli74/scripts/plots/2020fire/GRIDCRO2D', engine='netcdf4')
    
    lat = df_coords.variables['LAT'][:].values[0,0]
    #print("lat shape", lat.shape)
    lat_flt=np.ravel(lat)
    LAT=lat_flt #np.tile(lat_flt,1)
    
    lon = df_coords.variables['LON'][:].values[0,0]
    lon_flt=np.ravel(lon)
    LON=lon_flt #np.tile(lon_flt,1)
    
    df_hourly['Latitude'] = LAT
    df_hourly['Longitude'] = LON
    df_hourly['YYYYMMDDHH'] = day+turn_2_digits(real_hour_value)
    df_hourly['CMAQ12KM_O3(ppb)'] = cmaq_O3
    df_hourly['CMAQ12KM_NO2(ppb)'] = cmaq_NO2
    df_hourly['CMAQ12KM_CO(ppm)'] = cmaq_CO
    df_hourly['CMAQ_OC(ug/m3)'] = cmaq_PM25_CO
    df_hourly['CO(moles/s)'] = CO_emi
    df_hourly['PRSFC(Pa)'] = PRSFC
    df_hourly['PBL(m)'] = PBL
    df_hourly['TEMP2(K)'] = TEMP2
    df_hourly['WSPD10(m/s)'] = WSPD10
    df_hourly['WDIR10(degree)'] = WDIR10
    df_hourly['RGRND(W/m2)'] = RGRND
    df_hourly['CFRAC'] = CFRAC
    df_hourly['month'] = df_hourly['YYYYMMDDHH'].str[4:6]
    df_hourly['day'] = df_hourly['YYYYMMDDHH'].str[6:8]
    df_hourly['hours'] = df_hourly['YYYYMMDDHH'].str[8:10]
    print(f'Saving file: test_data_{day}_{turn_2_digits(real_hour_value)}.csv')
    df_hourly.to_csv(hourly_target_file, index=False)

print('Done with preparing testing data!')


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

