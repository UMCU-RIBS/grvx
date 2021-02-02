from numpy import gradient
import plotly.graph_objs as go

from bidso.utils import read_tsv
from bidso import file_Core

from .utils import to_html, to_div


def plot_smooth(plot_dir, parameters):
    rsquared_dir = parameters['paths']['output'] / 'nipype/grvx/corr_fmri_ecog_summary/output/rsquared'
    for one_tsv in rsquared_dir.glob('*.tsv'):
        results = read_tsv(one_tsv)
        subject = file_Core(one_tsv).subject

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
                tickfont=dict(
                    size=8,
                    ),
                ),
            yaxis=dict(
                dtick=0.1,
                rangemode='tozero',
                tickfont=dict(
                    size=8,
                    ),
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

        divs = [to_div(fig), ]
        to_html(divs, plot_dir / 'smooth' / f'{subject}_r2.html')
