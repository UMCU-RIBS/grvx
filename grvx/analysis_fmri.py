from boavus.freesurfer import reconall
from boavus.fsl import feat
from boavus.fmri import (compare,
                         at_electrodes,
                         )
from .core.constants import (FREESURFER_PATH,
                             ANALYSIS_PATH,
                             DATA_PATH,
                             PARAMETERS,
                             )
from .core.log import with_log


@with_log
def Run_FreeSurfer(lg, img_dir):

    reconall.main(
        bids_dir=DATA_PATH,
        freesurfer_dir=FREESURFER_PATH,
        )


@with_log
def Run_fMRI_feat(lg, img_dir):

    feat.main(
        bids_dir=DATA_PATH,
        analysis_dir=ANALYSIS_PATH,
        )


@with_log
def Compare_Feat(lg, img_dir):

    compare.main(
        analysis_dir=ANALYSIS_PATH,
        **PARAMETERS['fmri_compare'],
        )

    at_electrodes.main(
        bids_dir=DATA_PATH,
        freesurfer_dir=FREESURFER_PATH,
        analysis_dir=ANALYSIS_PATH,
        **PARAMETERS['at_electrodes'],
        )
