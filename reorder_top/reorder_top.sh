#!/bin/bash

# Manually reordered pdb is argument 1
# itp file with manually reordered atoms directive is argument 2
# Name of output file is argument 3

pdb=$1
itp=$2
out=$3

source /usr/local/gromacs/bin/GMXRC

python reorder_atoms.py -f $itp -o atoms.itp
# should make a write_bonds.py
python write_pairs.py -f atoms.itp -p $pdb -o pairs.itp
python write_angles.py -f pairs.itp -p $pdb -o angles.itp
python write_propers.py -f angles.itp -p $pdb -o propers.itp
python write_impropers.py -f propers.itp -p $pdb -o $out.itp

rm atoms.itp pairs.itp angles.itp propers.itp

