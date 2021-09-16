#!/usr/bin/env python

# Fix Gromacs gro file to have proper atom names and molecule names

import argparse

def get_n_molecules(top):

    f = open(top, 'r')

    for line in f:
        if line.startswith('system'):
            break

    nmol = []
    for line in f:
        nmol.append(int(line.split()[1]))

        if not line.startswith(tuple('0123456789')):
            break

    f.close()

    return nmol


def get_n_beads(top):

    f = open(top, 'r')

    nbeads = []
    for line in f:
        if line.startswith('mol '):
            nbeads.append(int(line.split()[1]))

    f.close()

    return nbeads

def get_beads(molecule_names,top):

    nmols = get_n_molecules(top)

    f = open(top, 'r')

    beads = {}
    for n in range(len(nmols)):

        for line in f:
            if line.startswith('mol '):
                molecule = molecule_names[n]
            if line.startswith('sitetypes'):
                break

        bead_list = []
        for line in f:
            if len(line.split()) == 1:
                bead_list.append(line.split()[0])
            else:
                break
        
        beads[molecule] = bead_list

    f.close()

    return beads


parser = argparse.ArgumentParser()
parser.add_argument('-g','--gro',
                    help='gro file to rename atoms')
parser.add_argument('-t','--top',default='cg.top',
                    help='CGTOP file for the MSCG system')
parser.add_argument('-m','--molecules',nargs='+',
                    help='sequence of molecule names to place in gro file')
parser.add_argument('-o','--output',default='output.gro',
                    help='output gro filename')
args = parser.parse_args()

nmols = get_n_molecules(args.top)
natoms = get_n_beads(args.top)
beads = get_beads(args.molecules,args.top)

f = open(args.gro, 'r')
header = f.readline()
n_tot = f.readline()

out = open(args.output, 'w')
out.write(header)
out.write(n_tot)

mol = 0
atom = 0
count = 0
for line in f:
    
    if len(line.split()) != 3:

        l = line.split()
        molecule_number = int(l[0].strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        number = int(l[2])
        x = float(l[3])
        y = float(l[4])
        z = float(l[5])

        molecule = args.molecules[mol]
        atom_name = beads[molecule][atom]

        new_line = "%5d%-5s%5s%5d%8.3f%8.3f%8.3f\n" %(molecule_number, molecule, atom_name, number, x, y, z)
        out.write(new_line)

        count += 1

        if count == nmols[mol] * natoms[mol]:
            mol += 1
            atom = 0
        elif atom == natoms[mol] - 1:
            atom = 0
        else:
            atom += 1

    else:
        out.write(line)

f.close()