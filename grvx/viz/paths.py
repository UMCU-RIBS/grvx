
def get_path(parameters, index, **kwargs):
    out = parameters['paths']['output'] / 'workflow'

    if 'frequency_band' in kwargs:
        freq = kwargs['frequency_band']
        freq_dir = f'_frequency_{freq[0]}.{freq[1]}'

    if 'subject' in kwargs:
        subj = kwargs['subject']
        subj_dir = f'_subject_{subj}'

    if index == 'elec':

        try:
            x = next(parameters['paths']['input'].glob(f'sub-{subj}/ses-*/ieeg/*_electrodes.tsv'))
        except StopIteration:
            print(f'Cound not find electrodes for {subj}')
            return

    elif index == 'summary_tsv':
        x = out / freq_dir / 'corr_fmri_ecog_summary' / 'output' / 'summary_per_subject.tsv'

    elif index == 'ieeg_tsv':
        x_dir = out / 'ieeg' / subj_dir / freq_dir / 'ecog_compare'
        try:
            x = next(x_dir.glob(f'sub-{subj}_*_compare.tsv'))
        except StopIteration:
            print(f'Cound not find compare.tsv in {x_dir}')
            return

    elif index == 'fmri_tsv':
        x_dir = out / 'fmri' / subj_dir / 'at_elec'
        try:
            x = next(x_dir.glob(f'sub-{subj}_*_compare.tsv'))
        except StopIteration:
            print(f'Cound not find compare.tsv in {x_dir}')
            return

    elif index == 'fmri_nii':
        x_dir = out / 'fmri' / subj_dir / 'fmri_compare'
        try:
            x = next(x_dir.glob(f'sub-{subj}_*_bold_compare.nii.gz'))
        except StopIteration:
            print(f'Cound not find compare.nii.gz in {x_dir}')
            return

    elif index == 'corr_tsv':
        x_dir = out / subj_dir / freq_dir / 'corr_fmri_ecog' / 'corr_values'
        try:
            x = next(x_dir.glob(f'sub-{subj}_*_r2.tsv'))
        except StopIteration:
            print(f'Cound not find r2 in {x_dir}')
            return

    if x.exists():
        return x

    else:
        print(f'Could not find {x}')
        return
