from wonambi.attr import Freesurfer
from bidso import Electrodes
from bidso.utils import read_tsv
from nibabel import load as nload
import plotly.graph_objs as go
from numpy import NaN, where, concatenate, mean
from functools import partial
from multiprocessing import Pool

from ..nodes.fmri.at_electrodes import compute_chan, ndindex, from_mrifile_to_chan, array
from .utils import to_div
from .paths import get_path


AXIS = dict(
    title="",
    visible=False,
    zeroline=False,
    showline=False,
    showticklabels=False,
    showgrid=False,
    )


def plot_surface(parameters, frequency_band, subject, surf):

    elec_file = get_path(parameters, 'elec', subject=subject)
    ieeg_file = get_path(parameters, 'ieeg_tsv', frequency_band=frequency_band, subject=subject)
    fmri_file = get_path(parameters, 'fmri_nii', subject=subject)
    if elec_file is None or ieeg_file is None or fmri_file is None:
        return

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

    if subject in surf:
        fmri_vals = surf[subject]
    else:
        print(f'Computing surf for {subject}')
        fmri_vals = project_mri_to_surf(fmri_file, vert, parameters['plot']['surface']['kernel'])
        surf[subject] = fmri_vals

    colorscale = 'balance'

    traces = [
        go.Scatter3d(
            x=elec['x'],
            y=elec['y'],
            z=elec['z'],
            text=labels,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                size=5,
                color=compare_ieeg['measure'],
                colorscale=colorscale,
                showscale=True,
                cmid=0,
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
            intensity=fmri_vals,
            cmid=0,
            colorscale='Balance',
            hoverinfo='skip',
            flatshading=False,
            colorbar=dict(
                title='fmri',
                titleside="top",
                ticks="outside",
                ticklabelposition="outside",
                x=1,
                ),
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
                        z=0,
                    ),
                    projection=dict(
                        type='orthographic',
                    ),
                    ),
                ),
            ),
        )

    return to_div(fig)


def project_mri_to_surf(fmri_file, vert, kernel):
    img = nload(str(fmri_file))
    mri = img.get_fdata()
    mri[mri == 0] = NaN

    nd = array(list(ndindex(mri.shape)))
    ndi = from_mrifile_to_chan(img, nd)

    partial_compute_chan = partial(compute_chan, KERNEL=kernel, ndi=ndi, mri=mri, distance='gaussian')

    with Pool() as p:
        fmri_vals = p.map(partial_compute_chan, vert)
    fmri_vals = [x[0] for x in fmri_vals]

    return fmri_vals
