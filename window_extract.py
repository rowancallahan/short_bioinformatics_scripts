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

with open(args.location_file, "r") as locations:
    for line in locations
        #add all of the different fasta headers to a set
        #each set should contain an element that also has the start and end locations
        print(line)



'''
with open(args.fasta_file,'r') as fasta, open(outfile,'w') as out:
    contig_started = False
    contig = ''
    title = ''

    for line in fasta:

        if line[0] == '>':
            if len(contig)>= args.min_len and contig_started:
                contig = '\n'.join([contig[i:i+75] for i in range(0,len(contig),75)])
                output = title + "\n" + contig + "\n"

                out.write(output)

            contig= ''
            contig_started = True
            title = line.rstrip()
        else:
            contig = contig + line.rstrip()
    else:
        if len(contig)>= args.min_len and contig_started:
            contig = '\n'.join([contig[i:i+75] for i in range(0,len(contig),75)])
            output = title + "\n" + contig + "\n"
            out.write(output)
'''

