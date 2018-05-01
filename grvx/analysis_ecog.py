from boavus.main import boavus

from .core.constants import (DATA_PATH,
                             ANALYSIS_PATH,
                             Parameters_Json,
                             PARAMETERS,
                             )
from .core.log import with_log


@with_log
def Compare_ECoG(lg, img_dir):

    PARAMETERS_JSON = Parameters_Json(PARAMETERS['preprocessing'])
    boavus([
        'ieeg',
        'preprocessing',
        '--bids_dir',
        str(DATA_PATH),
        '--analysis_dir',
        str(ANALYSIS_PATH),
        '--parameters',
        PARAMETERS_JSON.name,
        '--log',
        'debug',
        ])
    PARAMETERS_JSON.delete()

    PARAMETERS_JSON = Parameters_Json(PARAMETERS['psd'])
    boavus([
        'ieeg',
        'psd',
        '--analysis_dir',
        str(ANALYSIS_PATH),
        '--parameters',
        PARAMETERS_JSON.name,
        '--log',
        'debug',
        ])
    PARAMETERS_JSON.delete()

    PARAMETERS_JSON = Parameters_Json(PARAMETERS['compare_ecog'])
    boavus([
        'ieeg',
        'compare',
        '--analysis_dir',
        str(ANALYSIS_PATH),
        '--parameters',
        PARAMETERS_JSON.name,
        '--log',
        'debug',
        ])
    PARAMETERS_JSON.delete()
