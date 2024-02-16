import argparse
from collections import namedtuple
import os
import numpy as np
import matplotlib.pyplot as plt
import subprocess

Gene = namedtuple('Gene', ['name', 'chrm', 'start', 'end', 'strand'])

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stix_index', type=str, required=True)
    parser.add_argument('--gene_file', type=str, required=True)
    parser.add_argument('--gene', type=str, required=True)
    parser.add_argument('--out_file', type=str, required=True)
    parser.add_argument('--width', type=float, default=4.0)
    parser.add_argument('--height', type=float, default=1.0)
    return parser.parse_args()

def run_stix(index, gene, out_file):
    command = ['giggle',
               'search',
               '-i',index,
               '-v',
               '-r',f'{gene.chrm}:{gene.start}-{gene.end}']

    with open(out_file, 'w') as file:
        subprocess.run(command, stdout=file, text=True)

def get_genes(file):
    genes = {}

    with open(file) as lines:
        for line in lines:
            if line[0] == '#': continue
            A = line.rstrip().split()
            gene = Gene(A[3], A[0], int(A[1]), int(A[2]), A[5])
            genes[gene.name] = gene
    return genes

def extract_gene_hits(in_file):
    hits = []
    with open(in_file) as lines:
        for line in lines:
            if line[0] == '#': continue
            A = line.rstrip().split()
            hits.append( (int(A[1]), int(A[2]) ) )
    return hits

def get_gene_hits(stix_index, genes, gene, working_dir):
    stix_output = f'{working_dir}/{gene}.bed'

    run_stix(stix_index, genes[gene], stix_output)
    hits = extract_gene_hits(stix_output)

    os.remove(stix_output)

    return hits

def main():
    args = get_args()
    genes = get_genes(args.gene_file)

    working_dir = os.path.dirname(args.out_file)

    gene_hits = get_gene_hits(args.stix_index,
                              genes,
                              args.gene,
                              working_dir)

    bars = {}
    for start,end in gene_hits:
        if start not in bars:
            bars[start] = 0
        bars[start] = bars[start] + 1

    x_values = list(bars.keys())
    heights = [bars[x] for x in x_values]

    fig, ax = plt.subplots(figsize=(args.width, args.height))

    ax.bar(x_values, heights, width=1)

    ax.set_xlim( ( genes[args.gene].start, genes[args.gene].end) )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_linewidth(0.1)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis='x', which='both',length=0)
    ax.tick_params(axis='y', which='both',length=0)

    plt.tight_layout()
    plt.savefig(args.out_file, dpi=300)
if __name__ == '__main__':
    main()
