#!/usr/bin/env python

import argparse
import numpy as np
from mscg import *
from mscg.cli import cgmap
from mscg.cli import cgfm
from mscg.cli import cgdump

parser = argparse.ArgumentParser()
parser.add_argument('-m','--map',default='map.yaml',
                    help='yaml file with the AA to CG mapping')
parser.add_argument('-t','--top',default='cg.top',
                    help='CGTOP file detailing connectivity for MSCG')
parser.add_argument('-AA','--traj',default='traj.trr',
                    help='Input trajectory file with the AA simulation data')
parser.add_argument('-o','--output',default='CG.lammpstrj',
                    help='CG mapped file in LAMMPS format')
args = parser.parse_args()

top = Topology.read_file(args.top)

# Get all pair interactions from top file
pairs = []
for i in top.names_atom:
    for j in top.names_atom:
        if i != j:
            pairs.append(i + ':' + j)
print('Force-matching for %d nonbonded pair interactions' %(len(pairs)))

# Get all bond interactions
bonds = []
for i in top.names_bond:
    a1 = i.split('-')[0]
    a2 = i.split('-')[1]
    bonds.append(a1 + ':' + a2)
print('Force-matching for %d bond interactions' %(len(bonds)))

# Get all angle interactions
angles = []
for i in top.names_angle:
    a1 = i.split('-')[0]
    a2 = i.split('-')[1]
    a3 = i.split('-')[2]
    angles.append(a1 + ':' + a2 + ':' + a3)
print('Force-matching for %d angle interactions' %(len(angles)))

cgmap.main(map=args.map, traj=args.traj, out=args.output)
CG_traj = Trajectory(args.output,fmt='lammpstrj')

pair_list = ['model=BSpline,type=' + pair + ',min=3.0,max=15.0,resolution=0.2,order=6' for pair in pairs]
bond_list = ['model=BSpline,type=' + bond + ',min=2.5,max=3.8,resolution=0.05,order=3' for bond in bonds]
angle_list = ['model=BSpline,type=' + angle + ',min=1.48,max=2.96,resolution=0.2,order=3' for angle in angles]

# For now, only use standard ranges and cutoff for force-matching from tutorials
cgfm.main(
    top = args.top,
    traj = args.output,
    cut = 15.0,
    pair = pair_list,
    bond = bond_list,
    angle = angle_list
)

print('Finished force-matching! Saved to result.p')

p_table = []
for p in pairs:
    pair = p.split(':')
    p_table.append(pair[0] + '-' + pair[1])
dump_list = ['Pair_' + model + ',2.5,12.0,0.05' for model in p_table]
dump_list += ['Bond_' + model + ',2.0,5.0,0.05' for model in top.names_bond]
dump_list += ['Angle_' + model + ',1.5,3.0,0.05' for model in top.names_angle]

print('Dumping %d tables' %(len(dump_list)))

cgdump.main(
    file = 'result.p',
    dump = dump_list
)