#!/bin/bash

#SBATCH --time=1-00:00:00
#SBATCH --mem=1TB
#SBATCH --mail-user=snhossain@ebi.ac.uk
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

out_dir=$PWD/../outputs/GCA_000003025/genotyping/
region_dir=$PWD/../configs/regions
tmp_dir=$PWD/tmp
manifest_file=$PWD/../configs/GLnexus.manifest

seq=$1

mkdir -p $region_dir
mkdir -p ${out_dir}/parts
mkdir -p $tmp_dir
mkdir -p ${tmp_dir}/${seq}

cd ${tmp_dir}/${seq}

if [[ -d GLnexus.DB ]]
then
	rm -rf GLnexus.DB
fi

# run GLnexus
time glnexus_cli \
	--bed ${region_dir}/${seq}.bed \
	--config DeepVariantWGS \
	--list $manifest_file > $out_dir/parts/deepvariant.cohort.${seq}.bcf
bcftools view $out_dir/parts/deepvariant.cohort.${seq}.bcf | bgzip -c > $out_dir/parts/deepvariant.cohort.${seq}.vcf.gz

# run VEP
$ENSEMBL_ROOT_DIR/ensembl-vep/vep \
-i $out_dir/parts/deepvariant.cohort.${seq}.vcf.gz \
-o $out_dir/parts/deepvariant.cohort.${seq}_VEP.vcf.gz \
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
input_file=${base_dir}/deepvariant.cohort.${seq}_VEP.vcf.gz
output_file=${base_dir}/deepvariant.cohort.${seq}_VEP_novel.vcf.gz
cd ../..
sbatch -J run_extract_novel_${seq} -o outputs/run_extract_novel_${seq}.out -e outputs/run_extract_novel_${seq}.err 5c.run_extract_novel.sh ${input_file} ${output_file}

# get sites count
source 4c.analyse_genotype.sh $out_dir/parts/deepvariant.cohort.${seq}.vcf.gz ${output_file_base}_count.txt

# get frequency counts
python 4d.count_frequency.py -i $out_dir/parts/deepvariant.cohort.${seq}_VEP.vcf.gz --output_dir $out_dir/parts

sacct -j $SLURM_JOB_ID --format Timelimit,CPUTime,CPUTimeRAW,MaxRSS
