#!/bin/bash

#SBATCH -J test
#SBATCH -o test.out
#SBATCH -e test.err
#SBATCH --mem=68GB
#SBATCH --time=1-00:00:00
#SBATCH --mail-user=snhossain@ebi.ac.uk
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

base_dir=/hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241/outputs/GCA_000003025/genotyping/parts
seqs=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 X Y MT)


for seq in ${seqs[@]}
do
	echo "chorm $seq"
	python 5e.flag_callers_in_gt.py $seqs	
done
