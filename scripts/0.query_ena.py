# curl -X GET --header 'Accept: application/json' 'https://www.ebi.ac.uk/ena/portal/api/search?result=study&query=tax_eq(9823)&format=json'

import requests

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

# sr = requests.get('https://www.ebi.ac.uk/ena/portal/api/search?result=study&query=tax_eq(9823)&format=json')

tree = {}
size_tree = {}
for assembly_accession in pig_assemblies:
    tree[assembly_accession] = set()
    size_tree[assembly_accession] = 0

    ar = requests.get(f'https://www.ebi.ac.uk/ena/portal/api/search?result=assembly&query=assembly_accession={assembly_accession}&fields=wgs_set&format=json')
    for assembly in ar.json():
        wgs_set_name = assembly['wgs_set']

        wr = requests.get(f'https://www.ebi.ac.uk/ena/portal/api/search?result=wgs_set&query=wgs_set={wgs_set_name}&fields=study_accession&format=json')
        for wgs_set in wr.json():
            study_accession = wgs_set['study_accession']

            rr = requests.get(f'https://www.ebi.ac.uk/ena/portal/api/search?result=read_experiment&query=study_accession={study_accession}&fields=study_accession,study_title,run_accession,fastq_bytes,instrument_model,library_layout,library_strategy&format=json')
            
            for read_experiment in rr.json():
                study_title = read_experiment["study_title"]
                run_accession = read_experiment["run_accession"]
                fastq_bytes = sum([int(size)/1024/1024/1024/1024 for size in read_experiment["fastq_bytes"].split(";")])
                number_of_files = len([size for size in read_experiment["fastq_bytes"].split(";")])

                instrument_model = read_experiment["instrument_model"]
                library_layout = read_experiment["library_layout"]
                library_strategy = read_experiment["library_strategy"]

                # print(f"{assembly_accession}: {wgs_set_name}: {study_accession}: {study_title}: {run_accession}")
                print(f"{assembly_accession}\t {wgs_set_name}\t {study_accession}\t {study_title}\t {run_accession}\t {number_of_files}:{instrument_model}:{library_layout}:{library_strategy}")
                tree[assembly_accession].add(study_accession)
                size_tree[assembly_accession] += fastq_bytes

                # assembly_all_files_size = 0
                # for read_run in rr.json():
                #     file_bytes = read_run["fastq_bytes"]
                #     run_accession = read_run["run_accession"]

                #     # print(f"Read: {run_accession} file_sizes: {file_bytes}")

                #     run_all_files_size = 0
                #     for bytes in file_bytes.split(";"):
                #         try:
                #             run_all_files_size = run_all_files_size + int(bytes)
                #         except:
                #             pass 

                #     assembly_all_files_size = assembly_all_files_size + run_all_files_size

                # tree[study_accession] = assembly_all_files_size
            
        # print(f"{assembly_accession}: {assembly_all_files_size/1024/1024/1024/1024}")

# for accession in tree:
#     if len(tree[accession]) > 0:
#         print(f"{accession} {next(iter(tree[accession]))}")
#     else:
#         print(f"{accession} 0")

# for accession in size_tree:
#     print(f"{accession} {round(size_tree[accession], 2)}")

# for project in tree:
#     print(project, tree[project]/1024/1024/1024)