#!/usr/bin/env python

import argparse
from mscg import Topology, Trajectory
import numpy as np
import yaml

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


def get_masses(map,top):

    masses = []

    with open(map, 'r') as stream:
        mapping = yaml.safe_load(stream)
        
    for bead in top.names_atom:
        mass = 0
        wts = mapping['site-types'][bead]['x-weight']
        for w in wts:
            mass += float(w)
        masses.append(mass)

    return masses

parser = argparse.ArgumentParser()
parser.add_argument('-t','--top',default='cg.top',
                    help='CGTOP file detailing connectivity for MSCG')
parser.add_argument('-m','--map',default='map.yaml',
                    help='mapping file for the CG system -- used to find CG mass')
parser.add_argument('-CG','--traj',default='CG.lammpstrj',
                    help='CG mapped trajectory from force-match.py in LAMMPS format')
parser.add_argument('-o','--output',default='lammps',
                    help='name of the output .data file to save the topology')
args = parser.parse_args()

top = Topology.read_file(args.top)
top.system_name = args.output

nmol = get_n_molecules(args.top)
nbeads = get_n_beads(args.top)

molecule_ids = []
start = 1
end = nmol[0] + 1
for n,mol in enumerate(nmol):

    for i in range(start,end):
        molecule_ids += [i] * nbeads[n]

    start += mol
    if n < len(nmol) - 1:
        end += nmol[n+1]

masses = get_masses(args.map, top)
CG_traj = Trajectory(args.traj, fmt='lammpstrj')
CG_traj.read_frame()

top.save('lammps', masses=masses, molecule=molecule_ids,
          box=np.vstack([np.zeros(3),CG_traj.box]).T, x=CG_traj.x)

top_file = open(args.output + '.data', 'r')
add_charges = open(args.output + '_correct.data', 'w')

for line in top_file:
    if len(line.split())!= 0 and line.split()[0] == 'Atoms':
        add_charges.write(line)
        break
    else:
        add_charges.write(line)

line = top_file.readline()
add_charges.write(line)

for line in top_file:

    if len(line.split()) != 0:
    
        l = line.split()
        atom_id = l[0]
        mol_id = l[1]
        atom_type = l[2]
        x = l[3]
        y = l[4]
        z = l[5]

        charge = 0
        new_line = '%s %s %s %s %s %s %s\n' %(atom_id, mol_id, atom_type, charge, x, y, z)
        add_charges.write(new_line)

    else:
        add_charges.write(line)
        break

for line in top_file:
    add_charges.write(line)
