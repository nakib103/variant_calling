import sys, os
from cyvcf2 import VCF

input_file = sys.argv[1] if len(sys.argv) >= 2 else "../GCA_000003025_novel_VEP.vcf"
input_vcf = VCF(input_file)
ouptut_file = sys.argv[2] if len(sys.argv) >= 3 else "gene_count.tsv"

gene_count ={}
for variant in input_vcf:
    csq_str = variant.INFO["CSQ"]
    for csq in csq_str.split(","):
        gene = csq.split("|")[4]
       
        if gene not in gene_count:
            gene_count[gene] = 0

        gene_count[gene] += 1

print(gene_count)
with open(ouptut_file, "w") as file:
    for gene, count in sorted(gene_count.items(), key=lambda item: item[1]):
        file.write(f"{gene}\t{count}\n")
