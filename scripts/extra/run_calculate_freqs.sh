#!/bin/bash

#Submit this script with: sbatch thefilename
#For more details about each parameter, please check SLURM sbatch documentation https://slurm.schedmd.com/sbatch.html

#SBATCH --job-name=calc_freq
#SBATCH --time=5-00:00:00   # walltime
#SBATCH --ntasks=1   # number of tasks
#SBATCH --cpus-per-task=16   # number of CPUs Per Task i.e if your code is multi-threaded
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem=4G   # memory per node
#SBATCH --mail-user=snhossain@ebi.ac.uk   # email address
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

python $PWD/../4c.calculate_freqs.py
