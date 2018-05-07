from boavus import boavus

from .core.constants import (FREESURFER_PATH,
                             ANALYSIS_PATH,
                             DATA_PATH,
                             PARAMETERS,
                             Parameters_Json,
                             )
from .core.log import with_log


@with_log
def Run_FreeSurfer(lg, img_dir):
    FREESURFER_PATH.mkdir(exist_ok=True)

    boavus([
        'freesurfer',
        'reconall',
        '--bids_dir',
        str(DATA_PATH),
        '--freesurfer_dir',
        str(FREESURFER_PATH),
        '--log',
        'debug',
        ])


@with_log
def Run_fMRI_feat(lg, img_dir):
    boavus([
        'fsl',
        'feat',
        '--bids_dir',
        str(DATA_PATH),
        '--analysis_dir',
        str(ANALYSIS_PATH),
        '--log',
        'debug',
        ])


@with_log
def Compare_Feat(lg, img_dir):

    PARAMETERS_JSON = Parameters_Json(PARAMETERS['compare_fmri'])
    boavus([
        'fmri',
        'compare',
        '--analysis_dir',
        str(ANALYSIS_PATH),
        '--parameters',
        PARAMETERS_JSON.name,
        '--log',
        'debug',
        ])
    PARAMETERS_JSON.delete()

    PARAMETERS_JSON = Parameters_Json(PARAMETERS['atelectrodes'])
    boavus([
        'fmri',
        'at_electrodes',
        '--bids_dir',
        str(DATA_PATH),
        '--freesurfer_dir',
        str(FREESURFER_PATH),
        '--analysis_dir',
        str(ANALYSIS_PATH),
        '--parameters',
        PARAMETERS_JSON.name,
        '--log',
        'debug',
        ])
    PARAMETERS_JSON.delete()
