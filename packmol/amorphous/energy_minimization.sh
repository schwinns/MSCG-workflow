#!/bin/bash

grep -v BR amorphous.pdb > noBR.pdb
grep -v END noBR.pdb > amorphous_fixed.pdb
rm noBR.pdb
grep BR amorphous.pdb >> amorphous_fixed.pdb
echo END >> amorphous_fixed.pdb

source /usr/local/gromacs/bin/GMXRC

gmx editconf -f amorphous_fixed.pdb -o amorphous.gro -box 7 7 7
gmx grompp -f min.mdp -o min.tpr -c amorphous.gro -p topol.top
gmx mdrun -deffnm min