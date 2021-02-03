from numpy import arange
from scipy.stats import norm
import plotly.graph_objs as go

import colorlover as cl

from .utils import to_html, to_div


def plot_gaussian(plot_dir):
    x = arange(0, 30, .05)

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
        layout=go.Layout(
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
        )

    to_html([to_div(fig), ], plot_dir / 'gaussian.html')
