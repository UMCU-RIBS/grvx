from logging import getLogger

from numpy import argmax, polyfit, isnan, NaN, isin, empty
from numpy.testing import assert_array_equal
from scipy.stats import linregress, norm
from pickle import load, dump

from bidso.utils import read_tsv, replace_underscore


lg = getLogger(__name__)


def compute_corr_ecog_fmri(fmri_file, ecog_file, output_dir, PVALUE):
    output_dir.mkdir(exist_ok=True, parents=True)

    fmri_tsv = read_tsv(fmri_file)
    ecog_tsv = read_tsv(ecog_file)
    fmri_tsv = select_channels(fmri_tsv, ecog_tsv)
    kernel_sizes = fmri_tsv.dtype.names[1:]

    results_tsv = output_dir / replace_underscore(ecog_file.stem, 'bold_r2.tsv')
    with results_tsv.open('w') as f:
        f.write('Kernel\tRsquared\tSlope\tIntercept\n')

        for kernel in kernel_sizes:
            try:
                r2, slope, intercept = compute_rsquared(
                    ecog_tsv['measure'],
                    fmri_tsv[kernel],
                    ecog_tsv['pvalue'],
                    PVALUE)

            except Exception:
                r2 = slope = intercept = NaN

            f.write(f'{float(kernel):.2f}\t{r2}\t{slope}\t{intercept}\n')

    return results_tsv, fmri_file, ecog_file


def compute_corr_ecog_fmri_allfreq(fmri_file, ecog_file, min_n_sign_elec, pvalue, output_dir):
    output_dir.mkdir(exist_ok=True, parents=True)

    with ecog_file.open('rb') as f:
        ecog_stats = load(f)

    fmri_vals = read_tsv(fmri_file)
    fmri_idx = isin(fmri_vals['channel'], (ecog_stats.chan[0]))
    fmri_vals = fmri_vals[fmri_idx]
    assert_array_equal(fmri_vals['channel'], ecog_stats.chan[0])

    threshold = norm.ppf(1 - pvalue / 2)

    kernel_sizes = fmri_vals.dtype.names[1:]
    n_freq = ecog_stats.freq[0].shape[0]
    rsquared = empty((
        n_freq,
        len(kernel_sizes),
        ))
    slope = empty((
        n_freq,
        len(kernel_sizes),
        ))
    pvalue = empty((
        n_freq,
        len(kernel_sizes),
        ))

    for i_k, kernel in enumerate(kernel_sizes):
        for i_f in range(n_freq):
            x = ecog_stats.data[0][:, i_f]
            y = fmri_vals[kernel]
            rsquared[i_f, i_k], slope[i_f, i_k], pvalue[i_f, i_k] = compute_rsquared_pvalue(x, y, threshold, min_n_sign_elec)

    out_file = output_dir / 'corr_ecog_fmri_allfreq.pkl'
    with out_file.open('wb') as f:
        dump([rsquared, slope, pvalue], f)

    return out_file


def select_channels(fmri_vals, ecog_vals):
    """make sure we're using the same channels and in the same order
    """
    fmri_idx = isin(fmri_vals['channel'], (ecog_vals['channel']))
    fmri_vals = fmri_vals[fmri_idx]
    assert_array_equal(fmri_vals['channel'], ecog_vals['channel'])

    return fmri_vals


def compute_rsquared(x, y, p_val, PVALUE):
    mask = ~isnan(x) & ~isnan(y) & (p_val <= PVALUE)

    lr = linregress(x[mask], y[mask])
    return lr.rvalue ** 2, lr.slope, lr.intercept


def compute_rsquared_pvalue(x, y, threshold, min_n_sign_elec):
    mask = ~isnan(x) & ~isnan(y) & (abs(x) >= threshold)
    if sum(mask) < min_n_sign_elec:
        return NaN, NaN, 1
    lr = linregress(x[mask], y[mask])
    return lr.rvalue ** 2, lr.slope, lr.pvalue


def read_shape(one_tsv):
    results = read_tsv(one_tsv)
    k = [float(x['Kernel']) for x in results]
    rsquared = [float(x['Rsquared']) for x in results]

    return polyfit(k, rsquared, 2)[0], k[argmax(rsquared)], max(rsquared)
