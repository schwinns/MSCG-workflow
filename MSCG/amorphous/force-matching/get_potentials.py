#!/usr/bin/env python

import argparse
from mscg.cli import cgdump

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p','--pair',default=['I9A-I9A'],nargs='+',
                    help='pair potential to dump to a table')
parser.add_argument('-f','--file',default='result.p',
                    help='binary result file with pair potentials')
args = parser.parse_args()

# Create list of models to dump
dump_list = ['Pair_' + model + ',2.0,15.0,0.05' for model in args.pair]

# Dump models to tables
cgdump.main(
    file = args.file,
    dump = dump_list
)
