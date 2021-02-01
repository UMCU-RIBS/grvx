from difflib import SequenceMatcher
from pickle import load
from numpy import ones, hstack, sign, array, NaN
from numpy import concatenate as np_concatenate
from scipy.stats import ttest_ind, pearsonr

from wonambi.trans import math, concatenate, select
from wonambi.datatype import Data

from bidso import file_Core


def compare_ieeg_freq(file_A, file_B, frequency, baseline, merge_method, measure,
                      output_dir):
    """
    Parameters
    ----------
    baseline : bool
        if you want to substract baseline
    merge_method : str
        "dh2012"
    measure : str
        "dh2012_r2"
    """
    ieeg_A = file_Core(file_A)
    ieeg_B = file_Core(file_B)

    with file_A.open('rb') as f:
        dat_A = load(f)
    with file_B.open('rb') as f:
        dat_B = load(f)

    if baseline:
        dat_A, dat_B = correct_baseline(dat_A, dat_B, frequency)

    hfa_A = merge(dat_A, merge_method, frequency)
    hfa_B = merge(dat_B, merge_method, frequency)

    if measure == 'diff':
        ecog_stats = compute_diff(hfa_A, hfa_B)
    elif measure == 'percent':
        ecog_stats = compute_percent(hfa_A, hfa_B)
    elif measure in ('zstat', 'dh2012_t'):  # identical
        ecog_stats = compute_zstat(hfa_A, hfa_B)
        if measure == 'dh2012_t':
            ecog_stats.data[0] *= -1  # opposite sign in dh2012's script

    elif measure == 'dh2012_r2':
        ecog_stats = calc_dh2012_values(hfa_A, hfa_B, measure)

    # need to check pvalues
    if True:
        pvalues = calc_dh2012_values(hfa_A, hfa_B, 'dh2012_pv')
    else:
        pvalues = [NaN, ] * ecog_stats.number_of('chan')[0]

    output = file_Core(
        subject=ieeg_A.subject,
        session=ieeg_A.session,
        run=ieeg_A.run,
        acquisition=ieeg_A.acquisition,
        modality='compare',
        extension='.tsv',
        task=find_longest_match(ieeg_A.task, ieeg_B.task),
        )
    compare_file = output_dir / output.get_filename()
    with compare_file.open('w') as f:
        f.write('channel\tmeasure\tpvalue\n')
        for i, chan in enumerate(ecog_stats.chan[0]):
            f.write(f'{chan}\t{ecog_stats(trial=0, chan=chan)}\t{pvalues(trial=0, chan=chan)}\n')

    return compare_file


def merge(freq, method, frequency):

    freq = select(freq, freq=frequency)

    if method == '1a':
        freq = concatenate(freq, axis='time')
        freq = math(freq, operator_name='mean', axis='time')
        freq = math(freq, operator_name='mean', axis='freq')
        # only one value
        out = Data(freq.data[0][:, None], freq.s_freq, chan=freq.chan[0], time=(0, ))

    elif method == '1b':
        freq = concatenate(freq, axis='time')
        freq = math(freq, operator_name='dB')
        freq = math(freq, operator_name='mean', axis='freq')
        freq = math(freq, operator_name='mean', axis='time')
        # only one value
        out = Data(freq.data[0][:, None], freq.s_freq, chan=freq.chan[0], time=(0, ))

    elif method == '1c':
        freq = concatenate(freq, axis='time')
        freq = math(freq, operator_name='mean', axis='freq')
        freq = math(freq, operator_name='dB')
        freq = math(freq, operator_name='mean', axis='time')
        # only one value
        out = Data(freq.data[0][:, None], freq.s_freq, chan=freq.chan[0], time=(0, ))

    elif method == '1d':
        freq = concatenate(freq, axis='time')
        freq = math(freq, operator_name='mean', axis='freq')
        freq = math(freq, operator_name='mean', axis='time')
        freq = math(freq, operator_name='dB')
        # only one value
        out = Data(freq.data[0][:, None], freq.s_freq, chan=freq.chan[0], time=(0, ))

    elif method == '2a':
        freq = math(freq, operator_name='mean', axis='time')
        freq = math(freq, operator_name='mean', axis='freq')
        # one value per trial
        out = concatenate(freq, axis='trial')

    elif method == '2b':
        freq = math(freq, operator_name='dB')
        freq = math(freq, operator_name='mean', axis='time')
        freq = math(freq, operator_name='mean', axis='freq')
        # one value per trial
        out = concatenate(freq, axis='trial')

    elif method == '2c':
        freq = math(freq, operator_name='mean', axis='time')
        freq = math(freq, operator_name='dB')
        freq = math(freq, operator_name='mean', axis='freq')
        # one value per trial
        out = concatenate(freq, axis='trial')

    elif method == '2d':
        freq = math(freq, operator_name='mean', axis='time')
        freq = math(freq, operator_name='mean', axis='freq')
        freq = math(freq, operator_name='dB')
        # one value per trial
        out = concatenate(freq, axis='trial')

    elif method == '3a':
        freq = concatenate(freq, axis='time')
        # values per time point
        out = math(freq, operator_name='mean', axis='freq')

    elif method == '3b':
        freq = concatenate(freq, axis='time')
        freq = math(freq, operator_name='dB')
        # values per time point
        out = math(freq, operator_name='mean', axis='freq')

    elif method == '3c':
        freq = concatenate(freq, axis='time')
        freq = math(freq, operator_name='mean', axis='freq')
        # values per time point
        out = math(freq, operator_name='dB')

    elif method == 'dh2012':
        # identical to 3b, but use log instead of dB
        freq = concatenate(freq, axis='time')
        freq = math(freq, operator_name='log')
        # values per time point
        out = math(freq, operator_name='mean', axis='freq')

    return out


