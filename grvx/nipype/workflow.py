from shutil import rmtree
from nipype import Workflow, Node, MapNode, config, logging, JoinNode
from nipype.interfaces.fsl import FEAT, BET, FLIRT, Threshold
from nipype.interfaces.freesurfer import ReconAll
from numpy import arange

from ..nodes.ieeg import (
    function_ieeg_read,
    function_ieeg_preprocess,
    function_ieeg_powerspectrum,
    function_ieeg_compare,
    )
from ..nodes.fsl import function_prepare_design
from ..nodes.fmri import (
    function_fmri_compare,
    function_fmri_atelec,
    function_fmri_graymatter,
    )
from ..nodes.corr import function_corr, function_corr_summary

from .bids import bids_node

UPSAMPLE_RESOLUTION = 1
DOWNSAMPLE_RESOLUTION = 4
GRAYMATTER_THRESHOLD = 0.2

# this cannot be in a function, otherwise nipype ignores it
config.update_config({
    'execution': {
        'keep_inputs': 'false',
        'remove_unnecessary_outputs': 'false',
        'crashfile_format': 'text',
        },
    })


def workflow_ieeg(parameters):
    node_read = Node(function_ieeg_read, name='read')
    node_read.inputs.active_conditions = parameters['ieeg']['read']['active_conditions']
    node_read.inputs.baseline_conditions = parameters['ieeg']['read']['baseline_conditions']
    node_read.inputs.minimalduration = parameters['ieeg']['read']['minimalduration']

    node_preprocess = MapNode(function_ieeg_preprocess, name='preprocess', iterfield=['ieeg', ])
    node_preprocess.inputs.duration = parameters['ieeg']['preprocess']['duration']
    node_preprocess.inputs.reref = parameters['ieeg']['preprocess']['reref']
    node_preprocess.inputs.offset = parameters['ieeg']['preprocess']['offset']

    node_frequency = MapNode(function_ieeg_powerspectrum, name='powerspectrum', iterfield=['ieeg', ])
    node_frequency.inputs.method = parameters['ieeg']['powerspectrum']['method']
    node_frequency.inputs.taper = parameters['ieeg']['powerspectrum']['taper']
    node_frequency.inputs.duration = parameters['ieeg']['powerspectrum']['duration']

    node_compare = Node(function_ieeg_compare, name='ecog_compare')
    node_compare.inputs.frequency = parameters['ieeg']['ecog_compare']['frequency']
    node_compare.inputs.baseline = parameters['ieeg']['ecog_compare']['baseline']
    node_compare.inputs.method = parameters['ieeg']['ecog_compare']['method']
    node_compare.inputs.measure = parameters['ieeg']['ecog_compare']['measure']

    w = Workflow('ieeg')

    w.connect(node_read, 'ieeg', node_preprocess, 'ieeg')
    w.connect(node_preprocess, 'ieeg', node_frequency, 'ieeg')
    w.connect(node_frequency, 'ieeg', node_compare, 'in_files')

    return w


