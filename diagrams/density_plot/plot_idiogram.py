import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from math import ceil

IDEOGRAM_COLOR_MAP = {
    'gpos100': (0 / 255.0, 0 / 255.0, 0 / 255.0),
    'gpos': (0 / 255.0, 0 / 255.0, 0 / 255.0),
    'gpos75': (130 / 255.0, 130 / 255.0, 130 / 255.0),
    'gpos66': (160 / 255.0, 160 / 255.0, 160 / 255.0),
    'gpos50': (200 / 255.0, 200 / 255.0, 200 / 255.0),
    'gpos33': (210 / 255.0, 210 / 255.0, 210 / 255.0),
    'gpos25': (200 / 255.0, 200 / 255.0, 200 / 255.0),
    'gvar': (220 / 255.0, 220 / 255.0, 220 / 255.0),
    'gneg': (255 / 255.0, 255 / 255.0, 255 / 255.0),
    'acen': (217 / 255.0, 47 / 255.0, 39 / 255.0),
    'stalk': (100 / 255.0, 127 / 255.0, 164 / 255.0),
}

# data
idio = pd.read_csv(os.path.join(os.getcwd(), 'susScr11.ideo'), sep='\t')
chrom_map = {
        'chr1': 0, 'chr2': 1, 'chr3': 2, 'chr4': 3, 'chr5': 4, 'chr6': 5, 
        'chr7': 6, 'chr8': 7, 'chr9': 8, 'chr10': 9, 'chr11': 10, 'chr12': 11, 
        'chr13': 12, 'chr14': 13, 'chr15': 14, 'chr16': 15, 'chr17': 16, 
        'chr18': 17, 'chrX': 18, 'chrY': 19
    }
current_coverage = pd.read_csv(
        os.path.join(os.getcwd(), 'current_coverage_10k.txt'), sep='\t', 
        names=["chrom", "chromStart", "chromEnd", "counts"]
    )
novel_coverage = pd.read_csv(
        os.path.join(os.getcwd(), 'coverage_novel_10k.txt'), sep='\t', 
        names=["chrom", "chromStart", "chromEnd", "counts"]
    )

sns.set(style='darkgrid', palette="Paired")
sns.despine()

