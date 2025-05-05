#!/bin/bash

#SBATCH --time=1-00:00:00
#SBATCH --mem=1TB
#SBATCH --mail-user=snhossain@ebi.ac.uk
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

out_dir=$PWD/../outputs/GCA_000003025/genotyping/
region_dir=$PWD/../configs/regions
tmp_dir=$PWD/tmp
manifest_file=$PWD/GLnexus.manifest

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

time glnexus_cli \
	--bed ${region_dir}/${seq}.bed \
	--config DeepVariantWGS \
	--list $manifest_file > $out_dir/parts/deepvariant.cohort.${seq}.bcf
bcftools view $out_dir/parts/deepvariant.cohort.${seq}.bcf | bgzip -c > $out_dir/parts/deepvariant.cohort.${seq}.vcf.gz

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

sacct -j $SLURM_JOB_ID --format Timelimit,CPUTime,CPUTimeRAW,MaxRSS
