import os, json
from cyvcf2 import VCF, Writer

project_dir = "/hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241"
config_dir = os.path.join(project_dir, "configs")

file = "/hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241/outputs/GCA_000003025/analysis/test.vcf"
input_vcf = VCF(file)
for variant in input_vcf:
    print(variant.genotypes[66][:2])
exit(0)

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

with open(os.path.join(config_dir, "sample_population.json")) as f:
    sample_population = json.load(f)

population_sample = {}
for pop in sample_population:
    for sample in sample_population[pop]:
        if sample in population_sample:
            print(f"[ERROR] {sample} belongs to multiple population. Exiting ...")
            exit(1)
        population_sample[sample] = pop

input_vcf = VCF(os.path.join(project_dir, "outputs/GCA_000003025/analysis/GCA_000003025_with_af.vcf.gz"))
# add header for the frequency INFO fields
for pop in sample_population:
    input_vcf.add_info_to_header({'ID': f'{pop}_AC', 'Description': f'Allele count in {pop} population', 'Type':'Integer', 'Number': '1'})
    input_vcf.add_info_to_header({'ID': f'{pop}_AN', 'Description': f'Total number of alleles in {pop} population', 'Type':'Integer', 'Number': '1'})
    input_vcf.add_info_to_header({'ID': f'{pop}_AF', 'Description': f'Allele frequency in {pop} population', 'Type':'Float', 'Number': '1'})

output_vcf = Writer(os.path.join(project_dir, "outputs/GCA_000003025/analysis/GCA_000003025_with_af_2.vcf.gz"), input_vcf, mode="wz")
samples = input_vcf.samples

i = 1
for variant in input_vcf('1'):
    genotypes = variant.genotypes
    sample_genotypes = dict(zip(samples, genotypes))

    # get frequency info for each population and add to variant
    population_genotypes = {}
    for pop in sample_population:
        population_genotypes[pop] = {}
        for sample in sample_population[pop]:
            if sample not in sample_genotypes:
                population_genotypes[pop][sample] = sample_genotypes['patient1_' + sample]
            else:
                population_genotypes[pop][sample] = sample_genotypes[sample]
        (AC, AN, AF) = calcuate_freq(population_genotypes[pop])

        variant.INFO[f'{pop}_AC'] = AC
        variant.INFO[f'{pop}_AN'] = AN
        variant.INFO[f'{pop}_AF'] = AF

    
    output_vcf.write_record(variant)

    if i == 10:
        break
    i += 1

input_vcf.close()
output_vcf.close()