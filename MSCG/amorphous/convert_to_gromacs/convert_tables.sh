#!/bin/bash

python tables_to_gromacs.py -t tables/Pair_C-C1.table -o table.xvg
python tables_to_gromacs.py -t tables/Pair_C-C.table -o table_C_C.xvg
python tables_to_gromacs.py -t tables/Pair_C-C2.table -o table_C_C2.xvg
python tables_to_gromacs.py -t tables/Pair_C1-C1.table -o table_C1_C1.xvg
python tables_to_gromacs.py -t tables/Pair_C1-C2.table -o table_C1_C2.xvg
python tables_to_gromacs.py -t tables/Pair_C2-C2.table -o table_C2_C2.xvg
