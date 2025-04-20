import sys, os, json
from cyvcf2 import VCF, Writer

project_dir = "/hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241"
config_dir = os.path.join(project_dir, "configs")
assembly = "GCA_000003025"

def calcuate_freq(sample_genotype: dict) -> tuple:
    (AC, AN, AF) = (0, 0, 0.0)
    for sample in sample_genotype:
        genotype = sample_genotype[sample]

        if (genotype[0] == -1 and genotype[1] != -1) or (genotype[0] != -1 and genotype[1] == -1):
            print(f"[ERROR] Unable to parse genotype - { genotype[0] }/{ genotype[1] }, Exiting ...")
            exit(1)

        if genotype[0] != -1 or genotype[0] != -1:
            AN += 2
        
        if genotype[0] != -1:
            AC += genotype[0]

        if genotype[1] != -1:
            AC += genotype[1]

    AF = AC / AN if AN != 0 else 0
    return (AC, AN, AF)

# process CLI args
input_file = os.path.join(project_dir, f"outputs/{ assembly }/analysis/GCA_000003025_interim_af.vcf.gz")
if len(sys.argv) > 1:
    input_file = sys.argv[1]
output_file = os.path.join(project_dir, f"outputs/{ assembly }/analysis/GCA_000003025_interim_af_2.vcf.gz")
if len(sys.argv) > 2:
    output_file = sys.argv[2]

# create input vcf object
input_vcf = VCF(input_file)

# get sample and sample populations
samples = input_vcf.samples
with open(os.path.join(config_dir, "sample_population.json")) as f:
    sample_population = json.load(f)

# add population frequency headers
input_vcf.add_info_to_header({'ID': f'AC', 'Description': f'Total Allele count', 'Type':'Integer', 'Number': '1'})
input_vcf.add_info_to_header({'ID': f'AN', 'Description': f'Total number of alleles', 'Type':'Integer', 'Number': '1'})
input_vcf.add_info_to_header({'ID': f'AF', 'Description': f'Allele frequency', 'Type':'Float', 'Number': '1'})
for pop in sample_population:
    input_vcf.add_info_to_header({'ID': f'AC_{pop}', 'Description': f'Allele count in {pop} population', 'Type':'Integer', 'Number': '1'})
    input_vcf.add_info_to_header({'ID': f'AN_{pop}', 'Description': f'Total number of alleles in {pop} population', 'Type':'Integer', 'Number': '1'})
    input_vcf.add_info_to_header({'ID': f'AF_{pop}', 'Description': f'Allele frequency in {pop} population', 'Type':'Float', 'Number': '1'})

output_vcf = Writer(output_file, input_vcf, mode="wz")

for variant in input_vcf():
    genotypes = variant.genotypes
    sample_genotypes = dict(zip(samples, genotypes))

    # get frequency info for each population and add to variant
    population_genotypes = {}
    total_genotypes = {}
    for pop in sample_population:
        population_genotypes[pop] = {}
        for sample in sample_population[pop]:
            if sample not in sample_genotypes:
                population_genotypes[pop][sample] = sample_genotypes['patient1_' + sample]
                total_genotypes[sample] = sample_genotypes['patient1_' + sample]
            else:
                population_genotypes[pop][sample] = sample_genotypes[sample]
                total_genotypes[sample] = sample_genotypes[sample]
        (AC, AN, AF) = calcuate_freq(population_genotypes[pop])

        variant.INFO[f'AC_{pop}'] = AC
        variant.INFO[f'AN_{pop}'] = AN
        variant.INFO[f'AF_{pop}'] = AF
    
    (AC, AN, AF) = calcuate_freq(total_genotypes)
    variant.INFO['AC'] = AC
    variant.INFO['AN'] = AN
    variant.INFO['AF'] = AF

    
    output_vcf.write_record(variant)

input_vcf.close()
output_vcf.close()
