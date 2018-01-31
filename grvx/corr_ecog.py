from boavus.main import boavus
from .core.constants import (FREESURFER_PATH,
                             SCRIPTS_PATH,
                             DATA_PATH,
                             OUTPUT_PATH,
                             )


from .core.log import with_log


@with_log
def Corr_fMRI_to_Elec(lg, img_dir):

    PARAMETERS_JSON = SCRIPTS_PATH / 'parameters' / 'parameters_corrfmri.json'

    boavus([
        'ieeg',
        'corrfmri',
        '--output_dir',
        str(OUTPUT_PATH),
        '--freesurfer_dir',
        str(FREESURFER_PATH),
        '--bids_dir',
        str(DATA_PATH),
        '--parameters',
        str(PARAMETERS_JSON),
        '--log',
        'debug',
        ])
