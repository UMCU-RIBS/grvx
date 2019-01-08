from nipype import Function, Node

from ..core.constants import DATA_PATH

# TODO: put this into constants
SUBJECTS = [x.name[4:] for x in DATA_PATH.glob('sub-*')]
SUBJECTS = list(set(SUBJECTS) - {'spoo', 'zuil'})
SUBJECTS = list(set(SUBJECTS) - {'kuit', 'joure', 'maarn', 'mierlo'})  # no FS yet


def get_bids(bids_dir, subject):
    from bidso.find import find_in_bids

    return (
        'sub-' + subject,
        str(find_in_bids(bids_dir, subject=subject, modality='T1w', extension='.nii.gz')),
        str(find_in_bids(bids_dir, subject=subject, modality='bold', extension='.nii.gz')),
        str(find_in_bids(bids_dir, subject=subject, modality='ieeg', extension='.eeg')),
        str(find_in_bids(bids_dir, subject=subject, acquisition='*al', modality='electrodes', extension='.tsv')),
        )


BIDS = Function(
    input_names=[
        'bids_dir',
        'subject',
    ],
    output_names=[
        'subject',
        'anat',
        'func',
        'ieeg',
        'elec',
    ],
    function=get_bids,
    )


bids = Node(BIDS, name='bids')
bids.inputs.bids_dir = DATA_PATH
