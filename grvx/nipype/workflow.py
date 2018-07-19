from nipype import Workflow, Node, MapNode, config, logging
from nipype.interfaces.fsl import FEAT
from nipype.interfaces.freesurfer import ReconAll

from boavus.nipype import (function_ieeg_read,
                           function_ieeg_preprocess,
                           function_ieeg_frequency,
                           function_ieeg_compare,
                           FEAT_model,
                           function_fmri_compare,
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
        'keep_inputs': 'true',
        'remove_unnecessary_outputs': 'false',
        },
    })
logging.update_logging(config)


def create_grvx_workflow():
    bids.iterables = ('subject', SUBJECTS)

    node_reconall = Node(ReconAll(), name='freesurfer')
    node_reconall.inputs.subjects_dir = str(FREESURFER_PATH)
    node_reconall.inputs.flags = ['-cw256', ]

    node_featdesign = Node(FEAT_model, name='feat_design')
    node_featdesign.inputs.analysis_dir = str(ANALYSIS_PATH)

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

    node_ieeg_read = Node(function_ieeg_read, name='ieeg_read')
    node_ieeg_read.inputs.analysis_dir = str(ANALYSIS_PATH)

    node_ieeg_preprocess = MapNode(function_ieeg_preprocess, name='ieeg_preprocess', iterfield=['ieeg', ])
    node_ieeg_frequency = MapNode(function_ieeg_frequency, name='ieeg_frequency', iterfield=['ieeg', ])
    node_ieeg_frequency.inputs.method = 'dh2012'
    node_ieeg_frequency.inputs.taper = ''
    node_ieeg_frequency.inputs.duration = 2

    node_ieeg_compare = Node(function_ieeg_compare, name='ieeg_compare')
    node_ieeg_compare.inputs.analysis_dir = str(ANALYSIS_PATH)

    node_corr = Node(function_corr, name='corr_fmri_ecog')
    node_corr.inputs.output_dir = str(OUTPUT_PATH)
    node_corr.inputs.PVALUE = 0.05

    w = Workflow('grvx')
    w.base_dir = str(NIPYPE_PATH)
    w.connect(bids, 'subject', node_reconall, 'subject_id')
    w.connect(bids, 'anat', node_reconall, 'T1_files')

    w.connect(bids, 'func', node_featdesign, 'func')
    w.connect(bids, 'anat', node_featdesign, 'anat')

    w.connect(node_featdesign, 'fsf_file', node_feat, 'fsf_file')
    w.connect(node_feat, 'feat_dir', node_fmri_compare, 'feat_path')

    w.connect(node_fmri_compare, 'out_file', node_fmri_atelec, 'measure_nii')
    w.connect(bids, 'elec', node_fmri_atelec, 'electrodes')

    w.connect(bids, 'ieeg', node_ieeg_read, 'ieeg')
    w.connect(bids, 'elec', node_ieeg_read, 'electrodes')
    w.connect(node_ieeg_read, 'ieeg_files', node_ieeg_preprocess, 'ieeg')
    w.connect(node_ieeg_preprocess, 'ieeg', node_ieeg_frequency, 'ieeg')
    w.connect(node_ieeg_frequency, 'ieeg', node_ieeg_compare, 'in_files')

    w.connect(node_ieeg_compare, 'tsv_compare', node_corr, 'ecog_file')
    w.connect(node_fmri_atelec, 'fmri_vals', node_corr, 'fmri_file')

    w.write_graph(graph2use='flat')

    return w
