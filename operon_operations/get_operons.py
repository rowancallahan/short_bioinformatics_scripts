import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("orf_file")
args = parser.parse_args()
filename = args.orf_file
print(filename)

filename_backward = filename
filename_forward= filename 

forward = pd.read_csv(filename_forward, sep='\t', header=None)
backward = pd.read_csv(filename_backward, sep='\t', header=None)

def get_orfs(dataframe):

    distances = - dataframe[2][:-1].reset_index(drop=True) + dataframe[1][1:].reset_index(drop=True)
    orf_list = dataframe[0][1:].reset_index(drop=True)
    grouping = pd.concat([distances,orf_list], axis=1)
    grouping.columns = ['distance','id']
    operon_list = [[dataframe.iloc[0][0]]]

    for i in range(len(grouping)):
        if grouping.loc[i]['distance'] <= 100:
            operon_list[-1].append(grouping.loc[i]['id'])
        else:
            operon_list.append([grouping.loc[i]['id']])

    length = []
    for i in range(len(operon_list)):
        length.append(len(operon_list[i]))


    return(length, operon_list)

length, operon_list = get_orfs(forward)
length2, operon_list2 = get_orfs(backward)

for num in length:
    print(num)
for operon in operon_list:
    print(operon)


