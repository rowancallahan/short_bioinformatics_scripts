import re
import argparse

# first take the start and end of a specific title then calculate the windows, then search for the title, then grab the windows
#group the targets by gene can group by gene but there might not be enough
#list of groups of windows by gene, by gene group? get all windows and look at that

parser = argparse.ArgumentParser(description='pull out windows on either side of annotated genes')
parser.add_argument('fasta_file', metavar='fasta',help='the fasta file')
parser.add_argument('location_file',metavar='locations',help='the name of the locations file')
parser.add_argument('out_file', metavar='out',help='name of the outfile')
parser.add_argument('window_size',metavar='n',help='number of chars before and after')
#parser.add_argument('--in-place',dest='in_place',action='store_true', default=False, help='decides whether the file is edited in place or not')

args = parser.parse_args()
print(args.fasta_file,args.location_file, args.out_file,args.window_size)

file = args.location_file 
contig_file = "contig_test.fasta"

#method for finding windows given a file, this will allow us to multithread later
def find_window(start,end,contig_name,contig_info,contig_file_name):
    with open(contig_file_name,"r") as contigs:
        contig_started = False
        contig = ''
        contig_name = re.sub(r'_[0-9]*$','',contig_name)
        title = contig_name + '-' + contig_info 
        contig_re = "." + contig_name + ".*"
        search_key = re.compile(contig_re)

        for line in contigs:

            is_match = search_key.match(line) is not None
            if line[0] == '>' and is_match:
                contig_started = True
            elif line[0] == '>' and not is_match:
                if len(contig) >= end and contig_started:
                    contig = contig[start:end] 
                    contig = '\n'.join([contig[i:i+75] for i in range(0,len(contig),75)])
                    output = title + "\n" + contig + "\n"
                    return output
            elif contig_started:
                contig = contig + line.rstrip()


with open(file,"r") as locations:
    for line in locations:
        parsed = line.split('\t') 
         
        id = parsed[0]
        family = parsed[1]
        name = parsed[2]
        gene = parsed[3]
        start = parsed[5]
        end = parsed[6]
        print(id,family,name,gene,start,end)

        print(find_window(int(start),int(end),name,"testinfo",contig_file))


