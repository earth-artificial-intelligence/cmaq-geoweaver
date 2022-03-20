#!/bin/bash
#SBATCH --partition=gpuq                    # the DGX only belongs in the 'gpu'  partition
#SBATCH --qos=gpu                           # need to select 'gpu' QoS
#SBATCH --job-name=python-gpu
#SBATCH --output=python-gpu.%j.out
#SBATCH --error=python-gpu.%j.err
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=2                # up to 128; 
#SBATCH --gres=gpu:A100.40gb:1              # up to 8; only request what you need
#SBATCH --mem-per-cpu=3500M                 # memory per CORE; total memory is 1 TB (1,000,000 MB)
#SBATCH --export=ALL 
#SBATCH --time=0-00:20:00                   # set to 1hr; please choose carefully

set echo
umask 0027

module load ncl
# to see ID and state of GPUs assigned
cd ~/cmaq
dateYesterday=$(date -d "1 day ago" '+%-d')
dateMonth=$(date -d "yesterday" '+%-m')
ncl dateMonth=$dateMonth dateYesterday=$dateYesterday /groups/ESS/mislam25/cmaq12_airnow_O3.ncl

#ncl /home/mislam25/cmaq12_airnow_O3_mod.ncl

