#!/bin/bash


# Specify the name of the script you want to submit
SCRIPT_NAME="upload_results_generated.sh"
echo "write the slurm script into ${SCRIPT_NAME}"
cat > ${SCRIPT_NAME} << EOF
#!/bin/bash
#SBATCH -J upload_results       # Job name
#SBATCH --output=/scratch/%u/%x-%N-%j.out  # Output file`
#SBATCH --error=/scratch/%u/%x-%N-%j.err   # Error file`
#SBATCH -n 1               # Number of tasks
#SBATCH -c 1               # Number of CPUs per task (threads)
#SBATCH --mem=10G          # Memory per node (use units like G for gigabytes) - this job must need 200GB lol
#SBATCH -t 0-02:00         # Runtime in D-HH:MM format

# this step will only upload the gifs to the web server for visualization
# the netcdfs are too big to move.

echo "Saving file name list to filelist.txt"
find /groups/ESS3/zsun/cmaq/ai_results/gifs/  -printf "%f\n" > /groups/ESS3/zsun/cmaq/ai_results/gifs/filelist.txt

echo "Copying evaluation txt to public server.."
#scp -i /home/zsun/.ssh/id_geobrain_no.pem /groups/ESS3/zsun/cmaq/ai_results/evaluation/* zsun@129.174.131.229:/var/www/html/cmaq_site/evaluation/
rsync -u -e "ssh -i /home/zsun/.ssh/id_geobrain_no.pem" -avz /groups/ESS3/zsun/cmaq/ai_results/evaluation/* zsun@129.174.131.229:/var/www/html/cmaq_site/evaluation/


echo "Copying animation gifs to public server.."
#scp -i /home/zsun/.ssh/id_geobrain_no.pem /groups/ESS3/zsun/cmaq/ai_results/gifs/* zsun@129.174.131.229:/var/www/html/cmaq_site/gifs/
rsync -u -e "ssh -i /home/zsun/.ssh/id_geobrain_no.pem" -avz /groups/ESS3/zsun/cmaq/ai_results/gifs/* zsun@129.174.131.229:/var/www/html/cmaq_site/gifs/
  
echo "Copying CMAQ evaluation metrics to public server.."
#scp -i /home/zsun/.ssh/id_geobrain_no.pem /groups/ESS/share/projects/SWUS3km/graph/12km/alleva_12km_o3_fore.txt zsun@129.174.131.229:/var/www/html/cmaq_site/evaluation/
rsync -u -e "ssh -i /home/zsun/.ssh/id_geobrain_no.pem" -avz /groups/ESS/share/projects/SWUS3km/graph/12km/alleva_12km_o3_fore.txt zsun@129.174.131.229:/var/www/html/cmaq_site/evaluation/alleva_12km_o3_fore.txt

#echo "Copying CMAQ netcdf files to public server"
#rsync -u -e "ssh -i /home/zsun/.ssh/id_geobrain_no.pem" -avz "/groups/ESS3/zsun/cmaq/ai_results/netcdfs/*2024*" zsun@129.174.131.229:/var/www/html/cmaq_site/netcdfs/

echo "Done"



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

