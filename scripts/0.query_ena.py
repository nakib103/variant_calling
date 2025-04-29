''' 
1. ENA Metadata
https://ena-docs.readthedocs.io/en/latest/submit/general-guide/metadata.html

2. ENA API
Ref: https://docs.google.com/document/d/1CwoY84MuZ3SdKYocqssumghBF88PWxUZ/edit?tab=t.0

Example query -
Get searchable field: curl -X GET --header 'Accept: application/json' 'https://www.ebi.ac.uk/ena/portal/api/searchFields?result=wgs_set'
Get result: curl -X GET --header 'Accept: application/json' 'https://www.ebi.ac.uk/ena/portal/api/search?result=study&query=tax_eq(9823)&format=json'

Supported types are -
analysis
analysis_study
assembly
coding
noncoding
read_experiment
read_run
read_study
sample
sequence
study
taxon
tls_set
tsa_set
wgs_set
'''

import requests
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('-O', '--output', type=str, dest='output')
parser.add_argument('--format_by_pop', action='store_true', dest='format_by_pop')
parser.add_argument('--sample_population_file', type=str, dest='sample_population_file')
parser.add_argument('--compact_by_run', action='store_true', dest='compact_by_run')

args = parser.parse_args()

output_file = args.output or "query_ena_results.tsv"
format_by_pop = args.format_by_pop or False
sample_population_file = args.sample_population_file or "sample_population.json"
compact_by_run = args.compact_by_run or False

pig_assemblies = [
    "GCA_000472085",
    "GCA_001700135",
    "GCA_001700155",
    "GCA_001700165",
    "GCA_001700215",
    "GCA_001700235",
    "GCA_001700255",
    "GCA_001700295",
    "GCA_001700575",
    "GCA_002844635",
    "GCA_024718415",
    "GCA_021656055",
    "GCA_020567905",
    "GCA_019290145",
    "GCA_018555405",
    "GCA_001700195",
    "GCA_017957985",
    "GCA_015776825",
    "GCA_007644095"
]

metadata = [
    "assembly_accession",
    "wgs_set_name",
    "study_accession",
    "study_title",
    "sample_accession",
    "run_accession",
    "fastq_bytes",
    "number_of_files",
    "instrument_model",
    "library_layout",
    "library_strategy"
]

if format_by_pop:
    metadata = ["population"] + metadata
    with open(sample_population_file, "r") as file:
        sample_population = json.load(file)

tree = {}
with open(output_file, "w") as file:
    # print headers
    file.write("\t".join(metadata) + "\n")


    read_experiments = set()
    for assembly_accession in pig_assemblies:
        tree[assembly_accession] = []

        ar = requests.get(f'https://www.ebi.ac.uk/ena/portal/api/search?result=assembly&query=assembly_accession={assembly_accession}&fields=wgs_set&format=json')
        for assembly in ar.json():
            wgs_set_name = assembly['wgs_set']

            wr = requests.get(f'https://www.ebi.ac.uk/ena/portal/api/search?result=wgs_set&query=wgs_set={wgs_set_name}&fields=study_accession&format=json')
            for wgs_set in wr.json():
                study_accession = wgs_set['study_accession']

                rr = requests.get(f'https://www.ebi.ac.uk/ena/portal/api/search?result=read_experiment&query=study_accession={study_accession}&fields=study_accession,study_title,sample_accession,run_accession,fastq_bytes,instrument_model,library_layout,library_strategy&format=json')            
                for read_experiment in rr.json():
                    run_accession = read_experiment["run_accession"]

                    experiment_metadata = {
                        "assembly_accession": assembly_accession,
                        "wgs_set_name": wgs_set_name,
                        "study_accession": study_accession,
                        "study_title" : read_experiment["study_title"],
                        "sample_accession" : read_experiment["sample_accession"],
                        "run_accession" : read_experiment["run_accession"],
                        "fastq_bytes" : sum([int(size)/1024/1024/1024/1024 for size in read_experiment["fastq_bytes"].split(";")]),
                        "number_of_files" : len([size for size in read_experiment["fastq_bytes"].split(";")]),
                        "instrument_model" : read_experiment["instrument_model"],
                        "library_layout" : read_experiment["library_layout"],
                        "library_strategy" :  read_experiment["library_strategy"]
                    }
                    
                    tree[assembly_accession].append(experiment_metadata)

                    if (not format_by_pop and (compact_by_run and run_accession not in read_experiments)):
                        file.write("\t".join([str(experiment_metadata[item]) for item in experiment_metadata]) + "\n")

                    read_experiments.add(run_accession)

    if format_by_pop:
        # re-structure tree using sample_accession as key
        tree_by_sample = {}
        for assembly_accession in tree:
            for item in tree[assembly_accession]:
                sample_accession = item["sample_accession"]
                if sample_accession not in tree_by_sample:
                    tree_by_sample[item["sample_accession"]] = []
                tree_by_sample[item["sample_accession"]].append(item)

        # iterate by sample and write out relevant experiment runs
        read_experiments = set()
        for pop in sample_population:
            for sample_accession in sample_population[pop]:
                if sample_accession in tree_by_sample:
                    sample_metadata = tree_by_sample[sample_accession]
                    for items in sample_metadata:
                        run_accession = items["run_accession"]
                        if compact_by_run and run_accession not in read_experiments:
                            file.write(pop + "\t" + "\t".join([str(items[item]) for item in items]) + "\n")
                        read_experiments.add(run_accession)

file.close()