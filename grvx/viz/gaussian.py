from numpy import arange
from scipy.stats import norm
import plotly.graph_objs as go

import colorlover as cl


def plot_gaussian():
    x = arange(0, 30, .05)

    colorscale = cl.scales['9']['seq']['PuBuGn']
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
                linecolor='black',
                gridcolor='black',
                dtick=4,
                tickfont=dict(
                    size=8,
                    ),
                ),
            yaxis=dict(
                linecolor='black',
                gridcolor='black',
                tickmode='array',
                tickvals=[0, 1],
                ticktext=[0, 'MAX'],
                tickfont=dict(
                    size=8,
                    ),
                ),
            legend=dict(
                title=dict(
                    text='kernel σ',
                    font=dict(
                        size=10,
                        ),
                    ),
                itemwidth=30,
                font=dict(
                    size=8,
                    ),
                ),
            )
        )

    return fig
