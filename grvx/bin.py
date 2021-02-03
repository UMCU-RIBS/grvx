from argparse import ArgumentParser
from pathlib import Path
from json import load
from os import environ
from shutil import rmtree

from .nipype.workflow import create_grvx_workflow
from .viz import plot_results


def command():
    parser = ArgumentParser(
        prog='grvx',
        description='analysis')
    parser.add_argument(
        'parameters',
        help='point to parameters.json')
    parser.add_argument(
        '-n', '--nipype',
        action='store_true',
        help='prepare nipype workflow')
    parser.add_argument(
        '-a', '--analysis',
        action='store_true',
        help='run nipype workflow')
    parser.add_argument(
        '-p', '--plot',
        action='store_true',
        help='plot results')
    parser.add_argument(
        '--all',
        action='store_true',
        help='prepare, run analysis and plot results')
    parser.add_argument(
        '--reset',
        action='store_true',
        help='delete the whole output directory')

    args = parser.parse_args()

    parameters_path = Path(args.parameters).resolve()
    with parameters_path.open() as f:
        parameters = load(f)

    if parameters['paths']['freesurfer_subjects_dir'] is None:
        parameters['paths']['freesurfer_subjects_dir'] = Path(environ['SUBJECTS_DIR'])

    for k in parameters['paths']:
        parameters['paths'][k] = Path(parameters['paths'][k]).resolve()

    if args.reset:
        rmtree(parameters['paths']['output'], ignore_errors=True)

    if args.all or args.nipype or args.analysis:
        w = create_grvx_workflow(parameters)

    if args.all or args.analysis:
        w.run('MultiProc')

    if args.all or args.plot:
        plot_results(parameters)
