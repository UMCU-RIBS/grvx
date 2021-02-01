from logging import getLogger
from pickle import load, dump
from numpy import empty, arange
from wonambi.trans import montage
from wonambi.trans.select import _create_subepochs

from bidso.utils import replace_extension


lg = getLogger(__name__)


def preprocess_ecog(ieeg_file, reref, duration, offset, output_dir):
    """

    Parameters
    ----------
    reref : str
        'average' or 'regression'
    duration : int
        length of the segments
    offset : bool
        remove one sample for whole duration

    TODO
    ----
    labels_in_roi = find_labels_in_regions(electrodes, regions)
    clean_roi_labels = [label for label in clean_labels if label in labels_in_roi]
    data = select(data, chan=clean_roi_labels)
    """
    with ieeg_file.open('rb') as f:
        data = load(f)

    data = montage(data, ref_to_avg=True, method=reref)
    data = make_segments(data, duration, offset)

    output_file = output_dir / replace_extension(ieeg_file.name, 'proc.pkl')
    with output_file.open('wb') as f:
        dump(data, f)

    return output_file


def make_segments(dat, duration=2, offset=True):

    dur_smp = int(dat.s_freq * duration)
    if offset:
        dur_smp -= 1

    trials = []
    for d in dat.data:
        v = _create_subepochs(d, dur_smp, dur_smp)
        for i in range(v.shape[1]):
            trials.append(v[:, i, :])

    out = dat._copy(axis=False)
    out.data = empty(len(trials), dtype='O')
    out.axis['chan'] = empty(len(trials), dtype='O')
    out.axis['time'] = empty(len(trials), dtype='O')

    for i, trial in enumerate(trials):
        out.data[i] = trial
        out.axis['time'][i] = arange(i * dur_smp, i * dur_smp + dur_smp) / dat.s_freq
        out.axis['chan'][i] = dat.axis['chan'][0]

    return out
