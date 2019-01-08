from shutil import rmtree
from numpy import where

from pandas import DataFrame, read_pickle, isnull

from xelo2bids.core.constants import TASKS_PATH
from xelo2bids import bids_mri, xelo2bids

from .core.constants import DATA_PATH
from .core.log import with_log

bids_mri.RUN_DEFACE = False

"""
# only TR = 0.6
df = [
    {'subj': 'arnhem', 'ECoG': 'arnhem2097', 'fMRI': '6abaa4da1779fdcbf148b759f13f366e'},
    {'subj': 'boxtel', 'ECoG': 'boxtel1964', 'fMRI': '5dcbae36c46e31039d2cdd4155a85f2e'},
    {'subj': 'bunnik', 'ECoG': 'bunnik_bunnik011116_motor_right_hand_streched_palmUpS001R01_TaskXML', 'fMRI': 'bunnik_bunnik160916_WIP_Circle_MotorHand_PrestoSense40sl_u_SENSE_8_1_TaskXML'},
    {'subj': 'delft', 'ECoG': 'delft1802', 'fMRI': 'delft1818'},
    {'subj': 'duiven', 'ECoG': 'duiven_20170212-102941-001_TaskXML', 'fMRI': '516bec27a411e89fe71fbaee7783c014'},
    {'subj': 'erp', 'ECoG': 'erp1827', 'fMRI': 'erp1930'},
    {'subj': 'gord', 'ECoG': 'gord536', 'fMRI': 'gord518'},
    {'subj': 'groo', 'ECoG': 'groo47', 'fMRI': 'groo45'},
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
"""

TASKNAME = 'motor'


@with_log
def Read_As_Bids(lg):
    try:
        rmtree(DATA_PATH)
    except Exception:
        pass

    tasks = _find_tasks_with_motor()

    xelo2bids([
        '--log', 'debug',
        'create',
        str(DATA_PATH),
        '--keys',
        ]
        + tasks
        )


def _find_tasks_with_motor():

    df = read_pickle(TASKS_PATH)
    tasks = []

    for bodypart in ('Hand', 'Thumb'):
        for leftright in ('Left', 'Right'):

            ecog_subj = df.loc[
                (df.Technique == 'ECoG')
                & (df.TaskName == TASKNAME)
                & (df.BodyPart == bodypart)
                & (df.LeftRight == leftright),
                'SubjectCode'].unique()

            fmri_subj = df.loc[
                (df.Technique == 'fMRI')
                & (df.FieldStrength == '3T')
                & (isnull(df.TR) | (df.TR < 0.7))
                & (df.TaskName == TASKNAME)
                & (df.BodyPart == bodypart)
                & (df.LeftRight == leftright),
                'SubjectCode'].unique()

            subjects = set(ecog_subj) & set(fmri_subj)

            for subj in subjects:
                if subj in ('buij', 'albe', 'enge', 'weve', 'mars', 'mang'):  # don't remember why
                    continue
                if subj in ('arnhem', ):  # cannot use clinical data
                    continue

                for technique in ('fMRI', 'ECoG'):

                    if technique == 'fMRI':
                        i = where(
                            (df.Technique == technique)
                            & (df.FieldStrength == '3T')
                            & (isnull(df.TR) | (df.TR < 0.7))
                            & (df.SubjectCode == subj)
                            & (df.TaskName == TASKNAME)
                            & (df.BodyPart == bodypart)
                            & (df.LeftRight == leftright))[0]
                    else:
                        i = where(
                            (df.Technique == technique)
                            & (df.SubjectCode == subj)
                            & (df.TaskName == TASKNAME)
                            & (df.BodyPart == bodypart)
                            & (df.LeftRight == leftright))[0]

                    if len(i) == 1:
                        stem = df.index[i[0]]
                    elif (subj == 'boxtel') & (technique == 'ECoG'):
                        stem = 'boxtel1964'
                    elif (subj == 'bunnik') & (technique == 'ECoG'):
                        stem = 'bunnik_bunnik011116_motor_right_hand_streched_palmUpS001R01_TaskXML'
                    elif (subj == 'duiven') & (technique == 'ECoG'):
                        stem = 'duiven_20170212-102941-001_TaskXML'
                    elif (subj == 'itens') & (technique == 'ECoG'):
                        stem = 'itens_Itens_08032017_Motor_L_fingertappingS001R02_TaskXML'
                    elif (subj == 'ommen') & (technique == 'ECoG'):
                        stem = 'ommen_20170114-110422-013_TaskXML'
                    elif (subj == 'ruit') & (technique == 'ECoG'):
                        stem = 'ruit590'
                    elif (subj == 'vledder') & (technique == 'ECoG'):
                        stem = 'vledder_20170116-100726-001_TaskXML'
                    elif (subj == '') & (technique == 'ECoG'):
                        stem = ''
                    elif (subj == 'zuil') & (technique == 'ECoG'):
                        stem = 'zuil744'
                    else:
                        raise ValueError(f'Multiple tasks for {i}')

                    tasks.append(stem)

    return tasks
