from logging import getLogger
from numpy import mean, std
from pickle import dump
from wonambi import Dataset
from wonambi.trans import math, concatenate
from bidso import Task, Electrodes

lg = getLogger(__name__)


def read_ieeg_block(filename, electrode_file, cond, minimalduration, output_dir):
    d = Dataset(filename, bids=True)
    markers = d.read_markers()

    electrodes = Electrodes(electrode_file)
    elec_names = [x['name'] for x in electrodes.electrodes.tsv]
    elec_names = [x for x in elec_names if x in d.header['chan_name']]  # exclude elec location that have no corresponding channel

    clean_labels = _reject_channels(d, elec_names, cond, minimalduration)

    outputs = []
    for cond_name in cond:
        block_beg = []
        block_end = []

        for mrk in markers:

            if mrk['name'] in cond_name:
                dur = (mrk['end'] - mrk['start'])
                if dur >= minimalduration:
                    block_beg.append(mrk['start'])
                    block_end.append(mrk['end'])

        data = d.read_data(begtime=block_beg, endtime=block_end, chan=clean_labels)

        output_task = Task(filename)
        output_task.extension = '.pkl'
        output_task.task += cond_name
        output_file = output_dir / output_task.get_filename()
        with output_file.open('wb') as f:
            dump(data, f)
        outputs.append(output_file)

    return outputs


def _reject_channels(d, elec_names, cond, minimalduration):
    markers = d.read_markers()
    block_beg = []
    block_end = []
    for mrk in markers:
        if mrk['name'] in cond:
            dur = (mrk['end'] - mrk['start'])
            if dur >= minimalduration:

                block_beg.append(mrk['start'])
                block_end.append(mrk['end'])

    data = d.read_data(chan=elec_names, begtime=block_beg, endtime=block_end)
    data = concatenate(data, 'time')

    clean_labels = reject_channels(data, 3)
    return clean_labels


def reject_channels(dat, reject_chan_thresh):
    dat_std = math(dat, operator_name='nanstd', axis='time')
    THRESHOLD = reject_chan_thresh
    x = dat_std.data[0]
    thres = [mean(x) + THRESHOLD * std(x)]
    clean_labels = list(dat_std.chan[0][dat_std.data[0] < thres])
    return clean_labels
