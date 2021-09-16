#!/usr/bin/env python

# Convert LAMMPS tabulated potentials to Gromacs format

import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-t','--table',
                    help='table of LAMMPS potentials to convert to Gromacs')
parser.add_argument('-o','--output',default='table.xvg',
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
# File should contain 7 columns:    r   f   -f'   g   -g'   h   -h'
# where f, g, h come from V(r)
#                               V(r) = q_i*q_j / (4 pi eps0) * f  +  C * g  +  A * h
# 
# To properly convert:
#   A = 0 for all beads in topology (therefore h does not matter)
#   h,h' = 0 to be sure h does not contribute
#   f,f' = 0 for all r (removing Coulombic term because this should be captured by MSCG)
#   C = 1 for all beads in topology (therefore only the MSCG potential matters)
#   g = potential from LAMMPS format
#   -g' = force from LAMMPS format

# Add in a buffer near zero where all potential and forces are 0
dr = r[1] - r[0]
r_buff = np.arange(0,r[0],dr)
buff = r_buff.shape[0]

# Units for Gromacs
# r [=] nm
# potential [=] kJ/mol
# force [=] kJ/mol/nm

gromacs = np.zeros([lammps.shape[0]+buff,7])
gromacs[:buff,0] = r_buff / 10
gromacs[buff:,0] = r / 10
gromacs[buff:,3] = potential * 4.184
gromacs[buff:,4] = force * 4.184 / 10

# Write the data to a text file
header = 'Converted LAMMPS ' + args.table + ' to Gromacs tabulated interaction\n'
header += "r\t f(r)\t -f'(r)\t g(r)\t -g'(r)\t h(r)\t -h'(r)\n"

out = open(args.output, 'w')
out.write(header)
for line in gromacs:
    new_line = "%12.10e   %12.10e %12.10e   %12.10e %12.10e   %12.10e %12.10e\n" %(line[0],line[1],line[2],line[3],line[4],line[5],line[6])
    out.write(new_line)

