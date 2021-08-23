#!/bin/bash

# Manually reordered pdb is argument 1
# itp file with manually reordered atoms directive is argument 2
# Name of output file is argument 3

pdb=$1
itp=$2
out=$3

source /usr/local/gromacs/bin/GMXRC

python reorder_atoms.py -f $itp -o atoms.itp
python write_bonds.py -f atoms.itp -p $pdb -o bonds.itp --GLY 1
python write_pairs.py -f bonds.itp -p $pdb -o pairs.itp
python write_angles.py -f pairs.itp -p $pdb -o angles.itp --GLY 1
python write_propers.py -f angles.itp -p $pdb -o $out.itp --GLY 1

rm atoms.itp bonds.itp pairs.itp angles.itp

