import utils
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pickle

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp_file', type=str, required=True)
    parser.add_argument('--ctrl_file', type=str, required=True)
    #parser.add_argument('--gene_file', type=str, required=True)
    parser.add_argument('--max_ctrl_depth', type=int)
    parser.add_argument('--min_exp_depth', type=int)
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

    exp_fusions, g = utils.get_fusions(args.exp_file)
    ctrl_fusions, g = utils.get_fusions(args.ctrl_file)

#    exp_fusions = None
#    with open(args.exp_file, 'rb') as file:
#        exp_fusions = pickle.load(file)
#
#    ctrl_fusions = None
#    with open(args.ctrl_file, 'rb') as file:
#        ctrl_fusions = pickle.load(file)

    for exp_src in exp_fusions:
        for exp_dst in exp_fusions[exp_src]:
            ctrl_depth = 0
            exp_depth = exp_fusions[exp_src][exp_dst]
            if exp_src in ctrl_fusions and exp_dst in ctrl_fusions[exp_src]:
                ctrl_depth = ctrl_fusions[exp_src][exp_dst]

#            if args.max_ctrl_depth is not None \
#                    and ctrl_depth >= args.max_ctrl_depth:
#                continue
#
#            if args.min_exp_depth is not None \
#                    and exp_depth <= args.min_exp_depth:
#                continue

                print('\t'.join([exp_src,
                                 exp_dst,
                                 str(ctrl_depth),
                                 str(exp_depth)]))
    
if __name__ == '__main__':
    main()
