#!/bin/bash

usage() {
    echo "Usage: $0 [-h] -g GENE -f GENE_FILE -s STIX_RESULT"
}

while getopts ":hg:f:s:" option; do
    case "${option}" in
        h) usage
           exit;;
        g) gene=${OPTARG};;
        f) gene_file=${OPTARG};;
        s) stix_result=${OPTARG};;
        o) out_file=${OPTARG};;
    esac
done

bedtools intersect \
    -b ${stix_result} \
    -a ${gene_file} \
| grep -v -w ${gene} \
| cut -f 4 \
| sort \
| uniq -c
