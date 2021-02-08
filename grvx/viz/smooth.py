from numpy import gradient
import plotly.graph_objs as go

from bidso.utils import read_tsv

from .utils import to_div
from .paths import get_path


def plot_smooth(parameters, frequency_band, subject):

    corr_file = get_path(parameters, 'corr', frequency_band=frequency_band, subject=subject)
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
            range=(0, 20),
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
    divs = [to_div(fig), ]

    traces = [
        dict(
            x=results['Kernel'],
            y=gradient(gradient(results['Rsquared'])),
            marker=dict(
                color='black',
                ),
            ),
        ]

    layout.update(dict(
        yaxis=dict(
            dtick=0.002,
            range=(-0.005, 0.005),
            ),
        ))

    fig = go.Figure(
        data=traces,
        layout=layout,
        )

    divs.append(to_div(fig))
    return divs
