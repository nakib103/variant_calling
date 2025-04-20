#!/bin/bash

#Submit this script with: sbatch thefilename
#For more details about each parameter, please check SLURM sbatch documentation https://slurm.schedmd.com/sbatch.html

#SBATCH --time=5-00:00:00   # walltime
#SBATCH --ntasks=1   # number of tasks
#SBATCH --cpus-per-task=16   # number of CPUs Per Task i.e if your code is multi-threaded
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem=4G   # memory per node
#SBATCH --mail-user=snhossain@ebi.ac.uk   # email address
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

assemb=$1

dir=/hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241
i_dir=${dir}/outputs/${assemb}/variant_calling
o_dir=${dir}/outputs/${assemb}/postprocessing
q_dir=${dir}/outputs/${assemb}/qc

mkdir -p ${o_dir}
mkdir -p ${q_dir}
vc_files=""
for c_dir in $(find ${i_dir}/ -mindepth 1 -maxdepth 1 -type d)
do
	caller=$(basename ${c_dir})
	qcnt_file=${q_dir}/${caller}_count.txt
	#echo -e "SAMPLE\tALL\tpost_filter" > $qcnt_file

	#### filter for samples
	echo "Caller: $caller"
	echo "Filtering sample files based on quality"
	s_files=""
	for s_dir in $(find ${c_dir}/ -mindepth 1 -maxdepth 1 -type d)
	do
		sample=$(basename ${s_dir})
		i_file=${s_dir}/${sample}.${caller}.vcf.gz
		echo -e "\tSample: $sample"
	
		mkdir -p ${o_dir}/${caller}
		mkdir -p ${o_dir}/${caller}/${sample}
		of_file=${o_dir}/${caller}/${sample}/${sample}.${caller}.filtered.vcf.gz

		s_files="$s_files $of_file"

		if [[ $caller == strelka ]]
		then
			i_file=${s_dir}/${sample}.${caller}.variants.vcf.gz
		fi
		
		if [[ $caller == strelka || $caller == deepvariant ]]
		then
			# filter based on FILTER
			#bcftools filter --no-version -i 'FILTER="PASS"' $i_file -O z -o $of_file
			sleep 0.1
		fi
		# filter based on QUAL scores
		#bcftools filter --no-version -i 'QUAL>30' $i_file -O z -o $of_file
		#bcftools index $of_file
		
		#### qc
	 	#pre_cnt=$(zgrep -v "^#"	$i_file | wc -l)
		#pos_cnt=$(zgrep -v "^#" $of_file | wc -l)

		#echo -e "${sample}\t${pre_cnt}\t${pos_cnt}" >> $qcnt_file
	done

	#### merge for samples
	ofm_file=${o_dir}/${caller}/${caller}.filtered_merged.vcf.gz
	ofms_file=${o_dir}/${caller}/${caller}.filtered_merged_sorted.vcf.gz
	vc_files="$vc_files $ofms_file"
	
	echo "Merging all sample files into single one"
	if [[ $(echo $s_files | tr ' ' '\n' | wc -l) == 1 ]]
	then
		#mv $s_files $ofm_file
		sleep 0.1
	else
		echo "bcftools merge -m both $s_files -O z -o $ofm_file"
		#bcftools merge --no-version -m both $s_files -O z -o $ofm_file
		sleep 0.1
	fi

	# add caller info and sort
	echo "Adding caller info and sorting the merged file"
	#zgrep "^##" $ofm_file > ${ofms_file}_tmp
	echo '##INFO=<ID=VC,Number=1,Type=String,Description="Variant caller">' >> ${ofms_file}_tmp
	#zgrep "^#CHR" $ofm_file >> ${ofms_file}_tmp
	#zgrep -v "^#" $ofm_file | awk -v vc="$caller" 'BEGIN { OFS="\t" } {if ($8 == ".") {$8="VC="vc} else {$8="VC="vc";"$8}; print}' | sort -k1,1 -k2,2n  >> ${ofms_file}_tmp
	#bgzip ${ofms_file}_tmp
	#mv ${ofms_file}_tmp.gz $ofms_file
	
	# index
	echo "Create tabix index for the merged and sort file"
	#tabix -p vcf -f $ofms_file

	# for bcftools we need to update sample names
	if [[ $caller == bcftools ]]
	then
		echo "Update sample names for bcftools file"
		#tabix $ofms_file -H | sed -e 's/SAMN/patient1_SAMN/g' > ${ofms_file}_tmp
		#zgrep -v "^#" $ofms_file >> ${ofms_file}_tmp
		#bgzip ${ofms_file}_tmp

		#mv ${ofms_file}_tmp.gz ${ofms_file}
		#tabix -p vcf -f $ofms_file
		sleep 0.1
	fi
	
	# delete filtered_merged file
	echo "Delete merged file (keep the soreted one)"
	#rm $ofm_file
done

#### merge for callers
r_file=${o_dir}/${assemb}_duplicated.vcf.gz
rd_file=${o_dir}/${assemb}.vcf.gz
qr_file=${q_dir}/collapse_callers.txt

echo "Merging all caller files into single one"
bcftools concat --no-version -a $vc_files | bgzip > $r_file
#python 4b.collapse_callers.py $r_file $rd_file $qr_file
#tabix -p vcf -f $rd_file
