#!/bin/bash

#Submit this script with: sbatch thefilename
#For more details about each parameter, please check SLURM sbatch documentation https://slurm.schedmd.com/sbatch.html

#SBATCH --job-name=sarek
#SBATCH --time=14-00:00:00   # walltime
#SBATCH --ntasks=1   # number of tasks
#SBATCH --cpus-per-task=16   # number of CPUs Per Task i.e if your code is multi-threaded
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem=76G   # memory per node
#SBATCH --mail-user=snhossain@ebi.ac.uk   # email address
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH -o sarek.out
#SBATCH -e sarek.err

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
module add nextflow/23.04.1

assembly=GCA_002844635
if [[ $1 != "" ]]
then
	assembly=$1
fi
fasta_filename=GCA_002844635.2.fasta
if [[ $2 != "" ]]
then
        fasta_filename=$2
fi

nextflow run ../sarek \
	-profile singularity,slurm \
	--input ../configs/${assembly}.csv \
	--fasta ../inputs/${assembly}/${fasta_filename} \
	--outdir ../outputs/${assembly} \
	--igenomes_ignore \
	--skip_tools baserecalibrator \
	--tools strelka,deepvariant,freebayes,haplotypecaller,mpileup \
	-resume db0055e2-5cd2-407a-bab2-511bf6280236 \
	-with-timeline -with-trace -with-report

#--skip_tools baserecalibrator \
#--aligner dragmap
#--fasta ../inputs/${assembly}/${assembly}.?.fasta \
