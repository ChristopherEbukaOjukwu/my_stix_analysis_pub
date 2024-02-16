import utils
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file', type=str, required=True)
    parser.add_argument('--out_file', type=str, required=True)
    parser.add_argument('--min_depth', type=int, default=1)
    parser.add_argument('--max_depth', type=int, default=1000000)
    parser.add_argument('--width', type=float, default=6.0)
    parser.add_argument('--height', type=float, default=6.0)
    return parser.parse_args()

def main():
    args = get_args()

    fusions, genes = utils.get_fusions(args.in_file,
                                      min_depth=args.min_depth,
                                      max_depth=args.max_depth)

    gene_loc = {gene: index for index, gene in enumerate(genes)}

    data = np.full((len(genes), len(genes)), np.nan)

    for src_gene in genes:
        if src_gene not in fusions: continue
        for dst_gene in fusions[src_gene]:
            data[gene_loc[src_gene], gene_loc[dst_gene]] = \
                    fusions[src_gene][dst_gene]

    fig, ax = plt.subplots(figsize=(args.width, args.height))

    norm = mcolors.LogNorm(vmin=np.nanmin(data),
                           vmax=np.nanmax(data))

    cmap = plt.cm.winter.copy()
    cmap.set_bad(color='white')

    cax = ax.imshow(data, cmap='winter', norm=norm, interpolation='nearest')
    #cax = ax.imshow(data, cmap='hot', interpolation='nearest')
    #cax = ax.spy(data)
    fig.colorbar(cax)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(args.out_file, dpi=300)
#


if __name__ == '__main__':
    main()
