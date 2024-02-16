

def add_fusion(fusions, src, dst, depth):
    src, dst = sorted([src, dst])

    if src not in fusions:
        fusions[src] = {}
    fusions[src][dst] = depth


def get_fusions(in_file, min_depth=1, max_depth=1000000):
    fusions = {}
    genes = []

    with open(in_file) as lines:
        for line in lines:
            A = line.rstrip().split()
            src_gene = A[0]
            added = False


            for dst_gene, depth in [a.split(':') for a in A[1:]]:
                if dst_gene == src_gene: continue
                depth = int(depth)
                if depth >= min_depth and depth <= max_depth:
                    add_fusion(fusions, src_gene, dst_gene, int(depth))
                    genes.append(dst_gene)
                    added = True

            if added:
                genes.append(src_gene)

    return fusions, sorted(list(set(genes)))
