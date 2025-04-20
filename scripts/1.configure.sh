#!/bin/bash

#Submit this script with: sbatch thefilename
#For more details about each parameter, please check SLURM sbatch documentation https://slurm.schedmd.com/sbatch.html

#SBATCH --job-name=configure
#SBATCH --time=4-00:00:00   # walltime
#SBATCH --ntasks=1   # number of tasks
#SBATCH --cpus-per-task=2   # number of CPUs Per Task i.e if your code is multi-threaded
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem=2G   # memory per node
#SBATCH --mail-user=snhossain@ebi.ac.uk   # email address
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH -o configure.out
#SBATCH -e configure.err

assemb=$1

##### create symlink if needed #####
if [[ 0 == 1 ]]
then
	$input_dir=/hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241/inputs

	for file in ${input_dir}/*/samples/* 
	do 
		echo ok
		filename=$(basename $file)
		#ln -sf ${file} /hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241/inputs/GCA_000003025/samples/${filename}
	done
fi
####################################

if [[ "$assemb" != "" ]]
then
	python -u 1b.generate_config.py -a ${assemb} --check_integrity -v --no_workers 50
fi
