from bidso.utils import read_tsv
import plotly.graph_objs as go
from exportimages import export_plotly
from pathlib import Path


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

        xbins = dict(
            start=bin_size / -2,
            end=max_val + bin_size / 2,
            size=bin_size,
            )

        traces = []
        for acq in set(summary['acquisition']):

            values = summary[summary['acquisition'] == acq][value_type]
            traces.append(
                go.Histogram(
                    x=values,
                    xbins=xbins,
                    name=acq
                ))

        layout = go.Layout(
            barmode='stack',
            xaxis=dict(
                range=(0, max_val + bin_size / 2),
                dtick=dtick,
                ),
            yaxis=dict(
                title='# participants',
                dtick=1,
                ),
            )

        fig = go.Figure(
            data=traces,
            layout=layout,
            )
        export_plotly(fig, f'histogram_{value_type}.svg', int(3 * 96), int(5 * 96), wd)
