import sys
import os
import argparse
import requests
import subprocess
import concurrent.futures

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--assembly', type=str, required=True, dest='assembly')
parser.add_argument('-D', '--root_dir', type=str, dest='root_dir')
parser.add_argument('-M', '--check_assembly', action='store_true', dest='check_assembly')
parser.add_argument('-t', '--check_integrity', action='store_true', dest='check_integrity')
parser.add_argument('--report_instrument', action='store_true', dest='report_instrument')
parser.add_argument('-n', '--no_workers', type=int, dest='no_workers')
parser.add_argument('-v', '--verbose', action='store_true', dest='verbose')

args = parser.parse_args()

assembly = args.assembly
root_dir = args.root_dir or "/hps/nobackup/flicek/ensembl/variation/snhossain/issues/ensvar-6241"
check_assembly = args.check_assembly or False
check_integrity = args.check_integrity or False
report_instrument = args.report_instrument or False
no_workers = args.no_workers or 20
verbose = args.verbose or False
input_dir = f"{ root_dir }/inputs"
config_dir = f"{root_dir }/configs"
samples_dir = os.path.join(input_dir, assembly, "samples")
FILE_CORRUPTED = {}

if not os.path.exists(samples_dir):
    print(f"[ERROR] Samples directory not found - {samples_dir}")
    exit(1)
if os.listdir(samples_dir) == 0:
    print(f"[WARN] There is no samples file under - {samples_dir}")
    exit(1)

def gzip_integrity(file: str):
    print(f"[INFO] checking integrity of file - {file}\n")

    process = subprocess.run(['gzip', '-t', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    filename = os.path.basename(file)    
    if process.returncode != 0 or process.stderr.decode() != '':
        print(f"[WARN] { file } seems corrupted, skipping ...\nerror - { process.stderr.decode() }")
        FILE_CORRUPTED[filename] = True

    FILE_CORRUPTED[filename] = False

# we check gzip file integrity using multithred pool as they can be quite compute intensive
if check_integrity:
    for _, _, files in os.walk(samples_dir):
        with concurrent.futures.ThreadPoolExecutor(max_workers=no_workers) as executor:
            for file in files:
                if not file.startswith("SRR"):
                    continue

                executor.submit(gzip_integrity, os.path.join(samples_dir, file))

samples = {}
for _, _, files in os.walk(samples_dir):
    for file in files:
        if not file.startswith("SRR"):
            continue

        # get experiement accession from file name
        exp = file.split("_")[0]

        # get sample name querying the ENA api
        exp_r = requests.get(f'https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=run_accession={ exp }&fields=sample_accession&format=json')
        if exp_r.status_code != 200:
            print("[ERROR] Failed to get sample for experiment {exp} - { exp_r.reason }")
            exit(1)

        exp_rj = exp_r.json()
        if len(exp_rj) > 1:
            print("[ERROR] Multiple sample found for experiment {exp}")
            exit(1)
    
        sample = exp_rj[0]["sample_accession"]

        if verbose:
            print(f"[INFO] experiment: { exp }, sample: { sample }, file: { os.path.join(samples_dir, file) }")            
    
        # check if experiement run against the assembly we want
        if check_assembly:
            print("[INFO] Checking assembly ...")

        # skip file if it is corrupted
        if check_integrity:
            if FILE_CORRUPTED[file]:
                continue

        # report instrument model
        if report_instrument:
            exp_r = requests.get(f'https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=run_accession={ exp }&fields=instrument_model&format=json')
            if exp_r.status_code != 200:
                print("[WARN] Failed to get instrument model for experiment {exp} - { exp_r.reason }")
                continue

            exp_rj = exp_r.json()
            if len(exp_rj) > 1:
                print("[WARN] Multiple instrument model found for experiment {exp}")
                continue

            instrument_model = exp_rj[0]["instrument_model"]
            print(f"{ exp }\t{ instrument_model }")
            continue

        if sample not in samples:
            samples[sample] = {}
            samples[sample]["current_lane"] = 0

        if exp not in samples[sample]:
            samples[sample][exp] = {}
            samples[sample][exp]["file"] = []
            
        samples[sample]["current_lane"] = samples[sample]["current_lane"] + 1
        samples[sample][exp]["lane"] =  samples[sample]["current_lane"]
        samples[sample][exp]["sample"] = sample
        samples[sample][exp]["file"].append(file)

with open(os.path.join(config_dir, f"{assembly}.csv"), "w") as f:
    f.write("patient,sample,lane,fastq_1,fastq_2\n")
    for sample in samples:
        for exp in samples[sample]:
            if exp == "current_lane":
                continue
            d = samples[sample][exp]

            if len(d['file']) == 1:
                continue

            # for paired-end read lane number counted twice for each file
            lane = d['lane'] // 2 if (d['lane'] % 2 == 0) else d['lane']

            f.write(f"patient1,{ d['sample'] },lane{ lane }," + ",".join([f"{ samples_dir }/" + f for f in d['file']]) + "\n")

#example line
#patient1,SAMN01894461,lane8,../inputs/GCA_000472085/SRR652443_1.fastq.gz,../inputs/GCA_000472085/SRR652443_2.fastq.gz
