"""Put in this module functions that might end up in bidso because they are
reused often.
"""

def find_labels_in_regions(electrodes, regions):

    if len(regions) > 0:
        select_regions = lambda x: x['region'] in regions
    else:
        select_regions = lambda x: True

    return electrodes.electrodes.get(filter_lambda=select_regions,
                                     map_lambda=lambda x: x['name'])


def read_channels(ecog_tsv, labels, COLUMN):
    """Read the columns from an ecog_tsv file, in the order of labels.

    Parameters
    ----------
    ecog_tsv : list of dict
        list of dictionary (such as '_compare.tsv')
    labels : list of str
        list of channels to read
    COLUMN : str
        which column of ecog_tsv to read

    Returns
    -------
    list of str
        list of channels with values
    list of float
        list of ecog_tsv values taken from COLUMN in the order specified by
        labels
    """
    good_labels = []
    vals = []
    for l in labels:
        try:
            vals.append([float(x[COLUMN]) for x in ecog_tsv if x['channel'] == l][0])
        except IndexError:  # no electrode in ecog_tsv
            continue
        else:
            good_labels.append(l)

    return good_labels, vals
