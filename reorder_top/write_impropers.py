#!/usr/bin/env python

import argparse
from get_number_map import get_numbers

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',
                    help='file to rename atoms')
parser.add_argument('-p','--pdb',
                    help='pdb file to get original atom numbering from')
parser.add_argument('-o','--output',default='output.itp',
                    help='output filename')
args = parser.parse_args()

mapping = get_numbers(args.pdb)

f = open(args.file,'r')
out = open(args.output, 'w')

# Copy all lines before angles
for line in f:
    if line.startswith('[ dihedrals ] ; im'):
        out.write(line)
        break
    else:
        out.write(line)

for line in f:
    
    if line.startswith('[ ') or len(line.split()) == 0:
        out.write(line)
        break
    elif not line.startswith(';'):
        old_i = line.split()[0]
        old_j = line.split()[1]
        old_k = line.split()[2]
        old_l = line.split()[3]
        func = line.split()[4]

        new_i = mapping[old_i]
        new_j = mapping[old_j]
        new_k = mapping[old_k]
        new_l = mapping[old_l]

        new_line = "\t%s\t%s\t%s\t%s\t%s\n" %(new_i,new_j,new_k,new_l,func)
        out.write(new_line)
    else:
        out.write(line)

for line in f:
    out.write(line)