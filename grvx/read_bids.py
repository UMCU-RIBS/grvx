from shutil import rmtree

from pandas import DataFrame

from xelo2bids.bids_tree import create_bids, DF_TASKS

from .core.constants import DATA_PATH
from .core.log import with_log

{'subj': 'duiven', 'ECoG': 'duiven_20170212-102941-001_TaskXML', 'fMRI': '516bec27a411e89fe71fbaee7783c014'},
{'subj': 'ommen', 'ECoG': 'ommen_20170114-110422-013_TaskXML', 'fMRI': 'ffa534bac2f46a876d04dd5129bb8f5a'},

df = [
    {'subj': 'vledder', 'ECoG': 'vledder_20170116-100726-001_TaskXML', 'fMRI': 'bc2b8247f88b8027599f0bf806dc389c'},
    {'subj': 'bunnik', 'ECoG': 'bunnik_bunnik011116_motor_right_hand_streched_palmUpS001R01_TaskXML', 'fMRI': 'bunnik_bunnik160916_WIP_Circle_MotorHand_PrestoSense40sl_u_SENSE_8_1_TaskXML'},
    ]
commontasks = DataFrame(df)


@with_log
def Read_As_Bids(lg, img_dir):
    """
    try:
        rmtree(DATA_PATH)
    except:
        pass

    try:
        DATA_PATH.mkdir()
    except:
        pass
    """

    ALL_SUBJ = set(commontasks.subj)
    stems = DF_TASKS.loc[(DF_TASKS['SubjectCode'].isin(ALL_SUBJ)) & (DF_TASKS['TaskName'] == 't1_anatomy_scan'), 'stem']

    create_bids(DATA_PATH, list(stems) + list(commontasks.ECoG) + list(commontasks.fMRI))
