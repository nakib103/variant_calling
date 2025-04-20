from cyvcf2 import VCF, Writer
import os

base_dir = "/hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241/outputs/GCA_000003025/analysis"
input_vcf = VCF(os.path.join(base_dir, "GCA_000003025_VEP.vcf.gz"))
output_vcf = Writer(os.path.join(base_dir, "GCA_000003025_novel_VEP.vcf"), input_vcf)

i = 0
for variant in input_vcf:
    _id = variant.INFO["CSQ"].split(",")[0].split("|")[17]
    if _id == "":
        output_vcf.write_record(variant)

input_vcf.close()
output_vcf.close()