def compute_diff(hfa_A, hfa_B):
    hfa_A.data[0] -= hfa_B.data[0]
    return Data(hfa_A.data[0][:, 0], hfa_A.s_freq, chan=hfa_A.chan[0])


def compute_percent(hfa_A, hfa_B):
    x_A = math(hfa_A, operator_name='mean', axis=hfa_A.list_of_axes[1])
    x_B = math(hfa_B, operator_name='mean', axis=hfa_A.list_of_axes[1])

    perc = (x_A(trial=0) - x_B(trial=0)) / x_B(trial=0) * 100
    data_perc = Data(perc, hfa_A.s_freq, chan=hfa_A.chan[0])

    return data_perc


def compute_zstat(hfa_A, hfa_B):
    """
    TODO
    ----
    You can compute zstat by taking diff and then divide by standard deviation
    """
    zstat = ttest_ind(hfa_A.data[0], hfa_B.data[0], axis=1, equal_var=False).statistic

    return Data(zstat, hfa_A.s_freq, chan=hfa_A.chan[0])


def calc_dh2012_values(hfa_A, hfa_B, measure):
    """This is the exact translation of dh2012's Matlab code
    """
    ecog = hstack((hfa_A.data[0], hfa_B.data[0]))
    stim = hstack((ones(hfa_A.data[0].shape[1]), ones(hfa_B.data[0].shape[1]) * 0))

    val = []
    for ecog_chan in ecog:
        [r, p] = pearsonr(ecog_chan, stim)

        if measure == 'dh2012_r2':
            val.append(r ** 2 * sign(r))

        elif measure == 'dh2012_pv':
            val.append(p)

    return Data(array(val), hfa_A.s_freq, chan=hfa_A.chan[0])


def correct_baseline(freq_A, freq_B, frequency):
    move = select(freq_A, freq=frequency)
    rest = select(freq_B, freq=frequency)

    merged = merge_datasets(move, rest)
    merged = concatenate(merged, 'time')
    baseline = math(merged, operator_name='mean', axis='time')

    move.data[0] /= baseline.data[0][:, None, :]
    rest.data[0] /= baseline.data[0][:, None, :]
    return move, rest


def merge_datasets(dat1, dat2):
    both = dat1._copy(axis=False)
    both.data = np_concatenate((dat1.data, dat2.data))
    both.axis['time'] = np_concatenate((dat1.time, dat2.time))
    both.axis['chan'] = np_concatenate((dat1.chan, dat2.chan))
    both.axis['freq'] = np_concatenate((dat1.freq, dat2.freq))
    return both


def find_longest_match(taskA, taskB):
    s = SequenceMatcher(a=taskA, b=taskB).find_longest_match(0, len(taskA), 0, len(taskB))
    return taskA[s.a:(s.a + s.size)]
