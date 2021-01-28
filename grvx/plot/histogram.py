from bidso.utils import read_tsv
import plotly.graph_objs as go
from pathlib import Path


COLOR = {
    'clinical': 'rgb(0, 0, 255)',
    'experimental': 'rgb(255, 0, 0)',
    }

SHIFT = 'middle'  # middle / whole


def plot_histogram(wd):
    summary = read_tsv(Path('/Fridge/users/giovanni/projects/grvx/derivatives/nipype/grvx/corr_fmri_ecog_summary/output/summary_per_subject.tsv'))

    for value_type in ('size_at_peak', 'r2_at_peak', 'size_at_concave'):

        if value_type in ('size_at_peak', 'size_at_concave'):
            bin_size = 1
            dtick = 4
            max_val = 20
        elif value_type == 'r2_at_peak':
            bin_size = .1
            dtick = 0.2
            max_val = 1

        if SHIFT == 'middle':
            xbins = dict(
                start=bin_size / -2,
                end=max_val + bin_size / 2,
                size=bin_size,
                )

        else:
            xbins = dict(
                start=0,
                end=max_val + bin_size,
                size=bin_size,
                )

        traces = []
        for acq in set(summary['acquisition']):

            values = summary[summary['acquisition'] == acq][value_type]
            traces.append(
                go.Histogram(
                    x=values,
                    xbins=xbins,
                    name=acq,
                    marker=dict(
                        color=COLOR[acq],
                        ),
                ))

        layout = go.Layout(
            barmode='stack',
            showlegend=False,
            xaxis=dict(
                range=(0, max_val + bin_size / 2),
                dtick=dtick,
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

        fig = go.Figure(
            data=traces,
            layout=layout,
            )
        export_plotly(fig, f'histogram_{value_type}.svg', int(3 * 96), int(5 * 96), wd)
