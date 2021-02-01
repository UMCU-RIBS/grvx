"""Various functions, that I don't know where to place
"""
from nibabel import load as nload
from numpy import array, isnan
from nibabel import Nifti1Image
from pathlib import Path
from tempfile import mkstemp


def get_vox2ras_tkr(filename):
    """This should be identical
    mri_info --vox2ras-tkr filename
    """
    img = nload(str(filename))

    Nc, Nr, Ns = img.shape[:3]
    dC, dR, dS = img.header['pixdim'][1:4]
    vox2ras_tkr = array([
        [-dC, 0, 0, Nc / 2 * dC],
        [0, 0, dS, -Ns / 2 * dS],
        [0, -dR, 0, Nr / 2 * dR],
        [0, 0, 0, 1],
    ])

    return vox2ras_tkr


def ribbon2graymatter(ribbon_files, output_dir):
    graymatter_file = output_dir / 'graymatter.nii.gz'

    ribbon_rh_file = [x for x in ribbon_files if x.endswith('rh.ribbon.mgz')][0]
    ribbon_lh_file = [x for x in ribbon_files if x.endswith('lh.ribbon.mgz')][0]

    ribbon_rh = nload(str(ribbon_rh_file))
    ribbon_lh = nload(str(ribbon_lh_file))
    graymatter = ribbon_rh.get_data() + ribbon_lh.get_data()

    nifti = Nifti1Image(graymatter, ribbon_rh.affine)
    nifti.to_filename(str(graymatter_file))

    return graymatter_file


def mri_nan2zero(input_nii):
    """Remove NaN values and turn them into zeros (so that Freesurfer can handle
    them)

    Parameters
    ----------
    input_nii : Path
        path to nii.gz containing NaN

    Returns
    -------
    Path
        path to temporary nii.gz containing no NaN. You can remove the file
        with .unlink()
    """
    img = nload(str(input_nii))
    dat = img.get_data()
    dat[isnan(dat)] = 0
    img = Nifti1Image(dat, img.affine)

    tmp_nii = mkstemp(suffix='.nii.gz')[1]
    img.to_filename(tmp_nii)
    return Path(tmp_nii)
