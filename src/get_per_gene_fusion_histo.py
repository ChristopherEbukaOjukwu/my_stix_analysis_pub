import utils
import argparse
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file', type=str, required=True)
    parser.add_argument('--out_file', type=str, required=True)
    parser.add_argument('--width', type=float, default=6.0)
    parser.add_argument('--height', type=float, default=3.0)
    parser.add_argument('--bins', type=int, default=20)
    parser.add_argument('--min_depth', type=int, default=2)
    return parser.parse_args()

def main():
    args = get_args()

    fusions, genes = utils.get_fusions(args.in_file)

    num_fusion_genes = []
    per_fusion_depth = []
    for src_gene in fusions:
        num_fusion_genes.append(len(fusions[src_gene]))
        for dst_gene in fusions[src_gene]:
            per_fusion_depth.append(fusions[src_gene][dst_gene])


    min_depth_fusion_genes = []
    for src_gene in fusions:
        num_fusions = 0
        for dst_gene in fusions[src_gene]:
            if fusions[src_gene][dst_gene] >= args.min_depth:
                num_fusions += 1
        min_depth_fusion_genes.append(num_fusions)

    fig, axs = plt.subplots(3, 1, figsize=(args.width, args.height))

    axs[0].hist(num_fusion_genes, bins=args.bins)
    axs[0].set_xlabel('Num. of fusions per gene ($\mu=$' \
                     + str(round(np.mean(num_fusion_genes),1)) \
                     + ')')
    axs[0].set_ylabel('Freq.')
    axs[0].set_yscale('log')

    axs[1].hist(min_depth_fusion_genes, bins=args.bins)
    axs[1].set_xlabel('Num. of fusions with depth >= ' \
                      + str(args.min_depth) \
                      + ' ($\mu=$' \
                      + str(round(np.mean(min_depth_fusion_genes),1)) \
                      + ')')
    axs[1].set_ylabel('Freq.')
    axs[1].set_yscale('log')

    max_x = max([axs[0].get_xlim()[1], axs[1].get_xlim()[1]])
    min_x = min([axs[0].get_xlim()[0], axs[1].get_xlim()[0]])
    axs[0].set_xlim((min_x,max_x))
    axs[1].set_xlim((min_x,max_x))

    axs[2].hist(per_fusion_depth, bins=args.bins)
    axs[2].set_xlabel('Depth per fusion')
    axs[2].set_ylabel('Freq.')
    axs[2].set_yscale('log')

    for ax in axs:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(args.out_file, dpi=300)

if __name__ == '__main__':
    main()
