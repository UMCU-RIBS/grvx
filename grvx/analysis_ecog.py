from boavus.main import boavus

from .core.constants import (DATA_PATH,
                             OUTPUT_PATH,
                             Parameters_Json,
                             PARAMETERS,
                             )
from .core.log import with_log


@with_log
def Compare_ECoG(lg, img_dir):

    boavus([
        'ieeg',
        'preprocessing',
        '--bids_dir',
        str(DATA_PATH),
        '--output_dir',
        str(OUTPUT_PATH),
        '--log',
        'debug',
        ])

    PARAMETERS_JSON = Parameters_Json(PARAMETERS['psd'])
    boavus([
        'ieeg',
        'psd',
        '--output_dir',
        str(OUTPUT_PATH),
        '--parameters',
        PARAMETERS_JSON.name,
        '--log',
        'debug',
        ])
    PARAMETERS_JSON.delete()

    PARAMETERS_JSON = Parameters_Json(PARAMETERS['compare'])
    boavus([
        'ieeg',
        'compare',
        '--output_dir',
        str(OUTPUT_PATH),
        '--parameters',
        PARAMETERS_JSON.name,
        '--log',
        'debug',
        ])
    PARAMETERS_JSON.delete()
