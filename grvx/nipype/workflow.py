from nipype import Workflow, Node
from nipype.interfaces.fsl import FEAT

from boavus.freesurfer.reconall import node_reconall
from boavus.nipype import node_featdesign

from .bids import bids, SUBJECTS
from ..core.constants import NIPYPE_PATH, FREESURFER_PATH, ANALYSIS_PATH

node_feat = Node(FEAT(), name='feat')


def create_grvx_workflow():
    bids.iterables = ('subject', SUBJECTS)
    node_reconall.inputs.subjects_dir = str(FREESURFER_PATH)
    node_featdesign.inputs.analysis_dir = str(ANALYSIS_PATH)

    w = Workflow('grvx')
    w.base_dir = str(NIPYPE_PATH)
    # w.connect(bids, 'subject', node_reconall, 'subject_id')
    # w.connect(bids, 'anat', node_reconall, 'T1_files')
    w.connect(bids, 'func', node_featdesign, 'func')
    w.connect(bids, 'anat', node_featdesign, 'anat')

    w.connect(node_featdesign, 'fsf_file', node_feat, 'fsf_file')

    w.write_graph(graph2use='flat')

    return w
