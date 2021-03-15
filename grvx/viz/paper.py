from shutil import rmtree
from wonambi.attr import Freesurfer
from bidso import Electrodes
from bidso.utils import read_tsv
import plotly.graph_objs as go
from numpy import where, concatenate, mean
from subprocess import run

from .paths import get_path
from .surfaces import AXIS, project_mri_to_surf
from .gaussian import plot_gaussian
from .scatter import plot_scatter
from .smooth import plot_smooth, plot_gradient
from .histogram import plot_histogram
from .utils import merge, LAYOUT
from .compare_freq import plot_freq_comparison
from .revision import revision


def plot_results(parameters):

    revision(parameters)

    return

    plot_dir = parameters['paths']['output'] / 'paper'
    try:
        rmtree(plot_dir)
    except OSError:
        pass
    plot_dir.mkdir(exist_ok=True, parents=True)

    fig = plot_gaussian()
    layout = dict(
        width=250,
        height=180,
        )
    fig.update_layout(merge(LAYOUT, layout))
    fig.write_image(str(plot_dir / 'gaussian.svg'))

    for freq in parameters['ieeg']['ecog_compare']['frequency_bands']:

        freq_dir = plot_dir / f"frequency_{freq[0]}_{freq[1]}"
        freq_dir.mkdir(exist_ok=True, parents=True)

        fig = paper_plot_scatter(parameters, freq)
        fig.write_image(str(freq_dir / 'scatter.svg'))

        fig = paper_plot_smooth(parameters, freq)
        fig.write_image(str(freq_dir / 'smooth.svg'))

        fig = paper_plot_gradient(parameters, freq)
        fig.write_image(str(freq_dir / 'gradient.svg'))

        figs = paper_plot_histogram(parameters, freq)
        for fig, value_type in zip(figs, ('r2_at_peak', 'size_at_peak', 'size_at_concave')):
            fig.write_image(str(freq_dir / f'{value_type}.svg'))

    # TODO: this should be specified in parameters.json
    freq = parameters['ieeg']['ecog_compare']['frequency_bands'][-1]
    subjects = [x.stem[4:] for x in parameters['paths']['input'].glob('sub-*')]
    for subject in subjects:
        fig = plot_smooth(parameters, freq, subject)
        fig.write_image(str(freq_dir / f'{subject}_smooth.svg'))

        fig = paper_plot_surf_ecog(parameters, freq, subject)
        fig_name = str(freq_dir / f'{subject}_surface_ecog.png')
        fig.write_image(fig_name)
        run(['convert', fig_name, '-trim', fig_name])

        fig = paper_plot_surf_bold(parameters, subject)
        fig_name = str(freq_dir / f'{subject}_surface_bold.png')
        fig.write_image(fig_name)
        run(['convert', fig_name, '-trim', fig_name])

    figs = paper_plot_freq_comparison(parameters)
    names = (
        'comparefreq_r2_at_peak',
        'comparefreq_size_at_peak',
        'comparefreq_size_at_concave',
        )
    for fig, name in zip(figs, names):
        fig.write_image(str(plot_dir / f'{name}.svg'))


def paper_plot_scatter(parameters, freq):

    fig = plot_scatter(parameters, freq, parameters['plot']['subject'])

    layout = dict(
        width=500,
        height=200,
        xaxis=dict(
            showline=False,
            showgrid=False,
            title=dict(
                text='ECoG (<i>z</i>-statistics)',
                standoff=4,
                ),
            ),
        yaxis=dict(
            showline=False,
            showgrid=False,
            title=dict(
                text='fMRI (<i>z</i>-statistics)',
                standoff=8,
                ),
            ),
        shapes=[
            dict(
                type='line',
                x0=0,
                x1=1,
                xref='paper',
                y0=0,
                y1=0,
                layer='below',
                line=dict(
                    width=2,
                    color='gray',
                ),
            ),
            dict(
                type='line',
                x0=0,
                x1=0,
                y0=0,
                y1=1,
                yref='paper',
                layer='below',
                line=dict(
                    width=2,
                    color='gray',
                ),
            )

        ]
    )

    fig.update_layout(merge(LAYOUT, layout))

    return fig


