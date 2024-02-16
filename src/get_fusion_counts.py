import utils
import argparse
import numpy as np
import matplotlib.pyplot as plt

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp_files', nargs='+', type=str, required=True)
    parser.add_argument('--fusion_file', type=str, required=True)
    return parser.parse_args()

def get_fusion_list(file):
    fusion_list = []

    with open(file) as lines:
        for line in lines:
            A = line.rstrip().split()
            fusion_list.append(A)
    return fusion_list

def main():
    args = get_args()

    exp_fusions = []
    for exp_file in args.exp_files:
        f, g = utils.get_fusions(exp_file)
        exp_fusions.append(f)

    fusion_list = get_fusion_list(args.fusion_file)

    for src, dst, tissue, count  in fusion_list:
        output = [src, dst, tissue, count]
        for exp_fusion in exp_fusions:
            exp_depth = 0
            if src in exp_fusion and dst in exp_fusion[src]:
                exp_depth = exp_fusion[src][dst]
            output.append(str(exp_depth))

        print('\t'.join(output))


if __name__ == '__main__':
    main()
