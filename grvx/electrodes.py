from boavus.main import boavus

from .core.constants import (FREESURFER_PATH,
                             DATA_PATH,
                             ANALYSIS_PATH,
                             Parameters_Json,
                             )
from .core.log import with_log


@with_log
def Project_Elec_On_Surf(lg, img_dir):

    PARAMETERS_JSON = Parameters_Json({'acquisition': '*al', 'parallel': True})
    boavus([
        'ieeg',
        'project_electrodes',
        '--bids_dir',
        str(DATA_PATH),
        '--freesurfer_dir',
        str(FREESURFER_PATH),
        '--analysis_dir',
        str(ANALYSIS_PATH),
        '--log',
        'debug',
        '--parameters',
        PARAMETERS_JSON.name,
        ])
    PARAMETERS_JSON.delete()


@with_log
def Assign_Regions_To_Elec(lg, img_dir):
    PARAMETERS_JSON = Parameters_Json({'acquisition': '*projected', 'parallel': True})
    boavus([
        'ieeg',
        'assign_regions',
        '--bids_dir',
        str(DATA_PATH),
        '--freesurfer_dir',
        str(FREESURFER_PATH),
        '--log',
        'debug',
        '--parameters',
        PARAMETERS_JSON.name,
        ])
    PARAMETERS_JSON.delete()

    PARAMETERS_JSON = Parameters_Json({'acquisition': '*ctmr', 'parallel': True})
    boavus([
        'ieeg',
        'assign_regions',
        '--bids_dir',
        str(DATA_PATH),
        '--freesurfer_dir',
        str(FREESURFER_PATH),
        '--log',
        'debug',
        '--parameters',
        PARAMETERS_JSON.name,
        ])
    PARAMETERS_JSON.delete()
