#!/bin/bash

#Submit this script with: sbatch thefilename
#For more details about each parameter, please check SLURM sbatch documentation https://slurm.schedmd.com/sbatch.html

#SBATCH --job-name=site_conflict
#SBATCH --time=5-00:00:00   # walltime
#SBATCH --ntasks=1   # number of tasks
#SBATCH --cpus-per-task=16   # number of CPUs Per Task i.e if your code is multi-threaded
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem=4G   # memory per node
#SBATCH --mail-user=snhossain@ebi.ac.uk   # email address
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

assemb=GCA_000003025

dir=/hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241
o_dir=${dir}/outputs/${assemb}/postprocessing
q_dir=${dir}/outputs/${assemb}/qc

r_file=${o_dir}/${assemb}_duplicated.vcf.gz
rd_file=${o_dir}/${assemb}.vcf.gz
qr_file=${q_dir}/collapse_callers.txt

if [[ $1 == test ]]
then
	r_file=$PWD/site_conflict.vcf
	rd_file=$PWD/out_site_conflict.vcf.gz
	qr_file=$PWD/qc_site_conflict.txt
fi

python $PWD/../4b.collapse_callers.py $r_file $rd_file $qr_file
tabix -p vcf -f $rd_file
