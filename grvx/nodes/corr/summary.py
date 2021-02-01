from bidso import file_Core
from numpy import gradient, argmin, argmax
from shutil import copy
from bidso.utils import read_tsv


def collect_corr(in_files, ecog_files, fmri_files, output_dir):

    rsquared_dir = output_dir / 'rsquared'
    rsquared_dir.mkdir(parents=True, exist_ok=True)

    ecog_dir = output_dir / 'ecog'
    ecog_dir.mkdir(parents=True, exist_ok=True)

    fmri_dir = output_dir / 'fmri'
    fmri_dir.mkdir(parents=True, exist_ok=True)

    for in_file in in_files:
        copy(in_file, rsquared_dir)

    for in_file in ecog_files:
        copy(in_file, ecog_dir)

    for in_file in fmri_files:
        copy(in_file, fmri_dir)

    _compute_summary(in_files, output_dir)


def _compute_summary(in_files, output_dir):

    summary_file = output_dir / 'summary_per_subject.tsv'

    with summary_file.open('w') as f:

        f.write(f'subject\tsession\ttask\tacquisition\tsize_at_peak\tr2_at_peak\tslope_at_peak\tintercept_at_peak\tsize_at_concave\tr2_at_concave\tdiff_r2\n')

        for corr_file in in_files:

            corr_tsv = read_tsv(corr_file)
            size_max, r2_max, slope, intercept = corr_tsv[argmax(corr_tsv['Rsquared'])]

            deriv = gradient(gradient(corr_tsv['Rsquared']))
            size_deriv, r2_deriv, *dummy = corr_tsv[argmin(deriv)]

            file_info = file_Core(corr_file)

            f.write(f'{file_info.subject}\t{file_info.session}\t{file_info.task}\t{file_info.acquisition}\t{size_max}\t{r2_max}\t{slope}\t{intercept}\t{size_deriv}\t{r2_deriv}\t{r2_max - r2_deriv}\n')
