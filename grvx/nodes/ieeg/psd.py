from pickle import load, dump
from logging import getLogger
from numpy import empty, array
from scipy.signal import welch

from wonambi.trans import timefrequency
from wonambi.datatype import ChanTimeFreq
from bidso.utils import replace_extension

lg = getLogger(__name__)

HALFBANDWIDTH = 2


def compute_powerspectrum(ieeg_file, method, taper, duration, output_dir):
    """
    compute psd

    Parameters
    ----------
    method : str
        "spectrogram" or "dh2012"
    taper : str
        "dpss", "boxcar", "hann" (only if method=='spectrogram')
    duration : float
        duration of the trials
    """

    with ieeg_file.open('rb') as f:
        dat = load(f)

    if method == 'spectrogram':
        freq = compute_frequency(dat, taper, duration)
    elif method == 'dh2012':
        freq = compute_welch_dh2012(dat, duration)
    else:
        raise ValueError(f'Unknown method "{method}"')

    output_file = output_dir / replace_extension(ieeg_file.name, 'psd.pkl')
    with output_file.open('wb') as f:
        dump(freq, f)

    return output_file


def compute_frequency(dat, taper, duration):
    """Remove epochs which have very high activity in high-freq range, then
    average over time (only high-freq range) and ALL the frequencies."""

    dat = timefrequency(
        dat,
        method='spectrogram',
        taper=taper,
        duration=duration,
        halfbandwidth=HALFBANDWIDTH,
        )

    return dat


def compute_welch_dh2012(data, duration):
    NPERSEG = 102
    NFFT = data.s_freq * duration

    freq = ChanTimeFreq()
    freq.s_freq = data.s_freq
    freq.start_time = data.start_time
    freq.axis['chan'] = data.axis['chan']
    freq.axis['freq'] = empty(data.number_of('trial'), dtype='O')
    freq.axis['time'] = empty(data.number_of('trial'), dtype='O')
    freq.data = empty(data.number_of('trial'), dtype='O')

    for i, x in enumerate(data.data):
        [f, Pxx] = welch(x, window='hamming', fs=data.s_freq, nperseg=NPERSEG,
                         nfft=NFFT, noverlap=0, detrend=False)
        freq.freq[i] = f
        freq.time[i] = array([i, ], dtype='float')
        freq.data[i] = Pxx[:, None, :]

    return freq