def paper_plot_smooth(parameters, freq):
    fig = plot_smooth(parameters, freq, parameters['plot']['subject'])

    layout = dict(
        width=500,
        height=200,
        xaxis=dict(
            title=dict(
                text='kernel σ (mm)',
                standoff=4,
                ),
            ),
        yaxis=dict(
            title=dict(
                text='explained variance',
                standoff=8,
                ),
            dtick=0.1,
            ),
        )

    fig.update_layout(merge(LAYOUT, layout))

    return fig


def paper_plot_smooth_small(parameters, freq):
    fig = plot_smooth(parameters, freq, parameters['plot']['subject'])

    layout = dict(
        width=500,
        height=200,
        xaxis=dict(
            title=dict(
                text='',
                ),
            ),
        yaxis=dict(
            title=dict(
                text='',
                ),
            dtick=0.1,
            ),
        )

    fig.update_layout(merge(LAYOUT, layout))

    return fig

def paper_plot_gradient(parameters, freq):
    fig = plot_gradient(parameters, freq, parameters['plot']['subject'])

    layout = dict(
        width=500,
        height=200,
        xaxis=dict(
            title=dict(
                text='kernel σ (mm)',
                ),
            ),
        yaxis=dict(
            title=dict(
                text='Concavity',
                ),
            dtick=0.002,
            ),
        )

    fig.update_layout(merge(LAYOUT, layout))

    return fig


def paper_plot_histogram(parameters, freq):
    figs = plot_histogram(parameters, freq)

    layout = dict(
        width=500,
        height=200,
        xaxis=dict(
            title=dict(
                standoff=4,
            ),
            linecolor='black',
            gridcolor='lightGray',
            ),
        yaxis=dict(
            title=dict(
                text='# participants',
                standoff=8,
            ),
            linecolor='black',
            gridcolor='lightGray',
            dtick=2,
            ),

        )

    XAXIS = (
        'explained variance (r<sup>2</sup>)',
        'kernel σ (mm)',
        'kernel σ (mm)',
        )

    layout = merge(LAYOUT, layout)
    for i, xaxis in enumerate(XAXIS):
        xaxis_title = dict(xaxis=dict(title=dict(text=xaxis)))
        figs[i] = figs[i].update_layout(merge(layout, xaxis_title))

    return figs


def paper_plot_freq_comparison(parameters):
    figs = plot_freq_comparison(parameters)

    layout = dict(
        title=dict(
            text='',
            ),
        width=300,
        height=300,
        )

    layout = merge(LAYOUT, layout)
    figs = [fig.update_layout(layout) for fig in figs]

    figs[3] = figs[3].update_layout(
        dict(
            xaxis=dict(
                showgrid=False,
            ),
            yaxis=dict(
                showgrid=False,
            ),
        ))

    return figs


