from logging import getLogger
from numpy import array_equal, errstate, loadtxt, NaN

from nibabel import load as nload
from nibabel import save as nsave
from nibabel import Nifti1Image

from bidso.utils import replace_extension

lg = getLogger(__name__)


def compare_fmri(feat_path, measure, normalize_to_mean, output_dir):
    # measure='percent', normalize_to_mean=False):

    if measure == 'percent':
        fmri_stat = compute_percent(feat_path, normalize_to_mean)
    elif measure == 'zstat':
        fmri_stat = compute_zstat(feat_path)
    else:
        raise ValueError(f'Unknown measure: {measure}')

    task_path = output_dir / replace_extension(feat_path.name, '_compare.nii.gz')
    nsave(fmri_stat, str(task_path))

    return task_path


def compute_percent(feat_path, normalize_to_mean):
    """Calculate percent change for a task.

    Parameters
    ----------

    Returns
    -------
    instance of nibabel.Nifti1Image
        percent change as image
    """
    design = read_design(feat_path)

    pe_mri = nload(str(feat_path / 'stats' / 'pe1.nii.gz'))

    pe = pe_mri.get_data()
    pe[pe == 0] = NaN
    perc = pe * 100 * design.ptp()

    if normalize_to_mean:
        """I'm not sure if this is necessary, but for sure it increases the level
        of noise"""
        mean_mri = nload(str(feat_path / 'mean_func.nii.gz'))
        mean_func = mean_mri.get_data()
        array_equal(pe_mri.affine, mean_mri.affine)
        with errstate(invalid='ignore'):
            perc /= mean_func

    mask_mri = nload(str(feat_path / 'mask.nii.gz'))
    mask = mask_mri.get_data().astype(bool)
    perc[~mask] = NaN

    return Nifti1Image(perc, pe_mri.affine)


def compute_zstat(feat_path):
    return nload(str(feat_path / 'stats' / 'zstat1.nii.gz'))


def read_design(feat_path):
    """TODO: this could be a method of Feat"""
    return loadtxt(str(feat_path / 'design.mat'), skiprows=5)
