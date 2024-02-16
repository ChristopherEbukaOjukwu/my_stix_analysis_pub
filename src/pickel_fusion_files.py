import utils
import argparse
import pickle

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file', type=str, required=True)
    parser.add_argument('--out_file', type=str, required=True)
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

    fusion_file, g = utils.get_fusions(args.in_file)

    with open(args.out_file, 'wb') as file:
        pickle.dump(fusion_file, file)
    
if __name__ == '__main__':
    main()
