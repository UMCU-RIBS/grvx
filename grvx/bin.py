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
        '-f',
        action='store_true',
        help='prepare nipype workflow')
    list_functions = parser.add_subparsers(title='Functions')

    functions = {
        'all': list_functions.add_parser('all', help='all = analysis + plot'),
        'analysis': list_functions.add_parser('analysis', help='run nipype analysis but no plotting'),
        }
    functions['all'].set_defaults(analysis=True, plot=True)
    functions['analysis'].set_defaults(analysis=True, plot=False)

    for fct in functions.values():
        fct.add_argument(
            'parameters',
            help='point to parameters.json')
        fct.add_argument(
            '--dry_run',
            action='store_true',
            help='prepare nipype workflow, but do not run it yet')
        fct.add_argument(
            '--reset',
            action='store_true',
            help='delete the whole output directory')

    plt_arg = list_functions.add_parser('plot', help='plot only')
    plt_arg.set_defaults(analysis=False, plot=True, parameters=None)
    plt_arg.add_argument('output_folder', help='point to the output folder (it should contain a parameters.json and the "workflow" folder, and it will write in the "plot" folder)')

    args = parser.parse_args()

    if args.parameters is not None:  # all or analysis
        parameters_path = Path(args.parameters).resolve()
    else:  # only plot
        parameters_path = Path(args.output_folder).resolve() / 'parameters.json'

    with parameters_path.open() as f:
        parameters = load(f)
    for k in parameters['paths']:
        parameters['paths'][k] = Path(parameters['paths'][k]).resolve()

    if parameters['paths']['freesurfer_subjects_dir'] is None:
        parameters['paths']['freesurfer_subjects_dir'] = Path(environ['SUBJECTS_DIR'])

    if args.analysis:

        if args.reset:
            rmtree(parameters['paths']['output'], ignore_errors=True)

        w = create_grvx_workflow(parameters)

        if not args.dry_run:
            w.run('MultiProc')

    if args.plot:
        plot_results(parameters)
