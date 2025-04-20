total_count = 0
freq_sum = 0.0
with open("data/GCA_000003025_novel_frequency_count.tsv") as f:
    for line in f:
        (freq, count) = [it.strip() for it in line.split("\t")]
        freq = float(freq)
        count = int(count)

        total_count += count
        freq_sum += (freq*count)

    avg_freq = freq_sum / total_count
    print(avg_freq)