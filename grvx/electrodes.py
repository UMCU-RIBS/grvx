from boavus.ieeg import (project_electrodes,
                         assign_regions,
                         )
from .core.constants import (FREESURFER_PATH,
                             DATA_PATH,
                             ANALYSIS_PATH,
                             OUTPUT_PATH,
                             )
from .core.log import with_log


@with_log
def Project_Elec_On_Surf(lg, img_dir):

    project_electrodes.main(
        bids_dir=DATA_PATH,
        freesurfer_dir=FREESURFER_PATH,
        analysis_dir=ANALYSIS_PATH,
        acquisition='ctmr',
        )


@with_log
def Assign_Regions_To_Elec(lg, img_dir):

    assign_regions.main(
        bids_dir=DATA_PATH,
        freesurfer_dir=FREESURFER_PATH,
        acquisition='*projected',
        )
