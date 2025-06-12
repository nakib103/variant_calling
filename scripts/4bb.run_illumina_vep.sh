#!/bin/bash

#SBATCH --time=1-00:00:00
#SBATCH --mem=300GB
#SBATCH --mail-user=snhossain@ebi.ac.uk
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

out_dir=$PWD/../outputs/GCA_000003025/genotyping/illumina
tmp_dir=$PWD/tmp
manifest_file=$PWD/../configs/illumina.manifest

seq=$1

mkdir -p $tmp_dir
cd ${tmp_dir}

# run GLnexus
output_file_base=${out_dir}/illumina.cohort.${seq}
time gvcfgenotyper \
	-f /hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241/inputs/GCA_000003025/Sus_scrofa.Sscrofa11.1.dna.toplevel.fa \
	-l $manifest_file \
	-r $seq \
	-Ob -o ${output_file_base}.bcf

bcftools view ${output_file_base}.bcf | bgzip -c > ${output_file_base}.vcf.gz

# run VEP
$ENSEMBL_ROOT_DIR/ensembl-vep/vep \
-i ${output_file_base}.vcf.gz \
-o ${output_file_base}_VEP.vcf.gz \
--force \
--cache /nfs/production/flicek/ensembl/variation/data/VEP/tabixconverted \
--cache_version 113 \
--offline \
--species sus_scrofa \
--check_existing \
--vcf \
--variant_class \
--canonical \
--compress_output bgzip

# extract novel variant
input_file=${output_file_base}_VEP.vcf.gz
output_file=${output_file_base}_VEP_novel.vcf.gz
cd ..
sbatch -J run_extract_novel_${seq} -o outputs/run_extract_novel_${seq}.out -e outputs/run_extract_novel_${seq}.err 5c.run_extract_novel.sh ${input_file} ${output_file}

# get sites count
source 4c.analyse_genotype.sh ${output_file_base}.vcf.gz ${output_file_base}_count.txt

# get frequency counts
python 4d.count_frequency.py -i ${output_file_base}_VEP.vcf.gz --output_dir $out_dir

sacct -j $SLURM_JOB_ID --format Timelimit,CPUTime,CPUTimeRAW,MaxRSS
