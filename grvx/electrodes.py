from boavus.main import boavus

from .core.constants import (FREESURFER_PATH,
                             DATA_PATH,
                             ANALYSIS_PATH,
                             PARAMETERS,
                             Parameters_Json,
                             )
from .core.log import with_log


@with_log
def Project_Elec_On_Surf(lg, img_dir):

    PARAMETERS_JSON = Parameters_Json(PARAMETERS['electrodes'])
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

    PARAMETERS_JSON = Parameters_Json(PARAMETERS['electrodes'])
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
