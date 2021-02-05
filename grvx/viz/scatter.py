from bidso.utils import read_tsv
from numpy import argmax
import plotly.graph_objs as go

from .utils import to_div
from ..nodes.corr.corrfmri import select_channels


def plot_scatter(parameters, subject):

    pvalue = parameters['corr']['pvalue']

    fmri_dir = parameters['paths']['output'] / f'workflow/fmri/_subject_{subject}/at_elec'
    fmri_file = next(fmri_dir.glob(f'sub-{subject}_*_compare.tsv'))

    ieeg_dir = parameters['paths']['output'] / f'workflow/ieeg/_subject_{subject}/ecog_compare'
    ecog_file = next(ieeg_dir.glob(f'sub-{subject}_*_compare.tsv'))

    corr_dir = parameters['paths']['output'] / f'workflow/_subject_{subject}/corr_fmri_ecog/corr_values/'
    corr_file = next(corr_dir.glob(f'sub-{subject}_*_r2.tsv'))

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

    return to_div(fig)
