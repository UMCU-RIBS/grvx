from pickle import load, dump
from logging import getLogger
from multiprocessing import Pool
import warnings
from numpy import (array,
                   diff,
                   empty,
                   mean,
                   percentile,
                   pi,
                   stack,
                   roll,
                   )

from scipy.signal import (iirdesign,
                          lfilter,
                          group_delay,
                          )
from scipy.stats.mstats import gmean

from bidso.find import find_in_bids
from bidso.utils import replace_extension

from wonambi.trans import math

lg = getLogger(__name__)


def main(analysis_dir, bands=[], method="5", noparallel=False):
    """
    extract timefrequency after bandpass

    Parameters
    ----------
    analysis_dir : path

    bands : str
        write down frequency bands as 70-90,90-110 (no spaces)
    method : str
        "1", "2", "3", "4", "5"
    noparallel : bool
        if it should run serially (i.e. not parallely, mostly for debugging)
    """
    # convert str "70-90,90-110" to [[70, 90], [90, 110]]
    bands = [[float(f) for f in b.split('-')] for b in bands.split(',')]

    args = []
    for ieeg_file in find_in_bids(analysis_dir, modality='ieegproc', extension='.pkl', generator=True):
        args.append((ieeg_file, bands, method))

    if noparallel:
        for arg in args:
            save_frequency(*arg)
    else:
        with Pool() as p:
            p.starmap(save_frequency, args)


def save_frequency(ieeg_file, bands, method):
    with ieeg_file.open('rb') as f:
        data = load(f)

    data = butterpass_eeglabdata(data, bands)
    data = extract_broadband(data, method)

    output_file = replace_extension(ieeg_file, 'broadband.pkl')
    with output_file.open('wb') as f:
        dump(data, f)


def butterpass_eeglabdata(data, bands=[]):
    data1 = data._copy()
    data1.axis['filter'] = empty(data.number_of('trial'), dtype='O')
    data1.data = empty(data.number_of('trial'), dtype='O')

    for i in range(data.number_of('trial')):
        data1.axis['filter'][i] = array([f'{bp[0]}-{bp[1]}' for bp in bands])
        trial = []
        for bp in bands:
            trial.append(butterpass_eeglabdata_core(data(trial=i), bp, data.s_freq))

        data1.data[i] = stack(trial, axis=2)

    return data1


def butterpass_eeglabdata_core(signal, band, srate, Rp=3, Rs=60, bw=.5):

    nyqLimit = srate / 2
    Fpass1 = band[0] / nyqLimit
    Fpass2 = band[1] / nyqLimit
    Fstop1 = Fpass1 * bw
    Fstop2 = Fpass2 / bw

    b, a = iirdesign([Fpass1, Fpass2], [Fstop1, Fstop2], Rp, Rs, ftype='butter', output='ba')
    y = lfilter(b, a, signal)

    # measure time shift of filter
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        f, gd = group_delay((b, a), int(srate), False)
    f = f * nyqLimit / pi
    shift_frames = int(mean(gd[(f > band[0]) & (f <= band[1])]))

    # correct for time shift of filter
    return roll(y, -shift_frames)


def whiten(x):
    return (x - x.mean()) / diff(percentile(x, [.25, .75]))


def extract_broadband(data, method):

    if method == '1':  # 'abs(hilbert)'
        data = math(data, operator=whiten)
        data = math(data, operator=mean, axis='filter')
        data = math(data, operator_name=['hilbert', 'abs'], axis='time')

    elif method == '2':  # 'abs(hilbert(bp))'
        data = math(data, operator=whiten)
        data = math(data, operator_name='mean', axis='filter')
        data = math(data, operator_name=['hilbert', 'abs', 'square'], axis='time')

    elif method == '3':  # 'abs(hilbert(sum(whiten(bp))))'
        data = math(data, operator=whiten)
        data = math(data, operator_name=['hilbert', 'abs'], axis='time')
        data = math(data, operator=gmean, axis='filter')

    elif method == '4':  # 'sum(abs(hilbert(whiten(bp))))'
        data = math(data, operator=whiten)
        data = math(data, operator_name=['hilbert', 'abs', 'square'], axis='time')
        data = math(data, operator=gmean, axis='filter')

    elif method == '5':  # 'sum(abs(hilbert(bp)))'
        data = math(data, operator_name=['hilbert', 'abs', 'square'], axis='time')
        data = math(data, operator=gmean, axis='filter')

    return data
