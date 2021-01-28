from bidso.utils import read_tsv
from boavus.corr.corrfmri import select_channels
import plotly.graph_objs as go
from pathlib import Path

pvalue = 0.05  # TODO: PARAMETERS


def plot_scatter(wd):
    summary = read_tsv(Path('/Fridge/users/giovanni/projects/grvx/derivatives/nipype/grvx/corr_fmri_ecog_summary/output/summary_per_subject.tsv'))
    ecog_file = Path('/Fridge/users/giovanni/projects/grvx/derivatives/nipype/grvx/corr_fmri_ecog_summary/output/ecog/sub-delft_ses-UMCUECOGday01_task-motorHandLeft_run-1_acq-clinical_compare.tsv')
    fmri_file = Path('/Fridge/users/giovanni/projects/grvx/derivatives/nipype/grvx/corr_fmri_ecog_summary/output/fmri/sub-delft_ses-UMCU3Tdaym13_task-motorHandLeft_run-1_bold_compare.tsv')

    fmri_tsv = read_tsv(fmri_file)
    ecog_tsv = read_tsv(ecog_file)
    fmri_tsv = select_channels(fmri_tsv, ecog_tsv)

    kernel = str(summary[summary['subject'] == 'delft']['size_at_peak'].item())
    slope = summary[summary['subject'] == 'delft']['slope_at_peak']
    intercept = summary[summary['subject'] == 'delft']['intercept_at_peak']

    x_ecog = ecog_tsv['measure']
    y_fmri = fmri_tsv[kernel]

    traces = [
        go.Scatter(
            name='not significant',
            x=x_ecog[ecog_tsv['pvalue'] > pvalue],
            y=y_fmri[ecog_tsv['pvalue'] > pvalue],
            mode='markers',
            marker=go.Marker(
                symbol='circle',
                color='rgb(204, 204, 204)',
                )
            ),
        go.Scatter(
            name='significant',
            x=x_ecog[ecog_tsv['pvalue'] <= pvalue],
            y=y_fmri[ecog_tsv['pvalue'] <= pvalue],
            mode='markers',
            marker=go.Marker(
                symbol='circle',
                color='rgb(0, 0, 0)',
                )
            ),
        go.Scatter(
            x=x_ecog,
            y=slope * x_ecog + intercept,
            mode='lines',
            marker=go.Marker(
                color='black'
                ),
            ),
        ]

    layout = go.Layout(
        showlegend=False,
        xaxis=dict(
            tickfont=dict(
                size=8,
                ),
            ),
        yaxis=dict(
            tickfont=dict(
                size=8,
                ),
            ),
        )

    fig = go.Figure(
        data=traces,
        layout=layout,
        )

    export_plotly(fig, 'scatter.svg', int(3 * 96), int(5 * 96), wd)
