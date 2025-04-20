import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
import os
from math import ceil

# data
# idio = pd.read_csv(os.path.join(os.getcwd(), '/data/susScr11.ideo'), sep='\t')
chrom_map = {
        'chr1': 0, 'chr2': 1, 'chr3': 2, 'chr4': 3, 'chr5': 4, 'chr6': 5, 
        'chr7': 6, 'chr8': 7, 'chr9': 8, 'chr10': 9, 'chr11': 10, 'chr12': 11, 
        'chr13': 12, 'chr14': 13, 'chr15': 14, 'chr16': 15, 'chr17': 16, 
        'chr18': 17, 'chrX': 18, 'chrY': 19
    }
current_coverage = pd.read_csv(
        os.path.join(os.getcwd(), 'data/current_coverage_100k.txt'), sep='\t', 
        names=["chrom", "chromStart", "chromEnd", "counts"]
    )
novel_coverage = pd.read_csv(
        os.path.join(os.getcwd(), 'data/coverage_novel_100k.txt'), sep='\t', 
        names=["chrom", "chromStart", "chromEnd", "counts"]
    )

novel_start_pos = pd.read_csv(
        os.path.join(os.getcwd(), 'data/chr1_start_pos_novel.txt'), sep='\t', 
        header = 0, names=["chrom", "chromStart"]
    )

# sns.barplot(data=current_coverage, x="chromStart", y="counts")
# plt.show()
# exit()

# print(current_coverage[current_coverage["chrom"] == "chr1"].sort_values(by='counts'))
# print(novel_coverage[novel_coverage["chrom"] == "chr1"].sort_values(by='counts'))

current_low_coverage = current_coverage[current_coverage["chrom"] == "chr1"].sort_values(by='counts').iloc[:100, :]
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(current_low_coverage)
# print(current_low_coverage)
# print(current_low_coverage["chromEnd"])
new_coverage_in_low_area = novel_coverage[
        novel_coverage["chrom"].isin(current_low_coverage["chrom"])
        & novel_coverage["chromStart"].isin(current_low_coverage["chromStart"])
        & novel_coverage["chromEnd"].isin(current_low_coverage["chromEnd"])
    ]
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(new_coverage_in_low_area)
# print(new_coverage_in_low_area)

# fig, axes = plt.subplots(2, figsize=(20, 5))
# sns.set(style='darkgrid', palette="Paired")
# axes[0].set_title('current low coverage')
# axes[0].tick_params(labelrotation=90)
# sns.barplot(ax=axes[0], data=current_low_coverage, x="chromStart", y="counts")
# axes[1].set_title('novel coverage on previous low coverage region')
# axes[1].tick_params(labelrotation=90)
# sns.barplot(ax=axes[1], data=new_coverage_in_low_area, x="chromStart", y="counts")
# plt.tight_layout()
# plt.show()

print(novel_start_pos[novel_start_pos["chrom"] == "1"])
sns.set(style='darkgrid', palette="Paired")
plt.title('current low coverage')
plt.xticks(rotation=90)
sns.kdeplot(data=novel_start_pos[novel_start_pos["chrom"] == "1"], y="chromStart")
# sns.barplot(data=current_low_coverage, x="chromStart", y="counts")
# sns.barplot(data=new_coverage_in_low_area, x="chromStart", y="counts")
# top_bar = mpatches.Patch(color='darkblue', label='known varinats')
# bottom_bar = mpatches.Patch(color='lightblue', label='novel variants')
# plt.legend(handles=[top_bar, bottom_bar])
plt.tight_layout()
# plt.show()