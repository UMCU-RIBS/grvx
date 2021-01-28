from pathlib import Path
from numpy import gradient
import plotly.graph_objs as go

from bidso.utils import read_tsv
from bidso import file_Core


def plot_smooth(wd):
    for one_tsv in Path('/Fridge/users/giovanni/projects/grvx/derivatives/nipype/grvx/corr_fmri_ecog_summary/output/rsquared').glob('*.tsv'):
        results = read_tsv(one_tsv)
        subject = file_Core(one_tsv).subject

        traces = [
            dict(
                x=results['Kernel'],
                y=results['Rsquared'],
                marker=dict(
                    color='k',
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
        export_plotly(fig, f'smooth_{subject}_r2.svg', int(3 * 96), int(5 * 96), wd)

        traces = [
            dict(
                x=results['Kernel'],
                y=gradient(gradient(results['Rsquared'])),
                marker=dict(
                    color='k',
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
        export_plotly(fig, f'smooth_{subject}_deriv.svg', int(3 * 96), int(5 * 96), wd)
