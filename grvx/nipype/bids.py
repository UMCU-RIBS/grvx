from nipype import Function, Node


def get_bids(bids_dir, subject):
    from bidso.find import find_in_bids

    return (
        'sub-' + subject,
        str(find_in_bids(bids_dir, subject=subject, modality='T1w', extension='.nii.gz')),
        str(find_in_bids(bids_dir, subject=subject, modality='bold', extension='.nii.gz')),
        str(find_in_bids(bids_dir, subject=subject, modality='ieeg', extension='.eeg')),
        str(find_in_bids(bids_dir, subject=subject, modality='electrodes', extension='.tsv')),
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
# bids.inputs.bids_dir = DATA_PATH
