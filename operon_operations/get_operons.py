import re
import pandas as pd
import argparse

column_list = ['ID', 'Start', 'End']
forward = pd.DataFrame(columns=column_list)
backward = pd.DataFrame(columns=column_list)

parser = argparse.ArgumentParser()
parser.add_argument("orf_file")
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

series1 = pd.Series(str(operon) for operon in operon_list)
series2 = pd.Series(len(operon) for operon in operon_list)
series3 = pd.Series(str(operon) for operon in operon_list2)
series4 = pd.Series(len(operon) for operon in operon_list2)

forward = pd.concat([series1, series2], axis=1) 
backward = pd.concat([series3,series4], axis=1)

whole = pd.concat([forward,backward], axis=0, ignore_index=True)


with pd.option_context('display.max_rows', None, 'display.max_columns', None):

    print(whole)