def paper_plot_surf_ecog(parameters, frequency_band, subject):

    elec_file = get_path(parameters, 'elec', subject=subject)
    ieeg_file = get_path(parameters, 'ieeg_tsv', frequency_band=frequency_band, subject=subject)
    freesurfer_dir = parameters['paths']['freesurfer_subjects_dir'] / f'sub-{subject}'

    compare_ieeg = read_tsv(ieeg_file)
    fs = Freesurfer(freesurfer_dir)
    electrodes = Electrodes(elec_file)

    elec = electrodes.electrodes.tsv
    all_elec = []
    labels = []
    for chan in compare_ieeg:
        i_chan = where(elec['name'] == chan['channel'])[0]
        all_elec.append(elec[i_chan])
        labels.append(f"{chan['channel']} = {chan['measure']:0.3f}")

    elec = concatenate(all_elec)

    if mean(elec['x']) > 0:
        right_or_left = 1
        hemi = 'rh'
    else:
        right_or_left = -1
        hemi = 'lh'

    fs = Freesurfer(freesurfer_dir)
    pial = getattr(fs.read_brain(), hemi)

    vert = pial.vert + fs.surface_ras_shift

    colorscale = 'balance'

    traces = [
        go.Scatter3d(
            x=elec['x'] + right_or_left,
            y=elec['y'],
            z=elec['z'] + 1,
            text=labels,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                size=5,
                color=compare_ieeg['measure'],
                colorscale=colorscale,
                showscale=False,
                cmin=-10,
                cmax=10,
                colorbar=dict(
                    title='electrodes',
                    titleside="top",
                    ticks="outside",
                    ticklabelposition="outside",
                    x=0,
                    ),
            ),
        ),
        go.Mesh3d(
            x=vert[:, 0],
            y=vert[:, 1],
            z=vert[:, 2],
            i=pial.tri[:, 0],
            j=pial.tri[:, 1],
            k=pial.tri[:, 2],
            color='gray',
            hoverinfo='skip',
            flatshading=False,
            lighting=dict(
                ambient=0.18,
                diffuse=1,
                fresnel=0.1,
                specular=1,
                roughness=0.1,
                ),
            lightposition=dict(
                x=0,
                y=0,
                z=-1,
                ),
            ),
        ]

    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            scene=dict(
                xaxis=AXIS,
                yaxis=AXIS,
                zaxis=AXIS,
                camera=dict(
                    eye=dict(
                        x=right_or_left,
                        y=0,
                        z=1,
                    ),
                    projection=dict(
                        type='orthographic',
                    ),
                    ),
                ),
            ),
        )

    return fig


def paper_plot_surf_bold(parameters, subject):

    elec_file = get_path(parameters, 'elec', subject=subject)
    fmri_file = get_path(parameters, 'fmri_nii', subject=subject)

    freesurfer_dir = parameters['paths']['freesurfer_subjects_dir'] / f'sub-{subject}'

    fs = Freesurfer(freesurfer_dir)
    electrodes = Electrodes(elec_file)

    elec = electrodes.electrodes.tsv

    if mean(elec['x']) > 0:
        right_or_left = 1
        hemi = 'rh'
    else:
        right_or_left = -1
        hemi = 'lh'

    fs = Freesurfer(freesurfer_dir)
    pial = getattr(fs.read_brain(), hemi)

    vert = pial.vert + fs.surface_ras_shift
    fmri_vals = project_mri_to_surf(fmri_file, vert, parameters['plot']['surface']['kernel'])

    colorscale = 'balance'

    traces = [
        go.Scatter3d(
            x=elec['x'] + right_or_left,
            y=elec['y'],
            z=elec['z'] + 1,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                size=5,
                color='black',
            ),
        ),
        go.Mesh3d(
            x=vert[:, 0],
            y=vert[:, 1],
            z=vert[:, 2],
            i=pial.tri[:, 0],
            j=pial.tri[:, 1],
            k=pial.tri[:, 2],
            intensity=fmri_vals,
            cmax=4,
            cmin=-4,
            colorscale=colorscale,
            hoverinfo='skip',
            flatshading=False,
            showscale=False,
            lighting=dict(
                ambient=0.18,
                diffuse=1,
                fresnel=0.1,
                specular=1,
                roughness=0.1,
                ),
            lightposition=dict(
                x=0,
                y=0,
                z=-1,
                ),
            ),
        ]

    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            scene=dict(
                xaxis=AXIS,
                yaxis=AXIS,
                zaxis=AXIS,
                camera=dict(
                    eye=dict(
                        x=right_or_left,
                        y=0,
                        z=1,
                    ),
                    projection=dict(
                        type='orthographic',
                    ),
                    ),
                ),
            ),
        )

    return fig
