import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df_exist = pd.read_csv("data/GCA_000003025_existingCalled_frequency_count.tsv", sep="\t", names=["freq", "count"])
df_novel = pd.read_csv("data/GCA_000003025_novel_frequency_count.tsv", sep="\t", names=["freq", "count"])

df_exist["log_count"] = np.log10(df_exist["count"])
df_novel["log_count"] = np.log10(df_novel["count"])

df_exist["ratio"] = np.log10(df_exist["count"] / df_exist["count"].sum())
df_novel["ratio"] = np.log10(df_novel["count"] / df_novel["count"].sum())

f, ax = plt.subplots(1, 1)
y_col = "ratio"
y_label = "log10 ratio"
sns.lineplot(data=df_exist, x="freq", y=y_col, color="blue", label="known called")
sns.lineplot(data=df_novel, x="freq", y=y_col, color="red", label="novel")
ax.legend()
plt.ylabel(y_label)
plt.xlabel("frequency")
plt.show()