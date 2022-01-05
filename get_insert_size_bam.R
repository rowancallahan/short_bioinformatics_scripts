library(tidyverse)
library(plyranges)
library(readr)
library(stringr)
library(Rsamtools)

args<-commandArgs(TRUE)
#fl <- args[1]
#gene_reference <- args[2]
#output_table <- args[3]

#now we get to work loading the bamfile using rsamtools
# WE are going to filter out all of the reads that
#we are also going to get rid of the actual read 
fl <- args[1]
param <- ScanBamParam(what=c("rname", "strand", "pos", "qwidth", "isize", "qname"), mapqFilter=255)
res <- scanBam(fl, param=param)
reads_df <- as.data.frame(res)
rm(res)
gc()
#create a granges file that comes from a reference gtf to annotate our genomes
gene_reference <- args[2]
gene_bedfile <- read.delim(gene_reference, header=F, quote="") %>%
  filter(V3=="transcript")
gene_bedfile$V9 <- gene_bedfile %>% pull(V9) %>% str_replace_all("\"", "")
gene_bedfile$genename <- gene_bedfile$V9 %>% str_extract("(?<=gene_name ).*;$") %>%
  str_replace(";", "")
gene_name_granges <- data.frame(seqnames=gene_bedfile$V1, start=gene_bedfile$V4, width=
                                  gene_bedfile$V5 - gene_bedfile$V4 +1, end=gene_bedfile$V5,
                                strand = gene_bedfile$V7, name=gene_bedfile$genename)
gene_name_granges_uniq <- gene_name_granges[!duplicated(gene_name_granges$name),] %>% 
  as_granges()
gene_name_granges <- gene_name_granges %>% as_granges()


#reads filtered by size
granges_reads_df <- data.frame(seqnames=reads_df$rname, 
                                     start=reads_df$pos,
                                     width=reads_df$qwidth,
                                     end = reads_df$pos + reads_df$qwidth - 1,
                                     insert_size = reads_df$isize,
                                     strand= reads_df$strand,
                                     readname = reads_df$qname)


#get the output file prefix
output_file_prefix <- args[3]

#finding gene names for both of the differen granges lists
granges_reads_df_filtered <- granges_reads_df %>% filter(insert_size > 500) %>% filter(insert_size < 2500) %>% as_granges()
overlap_list <- find_overlaps_directed(granges_reads_df_filtered, gene_name_granges_uniq, minoverlap = 20) %>% 
  as.data.frame() 
overlap_list$file <- output_file_prefix

#now do the same for all reads
all_reads <- granges_reads_df %>% as_granges()
overlap_list_all <- find_overlaps_directed(all_reads, gene_name_granges_uniq) %>% 
  as.data.frame()
overlap_list_all$file <- output_file_prefix


#print out the most frequent in our filtered list
name_list <- overlap_list$name %>% table() %>%as.data.frame() %>%
  filter(Freq>=7) %>% pull(".")
cat(as.character(name_list), sep="\n")


write.table(overlap_list, file=paste0(output_file_prefix,"_length_list.txt"), sep="\t", quote=F, row.names = F, col.names = T)


#now lets filter for things that are in our liver list
#gene_list <- args[4]
gene_list <- c("TSPAN6") # put in your list of genes that you are interested in looking at here
gene_overlap_list <- overlap_list_all %>% filter(name %in% gene_list)
#now we will write this overlapped list to a file
write.table(gene_overlap_list, file=paste0(output_file_prefix,"_gene_list.txt"), sep="\t", quote=F, row.names = F, col.names = T)


