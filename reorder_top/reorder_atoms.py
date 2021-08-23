#!/usr/bin/env python

# Fix topology file to have proper atom names in atoms directory

import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',
                    help='file to rename atoms')
parser.add_argument('-o','--output',default='output.itp',
                    help='output filename')
args = parser.parse_args()

f = open(args.file,'r')
header = []
for line in f:
    header.append(line)
    if len(line.split()) != 0 and line.split()[0] == '[':
        break

out = open(args.output, 'w')
for head in header:
    out.write(head)

atom_names = {}
atoms = False
number = 0
for line in f:

    if len(line.split()) != 0 and line.split()[0] == '[' and line.split()[1] == 'atoms':
        atoms = True
        out.write(line)
    elif len(line.split()) != 0 and line.split()[0] == '[' and line.split()[1] == 'bonds':
        atoms = False
        out.write(line)
    elif len(line.split()) != 0 and atoms and not line.startswith(';'): # atoms directory

        l = line.split()
        number += 1
        atom_type = l[1]
        resid_number = l[2]
        resid_name = l[3]
        atom_name = str(l[4].strip('0123456789'))
        charge = l[6]
        mass = l[7]

        if not atom_name in atom_names:
            atom_names[atom_name] = 0
            atom_number = ''
        else:
            atom_names[atom_name] += 1
            atom_number = atom_names[atom_name]

        atom = atom_name + str(atom_number)

        new_line = "%d\t%s\t%s\t%s\t%s\t%d\t%s\t%s\n" %(number,atom_type,resid_number,resid_name,atom,number,charge,mass)        
        out.write(new_line)
    else:
        out.write(line)