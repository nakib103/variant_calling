#!/bin/bash


#SBATCH -J run_vep
#SBATCH --mem=68GB
#SBATCH --time=1-00:00:00
#SBATCH --mail-user=snhossain@ebi.ac.uk
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

python 4d.count_frequency.py -i $1 --output_dir $2
