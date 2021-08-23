#!/bin/bash

# MUST DO SEPARATELY
#packmol < top.inp > top.log
#packmol < bott.inp > bott.log

# Output of packmol scripts should be top.pdb and bott.pdb

# Merge the two pdbs and organize according to the topology
grep -v BR top.pdb > noBR.pdb
grep -v END noBR.pdb > bilayer.pdb
rm noBR.pdb
grep -v BR bott.pdb >> bilayer.pdb
grep BR top.pdb >> bilayer.pdb
grep BR bott.pdb >>  bilayer.pdb
echo END >> bilayer.pdb

# Obtain the box sizes from user input for energy minimization
# echo -e "x box length (nm): "
# read x
# echo -e "y box length (nm): "
# read y
# echo -e "z box length (nm): "
# read z

# Generate box and perform energy minimization
# May need to change gromacs path
# Need to have min.mdp and topol.top correct and in current working directory
source /usr/local/gromacs/bin/GMXRC
gmx editconf -f bilayer.pdb -o bilayer.gro -box 6 6 10
gmx grompp -f min.mdp -o min.tpr -c bilayer.gro -p reordered.top
gmx mdrun -deffnm min

gmx editconf -f min.gro -o min.pdb