fig, axes = plt.subplots(ceil(len(chrom_map) / 2), 2, figsize=(20, 5))
xmax = idio.chromEnd.max() * 1.1
for chrom, df_cc in current_coverage.groupby('chrom'):
    if chrom not in chrom_map:
        continue

    chrom_idx = chrom_map[chrom]

    # # ax.set_title("Title")
    # # ax.set_ylabel('Position')

    xticks = np.arange(0, xmax, xmax / 10)
    axes[chrom_idx // 2][chrom_idx % 2].set_xticks(xticks)
    # ax.set_xticklabels(['{0}M'.format(int(i / 10 ** 6)) for i in xticks])
    axes[chrom_idx // 2][chrom_idx % 2].set_xticklabels([])

    # axes[chrom_idx // 2][chrom_idx % 2].set_yticks([0, 1])
    # # ax.set_yticklabels([chrom for (chrom, index) in sorted(chrom_map.items(), key=lambda x: x[1])], ha='left')
    # axes[chrom_idx // 2][chrom_idx % 2].set_yticklabels(["current", "novel"])

    axes[chrom_idx // 2][chrom_idx % 2].set_ylabel(chrom)

    # axes[chrom_idx].set_xbound(0, xmax)
    # # ax.set_ybound(0, len(chrom_map))

    # axes[chrom_idx].hist(df_cc.counts, df_cc.chromStart)
    df_nc = novel_coverage[novel_coverage["chrom"] == chrom]
    df_nc["avg_counts"] = df_nc["counts"] / df_nc["counts"].max() + 1.0
    df_cc["smooth_counts"] = (df_cc["counts"] * 0.25)
    df_cc["avg_counts"] = df_cc["smooth_counts"] / df_cc["smooth_counts"].max()

    df_nc["diff"] = df_nc["counts"] - df_cc["counts"]
    # df_nc["diff"] = df_nc["new_counts"] / df_nc["new_counts"].max() + 1.0
    
    # axes[chrom_idx // 2][chrom_idx % 2].scatter(df_cc["chromStart"], df_cc["avg_counts"], marker = '.', linewidths=0.05, s=3)
    # axes[chrom_idx // 2][chrom_idx % 2].scatter(df_nc["chromStart"], df_nc["avg_counts"], marker = '.', linewidth=0.05, s=3, color="black")

    sns.barplot(ax = axes[chrom_idx // 2][chrom_idx % 2], data = df_cc, x = df_cc["chromStart"], y = df_cc["avg_counts"])
    # sns.barplot(ax = axes[chrom_idx // 2][chrom_idx % 2], data = df_nc, x = df_cc["chromStart"], y = df_nc["avg_counts"], color="black")
    
    # df = pd.DataFrame({'y': df_cc["counts"], 'x': df_cc["chromStart"]}) 
    # df = df_cc[df_cc["chromStart"] < 500000]
    # sns.displot(data = df, y="counts", x="chromEnd", kind="kde")
    # sns.countplot(data = df, y="counts")

# fig, axes = plt.subplots(figsize=(20, 5))
# for chrom, df_cc in current_coverage.groupby('chrom'):
#     if chrom not in chrom_map or chrom != "chrY":
#         continue

#     chrom_idx = chrom_map[chrom]
#     # # for i, row in df_cc.iterrows():
#     #     # r = plt.Rectangle((chrom_map[chrom], row.chromStart), row.chromEnd - row.chromStart, .2, color=IDEOGRAM_COLOR_MAP[row.gieStain])
#     #     # axes[chrom_idx].add_patch(r)

#     # # ax.set_title("Title")
#     # # ax.set_ylabel('Position')

#     # xticks = np.arange(0, xmax, xmax / 10)
#     # axes.set_xticks(xticks)
#     # # ax.set_xticklabels(['{0}M'.format(int(i / 10 ** 6)) for i in xticks])
#     # axes.set_xticklabels([])

#     axes.set_yticks([0, 1])
#     # # ax.set_yticklabels([chrom for (chrom, index) in sorted(chrom_map.items(), key=lambda x: x[1])], ha='left')
#     axes.set_yticklabels(["current", "novel"])

#     axes.set_ylabel(chrom)

#     # axes[chrom_idx].set_xbound(0, xmax)
#     # # ax.set_ybound(0, len(chrom_map))

#     # axes[chrom_idx].hist(df_cc.counts, df_cc.chromStart)
#     df_nc = novel_coverage[novel_coverage["chrom"] == chrom]
#     df_nc["avg_counts"] = df_nc["counts"] / df_nc["counts"].max() + 1.0
#     df_cc["avg_counts"] = df_cc["counts"] / df_cc["counts"].max()

#     df_nc["new_counts"] = df_nc["counts"] + df_cc["counts"]
#     df_nc["new_avg_counts"] = df_nc["new_counts"] / df_nc["new_counts"].max() + 1.0
#     # axes[chrom_idx // 2][chrom_idx % 2].scatter(df_cc["chromStart"], df_cc["avg_counts"], marker = '.', linewidths=0.05, s=3)
#     # axes[chrom_idx // 2][chrom_idx % 2].scatter(df_nc["chromStart"], df_nc["avg_counts"], marker = '.', linewidth=0.05, s=3, color="black")
#     sns.lineplot(data = df_cc[df_cc["chromStart"] < 5000000], x = df_cc["chromStart"], y = df_cc["avg_counts"])
#     sns.lineplot(data = df_nc[df_nc["chromStart"] < 5000000], x = df_cc["chromStart"], y = df_nc["new_avg_counts"], color="black")
#     # df = pd.DataFrame({'y': df_cc["counts"], 'x': df_cc["chromStart"]}) 
#     # df = df_cc[df_cc["chromStart"] < 500000]
#     # sns.displot(data = df, y="counts", x="chromEnd", kind="kde")
#     # sns.countplot(data = df, y="counts")

#     # axes.plot()

plt.show()