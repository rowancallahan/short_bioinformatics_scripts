import argparse
import pandas as pd
import re

parser = argparse.ArgumentParser()
parser.add_argument("orf_file")
parser.add_argument("hits_file")
args = parser.parse_args()
filename = args.orf_file
hits = args.hits_file
genome_id = args.hits_file[:-27] #TODO need to parse the name of this file correctly

#read in and clean all of the files
orfs_file = pd.read_csv(filename, sep="\t",encoding="utf-8",index_col=0)
hits = pd.read_csv(hits, sep="\t", encoding="utf-8", header=None)
hits[0] = hits.applymap(lambda x: re.sub("^.*\.","",str(x))) #clean up the name of the orf to just get the specific orf_id information without the intro characters


#we add the locus id as a value with its key being one of the orfs
#this allows us to easily lookup locus id by simply specifying orf_id

locus_dict = {}
for row_num in range(len(orfs_file)):
    values  =  [str(x) for x in str(orfs_file.iloc[row_num, 0]).split(',') ]
    for val in values:
        locus_dict[val] = str(orfs_file.iloc[row_num,2])

#now lets start writing each row
rows = []
for row_num in range(len(hits)):
    index = str(hits.iloc[row_num, 0])
    locus_id = locus_dict[index]
    orfs = orfs_file.loc[orfs_file.iloc[:,2] == locus_id].iloc[0]
    n_genes = len(str(orfs).split(',')) 

    row_list = [genome_id, hits.iloc[row_num, 1] , locus_id, orfs, n_genes, "NaN"] 
    index_list = ["genome_id", "human_interactor", "locus", "orfs", "n_orfs", "num_interactors"]
    row = pd.Series(row_list, index=index_list)
    rows.append(row)


#stitch all of the rows together now
df = pd.concat(rows, axis=1).T

#now find out how many times each locus is listed
#this will tell us how many human interactors are shared in this locus
df['num_interactors'] = df.groupby('locus')['locus'].transform('count')

print(df)


