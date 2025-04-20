from cyvcf2 import VCF
import copy

input_vcf = VCF("../../data/sus_scrofa_incl_consequences_VEP.vcf.gz")
chrom_lengths = {
    "1":	274330532,
    "10":	69359453,
    "11":	79169978,
    "12":	61602749,
    "13":	208334590,
    "14":	141755446,
    "15":	140412725,
    "16":	79944280,
    "17":	63494081,
    "18":	55982971,
    "2":	151935994,
    "3":	132848913,
    "4":	130910915,
    "5":	104526007,
    "6":	170843587,
    "7":	121844099,
    "8":	138966237,
    "9":	139512083,
    "X":	125939595,
    "Y":	43547828,
    "MT":    16613}

pos_covered = {}
for chrom in chrom_lengths:
    pos_covered[chrom] = set()
    for variant in input_vcf(chrom):
        # print(variant.CHROM, variant.POS, variant.REF, variant.ALT)
        for alt in variant.ALT:
            pos = variant.POS
            len_affected = len(variant.REF)
            if variant.REF[0] == variant.ALT[0]:
                pos += 1
                if len_affected != 1:   # for insertion
                    len_affected -= 1 
            
            pos_covered[chrom].update(range(pos, pos+len_affected))

input_vcf.close()

new_pos_covered = copy.deepcopy(pos_covered)
input_vcf = VCF("../../data/GCA_000003025_novel_VEP.vcf.gz")

for chrom in chrom_lengths:
    for variant in input_vcf(chrom):
        # print(variant.CHROM, variant.POS, variant.REF, variant.ALT)
        for alt in variant.ALT:
            pos = variant.POS
            len_affected = len(variant.REF)
            if variant.REF[0] == variant.ALT[0]:
                pos += 1
                if len_affected != 1:   # for insertion
                    len_affected -= 1 
            
            new_pos_covered[chrom].update(range(pos, pos+len_affected))
    # print(chrom, chrom_lengths[chrom], len(new_pos_covered[chrom]), len(new_pos_covered[chrom])/chrom_lengths[chrom])
input_vcf.close()

for chrom in chrom_lengths:
    print(chrom, chrom_lengths[chrom], len(pos_covered[chrom]), len(pos_covered[chrom])/chrom_lengths[chrom]*100, len(new_pos_covered[chrom]), len(new_pos_covered[chrom])/chrom_lengths[chrom]*100, (len(new_pos_covered[chrom]) - len(pos_covered[chrom]))/(len(pos_covered[chrom])*100))