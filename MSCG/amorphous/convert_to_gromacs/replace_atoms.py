#!/usr/bin/env python

# Fix Gromacs gro file to have proper atom names and molecule names

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-g','--gro',
                    help='gro file to rename atoms')
parser.add_argument('-a','--atoms',nargs='+',
                    help='sequence of atom names to place in gro file')
parser.add_argument('-m','--molecules',nargs='+',
                    help='sequence of molecule names to place in gro file')
parser.add_argument('-n','--natoms',nargs='+',
                    help='number of atoms in each molecule defined in --molecules')            
parser.add_argument('-o','--output',default='output.gro',
                    help='output gro filename')
args = parser.parse_args()

tot = 0
for n in args.natoms:
    tot += int(n)

if len(args.atoms) != tot:
    raise KeyError('Number of atoms and atoms in molecules are not equal')

start = 0
m = []
for i,mol in enumerate(args.molecules):
    m.append(args.atoms[start:start+int(args.natoms[i])])
    start = int(args.natoms[i])
    

f = open(args.gro,'r')
header = f.readline()
n_total = f.readline().split()[0]

out = open(args.output, 'w')
out.write(header)
out.write(n_total + '\n')

a = 0
i = 0
for line in f:

    if len(line.split()) != 3: # if not the last line

        l = line.split()
        atom_number = int(l[0].strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        number = int(l[2])
        x = float(l[3])
        y = float(l[4])
        z = float(l[5])

        new_line = "%5d%-5s%5s%5d%8.3f%8.3f%8.3f\n" %(atom_number, args.molecules[i], m[i][a], number, x, y, z)        
        if a == len(m[i]) - 1:
            a = 0
            if i == len(args.molecules) - 1:
                i = 0
            else:
                i += 1
        else:
            a += 1 
    
        out.write(new_line)
    else: # if box vector line
        out.write(line)

