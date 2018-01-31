from boavus.main import boavus

from .core.constants import (DATA_PATH,
                             OUTPUT_PATH,
                             SCRIPTS_PATH,
                             )
from .core.log import with_log

PARAMETERS_JSON = SCRIPTS_PATH / 'parameters' / 'parameters_compare.json'


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

    boavus([
        'ieeg',
        'psd',
        '--output_dir',
        str(OUTPUT_PATH),
        '--log',
        'debug',
        ])

    boavus([
        'ieeg',
        'compare',
        '--output_dir',
        str(OUTPUT_PATH),
        '--parameters',
        str(PARAMETERS_JSON),
        '--log',
        'debug',
        ])
