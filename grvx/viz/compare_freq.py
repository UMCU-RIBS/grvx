from numpy import max, r_, mean
from scipy.stats import ttest_rel
from scipy.stats import linregress
from bidso.utils import read_tsv
import plotly.graph_objs as go

from .paths import get_path

axis_label = lambda freq: f'Frequency {freq[0]} - {freq[1]} Hz'


def plot_freq_comparison(parameters):
    freqA = parameters['ieeg']['ecog_compare']['frequency_bands'][parameters['plot']['compare']['freqA']]
    freqB = parameters['ieeg']['ecog_compare']['frequency_bands'][parameters['plot']['compare']['freqB']]

    actA = read_tsv(get_path(parameters, 'summary_tsv', frequency_band=freqA))
    actB = read_tsv(get_path(parameters, 'summary_tsv', frequency_band=freqB))

    max_r = max(r_[actA['r2_at_peak'], actB['r2_at_peak']])
    result = ttest_rel(actA['r2_at_peak'], actB['r2_at_peak'])

    traces = [
        go.Scatter(
            x=actA['r2_at_peak'],
            y=actB['r2_at_peak'],
            text=actA['subject'],
            mode='markers',
            marker=dict(
                color='black',
            ),
        )
    ]

    figs = []
    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            height=500,
            width=500,
            title=dict(
                text=f'R<sup>2</sub> values (paired t-test, <i>p</i> = {result.pvalue:0.03f})'
            ),
            xaxis=dict(
                title=dict(
                    text=axis_label(freqA),
                    ),
                tick0=0,
                dtick=0.1,
                range=[0, max_r + 0.1],
                ),
            yaxis=dict(
                title=dict(
                    text=axis_label(freqB),
                    ),
                tick0=0,
                dtick=0.1,
                range=[0, max_r + 0.1],
                ),
            shapes=[
                dict(
                    type='line',
                    layer='below',
                    x0=0,
                    x1=max_r + 0.1,
                    y0=0,
                    y1=max_r + 0.1,
                    line=dict(
                        color='gray',
                    )
                )
            ]
        )
        )
    figs.append(fig)

    for param in ('size_at_peak', 'size_at_concave'):
        fig = _plot_compare_size(actA, actB, param, parameters, freqA, freqB)
        figs.append(fig)

    param = 'slope_at_peak'
    min_r = min(r_[actA[param], actB[param]])
    max_r = max(r_[actA[param], actB[param]])
    diff_act = mean(actA[param] - actB[param])
    result = ttest_rel(actA[param], actB[param])
    regr = linregress(actA['slope_at_peak'], actB['slope_at_peak'])

    traces = [
        go.Scatter(
            x=actA[param],
            y=actB[param],
            text=actA['subject'],
            mode='markers',
            marker=dict(
                color='black',
            ),
        )
    ]

    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            height=500,
            width=500,
            title=dict(
                text=f'Difference [{freqA[0]}-{freqA[1]}] Hz - [{freqB[0]}-{freqB[1]}] Hz = {diff_act:0.2f}<br />paired t-test, <i>p</i> = {result.pvalue:0.03f}<br />regression slope = {regr.slope:0.3f} <i>p</i> = {regr.pvalue:0.03f}'
            ),
            xaxis=dict(
                title=dict(
                    text=axis_label(freqA),
                    ),
                tick0=0,
                dtick=0.2,
                range=[min_r - 0.1, max_r + 0.1],
                ),
            yaxis=dict(
                title=dict(
                    text=axis_label(freqB),
                    ),
                tick0=0,
                dtick=0.2,
                range=[min_r - 0.1, max_r + 0.1],
                scaleanchor="x",
                scaleratio=1,
                ),
            shapes=[
                dict(
                    type='line',
                    layer='below',
                    x1=-min_r - 0.1,
                    x0=-max_r - 0.1,
                    y1=min_r + 0.1,
                    y0=max_r + 0.1,
                    line=dict(
                        color='gray',
                    )
                ),
                dict(
                    type='line',
                    layer='below',
                    x0=0,
                    x1=1,
                    y0=0,
                    y1=0,
                    xref='paper',
                    line=dict(
                        width=2,
                        color='gray',
                    )
                ),
                dict(
                    type='line',
                    layer='below',
                    x0=0,
                    x1=0,
                    y0=0,
                    y1=1,
                    yref='paper',
                    line=dict(
                        width=2,
                        color='gray',
                    )
                ),
            ]
        )
        )
    figs.append(fig)

    return figs


def _plot_compare_size(actA, actB, param, parameters, freqA, freqB):
    diff_act = mean(actA[param] - actB[param])
    result = ttest_rel(actA[param], actB[param])

    traces = [
        go.Scatter(
            x=actA[param],
            y=actB[param],
            text=actA['subject'],
            mode='markers',
            marker=dict(
                color='black',
            ),
        )
    ]

    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            height=500,
            width=500,
            title=dict(
                text=f'{param}<br />Difference [{freqA[0]}-{freqA[1]}] Hz - [{freqB[0]}-{freqB[1]}] Hz = {diff_act:0.2f}<br />paired t-test, <i>p</i> = {result.pvalue:0.03f}'
            ),
            xaxis=dict(
                title=dict(
                    text=axis_label(freqA),
                    ),
                tick0=0,
                dtick=5,
                range=[0, parameters['fmri']['at_elec']['kernel_end'] + 1],
                ),
            yaxis=dict(
                title=dict(
                    text=axis_label(freqB),
                    ),
                tick0=0,
                dtick=5,
                range=[0, parameters['fmri']['at_elec']['kernel_end'] + 1],
                scaleanchor="x",
                scaleratio=1,
                ),
            shapes=[
                dict(
                    type='line',
                    layer='below',
                    x0=0,
                    x1=parameters['fmri']['at_elec']['kernel_end'] + 1,
                    y0=0,
                    y1=parameters['fmri']['at_elec']['kernel_end'] + 1,
                    line=dict(
                        color='gray',
                    )
                )
            ]
        )
        )

    return fig
