from shutil import rmtree

from pandas import DataFrame

from xelo2bids.bids_tree import create_bids, DF_TASKS
from xelo2bids import bids_mri

from .core.constants import DATA_PATH
from .core.log import with_log

bids_mri.RUN_DEFACE = False

# only TR = 0.6
df = [
    {'subj': 'arnhem', 'ECoG': 'arnhem2097', 'fMRI': 'd44f92264b48326c0c365b86c6e9b6e1'},
    {'subj': 'boxtel', 'ECoG': 'boxtel1964', 'fMRI': '5dcbae36c46e31039d2cdd4155a85f2e'},
    {'subj': 'bunnik', 'ECoG': 'bunnik_bunnik011116_motor_right_hand_streched_palmUpS001R01_TaskXML', 'fMRI': 'bunnik_bunnik160916_WIP_Circle_MotorHand_PrestoSense40sl_u_SENSE_8_1_TaskXML'},
    {'subj': 'delft', 'ECoG': 'delft1802', 'fMRI': 'delft1818'},
    {'subj': 'duiven', 'ECoG': 'duiven_20170212-102941-001_TaskXML', 'fMRI': '516bec27a411e89fe71fbaee7783c014'},
    {'subj': 'erp', 'ECoG': 'erp1827', 'fMRI': 'erp1930'},
    {'subj': 'gord', 'ECoG': 'gord536', 'fMRI': 'gord518'},
    {'subj': 'groo', 'ECoG': 'groo47', 'fMRI': 'groo45'},
    {'subj': 'heek', 'ECoG': 'heek_20180217-143702-003_TaskXML', 'fMRI': 'heek_V7711_fMRI_MotorHand-Circle_14_1_TaskXML'},
    {'subj': 'itens', 'ECoG': 'itens_Itens_08032017_Motor_L_fingertappingS001R02_TaskXML', 'fMRI': '814a028cd01fbdb3949626f6b2e85018'},
    {'subj': 'maas', 'ECoG': 'maas480', 'fMRI': 'maas470'},
    {'subj': 'ommen', 'ECoG': 'ommen_20170114-110422-013_TaskXML', 'fMRI': 'ffa534bac2f46a876d04dd5129bb8f5a'},
    {'subj': 'ruit', 'ECoG': 'ruit590', 'fMRI': 'ruit570'},
    {'subj': 'smilde', 'ECoG': 'smilde1969', 'fMRI': '98f3b01b064e8a78a942cbb7545bab91'},
    {'subj': 'spoo', 'ECoG': 'spoo371', 'fMRI': 'spoo360'},
    {'subj': 'tesf', 'ECoG': 'tesf454', 'fMRI': 'tesf446'},
    {'subj': 'vledder', 'ECoG': 'vledder_20170116-100726-001_TaskXML', 'fMRI': 'bc2b8247f88b8027599f0bf806dc389c'},
    {'subj': 'zuil', 'ECoG': 'zuil744', 'fMRI': 'zuil732'},
    {'subj': 'zwolle', 'ECoG': 'zwolle2008', 'fMRI': '8d21531d6cf396703b909c0324df3550'},
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
