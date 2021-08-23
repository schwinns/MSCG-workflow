#!/usr/bin/env python

import argparse
from get_number_map import get_numbers

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',
                    help='file to rename atoms')
parser.add_argument('-p','--pdb',
                    help='pdb file to get original atom numbering from')
parser.add_argument('--GLY',default=0,
                    help='include this flag if reordering a GLY topology')
parser.add_argument('-o','--output',default='output.itp',
                    help='output filename')
args = parser.parse_args()

mapping = get_numbers(args.pdb)

f = open(args.file,'r')
out = open(args.output, 'w')

# Copy all lines before angles
for line in f:
    if line.startswith('[ dihedrals ]'):
        out.write(line)
        break
    else:
        out.write(line)

for line in f:
    
    if line.startswith('[ ') or len(line.split()) == 0:
        out.write(line)
        break
    elif not line.startswith(';'):

        l = line.split()

        if args.GLY:
            old_i = l[0]
            old_j = l[1]
            old_k = l[2]
            old_l = l[3]
            func = l[4]
            C0 = l[5]
            C1 = l[6]
            C2 = l[7]
            C3 = l[8]
            C4 = l[9]
            C5 = l[10]

            new_i = mapping[old_i]
            new_j = mapping[old_j]
            new_k = mapping[old_k]
            new_l = mapping[old_l]

            new_line = "\t%s\t%s\t%s\t%s\t%s\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\n" %(new_i,new_j,new_k,new_l,func,C0,C1,C2,C3,C4,C5)


        else:
            old_i = l[0]
            old_j = l[1]
            old_k = l[2]
            old_l = l[3]
            func = l[4]

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