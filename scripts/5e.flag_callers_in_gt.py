from cyvcf2 import VCF
import sys

original_file = "/hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241/outputs/GCA_000003025/analysis/GCA_000003025_af.vcf.gz"
gt_file = "/hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241/outputs/GCA_000003025/genotyping/parts/deepvariant.cohort.1.vcf.gz"

original_vcf = VCF(original_file)
gt_vcf = VCF(gt_file)
#region = "1:1-10000"
region = sys.argv[1]

cnt = 0
sites = {}
for variant in original_vcf(region):
    cnt += 1
    pos = variant.POS
    ref = variant.REF
    alts = variant.ALT
    
    if pos not in sites:
        sites[pos] = {}

    if ref not in sites[pos]:
        sites[pos][ref] = set()

    sites[pos][ref] = sites[pos][ref].union(alts)
#print(sites)
print(cnt)

cnt = 0
flagged = 0
gt_sites = {}
for variant in gt_vcf(region):
    cnt += 1
    pos = variant.POS
    ref = variant.REF
    alts = variant.ALT

    if pos not in gt_sites:
        gt_sites[pos] = {}

    if ref not in gt_sites[pos]:
        gt_sites[pos][ref] = set()

    gt_sites[pos][ref] = gt_sites[pos][ref].union(alts)

    if pos in sites and ref in sites[pos]:
        if sites[pos][ref].intersection(set(alts)):
            flagged += 1
#print(gt_sites)
print(cnt)
print(flagged)

original_vcf.close()
gt_vcf.close()
