from numpy import log10
from pickle import load
import plotly.graph_objects as go

from .utils import to_div
from .paths import get_path


def plot_allfreq(parameters, subject):

    allfreq_file = get_path(parameters, 'allfreq', subject=subject)
    if allfreq_file is None:
        return

    with allfreq_file.open('rb') as f:
        rsquared, slope, pvalue, axes = load(f)

    sign = pvalue < 0.05
    rsquared[~sign] = 0
    slope[~sign] = 0

    layout = go.Layout(
        yaxis=dict(
            range=(0, 100)
            )
        )

    traces = [
        go.Heatmap(
            x=axes['kernels'],
            y=axes['freq'],
            z=-log10(pvalue),
            colorscale='Hot',
            zmin=0,
            zmax=4,
        )
    ]
    fig = go.Figure(
        data=traces,
        layout=layout
        )
    divs = [to_div(fig), ]

    traces = [
        go.Heatmap(
            x=axes['kernels'],
            y=axes['freq'],
            z=rsquared,
            colorscale='Hot',
            zmin=0,
            zmax=1,
        )
        ]
    fig = go.Figure(
        data=traces,
        layout=layout
        )
    divs.append(to_div(fig))

    traces = [
        go.Heatmap(
            x=axes['kernels'],
            y=axes['freq'],
            z=slope,
            colorscale='balance',
            zmin=-0.5,
            zmax=0.5,
        )
        ]
    fig = go.Figure(
        data=traces,
        layout=layout
        )
    divs.append(to_div(fig))

    return divs
