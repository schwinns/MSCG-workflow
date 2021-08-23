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

# Copy all lines before pairs
for line in f:
    if line.startswith('[ pairs ]'):
        out.write(line)
        break
    else:
        out.write(line)

for line in f:
    
    if line.startswith('[ ') or len(line.split()) == 0:
        out.write(line)
        break
    elif not line.startswith(';'):

        old_ai = line.split()[0]
        old_aj = line.split()[1]
        func = line.split()[2]

        new_ai = mapping[old_ai]
        new_aj = mapping[old_aj]

        new_line = "\t%s\t%s\t%s\n" %(new_ai,new_aj,func)        
        out.write(new_line)
    
    else:
        out.write(line)

for line in f:
    out.write(line)