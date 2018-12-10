# This scripts takes a huge fasta file and removes all of the contigs that are shorter than a specified length
#inspiration taken heavily from biopython.SeqIO.fastaIO

#This is written to intentionally have few requirements and only use base python so it can be used as a python command line utility
import argparse

parser = argparse.ArgumentParser(description='remove contigs below a certain size from large fasta file')
parser.add_argument('fasta_file', metavar='fasta')
parser.add_argument('--in-place',dest='in_place',action='store_true', default=False, help='decides whether the file is edited in place or not')

args = parser.parse_args()
outfile = ''


with open(args.fasta_file,'r') as fasta:
    output = ''
    contig_started = False
    contig = ''
    title = ''

    for line in fasta:

        if line[0] == '>':
            if len(contig)>= 500 and contig_started:
                contig = '\n'.join([contig[i:i+75] for i in range(0,len(contig),75)])
                output = output + title + "\n" + contig + "\n"

            contig= ''
            contig_started = True
            title = line.rstrip()
        else:
            contig = contig + line.rstrip()
    else:
        if len(contig)>= 500 and contig_started:
            contig = '\n'.join([contig[i:i+75] for i in range(0,len(contig),75)])
            output = output + title + "\n" + contig + "\n"


if args.in_place:
    outfile = args.fasta_file
    print('inplace specified, writing to %s' % outfile)
    with open(outfile,'w') as out:
        out.write(output)

else:
    outfile = args.fasta_file[:-6] + '.filtered.fasta' 
    print(output)

