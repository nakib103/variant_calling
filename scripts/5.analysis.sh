#!/bin/bash

#SBATCH -J analysis
#SBATCH -o analysis.out
#SBATCH -e analysis.err
#SBATCH --time=3-00:00:00   # walltime
#SBATCH --ntasks=1   # number of tasks
#SBATCH --cpus-per-task=1   # number of CPUs Per Task i.e if your code is multi-threaded
#SBATCH --nodes=1   # number of nodes
#SBATCH -p standard   # partition(s)
#SBATCH --mem=256G   # memory per node
#SBATCH --mail-user=snhossain@ebi.ac.uk   # email address
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

dir=/hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241
assembly=$1
ensembl_release=113

source ~/.bash_nw
module add nextflow/24.04.3
module add singularity-3.8.7-gcc-11.2.0-jtpp6xx

vcf=${dir}/outputs/${assembly}/analysis/${assembly}.vcf.gz
#vcf=$PWD/../data/sus_scrofa_incl_consequences.vcf.gz
outdir=${dir}/outputs/${assembly}/analysis
#outdir=$PWD/../data
# check existing variants and variant consequence
nextflow run $ENSEMBL_ROOT_DIR/ensembl-vep/nextflow/main.nf \
	-profile slurm,singularity \
	--vcf ${vcf} \
	--outdir ${outdir} \
	--bin_size 250000 \
	--vep_config ${dir}/scripts/sus_scrofa.ini
