import re
import pandas as pd
import argparse
import hashlib

column_list = ['ID', 'Start', 'End']
forward = pd.DataFrame(columns=column_list)
backward = pd.DataFrame(columns=column_list)

parser = argparse.ArgumentParser()
parser.add_argument("orf_file")
parser.add_argument("outname")
args = parser.parse_args()
filename = args.orf_file


with open(filename) as file:
    for line in file:
        split = line.rstrip().split("\t")
        if len(split) >=8:
            split[8] = re.sub(';.*;','',split[8]).replace("ID=","")
            if split[6] == "+":
                row = pd.Series([split[8], int(split[3]), int(split[4])], index=column_list)
                forward = forward.append(row, ignore_index=True)
            elif split[6] == "-":
                row = pd.Series([split[8], int(split[3]), int(split[4])], index=column_list)
                backward = backward.append(row, ignore_index=True)

def get_orfs(dataframe):
    distances = - dataframe['End'][:-1].reset_index(drop=True) + dataframe['Start'][1:].reset_index(drop=True) #we want the distances between the end of one orf to the start of the next
    orf_list = dataframe['ID'][1:].reset_index(drop=True)
    grouping = pd.concat([distances,orf_list], axis=1)
    grouping.columns = ['distance','id']
    operon_list = [[dataframe.iloc[0][0]]]

    for i in range(len(grouping)):
        if grouping.loc[i]['distance'] <= 100:
            operon_list[-1].append(grouping.loc[i]['id'])
        else:
            operon_list.append([grouping.loc[i]['id']])

    return(operon_list)

operon_list = get_orfs(forward)
operon_list2 = get_orfs(backward)

forward_list = pd.Series(",".join(operon) for operon in operon_list)
forward_length = pd.Series(len(operon) for operon in operon_list)
forward_operon_id = pd.Series(hashlib.sha1(str(operon).encode("utf-8")).hexdigest() for operon in operon_list)
backwards_list = pd.Series(",".join(operon) for operon in operon_list2)
backwards_length = pd.Series(len(operon) for operon in operon_list2)
backwards_operon_id = pd.Series(hashlib.sha1(str(operon).encode("utf-8")).hexdigest() for operon in operon_list2)
 

forward = pd.concat([forward_list, forward_length, forward_operon_id], axis=1) 
backward = pd.concat([backwards_list, backwards_length, backwards_operon_id], axis=1)

whole = pd.concat([forward,backward], axis=0, ignore_index=True)

whole.to_csv(args.outname, sep="\t", encoding="utf-8")

with pd.option_context('display.max_rows', None, 'display.max_columns', None):

    print(whole)



