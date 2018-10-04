from numpy import arange
from scipy.stats import norm
import plotly.graph_objs as go
from exportimages import export_plotly

import colorlover as cl


def plot_gaussian(wd):
    x = arange(0, 30, .05)

    layout = go.Layout(
        xaxis=dict(
            dtick=4,
            tickfont=dict(
                size=8,
                ),
            ),
        yaxis=dict(
            dtick=1,
            tickfont=dict(
                size=8,
                ),
            ),
        )

    colorscale = cl.scales['9']['seq']['Blues']
    scales = cl.interp(colorscale, 30)

    traces = []
    for i, K in enumerate(arange(1, 11)):

        y = norm.pdf(x, scale=K) / norm.pdf(0, scale=K)
        traces.append(dict(
            x=x,
            y=y,
            name=f'{K:d}mm',
            marker=dict(
                color=scales[i * 2 + 5],
                ),
            ))

    fig = go.Figure(
        data=traces,
        layout=layout,
        )

    export_plotly(fig, 'gaussian.svg', int(4.5 * 90), int(6 * 90), wd)
