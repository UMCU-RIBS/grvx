from nipype import Workflow, Node, MapNode
from nipype.interfaces.fsl import FEAT

from boavus.freesurfer.reconall import node_reconall
from boavus.nipype import (function_ieeg_read,
                           function_ieeg_preprocess,
                           function_ieeg_frequency,
                           FEAT_model,
                           )

from .bids import bids, SUBJECTS
from ..core.constants import NIPYPE_PATH, FREESURFER_PATH, ANALYSIS_PATH



def create_grvx_workflow():
    node_reconall.inputs.subjects_dir = str(FREESURFER_PATH)
    bids.iterables = ('subject', SUBJECTS)

    node_featdesign = Node(FEAT_model, name='feat_design')
    node_featdesign.inputs.analysis_dir = str(ANALYSIS_PATH)

    node_feat = Node(FEAT(), name='feat')

    node_ieeg_read = Node(function_ieeg_read, name='ieeg_read')
    node_ieeg_read.inputs.analysis_dir = str(ANALYSIS_PATH)

    node_ieeg_preprocess = MapNode(function_ieeg_preprocess, name='ieeg_preprocess', iterfield=['ieeg', ])
    node_ieeg_frequency = MapNode(function_ieeg_frequency, name='ieeg_frequency', iterfield=['ieeg', ])
    node_ieeg_frequency.inputs.method = 'dh2012'
    node_ieeg_frequency.inputs.taper = ''
    node_ieeg_frequency.inputs.duration = 2

    w = Workflow('grvx')
    w.base_dir = str(NIPYPE_PATH)
    # w.connect(bids, 'subject', node_reconall, 'subject_id')
    # w.connect(bids, 'anat', node_reconall, 'T1_files')

    # w.connect(bids, 'func', node_featdesign, 'func')
    # w.connect(bids, 'anat', node_featdesign, 'anat')

    # w.connect(node_featdesign, 'fsf_file', node_feat, 'fsf_file')

    w.connect(bids, 'ieeg', node_ieeg_read, 'ieeg')
    w.connect(bids, 'elec', node_ieeg_read, 'electrodes')
    w.connect(node_ieeg_read, 'ieeg_files', node_ieeg_preprocess, 'ieeg')
    w.connect(node_ieeg_preprocess, 'ieeg', node_ieeg_frequency, 'ieeg')

    w.write_graph(graph2use='flat')

    return w
