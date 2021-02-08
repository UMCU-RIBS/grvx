
def get_path(parameters, index, **kwargs):
    out = parameters['paths']['output'] / 'workflow'

    if 'frequency_band' in kwargs:
        freq = kwargs['frequency_band']
        freq_dir = f'_frequency_{freq[0]}.{freq[1]}'

    if 'subject' in kwargs:
        subj = kwargs['subject']
        subj_dir = f'_subject_{subj}'

    if index == 'summary_tsv':
        x = out / freq_dir / 'corr_fmri_ecog_summary' / 'output' / 'summary_per_subject.tsv'

    elif index == 'corr':
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
