#!/usr/bin/env python3
"""
Run one or all functions of GRVX analysis and make a log as html or pdf.
"""
from argparse import ArgumentParser
from pathlib import Path

import grvx

from grvx.core.constants import ALL_FUNC, PROJECT
from grvx.core.log import run_pandoc

BASE_PATH = Path(__file__).resolve().parent


parser = ArgumentParser(prog=PROJECT,
                        description=PROJECT.upper() + ' analysis')
parser.add_argument('--all', action='store_true',
                    help='run ALL the analysis steps')
parser.add_argument('--to', default='html',
                    help='format to export to: html (default), pdf')
parser.add_argument('--pandoc', action='store_true',
                    help='no analysis, only run pandoc')


for abbr, func_name in ALL_FUNC.items():
    parser.add_argument(abbr, help=func_name.replace('_', ' '),
                        action='store_true')
args = parser.parse_args()


if __name__ == '__main__':

    for abbr, func_name in ALL_FUNC.items():
        if args.all or getattr(args, abbr[1:]):
            eval('grvx.' + func_name + '()')

    run_pandoc(args.to)
