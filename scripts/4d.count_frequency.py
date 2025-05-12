import os
import sys
from cyvcf2 import VCF

import configparser
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True,  dest="input", type=str)
parser.add_argument("--output_dir", dest="output_dir", type=str)
parser.add_argument("--decimal", dest="decimal", type=int)
parser.add_argument("--debug", dest="debug", action="store_true")
args = parser.parse_args()

input_file = args.input
output_dir = args.output_dir or os.getcwd()
decimal = args.decimal or 4
debug = args.debug or False

input_vcf = VCF(input_file)
output_file_prefix = os.path.basename(input_file).replace(".vcf", "").replace(".gz", "")
output_file_novel = os.path.join(output_dir, output_file_prefix + "_freq_cnt_novel.tsv")
output_file_knownCalled = os.path.join(output_dir, output_file_prefix + "_freq_cnt_knownCalled.tsv")

i = -1
if debug:
    i = 100
frequency_count_novel = {}
frequency_count_knownCalled = {}
for variant in input_vcf:
    if variant.FILTER == "MONOALLELIC":
        continue

    _id = variant.INFO["CSQ"].split(",")[0].split("|")[17]       

    freqs = variant.INFO["AF"]
    if isinstance(freqs, float):
        freqs = (freqs,)
    for freq in freqs:
        format_freq = str(round(freq, decimal))

        if _id == "":
            if format_freq not in frequency_count_novel:
                frequency_count_novel[format_freq] = 0
            frequency_count_novel[format_freq] += 1
        else:
            if format_freq not in frequency_count_knownCalled:
                frequency_count_knownCalled[format_freq] = 0
            frequency_count_knownCalled[format_freq] += 1

    if i == 0:
        break
    i = i - 1
input_vcf.close()

with open(output_file_novel, "w") as file:
    for freq in frequency_count_novel:
        file.write(f"{freq}\t{frequency_count_novel[freq]}\n")

with open(output_file_knownCalled, "w") as file:
    for freq in frequency_count_knownCalled:
        file.write(f"{freq}\t{frequency_count_knownCalled[freq]}\n")
