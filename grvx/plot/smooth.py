from pathlib import Path
from numpy import gradient
import plotly.graph_objs as go
from exportimages import export_plotly

from bidso.utils import read_tsv


def plot_smooth(wd):
    one_tsv = '/Fridge/users/giovanni/projects/grvx/derivatives/nipype/grvx/_subject_delft/corr_fmri_ecog/corr_values/sub-delft_ses-UMCUECOGday01_task-motorHandLeft_run-1_acq-clinical_bold_r2.tsv'
    one_tsv = Path(one_tsv)
    results = read_tsv(one_tsv)

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
            dtick=0.25,
            tickfont=dict(
                size=8,
                ),
            ),
        )

    fig = go.Figure(
        data=traces,
        layout=layout,
        )
    export_plotly(fig, 'smooth_r2.svg', int(3 * 96), int(5 * 96), wd)

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
    export_plotly(fig, 'smooth_deriv.svg', int(3 * 96), int(5 * 96), wd)
