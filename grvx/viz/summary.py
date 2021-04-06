from bidso.utils import read_tsv
from numpy import min, max, std, mean, genfromtxt, array
from nibabel import load

from .paths import get_path


def summary_info(parameters):

    participants_tsv = parameters['paths']['input'] / 'participants.tsv'
    participants = read_tsv(participants_tsv)
    print('making sure that all the patients are included')

    print(f'# participants: {len(participants)}')
    print(f"# female participants: {(participants['sex'] == 'Female').sum()}")
    print(f"# underage participants: {(participants['age'] < 18).sum()}")
    print(f"age: mean {mean(participants['age']): 8.3f}, s.d. {std(participants['age']): 8.2f}, [ {min(participants['age']): 8.3f} - {max(participants['age']): 8.3f}]")

    subjects = [subj[4:] for subj in participants['participant_id']]

    revision_dir = parameters['paths']['output'] / 'revision'
    revision_dir.mkdir(exist_ok=True)

    for freq in parameters['ieeg']['ecog_compare']['frequency_bands']:

        df = {
            'n_elec': [],
            'perc_elec': [],
            'max': [],
            'min': [],
            }

        freq_name = f'{freq[0]}_{freq[1]}'
        with (revision_dir / f'table_{freq_name}.txt').open('w') as f:
            f.write(r'^ participant ^ # electrodes ^ \% significant electrodes ^ maximum z-score ^ minimum z-score ^\n')
            for subj in subjects:
                ieeg_tsv = get_path(parameters, 'ieeg_tsv', frequency_band=freq, subject=subj)
                ieeg = read_tsv(ieeg_tsv)

                n_elec = len(ieeg)
                n_sign = (ieeg["pvalue"] <= 0.05).sum()

                df['n_elec'].append(n_elec)
                df['perc_elec'].append(float(n_sign) / n_elec * 100)

                df['max'].append(ieeg["measure"].max())
                df['min'].append(ieeg["measure"].min())
                f.write(rf'| {subj} | {df["n_elec"][-1]} | {df["perc_elec"][-1]:.2f}\% | {df["max"][-1]:.3f} | {df["min"][-1]:.3f} |\n')

            f.write('\n')
            f.write(r'^ measure ^ # electrodes ^ \% significant electrodes ^ maximum z-score ^ minimum z-score ^\n')
            f.write(rf'| mean | {mean(df["n_elec"]): 8.3f} | {mean(df["perc_elec"]): 8.2f}\% | {mean(df["max"]): 8.3f} | {mean(df["min"]): 8.3f} |\n')
            f.write(rf'| s.d. | {std(df["n_elec"]): 8.3f} | {std(df["perc_elec"]): 8.2f}\% | {std(df["max"]): 8.3f} | {std(df["min"]): 8.3f} |\n')
            f.write(rf'| min  | {max(df["n_elec"]): 8.3f} | {max(df["perc_elec"]): 8.2f}\% | {min(df["max"]): 8.3f} | {min(df["min"]): 8.3f} |\n')
            f.write(rf'| max  | {min(df["n_elec"]): 8.3f} | {min(df["perc_elec"]): 8.2f}\% | {max(df["max"]): 8.3f} | {max(df["min"]): 8.3f} |\n')

    df = {
        'n_vox': [],
        'perc_vox': [],
        'max': [],
        'min': [],
        }

    ZTHRESH = 3.291

    with (revision_dir / 'table_bold.txt').open('w') as f:
        f.write(r'^ participant ^ # included voxels ^ \% significant voxels ^ maximum z-score ^ minimum z-score ^\n')
        for subj in subjects:

            fmri_tsv = get_path(parameters, 'fmri_nii', subject=subj)
            fmri = load(fmri_tsv)
            dat = fmri.get_fdata()

            n_vox = (dat > 0.001).sum() + (dat < -0.001).sum()
            n_sign = (dat > ZTHRESH).sum() + (dat < -ZTHRESH).sum()
            perc_vox = n_sign / n_vox * 100

            df['n_vox'].append(n_vox)
            df['perc_vox'].append(perc_vox)
            df['max'].append(dat.max())
            df['min'].append(dat.min())
            f.write(rf'| {subj} | {df["n_vox"][-1]} | {df["perc_vox"][-1]:.2f}\% | {df["max"][-1]:.3f} | {df["min"][-1]:.3f} |\n')

        f.write('\n')
        f.write(r'^ participant ^ # included voxels ^ \% significant voxels ^ maximum z-score ^ minimum z-score ^\n')
        f.write(rf'| mean | {mean(df["n_vox"]): 8.3f} | {mean(df["perc_vox"]): 8.2f}\% | {mean(df["max"]): 8.3f} | {mean(df["min"]): 8.3f} |\n')
        f.write(rf'| s.d. | {std(df["n_vox"]): 8.3f} | {std(df["perc_vox"]): 8.2f}\% | {std(df["max"]): 8.3f} | {std(df["min"]): 8.3f} |\n')
        f.write(rf'| min  | {max(df["n_vox"]): 8.3f} | {max(df["perc_vox"]): 8.2f}\% | {min(df["max"]): 8.3f} | {min(df["min"]): 8.3f} |\n')
        f.write(rf'| max  | {min(df["n_vox"]): 8.3f} | {min(df["perc_vox"]): 8.2f}\% | {max(df["max"]): 8.3f} | {max(df["min"]): 8.3f} |\n')

    with (revision_dir / 'table_summary.txt').open('w') as f:
        for val in ('size_at_peak', 'slope_at_peak', 'r2_at_peak', 'size_at_concave', 'r2_at_concave'):

            f.write(f'\n{val}\n')
            f.write('^ freq ^ mean ^ s.d. ^ min ^ max^\n')
            for freq in parameters['ieeg']['ecog_compare']['frequency_bands']:
                summ_tsv = get_path(parameters, 'summary_tsv', frequency_band=freq)
                summ = read_tsv(summ_tsv)
                x = summ[val]
                if val.startswith('r2_'):
                    x *= 100
                f.write(f'| {freq[0]}-{freq[1]} | {mean(x): 8.3f} | {std(x): 8.3f} | {min(x): 8.3f} | {max(x): 8.3f} |\n')

    w_dir = parameters['paths']['output'] / 'workflow'
    with (revision_dir / 'table_headmotion.txt').open('w') as f:
        f.write('^ head motion ^ mean ^ s.d. ^ min ^ max ^\n')
        for val in ('rel', 'abs'):
            x = array([genfromtxt(x) for x in w_dir.rglob(f'prefiltered_func_data_mcf_{val}_mean.rms')])
            f.write(f'| {val} | {mean(x): 8.3f} | {std(x): 8.3f} | {min(x): 8.3f} | {max(x): 8.3f} |\n')
