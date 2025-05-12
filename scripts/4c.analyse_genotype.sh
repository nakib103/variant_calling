#!/bin/bash

#SBATCH -J run_genotype_analysis
#SBATCH --mem=2GB
#SBATCH --time=2:00:00
#SBATCH --mail-user=snhossain@ebi.ac.uk
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

if [[ -z $1 ]]
then
	echo "ERROR: no input file given, exiting"
	exit 1
fi
input_vcf=$1

if [[ -z $2 ]]
then
        echo "ERROR: no output file given, exiting"
        exit 1
fi
output_file=$2

# site count
site_count=$(zgrep -v "^#" $input_vcf | wc -l)
monoallelic_sites=$(zgrep -v "^#" $input_vcf | awk '$7 == "MONOALLELIC"' | wc -l)

echo "file: $input_vcf" > $output_file
echo "site count: $site_count; monoallelic_sites: $monoallelic_sites" >> $output_file
echo "" >> $output_file


/homes/snhossain/opt/rtg/rtg vcfstats $input_vcf  >> $output_file
