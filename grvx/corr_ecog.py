from boavus.ieeg.corr_fmri import _main, _main_to_elec
from bidso import iEEG
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
                       arange(1, 10))
        print(result)


@with_log
def Corr_fMRI_to_Elec(lg, img_dir):
    for ieeg_file in DATA_PATH.rglob('*_ieeg.bin'):
        ieeg = iEEG(ieeg_file)
        feat_path = next((FEAT_PATH / f'sub-{ieeg.subject}').rglob('*.feat'))

        result = _main_to_elec(ieeg_file, feat_path, FREESURFER_PATH, DERIVATIVES_PATH,
                               arange(0.25, 4, 0.25), True)
        print(result)

        result_val = img_dir / f'corr_{ieeg_file.stem}.csv'
        with result_val.open('w') as f:
            f.write(','.join(str(x) for x in result))
