from cyvcf2 import VCF
import sys

input_file = sys.argv[1] if len(sys.argv) >= 2 else "../"
output_file = sys.argv[2] if len(sys.argv) >= 3 else ""

input_vcf = VCF(input_file)

i = 0
with open(output_file, "w") as f:
    f.write(f"CHROM\tPOS\tN_ALLELES\tN_CHR\tALLELE:FREQ\n")

    for variant in input_vcf:
        ACs = {}
        AN = 260
        AFs = {}
        for gt in variant.genotypes:
            if gt[0] == -1:
                gt[0] = 0
            if gt[1] == -1:
                gt[1] = 0

            for idx in range(2):
                if gt[idx] not in ACs:
                    ACs[gt[idx]] = 0
                ACs[gt[idx]] += 1

    
        for idx in ACs:
            AFs[idx] = ACs[idx] / AN

        #print(ACs)
        #print(AN)
        #print(AFs)

        #print(variant.genotypes)
        f.write(f"{variant.CHROM}\t{variant.POS}\t{len(variant.ALT)}\t260")
        for idx in AFs:
            if idx == 0:
                f.write(f"\t{variant.REF}:{AFs[idx]}")
            else:
                f.write(f"\t{variant.ALT[idx-1]}:{AFs[idx]}")
        f.write("\n")

