#!/bin/bash

#SBATCH -J run_vep
#SBATCH --mem=68GB
#SBATCH --time=1-00:00:00
#SBATCH --mail-user=snhossain@ebi.ac.uk
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

base_dir=/hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241/outputs/GCA_000003025/genotyping/parts
#seqs=(2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 X)
seqs=(Y MT)

for seq in ${seqs[@]}
do
	input_file=${base_dir}/deepvariant.cohort.${seq}_VEP.vcf.gz
	output_file=${base_dir}/deepvariant.cohort.${seq}_VEP_novel.vcf.gz
	sbatch -J run_extract_novel_${seq} -o output/run_extract_novel_${seq}.out -e output/run_extract_novel_${seq}.err 5c.run_extract_novel.sh ${input_file} ${output_file}

	output_file=${base_dir}/deepvariant.cohort.${seq}_count.txt
	sbatch 4c.analyse_genotype.sh $input_file $output_file
	sbatch 4extra.run_frequency_get.sh $input_file $base_dir
done
