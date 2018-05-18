from boavus.ieeg import corrfmri
from .core.constants import (DATA_PATH,
                             PARAMETERS,
                             OUTPUT_PATH,
                             ANALYSIS_PATH,
                             )


from .core.log import with_log


@with_log
def Corr_fMRI_to_Elec(lg, img_dir):

    corrfmri.main(
        output_dir=OUTPUT_PATH,
        analysis_dir=ANALYSIS_PATH,
        bids_dir=DATA_PATH,
        **PARAMETERS['corrfmri'],
        )
