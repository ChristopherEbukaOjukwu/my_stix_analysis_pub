import utils
import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys
import pickle

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--burden_file', type=str, required=True)
    parser.add_argument('--gene_cols', nargs='+',type=int, required=True)
    return parser.parse_args()

def get_burden(file):
    burden = {}
    with open(file) as lines:
        for line in lines:
            A = line.rstrip().split()
            burden[A[0]] = int(A[1])
    return burden

def main():
    args = get_args()

    burden = get_burden(args.burden_file)

    for line in sys.stdin:
        A = line.rstrip().split()
        for col in args.gene_cols:
            gene = A[col-1]
            depth = burden[gene] if gene in burden else 0
            A.append(str(depth))
        print('\t'.join(A))

    
if __name__ == '__main__':
    main()
