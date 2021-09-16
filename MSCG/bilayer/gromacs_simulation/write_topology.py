#!/usr/bin/env python

import argparse
#from mscg import Topology
import numpy as np
import yaml

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
parser.add_argument('-o','--output',default='topol.top',
                    help='name of the output .data file to save the topology')
args = parser.parse_args()

top = Topology.read_file(args.top)

out = open(args.output,'w')
header = '; Converted lammps CG system into Gromacs topology\n\n'
out.write(header)

# Write [ defaults ] directive
out.write('[ defaults ]\n')

defaults = {

    'nbfunc'    : 1,
    'comb-rule' : 1,
    'gen-pairs' : 'yes',
    'fudgeLJ'   : 0.5,
    'fudgeQQ'   : 0.8333,

}

line = '; '
l = []
for col in defaults:
    line += col + '\t\t'
    l.append(str(defaults[col]))
out.write(line + '\n')

line = ''
for param in l:
    line += param + '\t\t'
out.write(line + '\n\n')

# Write the [ atomtypes ] directive
out.write('[ atomtypes ]\n')

atomtypes = {

    'name'      : [],
    'bond_type' : [],
    'mass'      : [],
    'charge'    : '0',
    'ptype'     : 'A',
    'C'         : 1.0e00,
    'A'         : 0.0e00

}

for atom in top.names_atom:

    atomtypes['name'].append(atom)
    atomtypes['bond_type']