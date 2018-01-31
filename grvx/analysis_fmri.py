from boavus.main import boavus

from .core.constants import (FEAT_PATH,
                             FREESURFER_PATH,
                             DATA_PATH,
                             OUTPUT_PATH,
                             SCRIPTS_PATH,
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
    FEAT_PATH.mkdir(exist_ok=True)

    boavus([
        'fsl',
        'feat',
        '--bids_dir',
        str(DATA_PATH),
        '--feat_dir',
        str(FEAT_PATH),
        '--log',
        'debug',
        ])


@with_log
def Compare_Feat(lg, img_dir):

    PARAMETERS_JSON = SCRIPTS_PATH / 'parameters' / 'parameters_compare.json'

    boavus([
        'fmri',
        'compare',
        '--feat_dir',
        str(FEAT_PATH),
        '--output_dir',
        str(OUTPUT_PATH),
        '--parameters',
        str(PARAMETERS_JSON),
        '--log',
        'debug',
        ])
