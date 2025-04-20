from cyvcf2 import VCF
from Bio import bgzf
import sys
import os
import re
import numpy as np

CALLER_THRESHOLD = 3
SINGLE_CALLER_INFO = {
    "bcftools":     ["BQBZ", "DP4", "IDV", "IMF", "INDEL", "MQ0F", "MQBZ", "MQSBZ", "RPBZ", "SCBZ", "SGB", "VDB"],
    "freebayes":    ["AB", "ABP", "AO", "CIGAR", "DPB", "DPRA", "EPP", "EPPR", 
                    "GTI", "LEN", "MEANALT", "MIN_DP", "MQM", "MQMR", "NS", "NUMALT", "ODDS", "PAIRED", "PAIREDR", 
                    "PAO", "PQA", "PQR", "PRO", "QA", "QR", "RO", "RPL", "RPP", "RPPR", "RPR", "RUN", "SAF", 
                    "SAP", "SAR", "SRF", "SRP", "SRR", "TYPE", "technology.ILLUMINA"],
    "strelka":      ["BLOCKAVG_min30p3a", "CIGAR", "IDREP", "REFREP", "RU", "SNVHPOL"],
    "haplotypecaller":  ["BaseQRankSum", "ExcessHet", "FS", "InbreedingCoeff", "MLEAC",
                        "MLEAF", "MQRankSum", "QD", "ReadPosRankSum", "SOR"],
}
MULTI_CALLER_INFO = {
    "AC": ["bcftools", "freebayes", "haplotypecaller"],
    "AN": ["bcftools", "freebayes", "haplotypecaller"],
    "AF": ["freebayes", "haplotypecaller"],
    "DP": ["bcftools", "freebayes", "haplotypecaller"],
    "MQ": ["bcftools", "strelka", "haplotypecaller"],
    "CIGAR": ["freebayes", "strelka"],
    "END": ["freebayes", "strelka"]
}

# process CLI args
input_vcf = sys.argv[1] 
output_vcf = os.path.join(os.getcwd(), "collapse_callers.vcf.gz")
if len(sys.argv) > 2:
    output_vcf = sys.argv[2]
qc_file = os.path.join(os.getcwd(), "qc_collapse_callers.txt")
if len(sys.argv) > 3:
    qc_file = sys.argv[3]

def process_header(header: str) -> str:

    get_caller = {}
    for caller in SINGLE_CALLER_INFO:
        for id in SINGLE_CALLER_INFO[caller]:
            if id in get_caller:
                get_caller[id].append(caller)
            else:
                get_caller[id] = [caller]
    for id in MULTI_CALLER_INFO:
        for caller in MULTI_CALLER_INFO[id]:
            if id in get_caller:
                get_caller[id].append(caller)
            else:
                get_caller[id] = [caller]

    new_header = []
    for line in header.split('\n'):
        # remove patient1_ prefix from any sample name
        if 'patient1_SAMN' in line:
            line = line.replace('patient1_', '')

        # FORMAT: we only keep GT
        if line.startswith('##FORMAT=') and not line.startswith('##FORMAT=<ID=GT,'):
            continue
        
        # FILTER: remove all; currently we put '.' in FILTER field
        elif line.startswith('##FILTER='):
            continue
        
        # INFO: add caller prefix to ID
        elif line.startswith('##INFO='):
            id = re.search('ID=(.*?),', line).group(1)

            lines = []
            if id in get_caller:
                for caller in get_caller[id]:
                    lines.append(re.sub('ID=(.*?),', f'ID={caller}_{id},', line))
            else:
                lines = [line]
            line = lines

        if type(line) is str:
            line = [line]
        new_header += line
    return "\n".join(new_header)

if not os.path.exists(input_vcf):
    print(f"Input file does not exist: {input_vcf}")
    exit(1)

vcf_reader  = VCF(input_vcf)
samples     = [sample.replace('patient1_', '') for sample in vcf_reader.samples]
header      = process_header(vcf_reader.raw_header)

