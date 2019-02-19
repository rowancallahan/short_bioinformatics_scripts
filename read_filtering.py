# This scripts takes a huge fasta file and removes all of the contigs that are shorter than a specified length
#inspiration taken heavily from biopython.SeqIO.fastaIO

#This is written to intentionally have few requirements and only use base python so it can be used as a python command line utility
import argparse
import re

parser = argparse.ArgumentParser(description='remove contigs below a certain size from large fasta file')
parser.add_argument('fasta_file', metavar='fasta')
parser.add_argument('--min-len', default=500, type=int, help='the minimum length of sequences in order to be kept')
parser.add_argument('--in-place',dest='in_place',action='store_true', default=False, help='decides whether the file is edited in place or not')
parser.add_argument('--match', default=".*", type=str, help="the regex to use when filtering ")
parser.add_argument('--separate-files', dest='separate', action='store_true', default=False, help='whether to separate sequences out into separate files')

args = parser.parse_args()
print(args.match)
print(args.separate)

if args.in_place:
    outfile = args.fasta_file
    #print('inplace specified, writing to %s' % outfile)
else:
    outfile = args.fasta_file[:-6] + '.filtered.fasta' 


with open(args.fasta_file,'r') as fasta:
    contig_started = False
    contig = ''
    title = ''

    for line in fasta:

        if line[0] == '>': 
            if len(contig)>= args.min_len and contig_started and re.search(args.match, title):
                contig = '\n'.join([contig[i:i+75] for i in range(0,len(contig),75)])
                output = title + "\n" + contig + "\n"
                if args.separate: #if we are separating make a new file title
                    outfile = args.fasta_file[:-6] +title.replace(" ","_").replace(">","_") +".fasta"
		    #replace the whitespace
                with open(outfile,'a') as out: #open the file and write to it.
                    out.write(output)

            contig= ''
            contig_started = True
            title = line.rstrip()
        else:
            contig = contig + line.rstrip()
    else:
        if len(contig)>= args.min_len and contig_started and re.search(args.match, title):
            contig = '\n'.join([contig[i:i+75] for i in range(0,len(contig),75)])
            output = title + "\n" + contig + "\n"
            if args.separate: #if we are separating make a new file title
                outfile = args.fasta_file[:-6] + title.replace(" ","_").replace(">","_") + ".fasta" #replace the whitespace
            with open(outfile,'a') as out: #open the file and write to it.
                out.write(output)