def workflow_fmri(parameters):
    node_bet = Node(BET(), name='bet')
    node_bet.inputs.frac = 0.5
    node_bet.inputs.vertical_gradient = 0
    node_bet.inputs.robust = True

    node_featdesign = Node(function_prepare_design, name='feat_design')
    node_featdesign.inputs.active_conditions = parameters['fmri']['read']['active_conditions']

    node_feat = Node(FEAT(), name='feat')

    node_compare = Node(function_fmri_compare, name='fmri_compare')
    node_compare.inputs.measure = parameters['fmri']['fmri_compare']['measure']
    node_compare.inputs.normalize_to_mean = parameters['fmri']['fmri_compare']['normalize_to_mean']

    node_upsample = Node(FLIRT(), name='upsample')  # not perfect, there is a small offset
    node_upsample.inputs.apply_isoxfm = UPSAMPLE_RESOLUTION
    node_upsample.inputs.interp = 'nearestneighbour'

    node_downsample = Node(FLIRT(), name='downsample')  # not perfect, there is a small offset
    node_downsample.inputs.apply_xfm = True
    node_downsample.inputs.uses_qform = True
    # node_downsample.inputs.apply_isoxfm = DOWNSAMPLE_RESOLUTION
    node_downsample.inputs.interp = 'nearestneighbour'

    node_threshold = Node(Threshold(), name='threshold')
    node_threshold.inputs.thresh = GRAYMATTER_THRESHOLD
    node_threshold.inputs.args = '-bin'

    node_graymatter = Node(function_fmri_graymatter, name='graymatter')

    node_realign_gm = Node(FLIRT(), name='realign_gm')
    node_realign_gm.inputs.apply_xfm = True
    node_realign_gm.inputs.uses_qform = True

    kernel_sizes = arange(
        parameters['fmri']['at_elec']['kernel_start'],
        parameters['fmri']['at_elec']['kernel_end'],
        parameters['fmri']['at_elec']['kernel_step'],
        )
    node_atelec = Node(function_fmri_atelec, name='at_elec')
    node_atelec.inputs.distance = parameters['fmri']['at_elec']['distance']
    node_atelec.inputs.kernel_sizes = list(kernel_sizes)
    node_atelec.inputs.graymatter = parameters['fmri']['graymatter']

    w = Workflow('fmri')
    w.connect(node_bet, 'out_file', node_featdesign, 'anat')

    w.connect(node_featdesign, 'fsf_file', node_feat, 'fsf_file')
    w.connect(node_feat, 'feat_dir', node_compare, 'feat_path')

    if parameters['fmri']['upsample']:
        w.connect(node_compare, 'out_file', node_upsample, 'in_file')
        w.connect(node_compare, 'out_file', node_upsample, 'reference')
        w.connect(node_upsample, 'out_file', node_atelec, 'in_file')
    else:
        w.connect(node_compare, 'out_file', node_atelec, 'in_file')

    if parameters['fmri']['graymatter']:

        if parameters['fmri']['upsample']:
            w.connect(node_graymatter, 'out_file', node_realign_gm, 'in_file')
            w.connect(node_upsample, 'out_file', node_realign_gm, 'reference')
            w.connect(node_realign_gm, 'out_file', node_threshold, 'in_file')
        else:
            w.connect(node_graymatter, 'out_file', node_downsample, 'in_file')
            w.connect(node_compare, 'out_file', node_downsample, 'reference')
            w.connect(node_downsample, 'out_file', node_threshold, 'in_file')

        w.connect(node_threshold, 'out_file', node_atelec, 'graymatter')

    return w


def create_grvx_workflow(parameters):

    bids = bids_node(parameters)

    node_reconall = Node(ReconAll(), name='freesurfer')
    node_reconall.inputs.subjects_dir = str(parameters['paths']['freesurfer_subjects_dir'])
    node_reconall.inputs.flags = ['-cw256', ]

    node_corr = Node(function_corr, name='corr_fmri_ecog')
    node_corr.inputs.pvalue = parameters['corr']['pvalue']

    node_corr_summary = JoinNode(
        function_corr_summary,
        name='corr_fmri_ecog_summary',
        joinsource='bids',
        joinfield=('in_files', 'ecog_files', 'fmri_files'),
        )

    w_fmri = workflow_fmri(parameters)
    w_ieeg = workflow_ieeg(parameters)

    w = Workflow('workflow')
    w.base_dir = str(parameters['paths']['output'])

    if parameters['fmri']['graymatter']:
        w.connect(bids, 'subject', node_reconall, 'subject_id')  # we might use freesurfer for other stuff too
        w.connect(bids, 'anat', node_reconall, 'T1_files')
        w.connect(node_reconall, 'ribbon', w_fmri, 'graymatter.ribbon')

    w.connect(bids, 'ieeg', w_ieeg, 'read.ieeg')
    w.connect(bids, 'elec', w_ieeg, 'read.electrodes')

    w.connect(bids, 'anat', w_fmri, 'bet.in_file')
    w.connect(bids, 'func', w_fmri, 'feat_design.func')

    w.connect(bids, 'elec', w_fmri, 'at_elec.electrodes')

    w.connect(w_ieeg, 'ecog_compare.tsv_compare', node_corr, 'ecog_file')
    w.connect(w_fmri, 'at_elec.fmri_vals', node_corr, 'fmri_file')

    w.connect(node_corr, 'out_file', node_corr_summary, 'in_files')
    w.connect(w_ieeg, 'ecog_compare.tsv_compare', node_corr_summary, 'ecog_files')
    w.connect(w_fmri, 'at_elec.fmri_vals', node_corr_summary, 'fmri_files')

    w.write_graph(graph2use='flat')
    log_dir = parameters['paths']['output'] / 'log'

    config.update_config({
        'logging': {
            'log_directory': log_dir,
            'log_to_file': True,
            },
        })

    rmtree(log_dir, ignore_errors=True)
    log_dir.mkdir()
    logging.update_logging(config)

    return w