current_variant = None
current_identifier = None
current_info = {}
current_genotype = {}
genotype_qc = []
genotype_mismatch = False
with bgzf.open(output_vcf, "wt") as o_file:
    with open(qc_file, "w") as q_file:
        q_file.write("\t".join(["#CHROM", "POS", "ID", "REF", "ALT", "N_CALLERS", "CALLERS", "GT_MISMATCH", "GT_NONMISS"]) + "\n")
        o_file.write(header)

        for variant in vcf_reader:
            identifier = f"{ variant.CHROM }:{ variant.POS }:{ variant.REF }:{ '/'.join(variant.ALT) }"
            caller = variant.INFO['VC']

            if current_variant is None:
                current_identifier = identifier
                current_genotypes = variant.genotypes 
                current_genotype_quals = variant.gt_quals
                             
            if identifier != current_identifier:
                
                caller_count = len(current_info['VC'].split("&"))
     
                q_file.write("\t".join([
                    current_variant.CHROM,
                    str(current_variant.POS),
                    ".",
                    current_variant.REF,
                    ",".join(current_variant.ALT),
                    str(caller_count),
                    current_info['VC'],
                    str(genotype_mismatch),
                    ",".join(genotype_qc)
                ]) + "\n")

                if caller_count >= CALLER_THRESHOLD:
                    o_file.write("\t".join([
                        current_variant.CHROM,
                        str(current_variant.POS),
                        ".",
                        current_variant.REF,
                        ",".join(current_variant.ALT),
                        ".",
                        ".",
                        ";".join([f"{ key }={ current_info[key] }" for key in current_info]),
                        f"GT",
                        "\t".join(f"{ str('.' if genotype[0] == -1 else genotype[0]) }/{ str('.' if genotype[1] == -1 else genotype[1]) }" for genotype in current_genotypes)
                    ]) + "\n")

                current_variant = variant
                current_identifier = identifier

                current_info = {}
                for (key, value) in variant.INFO:
                    if key == "VC":
                        current_info["VC"] = caller
                    else:
                        current_info[f"{ caller }_{ key }"] = ",".join([str(v) for v in value]) if type(value) is tuple else value
                        
                current_genotypes = variant.genotypes
                for idx, genotype in enumerate(variant.genotypes):
                    # in some callers, like strelka, there can be Siteconflict and we do not get full genotype
                    if len(genotype) == 2:
                        current_genotypes[idx] = [-1, -1, genotype[1]]
                    else:
                        current_genotypes[idx] = genotype
                current_genotype_quals = variant.gt_quals

                for idx, genotype in enumerate(current_genotypes):
                    if current_genotypes[idx][:2] != [-1, -1]:
                        genotype_qc = [ f"{ samples[idx] }:{ caller }:{ genotype[0] }/{ genotype[1] }" ]

                genotype_mismatch = False

            else:
                current_variant = variant
                current_identifier = identifier
                
                for (key, value) in variant.INFO:
                    if key == "VC":
                        current_info["VC"] = current_info["VC"]+"&"+caller if "VC" in current_info else caller
                    else:
                        current_info[f"{ caller }_{ key }"] = ",".join([str(v) for v in value]) if type(value) is tuple else value

                genotypes = variant.genotypes
                genotype_quals = variant.gt_quals

                # in some callers, like strelka, there can be Siteconflict and we do not get full genotype
                for idx, genotype in enumerate(variant.genotypes):
                    if len(genotype) == 2:
                        genotypes[idx] = [-1, -1, genotype[1]]
                for idx, genotype in enumerate(genotypes):
                    if genotype != current_genotypes[idx]:
                        # if current GT is missing we override with the new genotype
                        if current_genotypes[idx][:2] == [-1, -1]:
                            current_genotypes[idx] = genotype
                        # if current and new GT none are missing we keep the one with higher GQ
                        elif genotype[:2] != [-1, -1]:
                            if genotype_quals[idx] > current_genotype_quals[idx]:
                                current_genotypes[idx] = genotype
                            
                            # there is genotype mismatch between callers - not in qc
                            genotype_mismatch = True

                    # keep record of genotype if not missing
                    if genotype[:2] != [-1, -1]:
                        genotype_qc.append(f"{ samples[idx] }:{ caller }:{ genotype[0] }/{ genotype[1] }")
