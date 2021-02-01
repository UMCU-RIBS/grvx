def read_prf():
    prestim = float(prestim)
    poststim = float(poststim)

    d = Dataset(ieeg_file, bids=True)
    events = array([x['start'] for x in d.read_markers()])

    data = d.read_data(
        begtime=list(events - prestim),
        endtime=list(events + poststim + 1 / d.header['s_freq']))
    data.attr['stimuli'] = read_prf_stimuli(d.dataset.task)
    all_data = (data, )
    conds = ['', ]



def read_prf_stimuli(task):
    """Read stimuli to compute the PRF

    Parameters
    ----------
    task : instance of bidso.Task
        task containing the events and filename
    """
    stimuli_dir = find_root(task.filename) / 'stimuli'

    stim_file = stimuli_dir / task.events.tsv[0]['stim_file']
    if stim_file.suffix == '.npy':
        stimuli = load(stim_file)

    elif stim_file.suffix == '.mat':
        mat = loadmat(stim_file)
        stimuli = mat['stimulus'][0, 0]['images']

    stim_file_index = array([int(x['stim_file_index']) - 1 for x in task.events.tsv])
    stimuli = stimuli[:, :, stim_file_index]

    return stimuli
