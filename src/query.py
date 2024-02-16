import argparse
from collections import namedtuple
import subprocess
import os
import time
import concurrent.futures
import sys

Gene = namedtuple('Gene', ['name', 'chrm', 'start', 'end', 'strand'])

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stix_index', type=str, required=True)
    parser.add_argument('--gene_file', type=str, required=True)
    parser.add_argument('--gene', type=str)
    parser.add_argument('--working_dir', type=str, required=True)
    parser.add_argument('--threads', type=int, default=1)
    return parser.parse_args()

def get_genes(file):
    genes = {}

    with open(file) as lines:
        for line in lines:
            if line[0] == '#': continue
            A = line.rstrip().split()
            gene = Gene(A[3], A[0], int(A[1]), int(A[2]), A[5])
            genes[gene.name] = gene
    return genes

def run_stix(index, gene, out_file):
    command = ['giggle',
               'search',
               '-i',index,
               '-v',
               '-r','{}:{}-{}'.format(gene.chrm, gene.start, gene.end)]

    with open(out_file, 'w') as file:
        result = subprocess.run(command, stdout=file)

    if result.stdout is not None:
        stdout_text = result.stdout.decode('utf-8')
    else:
        stdout_text = ""

    if result.stderr is not None:
        stderr_text = result.stderr.decode('utf-8')
    else:
        stderr_text = ""

    return stdout_text, stderr_text


def extract_dels(in_file, out_file):
    with open(out_file, 'w') as file:
        with open(in_file) as lines:
            for line in lines:
                if line[0] == '#': continue
                A = line.rstrip().split()
                if A[0] != A[4]: continue
                if A[3] != '1': continue
                if A[7] != '-1': continue
                file.write('\t'.join(A[4:7]) + '\n')

def intersect_genes(gene, in_file, out_file, gene_file):
    intersect_script = '/mnt/local/data/my_stix_analysis/src/intersect.sh'
    command = [intersect_script,
               '-g',
               gene,
               '-f',
               gene_file,
               '-s',
               in_file]

    with open(out_file, 'w') as file:
        result = subprocess.run(command,
                                stdout=file,
                                stderr=subprocess.PIPE)

    if result.stdout is not None:
        stdout_text = result.stdout.decode('utf-8')
    else:
        stdout_text = ""

    if result.stderr is not None:
        stderr_text = result.stderr.decode('utf-8')
    else:
        stderr_text = ""

    error = result.stderr

    if result.returncode != 0:
        print("Error:", error)

    return result.returncode

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def match_strand(src_gene, genes, pre_hit_file, out_file):
    hits = []
    with open (pre_hit_file) as lines:
        for line in lines:
            depth, dst_gene = line.strip().split()
            if genes[src_gene].strand == genes[dst_gene].strand:
                hits.append('{}:{}'.format(dst_gene, depth))

    if len(hits) > 0:
        with open(out_file, 'w') as file:
            hits = [src_gene] + hits
            file.write('\t'.join(hits) + '\n')

def run_gene(stix_index, genes, gene, gene_file, working_dir):
    stix_output = '{}/{}.bed'.format(working_dir, gene)
    dels = '{}/{}.dels.bed'.format(working_dir, gene)
    pre_hits = '{}/{}.pre_hits.txt'.format(working_dir, gene)
    hits = '{}/{}.hits.txt'.format(working_dir, gene)

    t0 = time.time()
    run_stix(stix_index, genes[gene], stix_output)
    extract_dels(stix_output, dels)
    r = intersect_genes(gene, dels, pre_hits, gene_file)
    match_strand(gene, genes, pre_hits, hits)
    os.remove(stix_output)
    os.remove(dels)
    os.remove(pre_hits)
    t1 = time.time()
    print(gene, round(t1-t0,2))
    return((gene, round(t1-t0,2)))

def run_genes(stix_index, genes, gene_file, working_dir, num_threads):
    ids = range(len(genes))

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) \
            as executor:
        future_to_file = \
            {executor.submit(run_gene,
                             stix_index,
                             genes,
                             gene,
                             gene_file,
                             working_dir): \
             gene for gene in genes}

        for future in concurrent.futures.as_completed(future_to_file):
            i = future_to_file[future]
            try:
                data = future.result()
                results.append(data)  # Aggregate results
            except Exception as exc:
                sys.stderr.write(str(i) + ' generated an exception: ' + str(exc))

    return results

def main():
    args = get_args()

    genes = get_genes(args.gene_file)
    make_dir(args.working_dir)
    if args.gene is not None:
        run_gene(args.stix_index, genes, args.gene, args.gene_file, args.working_dir)
    else:
        runtimes = run_genes(args.stix_index,
                             genes,
                             args.gene_file,
                             args.working_dir,
                             args.threads)


if __name__ == '__main__':
    main()
