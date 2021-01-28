from xelo2.database import access_database
from xelo2.api import Subject, Session, Run
from xelo2.bids.utils import prepare_subset
from xelo2.bids import create_bids
from pathlib import Path
from textwrap import dedent
from pandas import DataFrame


BAD_SUBJECTS = [
    'mars',  # very old
    'maas',  # TODO: maybe you can include it, but you need to check data
    'arnhem',  # no permission to use electrodes
    'boxtel',  # no permission to use electrodes
    'hulst',  # wait for freesurfer
    'delft',  # wait for freesurfer
    'smilde',  # no channels
    ]

task_name = 'motor'
JOIN = dedent("""\
    LEFT JOIN runs_sensorimotor ON runs_sensorimotor.run_id = runs.id
    LEFT JOIN recordings_epi ON recordings_epi.recording_id = recordings.id
    """)


EXCLUDE = [
    {
        'subject': 'boxtel',
        'session': 'IEMU',
        'xelo_stem': 'boxtel1964',
    },
    {
        'subject': 'bunnik',
        'session': 'IEMU',
        'xelo_stem': 'bunnik_bunnik011116_motor_right_hand_streched_palmUpS001R01_TaskXML',
    },
    {
        'subject': 'itens',
        'session': 'IEMU',
        'xelo_stem': 'itens_Itens_08032017_Motor_L_fingertappingS001R02_TaskXML',
    },
    {
        'subject': 'lemmer',
        'session': 'MRI',
        'xelo_stem': 'lemmer_motor_hand',
    },
    {
        'subject': 'lemmer',
        'session': 'IEMU',
        'xelo_stem': 'lemmer_EEG_34_TaskXML',
    },
    {
        'subject': 'ommen',
        'session': 'IEMU',
        'xelo_stem': 'ommen_20170114-110422-013_TaskXML',
    },
    {
        'subject': 'ruit',
        'session': 'IEMU',
        'xelo_stem': 'ruit590',
    },
    {
        'subject': 'vledder',
        'session': 'IEMU',
        'xelo_stem': 'vledder_20170116-100726-001_TaskXML',
    },
    {
        'subject': 'zuil',
        'session': 'IEMU',
        'xelo_stem': 'zuil744',
    },
    ]


def select_subject_with_two_sessions(db, body_part, left_right):
    mri_search = f"""task_name = 'motor' AND body_part = '{body_part}' AND left_right = '{left_right}' AND MagneticFieldStrength = '3T' AND RepetitionTime < 1 AND `recordings`.`id` IS NOT NULL"""
    iemu_search = f"""task_name = 'motor' AND body_part = '{body_part}' AND left_right = '{left_right}' AND name = 'IEMU' AND `recordings`.`id` IS NOT NULL"""

    mri_subset = prepare_subset(db, mri_search, join=JOIN)
    iemu_subset = prepare_subset(db, iemu_search, join=JOIN)

    return set(mri_subset['subjects']) & set(iemu_subset['subjects'])


def read_bids():

    db = access_database('xelo2', 'giovanni', 'password')
    bad_subjs = {Subject(db, code=x).id for x in BAD_SUBJECTS}

    subsets = None
    for body_part in ('hand', 'thumb'):
        for left_right in ('left', 'right'):

            subjs = select_subject_with_two_sessions(db, body_part, left_right)
            subjs = subjs - bad_subjs
            subj_str = ', '.join([f"'{x}'" for x in subjs])

            mri_search = f"""task_name = 'motor' AND body_part = '{body_part}' AND left_right = '{left_right}' AND RepetitionTime < 1 AND MagneticFieldStrength = '3T' AND `subjects`.`id` IN ({subj_str})"""
            subsets = prepare_subset(db, mri_search, subsets, join=JOIN)

            iemu_search = f"""task_name = 'motor' AND body_part = '{body_part}' AND left_right = '{left_right}' AND name = 'IEMU' AND `subjects`.`id` IN ({subj_str})"""
            subsets = prepare_subset(db, iemu_search, subsets, join=JOIN)

    recap = {
        'subject': [],
        'session': [],
        'start_time': [],
        'body_part': [],
        'left_right': [],
        'i_subj': [],
        'i_sess': [],
        'i_run': [],
        }

    for i_subj, i_sess, i_run in zip(subsets['subjects'], subsets['sessions'], subsets['runs']):
        subj = Subject(db, id=i_subj)
        sess = Session(db, i_sess)
        run = Run(db, i_run)

        to_exclude = False
        for ex in EXCLUDE:
            if ex['subject'] in subj.codes and sess.name == ex['session'] and run.xelo_stem != ex['xelo_stem']:
                to_exclude = True
        if to_exclude:
            continue

        if sess.name == 'MRI':
            rec = run.list_recordings()[0]
            rec.Sequence = '3T PRESTO'

        recap['subject'].append(subj.codes[0])
        recap['session'].append(sess.name)
        recap['start_time'].append(run.start_time)
        recap['body_part'].append(run.body_part)
        recap['left_right'].append(run.left_right)
        recap['i_subj'].append(i_subj)
        recap['i_sess'].append(i_sess)
        recap['i_run'].append(i_run)

    df = DataFrame(recap)
    df = df.sort_values(['subject', 'start_time']).reset_index(drop=True)
    df

    df.groupby(['subject', 'session']).count()

    subsets = {
        'subjects': list(df['i_subj']),
        'sessions': list(df['i_sess']),
        'runs': list(df['i_run']),
        }

    create_bids(
        db,
        Path('/Fridge/users/giovanni/projects/grvx_tmp/subjects/'),
        deface=False,
        subset=subsets)


if __name__ == '__main__':
    read_bids()
