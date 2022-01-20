import os
import pandas as pd
import sys

# path_references = sys.argv[1]
path_data = sys.argv[1]

# path_references = "/content/Epigenetics-and-genetics-references/Cpg_reference/Cpg_hg38/reference_bed/HM27"
# path_data="/content/meth27"
# for i in chr:
# df1=pd.read_csv(path_references+"/HM27.hg38_chr"+str(i)+".tsv",header=None,names=["chr","start","end","key"],sep="\t")
# df1=df1[["key"]]
for k in os.listdir(path_data):
    if k.startswith("chr"):
        df = pd.read_csv(path_data+"/"+k, sep="\t")
        df.index = df.iloc[:, 0]
        df = df.T
        df = df[df["Composite Element REF"] == "Beta_value"]
        df.index = pd.Series(df.index).apply(lambda x: x[:15])
        df = df.iloc[:, 1:]
        print("Complete for file:", k)
        # df.head()
        df = df.T
        df.to_csv(path_data+"/"+k, sep="\t", index="False")
        # df=df.drop(columns="key")
    else:
        pass
