from shutil import rmtree

from pandas import DataFrame

from xelo2bids.bids_tree import create_bids, DF_TASKS

from .core.constants import DATA_PATH
from .core.log import with_log

df = [
    {'subj': 'duiven', 'ECoG': 'duiven_20170212-102941-001_TaskXML', 'fMRI': '516bec27a411e89fe71fbaee7783c014'},
    {'subj': 'ommen', 'ECoG': 'ommen_20170114-110422-013_TaskXML', 'fMRI': 'ffa534bac2f46a876d04dd5129bb8f5a'},
    ]
commontasks = DataFrame(df)


@with_log
def Read_As_Bids(lg, img_dir):
    try:
        rmtree(DATA_PATH)
    except:
        pass

    try:
        DATA_PATH.mkdir()
    except:
        pass

    ALL_SUBJ = set(commontasks.subj)
    stems = DF_TASKS.loc[(DF_TASKS['SubjectCode'].isin(ALL_SUBJ)) & (DF_TASKS['TaskName'] == 't1_anatomy_scan'), 'stem']

    create_bids(DATA_PATH, list(stems) + list(commontasks.ECoG) + list(commontasks.fMRI))
