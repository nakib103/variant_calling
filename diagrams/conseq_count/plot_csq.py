import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sys, os
import math

coding_consequence = {
    "synonymous_variant",
    "missense_variant",
    "stop_gained",
    "inframe_insertion",
    "frameshift_variant",
    "start_lost",
    "stop_lost",
    "stop_retained_variant",
    "inframe_deletion",
    "start_retained_variant",
    "coding_sequence_variant",
    "protein_altering_variant",
    "NMD_transcript_variant"
}

# novel_variants_per_conseq = {'upstream_gene_variant': 2057596, 'non_coding_transcript_exon_variant': 308020, 'splice_donor_variant': 98377, 'non_coding_transcript_variant': 595600, 'intron_variant': 16605601, 'splice_region_variant': 138152, 'splice_polypyrimidine_tract_variant': 129185, 'splice_donor_region_variant': 29265, 'downstream_gene_variant': 2208919, '3_prime_UTR_variant': 371315, 'synonymous_variant': 964111, 'inframe_insertion': 2844, 'inframe_deletion': 3306, '5_prime_UTR_variant': 87334, 'splice_acceptor_variant': 57941, 'intergenic_variant': 7271853, 'stop_gained': 1879, 'missense_variant': 263849, 'splice_donor_5th_base_variant': 3794, 'mature_miRNA_variant': 35, 'frameshift_variant': 13420, 'stop_retained_variant': 409, 'stop_lost': 283, 'start_lost': 401, 'coding_sequence_variant': 978, 'protein_altering_variant': 59, 'NMD_transcript_variant': 37096, 'start_retained_variant': 92}
# existing_variants_per_conseq = {'upstream_gene_variant': 8155334, 'non_coding_transcript_exon_variant': 1444694, 'intron_variant': 78715057, 'non_coding_transcript_variant': 2605759, 'splice_region_variant': 121817, 'downstream_gene_variant': 8356164, '3_prime_UTR_variant': 1217927, 'synonymous_variant': 768562, '5_prime_UTR_variant': 256036, 'missense_variant': 525423, 'intergenic_variant': 32378952, 'splice_polypyrimidine_tract_variant': 152519, 'stop_gained': 15542, 'splice_acceptor_variant': 5069, 'splice_donor_5th_base_variant': 6537, 'splice_donor_variant': 5846, 'splice_donor_region_variant': 22246, 'inframe_insertion': 1445, 'frameshift_variant': 12300, 'mature_miRNA_variant': 89, 'start_lost': 1244, 'stop_lost': 779, 'stop_retained_variant': 714, 'inframe_deletion': 1632, 'start_retained_variant': 51, 'coding_sequence_variant': 717, 'protein_altering_variant': 390, 'NMD_transcript_variant': 141396}
input_file = sys.argv[1] if len(sys.argv) >= 2 else (os.getcwd() + "/data/existing_variant_count_by_conseq_canonical")
only_coding = int(sys.argv[2]) if len(sys.argv) >= 3 else 0

variant_count = {}
with open(input_file, "r") as file:
	for line in file:
		(conseq, count) = line.split("\t")
		variant_count[conseq] = int(count.strip())
variant_count_sorted = {k: v for k, v in sorted(variant_count.items(), key=lambda item: item[1])}

labels = []
data = []
total = 0
for x, y in variant_count_sorted.items():
	if only_coding and (x not in coding_consequence):
		continue
	
	labels.append(x)
	data.append(y)
	total += y

def calc_pct(pct, data):
    if pct < 1:
        return None
    else:
        return f"{pct:.1f}"

sns.set_style("whitegrid") 
plt.figure(figsize=(10,6)) 
# patches, texts, _ = plt.pie(data, startangle=90, autopct=lambda pct: calc_pct(pct, data))
# plt.legend(patches, labels, bbox_to_anchor=(1, 1), fontsize=8)
# plt.tight_layout()
# plt.show()
# plt.savefig('diagrams/novel_conseq_canonical.png', bbox_inches='tight')

log_data = [math.log10(d) for d in data]
sns.barplot(x=log_data, y=labels, palette='viridis')
plt.tight_layout()
plt.xlabel("Counts")
locs, labels = plt.xticks()
plt.xticks(locs, [f"1e{int(l)}"  for l in locs])
# plt.show()
plt.savefig('diagrams/barplot_existing_conseq_canonical.png', bbox_inches='tight')