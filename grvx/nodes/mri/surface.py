from logging import getLogger
from pathlib import Path
from subprocess import run, PIPE
from tempfile import TemporaryDirectory

from nibabel import Nifti1Image
from nibabel import load as niload
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage.morphology import binary_closing

from ..utils import check_subprocess


GAUSSIAN_FILTER = 1
CLOSING_ITER = 15
SMOOTH_ITERATION = 60

lg = getLogger(__name__)


def fill_surface(surf_in, surf_smooth):

    with TemporaryDirectory() as tmpdir:
        lg.debug(f'Temporary Directory for fill_surface: {tmpdir}')
        tmpdir = Path(tmpdir)

        vol_file = tmpdir / 'vol.mgz'
        vol_filled = tmpdir / 'filled.nii.gz'
        surf_filled = tmpdir / 'filled.surf'

        p = run([
            'mris_fill',
            '-c', '-r', '1',
            str(surf_in),
            str(vol_file),
            ], stdout=PIPE, stderr=PIPE)
        check_subprocess(p)

        _close_volume(vol_file, vol_filled)

        p = run([
            'mri_tessellate',
            str(vol_filled),
            '1',
            str(surf_filled),
            ], stdout=PIPE, stderr=PIPE)
        check_subprocess(p)

        p = run([
            'mris_smooth',
            '-nw',
            '-n', str(SMOOTH_ITERATION),
            str(surf_filled),
            str(surf_smooth)
            ], stdout=PIPE, stderr=PIPE)
        check_subprocess(p)


def _close_volume(vol_file, filled):

    vol = niload(str(vol_file))
    volume = vol.get_data()
    v = gaussian_filter(volume, GAUSSIAN_FILTER)

    # binarize
    v[v <= 25 / 255] = 0
    v[v > 25 / 255] = 1

    closed = binary_closing(v, iterations=CLOSING_ITER)
    n = Nifti1Image(closed.astype('float32'), vol.affine)
    n.to_filename(str(filled))

    return filled
