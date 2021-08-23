#!/usr/bin/env python

# Fix Gromacs gro file to have proper atom names

import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-g','--gro',
                    help='gro file to rename atoms')
parser.add_argument('-o','--output',default='output.gro',
                    help='output gro filename')
args = parser.parse_args()

f = open(args.gro,'r')
header = f.readline()
n_total = f.readline()

out = open(args.output, 'w')
out.write(header)
out.write(n_total)

atom_types = {}
mol_num = []
for line in f:

    if len(line.split()) != 3: # if not the last line

        l = line.split()
        molecule_number = int(l[0].strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        molecule_name = str(l[0].strip('0123456789'))
        atom_name = str(l[1].strip('0123456789'))
        number = int(l[2])
        x = float(l[3])
        y = float(l[4])
        z = float(l[5])

        if not atom_name in atom_types or molecule_number not in mol_num:
            atom_types[atom_name] = 0
            atom_number = ''
        else:
            atom_types[atom_name] += 1
            atom_number = atom_types[atom_name]

        atom = atom_name + str(atom_number)
        mol_num.append(molecule_number)

        new_line = "%5d%-5s%5s%5d%8.3f%8.3f%8.3f\n" %(molecule_number,molecule_name,atom,number, x, y, z)        
        out.write(new_line)


    else: # if box vector line
        out.write(line)
