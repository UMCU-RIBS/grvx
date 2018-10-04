#!/usr/bin/env python3
"""
Run one or all functions of GRVX analysis
"""
from argparse import ArgumentParser

from grvx.core.constants import PROJECT
from grvx.read_bids import Read_As_Bids
from grvx.nipype.workflow import create_grvx_workflow
from grvx.plotting import Plot_Results


parser = ArgumentParser(prog=PROJECT,
                        description=PROJECT.upper() + ' analysis')
parser.add_argument('--all', action='store_true',
                    help='read and run analysis')
parser.add_argument('-r', '--read', action='store_true',
                    help='read data into BIDS format')
parser.add_argument('-a', '--analysis', action='store_true',
                    help='run analysis (and plot)')
parser.add_argument('-p', '--plot', action='store_true',
                    help='plot results')

args = parser.parse_args()


if __name__ == '__main__':

    if args.all or args.read:
        Read_As_Bids()

    if args.all or args.analysis:
        w = create_grvx_workflow()
        w.run('MultiProc')

    if args.all or args.analysis or args.plot:
        Plot_Results()
