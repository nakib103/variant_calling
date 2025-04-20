import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

total_novel_variants = 16161956
novel_variants_per_sample = {
    "SAMN01894345" : 1350555,
    "SAMN01894346" : 1378107,
    "SAMN01894349" : 1235305,
    "SAMN01894360" : 1514708,
    "SAMN01894361" : 1508271,
    "SAMN01894367" : 1527875,
    "SAMN01894368" : 0,
    "SAMN01894369" : 1278574,
    "SAMN01894370" : 1610198,
    "SAMN01894386" : 0,
    "SAMN01894387" : 1010943,
    "SAMN01894388" : 1645019,
    "SAMN01894389" : 1355379,
    "SAMN01894390" : 1225479,
    "SAMN01894391" : 1532416,
    "SAMN01894392" : 1217620,
    "SAMN01894393" : 982184,
    "SAMN01894394" : 1259803,
    "SAMN01894395" : 1156572,
    "SAMN01894406" : 1277378,
    "SAMN01894407" : 1378384,
    "SAMN01894408" : 1173728,
    "SAMN01894409" : 1164510,
    "SAMN01894410" : 1280975,
    "SAMN01894411" : 1190760,
    "SAMN01894412" : 1170746,
    "SAMN01894434" : 1562421,
    "SAMN01894435" : 1306920,
    "SAMN01894436" : 1457426,
    "SAMN01894437" : 1275937,
    "SAMN01894438" : 1194849,
    "SAMN01894439" : 0,
    "SAMN01894440" : 1205245,
    "SAMN01894441" : 1350422,
    "SAMN01894442" : 1288301,
    "SAMN01894443" : 1048925,
    "SAMN01894444" : 1214799,
    "SAMN01894445" : 1275370,
    "SAMN01894446" : 1389512,
    "SAMN01894447" : 1293966,
    "SAMN01894448" : 1378147,
    "SAMN01894452" : 1189389,
    "SAMN01894455" : 1275500,
    "SAMN01894456" : 1231414,
    "SAMN01894457" : 1174068,
    "SAMN01894458" : 1384747,
    "SAMN01894459" : 1680889,
    "SAMN01894460" : 1656661,
    "SAMN01894461" : 2458980,
    "SAMN04440474" : 1471245,
    "SAMN04440475" : 1531103,
    "SAMN04440476" : 1495770,
    "SAMN04440477" : 1439225,
    "SAMN04440478" : 1599001,
    "SAMN04440479" : 2327013,
    "SAMN04440480" : 2323694,
    "SAMN04440481" : 2315775,
    "SAMN04440482" : 2393261,
    "SAMN07325927" : 1547976,
    "SAMN09531794" : 2780992,
    "SAMN15501053" : 1453850,
    "SAMN17319783" : 78986,
    "SAMN17319784" : 142018,
    "SAMN17319785" : 136814,
    "SAMN18035060" : 2830380,
    "SAMN22234287" : 2660648,
    "SAMN22234288" : 2709657,
    "SAMN22234289" : 2668200,
    "SAMN22234290" : 2722854,
    "SAMN22234291" : 2622716,
    "SAMN22234292" : 2430992,
    "SAMN22234293" : 2703902,
    "SAMN22234294" : 2596251,
    "SAMN22234295" : 2518671,
    "SAMN22234296" : 2354882,
    "SAMN22234297" : 2446967,
    "SAMN22234298" : 2400739,
    "SAMN22234299" : 2723886,
    "SAMN22234300" : 2649098,
    "SAMN22234301" : 2729691,
    "SAMN22234302" : 2918023,
    "SAMN22234303" : 2797847,
    "SAMN22234304" : 3080298,
    "SAMN22234305" : 3275790,
    "SAMN22234306" : 3246391,
    "SAMN22234307" : 3063773,
    "SAMN22234308" : 2444687,
    "SAMN22234309" : 2203596,
    "SAMN22234310" : 2102412,
    "SAMN22234311" : 2225096,
    "SAMN22234312" : 2167740,
    "SAMN22234313" : 2326434,
    "SAMN22234314" : 2488770,
    "SAMN22234315" : 2545443,
    "SAMN22234316" : 2478336,
    "SAMN22234317" : 2582613,
    "SAMN22234318" : 2528617,
    "SAMN22234319" : 2495563,
    "SAMN22234320" : 2673831,
    "SAMN22234321" : 2611404,
    "SAMN22234322" : 2402136,
    "SAMN22234323" : 2557322,
    "SAMN22234324" : 2436383,
    "SAMN22234325" : 2590595,
    "SAMN22234326" : 2502390,
    "SAMN22234327" : 2414529,
    "SAMN22234328" : 2398311,
    "SAMN22234329" : 2680053,
    "SAMN22234330" : 2676919,
    "SAMN22234331" : 2691251,
    "SAMN22234332" : 2670133,
    "SAMN22234333" : 2692280,
    "SAMN22234334" : 2710584,
    "SAMN22234335" : 2694792,
    "SAMN22234336" : 2652542,
    "SAMN22234337" : 2589880,
    "SAMN22234338" : 2579108,
    "SAMN22234339" : 2562875,
    "SAMN22234340" : 2597578,
    "SAMN22234341" : 2630603,
    "SAMN22234342" : 2676128,
    "SAMN22234691" : 414479,
    "SAMN22234692" : 430878,
    "SAMN22234693" : 414072,
    "SAMN22234694" : 187957,
    "SAMN22234695" : 166727,
    "SAMN22234696" : 250417,
    "SAMN22234697" : 260575,
    "SAMN22234698" : 255601,
    "SAMN22234699" : 227359
}

