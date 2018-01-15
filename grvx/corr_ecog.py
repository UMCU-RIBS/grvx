from boavus.ieeg.corr_fmri import _main
from numpy import arange
from .core.constants import (PARAMETERS,
                             FEAT_PATH,
                             FREESURFER_PATH,
                             DERIVATIVES_PATH,
                             DATA_PATH,
                             )


from .core.log import with_log


@with_log
def Corr_ECoG_fMRI(lg, img_dir):
    for ieeg_file in DATA_PATH.rglob('*_ieeg.bin'):
        feat_path = FEAT_PATH / 'sub-ommen/ses-daym25/func/sub-ommen_ses-daym25_task-motor-hand-left_run-00.feat'

        result = _main(ieeg_file, feat_path, FREESURFER_PATH, DERIVATIVES_PATH,
                arange(1, 10, .5))
        print(result)
