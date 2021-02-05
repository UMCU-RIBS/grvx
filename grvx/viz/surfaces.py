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


AXIS = dict(
    title="",
    visible=False,
    zeroline=False,
    showline=False,
    showticklabels=False,
    showgrid=False,
    )


def plot_surface(parameters, subject):

    fmri_dir = parameters['paths']['output'] / f'workflow/fmri/_subject_{subject}/fmri_compare'
    compare_fmri_file = next(fmri_dir.glob(f'sub-{subject}_*bold_compare.nii.gz'))

    ieeg_dir = parameters['paths']['output'] / f'workflow/ieeg/_subject_{subject}/ecog_compare'
    compare_ieeg_file = next(ieeg_dir.glob(f'sub-{subject}_*_compare.tsv'))

    elec_file = next(parameters['paths']['input'].glob(f'sub-{subject}/ses-*/ieeg/*_electrodes.tsv'))
    freesurfer_dir = parameters['paths']['freesurfer_subjects_dir'] / f'sub-{subject}'

    compare_ieeg = read_tsv(compare_ieeg_file)
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

    img = nload(str(compare_fmri_file))
    mri = img.get_fdata()
    mri[mri == 0] = NaN

    nd = array(list(ndindex(mri.shape)))
    ndi = from_mrifile_to_chan(img, nd)

    kernel = parameters['plot']['surface']['kernel']
    partial_compute_chan = partial(compute_chan, KERNEL=kernel, ndi=ndi, mri=mri, distance='gaussian')

    vert = pial.vert + fs.surface_ras_shift

    with Pool() as p:
        fmri_vals = p.map(partial_compute_chan, vert)
    fmri_vals = [x[0] for x in fmri_vals]

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