percentage_novel_variants_per_sample = {sample: novel_variants_per_sample[sample] / total_novel_variants for sample in novel_variants_per_sample}
# sns.barplot(data=percentage_novel_variants_per_sample, palette='viridis')
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.xlabel('Samples')
# plt.ylabel('Novel variant count (%)')
# plt.show()

### variants per variant class
variant_per_variant_class = {
    'labels': ['SNV', 'insertions', 'deletion', 'sequence_alteration'],
    'data': [10545547, 2957799, 2218038, 184220] 
}
sns.set_style("whitegrid") # Set style for chart
plt.figure(figsize=(6,6)) # Set figure size
patches = plt.pie(variant_per_variant_class["data"], labels=variant_per_variant_class["labels"], autopct='%1.1f%%') # Create pie chart
# plt.legend(patches, variant_per_variant_class["labels"], loc='center left', bbox_to_anchor=(-0.1, 1.),
#            fontsize=8)
# plt.show() # Show chart
plt.savefig('novel_variant_per_class.png', bbox_inches='tight')


### variants per chromosome
novel_variants_per_chrom = {
 "1" : 1403970,
  "10" : 500708,
  "11" : 554222,
  "12" : 494233,
 "13" : 1099043,
  "14" : 805218,
  "15" : 814799,
  "16" : 501998,
  "17" : 462098,
  "18" : 386690,
  "2" : 897612,
  "3" : 824963,
  "4" : 746777,
  "5" : 719854,
 "6" : 1111209,
  "7" : 752974,
  "8" : 807284,
  "9" : 837060,
     "MT" : 488,
  "X" : 612552,
  "Y" : 184702
}

existing_variants_per_chrom = {
    "1" : 7092245, 
    "10" : 2796047, 
    "11" : 2814192,
    "12" : 2092258,
    "13" : 5471794,
    "14" : 4230421,
    "15" : 4002056,
    "16" : 2669247,
    "17" : 2232203,
    "18" : 1969465,
    "2" : 4598886,
    "3" : 4100093,
    "4" : 4027007,
    "5" : 3327347,
    "6" : 4666390,
    "7" : 3961196,
    "8" : 4255451,
    "9" : 4445347,
    "X" : 1951955,
    "Y" : 22599,
    "MT": 0
}

percentage_novel_variants_per_chrom = {chrom: novel_variants_per_chrom[chrom] / (existing_variants_per_chrom[chrom] + novel_variants_per_chrom[chrom]) for chrom in novel_variants_per_chrom}

# sns.barplot(data=percentage_novel_variants_per_chrom, palette='viridis')
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.xlabel('Chromosome')
# plt.ylabel('Novel variant percentage (%)')
# plt.show()