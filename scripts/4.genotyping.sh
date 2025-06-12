#!/bin/bash

#SBATCH -J genotyping
#SBATCH -o genotyping.out
#SBATCH -e genotyping.err
#SBATCH --time=3-00:00:00
#SBATCH --mem=2GB
#SBATCH --mail-user=snhossain@ebi.ac.uk
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

log_dir=$PWD/outputs
region_dir=$PWD/../configs/regions

mkdir -p $region_dir

no_contig=1
if [[ ! -z $1 ]]
then
	no_contig=$1
fi

seq_match=1
if [[ ! -z $2 ]]
then
        seq_match=$1
fi

#seqs=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "16" "17" "18" "X" "Y" "MT")
#seqs=("1", "2", "3", "4", "5", "6", "7")
seqs=("8")

for seq in $(tabix /hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241/outputs/GCA_000003025/analysis/GCA_000003025.vcf.gz -l)
do
	length=$(m1 --silent sus_scrofa_core_113_111 -e "select sr.length from seq_region as sr, coord_system as cs where sr.coord_system_id = cs.coord_system_id and sr.name = \"$seq\";")
	if [[ -z $length ]]
	then
		length=$(m1 --silent sus_scrofa_core_113_111 -e "select sr.length from seq_region as sr, seq_region_synonym as srs, coord_system as cs where sr.seq_region_id = srs.seq_region_id and sr.coord_system_id = cs.coord_system_id and srs.synonym = \"$seq\";")
	fi

	if [[ $no_contig && ($seq == "AEMK"* || $seq == "FPYK"*) ]]
	then
		continue
	fi
	
	if [[ $seq_match && $(echo ${seqs[@]} | fgrep -w $seq) ]]
	then
		echo -e "$seq\t1\t$length" > ${region_dir}/${seq}.bed
		
		# GLnexus
		#sbatch -J genotyping_${seq} -o ${log_dir}/genotyping_${seq}.out -e ${log_dir}/genotyping_${seq}.err 4b.run_glnexus_vep.sh $seq
		
		# Illumina genotyper
		sbatch -J genotyping_${seq} -o ${log_dir}/illumina_genotyping_${seq}.out -e ${log_dir}/illumina_genotyping_${seq}.err 4bb.run_illumina_vep.sh $seq
	fi
done

sacct -j $SLURM_JOB_ID --format Timelimit,CPUTime,CPUTimeRAW,MaxRSS
