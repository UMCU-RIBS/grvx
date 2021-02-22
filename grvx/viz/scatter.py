from bidso.utils import read_tsv
from numpy import argmax
import plotly.graph_objs as go

from .utils import to_div
from .paths import get_path
from ..nodes.corr.corrfmri import select_channels


def plot_scatter(parameters, frequency_band, subject):

    pvalue = parameters['corr']['pvalue']

    ecog_file = get_path(parameters, 'ieeg_tsv', frequency_band=frequency_band, subject=subject)
    fmri_file = get_path(parameters, 'fmri_tsv', subject=subject)
    corr_file = get_path(parameters, 'corr_tsv', frequency_band=frequency_band, subject=subject)
    if ecog_file is None or fmri_file is None or corr_file is None:
        return

    fmri_tsv = read_tsv(fmri_file)
    ecog_tsv = read_tsv(ecog_file)
    fmri_tsv = select_channels(fmri_tsv, ecog_tsv)
    corr_tsv = read_tsv(corr_file)
    kernel, r2_max, slope, intercept = corr_tsv[argmax(corr_tsv['Rsquared'])]

    x_ecog = ecog_tsv['measure']
    y_fmri = fmri_tsv[str(kernel)]

    traces = [
        go.Scatter(
            text=ecog_tsv['channel'][ecog_tsv['pvalue'] > pvalue],
            x=x_ecog[ecog_tsv['pvalue'] > pvalue],
            y=y_fmri[ecog_tsv['pvalue'] > pvalue],
            mode='markers',
            name='',
            marker=dict(
                symbol='circle',
                color='rgb(204, 204, 204)',
                )
            ),
        go.Scatter(
            text=ecog_tsv['channel'][ecog_tsv['pvalue'] <= pvalue],
            x=x_ecog[ecog_tsv['pvalue'] <= pvalue],
            y=y_fmri[ecog_tsv['pvalue'] <= pvalue],
            mode='markers',
            name='',
            marker=dict(
                symbol='circle',
                color='rgb(0, 0, 0)',
                )
            ),
        go.Scatter(
            x=x_ecog,
            y=slope * x_ecog + intercept,
            mode='lines',
            marker=dict(
                color='black'
                ),
            ),
        ]

    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            showlegend=False,
        ),
        )

    return fig
