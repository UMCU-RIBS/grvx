from pathlib import Path

from sys import path
from functools import partial

from wonambi.attr import Channels, Freesurfer

from numpy import ndindex, zeros, NaN, mean, sum, corrcoef, diff, array, min, fill_diagonal, nanmin, median, exp, stack, isnan, where, arange, zeros
from numpy.linalg import norm
from nibabel import load, Nifti1Image
from nibabel.affines import apply_affine
from numpy.linalg import inv
from scipy.stats import ttest_ind
from scipy.io import loadmat
from numpy import dot, repeat, sign, diag
from nibabel import load as nload
from multiprocessing import Pool
from scipy.stats import linregress

path.append('/Fridge/users/giovanni/projects/mofe/scripts')
from mofe.core.preproc_ecog import _read_markers, preprocess_ecog, percent_ecog
from mofe.core import constants
constants.PARAMETERS['ecog']['channels']['regions'] = []

gauss = lambda x, s: exp(-.5 * (x ** 2 / s ** 2))


def from_chan_to_mrifile(img, fs, xyz):
    return apply_affine(inv(img.affine), xyz + fs.surface_ras_shift).astype(int)

def from_mrifile_to_chan(img, fs, xyz):
    return apply_affine(img.affine, xyz) - fs.surface_ras_shift


def _read_ecog_val():
    d = Dataset('/Fridge/users/giovanni/projects/grvx/subjects/sub-ommen/ses-day04/ieeg/sub-ommen_ses-day04_task-motor-hand-left_run-00_acq-experimental_ieeg.ns3')
    hfa_move, hfa_rest, chans, lg = preprocess_ecog(d.filename)
    # ecog_stats = percent_ecog(hfa_move, hfa_rest).data[0]
    t = ttest_ind(hfa_move.data[0], hfa_rest.data[0], axis=1).statistic
    return t, chans, hfa_move.chan[0]


def _read_chan(chan, fs):

    mat = loadmat('/Fridge/bci/data/14-420_adults/ommen/analysed/3D-CTMR/results_HD/project_electrodes_coord/Electrodes_displayed_on_surface.mat')['trielectrodes']
    chan = Channels(chan.return_label(), mat - fs.surface_ras_shift)
    return chan


def _upsample(img_lowres):
    lowres = img_lowres.get_data()
    r = lowres.copy()
    for i in range(3):
        r = repeat(r, 4, axis=i)

    af = img_lowres.affine.copy()
    af[:3, :3] /= 4
    af[:3, -1] -= diag(af)[:3] * 1.5  # I think it's 4 / 2 - 1 / 2 (not sure about where to get the sign)

    nifti = Nifti1Image(r, af)
    return nifti


def _read_fmri_val(to_plot):
    # fmri = percent_fmri(Path('/Fridge/users/giovanni/projects/mofe/derivatives/feat/sub-ommen/ses-daym25/func/sub-ommen_ses-daym25_task-motor-hand-left_run-00.feat'))

    img_lowres = nload('/Fridge/users/giovanni/projects/mofe/derivatives/feat/sub-ommen/ses-daym25/func/sub-ommen_ses-daym25_task-motor-hand-left_run-00.feat/stats/zstat1.nii.gz')
    upsampled = _upsample(img_lowres)
    if to_plot:
        upsampled.to_filename('/Fridge/users/giovanni/projects/grvx/derivatives/grvx/upsampled.nii.gz')

    return upsampled


def _compute_gauss(pos, mri_shape, ndi, gauss_size):
    dist_chan = norm(ndi - pos, axis=1)
    return gauss(dist_chan, gauss_size).reshape(mri_shape)


def _compute_voxmap(chan_xyz, mri_shape, ndi, gauss_size):

    p_compute_gauss = partial(_compute_gauss, mri_shape=mri_shape, ndi=ndi, gauss_size=gauss_size)
    with Pool() as p:
        all_m = p.map(p_compute_gauss, chan_xyz)
    ms = stack(all_m, axis=-1)
    MAX_STD = 3
    ms[ms.max(axis=-1) < gauss(gauss_size * MAX_STD, gauss_size), :] = NaN
    mq = ms / ms.sum(axis=-1)[..., None]

    return mq


def _main(KERNEL_SIZES, to_plot=False):

    fs = Freesurfer('/Fridge/users/giovanni/projects/grvx/derivatives/freesurfer/sub-ommen')
    ecog_val, chan, labels = _read_ecog_val()
    chan = _read_chan(chan, fs)
    chan = chan(lambda x: x.label in labels)
    print(len(chan.return_label()))
    print(len(ecog_val))
    print('ecog done')

    img = _read_fmri_val(to_plot)
    mri = img.get_data()
    print('fmri done')

    chan_xyz = chan.return_xyz()
    nd = array(list(ndindex(mri.shape)))
    ndi = from_mrifile_to_chan(img, fs, nd)
    print('ndindex done')

    r = []

    for gauss_size in KERNEL_SIZES:
        print(gauss_size)
        mq = _compute_voxmap(chan_xyz, mri.shape, ndi, gauss_size)
        if to_plot:
            t_val = arange(chan_xyz.shape[0])
            nifti_data = (mq * t_val[None, None, None, :]).sum(axis=-1)
            nifti = Nifti1Image(nifti_data, img.affine)
            nifti.to_filename('/Fridge/users/giovanni/projects/grvx/derivatives/grvx/trans_example.nii.gz')

        m = (mq * ecog_val[None, None, None, :]).sum(axis=-1)
        mask = (~isnan(mq[:, :, :, 0])) & (mri != 0)

        if to_plot:
            nifti_data = m.copy()
            nifti_data[~mask] = NaN  # also exclude area outside of fmri
            nifti = Nifti1Image(nifti_data, img.affine)
            nifti.to_filename('/Fridge/users/giovanni/projects/grvx/derivatives/grvx/ecog_to_mri.nii.gz')

        lr = linregress(m[mask], mri[mask])
        print(lr)

        r.append(lr.rvalue ** 2)

    return r
