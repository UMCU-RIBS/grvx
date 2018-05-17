from boavus.ieeg import (preprocessing,
                         psd,
                         compare,
                         )

from .core.constants import (DATA_PATH,
                             ANALYSIS_PATH,
                             PARAMETERS,
                             )
from .core.log import with_log


@with_log
def Compare_ECoG(lg, img_dir):

    preprocessing.main(
        bids_dir=DATA_PATH,
        analysis_dir=ANALYSIS_PATH,
        **PARAMETERS['preprocessing'],
        )

    psd.main(
        analysis_dir=ANALYSIS_PATH,
        **PARAMETERS['psd'],
        )

    compare.main(
        analysis_dir=ANALYSIS_PATH,
        **PARAMETERS['ecog_compare'],
        )
