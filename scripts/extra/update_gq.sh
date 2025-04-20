#!/bin/bash

file=/hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241/outputs/GCA_000003025/postprocessing/GCA_000003025_duplicated.vcf.gz
bgzip -cd $file | sed -e 's/ID=GQ,Number=1,Type=Integer/ID=GQ,Number=1,Type=Float/' | bgzip -c > ${file}_bkp
mv ${file}_bkp $file
