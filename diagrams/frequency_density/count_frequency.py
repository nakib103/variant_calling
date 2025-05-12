import sys

input_file = sys.argv[1]
output_file = sys.argv[2] if len(sys.argv) >= 3 else "frequency_count.txt"
decimal = int(sys.argv[3]) if len(sys.argv) >= 4 else 4

frequency_count = {}
with open(input_file, "r") as file:
    for line in file:
        if line.startswith("CHROM"):
            continue

        for allele_freq in line.split("\t")[5:]:
            freq = float(allele_freq.split(":")[1].strip())
            format_freq = str(round(freq, decimal))

            if format_freq not in frequency_count:
                frequency_count[format_freq] = 0
            frequency_count[format_freq] += 1

print(frequency_count)
print(len(frequency_count))
with open(output_file, "w") as file:
    for freq in frequency_count:
        file.write(f"{freq}\t{frequency_count[freq]}\n") 
