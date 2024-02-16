import utils
import argparse
import numpy as np
import matplotlib.pyplot as plt

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp_file', type=str, required=True)
    parser.add_argument('--ctrl_file', type=str, required=True)
    parser.add_argument('--out_file', type=str, required=True)
    parser.add_argument('--max_depth', type=int, default=1)
    return parser.parse_args()

def main():
    args = get_args()

    exp_fusions = utils.get_fusions(args.exp_file)
    ctrl_fusions = utils.get_fusions(args.ctrl_file)

    normed_fusions = {}

    for exp_src_gene in exp_fusions: 
        for exp_dst_gene in exp_fusions[exp_src_gene]:
            if exp_src_gene not in ctrl_fusions \
                    or exp_dst_gene not in ctrl_fusions[exp_src_gene]:
                utils.add_fusion(normed_fusions,
                                 exp_src_gene,
                                 exp_dst_gene,
                                 exp_fusions[exp_src_gene][exp_dst_gene])
            elif ctrl_fusions[exp_src_gene][exp_dst_gene] <= args.max_depth:
                utils.add_fusion(normed_fusions,
                                 exp_src_gene,
                                 exp_dst_gene,
                                 exp_fusions[exp_src_gene][exp_dst_gene])

    with open(args.out_file, 'w') as f:
        for src_gene in normed_fusions:
            out = [src_gene]
            for dst_gene in normed_fusions[src_gene]:
                out.append(f'{dst_gene}:{normed_fusions[src_gene][dst_gene]}')
            f.write('\t'.join(out) + '\n')

if __name__ == '__main__':
    main()
