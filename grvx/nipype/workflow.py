from nipype import Workflow, Node, MapNode, config, logging
from nipype.interfaces.fsl import FEAT, BET
from nipype.interfaces.freesurfer import ReconAll

from boavus.ieeg import (function_ieeg_read,
                         function_ieeg_preprocess,
                         function_ieeg_powerspectrum,
                         function_ieeg_compare,
                         )

from boavus.fsl import (function_prepare_design,
                        )
from boavus.nipype import (function_fmri_compare,
                           function_fmri_atelec,
                           function_corr,
                           )

from .bids import bids, SUBJECTS
from ..core.constants import NIPYPE_PATH, FREESURFER_PATH, ANALYSIS_PATH, OUTPUT_PATH


config.update_config({
    'logging': {
        'log_directory': NIPYPE_PATH / 'log',
        'log_to_file': True,
        },
    'execution': {
        'crashdump_dir': NIPYPE_PATH / 'log',
        'keep_inputs': 'false',
        'remove_unnecessary_outputs': 'false',
        },
    })
logging.update_logging(config)


def workflow_ieeg():
    node_read = Node(function_ieeg_read, name='read')
    node_read.inputs.conditions = {'move': '49', 'rest': '48'}
    node_read.inputs.minimalduration = 20

    node_preprocess = MapNode(function_ieeg_preprocess, name='preprocess', iterfield=['ieeg', ])
    node_preprocess.inputs.duration = 2
    node_preprocess.inputs.reref = 'average'

    node_frequency = MapNode(function_ieeg_powerspectrum, name='powerspectrum', iterfield=['ieeg', ])
    node_frequency.inputs.method = 'dh2012'
    node_frequency.inputs.taper = ''
    node_frequency.inputs.duration = 2

    node_compare = Node(function_ieeg_compare, name='compare')
    node_compare.inputs.frequency = (65, 96)
    node_compare.inputs.baseline = False
    node_compare.inputs.method = 'dh2012'
    node_compare.inputs.measure = 'dh2012_r2'

    w = Workflow('ieeg')

    w.connect(node_read, 'ieeg', node_preprocess, 'ieeg')
    w.connect(node_preprocess, 'ieeg', node_frequency, 'ieeg')
    w.connect(node_frequency, 'ieeg', node_compare, 'in_files')

    return w


def workflow_fmri():
    node_bet = Node(BET(), name='bet')
    node_bet.inputs.frac = 0.5
    node_bet.inputs.vertical_gradient = 0
    node_bet.inputs.robust = True

    node_featdesign = Node(function_prepare_design, name='feat_design')

    node_feat = Node(FEAT(), name='feat')

    node_fmri_compare = Node(function_fmri_compare, name='fmri_compare')
    node_fmri_compare.inputs.analysis_dir = str(ANALYSIS_PATH)
    node_fmri_compare.inputs.measure = 'percent'
    node_fmri_compare.inputs.normalize_to_mean = False

    node_fmri_atelec = Node(function_fmri_atelec, name='fmri_atelec')
    node_fmri_atelec.inputs.upsample = False
    node_fmri_atelec.inputs.graymatter = False
    node_fmri_atelec.inputs.distance = 'gaussian'
    node_fmri_atelec.inputs.kernel_start = 4
    node_fmri_atelec.inputs.kernel_end = 9
    node_fmri_atelec.inputs.kernel_step = 1

    w = Workflow('fmri')
    w.connect(node_bet, 'out_file', node_featdesign, 'anat')

    # w.connect(node_featdesign, 'fsf_file', node_feat, 'fsf_file')
    # w.connect(node_feat, 'feat_dir', node_fmri_compare, 'feat_path')

    return w


def create_grvx_workflow():
    bids.iterables = ('subject', SUBJECTS)

    node_reconall = Node(ReconAll(), name='freesurfer')
    node_reconall.inputs.subjects_dir = str(FREESURFER_PATH)
    node_reconall.inputs.flags = ['-cw256', ]

    node_corr = Node(function_corr, name='corr_fmri_ecog')
    node_corr.inputs.output_dir = str(OUTPUT_PATH)
    node_corr.inputs.PVALUE = 0.05

    w_fmri = workflow_fmri()
    w_ieeg = workflow_ieeg()

    w = Workflow('grvx')
    w.base_dir = str(NIPYPE_PATH)
    # w.connect(bids, 'subject', w_fmri, 'freesurfer.subject_id')
    # w.connect(bids, 'anat', w_fmri, 'freesurfer.T1_files')

    w.connect(bids, 'anat', w_fmri, 'bet.in_file')
    w.connect(bids, 'func', w_fmri, 'feat_design.func')

    w.connect(bids, 'ieeg', w_ieeg, 'read.ieeg')
    w.connect(bids, 'elec', w_ieeg, 'read.electrodes')

    # w.connect(node_fmri_compare, 'out_file', node_fmri_atelec, 'measure_nii')
    # w.connect(bids, 'elec', node_fmri_atelec, 'electrodes')

    # w.connect(node_ieeg_compare, 'tsv_compare', node_corr, 'ecog_file')
    # w.connect(node_fmri_atelec, 'fmri_vals', node_corr, 'fmri_file')

    w.write_graph(graph2use='flat')

    return w
