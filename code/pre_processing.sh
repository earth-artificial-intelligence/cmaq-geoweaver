#!/bin/bash

#SBATCH --partition=normal                 # will run on any cpus in the 'normal' partition
#SBATCH --job-name=python-cpu
#SBATCH --output=python-cpu.%j.out
#SBATCH --error=python-cpu.%j.err
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1                   # up to 48 per node
#SBATCH --mem-per-cpu=3500M                 # memory per CORE; maximum is 180GB per node
#SBATCH --export=ALL
#SBATCH --time=0-00:05:00                   # set to 1hr; please choose carefully

set echo
umask 0027


python cmaq/pre_processing.py
exit
