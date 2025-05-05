#!/bin/bash

#SBATCH -J run_extract_novel
#SBATCH -o output/run_extract_novel.out
#SBATCH -e output/run_extract_novel.err
#SBATCH --mem=24GB
#SBATCH --time=5:00:00
#SBATCH --mail-user=snhossain@ebi.ac.uk
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

if [[ -z $1 ]]
then
	echo "ERROR: input and output file not give, exiting ..."
	exit 1
fi

if [[ -z $2 ]]
then
        echo "ERROR: output file not give, exiting ..."
        exit 1
fi

input_file=$1
output_file=$2

python 5d.extract_novel.py -i $input_file -o $output_file
