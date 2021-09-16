#!/usr/bin/env python

# Convert LAMMPS topology data file to a Gromacs gro file

import argparse
import MDAnalysis as mda

parser = argparse.ArgumentParser()
parser.add_argument('-l','--lammps',
                    help='lammps topology .data file to convert to gro')         
parser.add_argument('-o','--output',default='output.gro',
                    help='output gro filename')
args = parser.parse_args()

u = mda.Universe(args.lammps)
u.atoms.write(args.output)