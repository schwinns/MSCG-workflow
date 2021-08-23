#!/usr/bin/env python

def get_numbers(pdb):
    f = open(pdb,'r')

    mapping = {}
    atom_types = {}
    mol_num = []
    number = 1
    for line in f:

        if line.startswith('ATOM'):
            l = line.split()
            molecule_number = l[4]
            atom_name = str(l[2].strip('0123456789'))
            old_number = l[1]
        
            if not atom_name in atom_types or molecule_number not in mol_num:
                atom_types[atom_name] = 0
                atom_number = ''
            else:
                atom_types[atom_name] += 1
                atom_number = atom_types[atom_name]

            mol_num.append(molecule_number)

            mapping[old_number] = number
            number += 1

    f.close()

    return mapping