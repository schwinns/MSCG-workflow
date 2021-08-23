#!/bin/bash

# Manually reordered pdb is argument 1
# Name of output files is argument 2

tmp=$1
out=$2

source /usr/local/gromacs/bin/GMXRC

gmx editconf -f $tmp -o tmp.gro
python rename_atoms.py -g tmp.gro -o $out.gro
gmx editconf -f $out.gro -o $out.pdb

