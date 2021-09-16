#!/usr/bin/env python

# Convert LAMMPS tabulated potentials to Gromacs format

import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-t','--table',
                    help='table of LAMMPS potentials to convert to Gromacs')
parser.add_argument('-o','--output',default='table_a0.xvg',
                    help='Gromacs output file with tabulated interaction')
args = parser.parse_args()

# Load in the LAMMPS data
# Contains 4 columns:       id  r           potential   force
# Units:                    #   Angstroms   Kcal/mol    Kcal/mol/Angstrom
lammps = np.loadtxt(args.table, skiprows=5)
r = lammps[:,1]
potential = lammps[:,2]
force = lammps[:,3]

# Convert tables to Gromacs format
# File should contain 3 columns:    r   f   -f'
# where f come from V(r)
#                               V(r) = k * f(r)
# 
# To properly convert:
#   k = 1 for all beads in topology

# Add in a buffer near zero where all potential and forces are 0
dr = r[1] - r[0]
r_buff = np.arange(0,r[0],dr) # depends on even/odd number in arange (no -dr for 0.002 step and 0.5)
buff = r_buff.shape[0]

# Units for Gromacs
# r [=] degrees
# potential [=] kJ/mol
# force [=] kJ/mol/degrees

gromacs = np.zeros([lammps.shape[0]+buff,3])
gromacs[:buff,0] = r_buff
gromacs[buff:,0] = r
gromacs[buff:,1] = potential * 4.184
gromacs[buff:,2] = force * 4.184

# Write the data to a text file
header = '# Converted LAMMPS ' + args.table + ' to Gromacs tabulated interaction\n'
header += "# r\t f(r)\t -f'(r)\n"

out = open(args.output, 'w')
out.write(header)
for line in gromacs:
    new_line = "%12.10e %12.10e %12.10e\n" %(line[0],line[1],line[2])
    out.write(new_line)
