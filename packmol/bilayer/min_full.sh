#!/bin/bash

source /usr/local/gromacs/bin/GMXRC

gmx editconf -f bilayer_gly.pdb -o bilayer_gly.gro -box 6 6 10
gmx grompp -f min_full.mdp -o min_full.tpr -c bilayer_gly.gro -p reordered_full.top
gmx mdrun -deffnm min_full