#!/bin/bash

#SBATCH -J run_vep
#SBATCH --mem=68GB
#SBATCH --time=1-00:00:00
#SBATCH --mail-user=snhossain@ebi.ac.uk
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

base_dir=/hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241/outputs/GCA_000003025/genotyping/parts
seqs=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 X Y MT)


for seq in ${seqs[@]}
do
	input_file=${base_dir}/deepvariant.cohort.1_VEP.vcf.gz
	output_file=${base_dir}/deepvariant.cohort.1_VEP_novel.vcf.gz
	python 5c.run_extract_novel.sh ${input_file} ${output_file}
done
