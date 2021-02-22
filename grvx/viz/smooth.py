from numpy import gradient
import plotly.graph_objs as go

from bidso.utils import read_tsv

from .paths import get_path


def plot_smooth(parameters, frequency_band, subject):

    corr_file = get_path(parameters, 'corr_tsv', frequency_band=frequency_band, subject=subject)
    if corr_file is None:
        return

    results = read_tsv(corr_file)

    traces = [
        dict(
            x=results['Kernel'],
            y=results['Rsquared'],
            marker=dict(
                color='black',
                ),
            ),
        ]

    layout = go.Layout(
        xaxis=dict(
            dtick=4,
            range=(
                0,
                parameters['fmri']['at_elec']['kernel_end']
                ),
            ),
        yaxis=dict(
            dtick=0.02,
            rangemode='tozero',
            ),
        )

    fig = go.Figure(
        data=traces,
        layout=layout,
        )
    return fig


def plot_gradient(parameters, frequency_band, subject):

    corr_file = get_path(parameters, 'corr_tsv', frequency_band=frequency_band, subject=subject)
    if corr_file is None:
        return

    results = read_tsv(corr_file)

    traces = [
        dict(
            x=results['Kernel'],
            y=gradient(gradient(results['Rsquared'])),
            marker=dict(
                color='black',
                ),
            ),
        ]

    layout = go.Layout(
        xaxis=dict(
            dtick=4,
            range=(
                0,
                parameters['fmri']['at_elec']['kernel_end']
                ),
            ),
        yaxis=dict(
            dtick=0.002,
            range=(-0.005, 0.005),
            ),
        )

    fig = go.Figure(
        data=traces,
        layout=layout,
        )

    return fig
