from pathlib import Path
from shutil import copyfile
from subprocess import run, PIPE
from tempfile import mkstemp

from bidso.utils import bids_mkdir, replace_underscore, replace_extension

from ..utils import check_subprocess, ENVIRON


def run_reorient2std(nii):
    """This function simply reorients nifti, so that FSL can work with it
    more easily (reg works much better after running this function).
    """
    tmp_nii = mkstemp(suffix='.nii.gz')[1]
    p = run([
        'fslreorient2std',
        str(nii),
        tmp_nii,
        ], stdout=PIPE, stderr=PIPE, env=ENVIRON)
    check_subprocess(p)
    copyfile(tmp_nii, nii)
    Path(tmp_nii).unlink()


def run_flirt_resample(nii_in, nii_out, target_resolution):
    """Downsample and upsample mri
    """
    p = run([
        'flirt',
        '-in', str(nii_in),
        '-ref', str(nii_in),
        '-out', str(nii_out),
        '-applyisoxfm', str(target_resolution),
        ], stdout=PIPE, stderr=PIPE, env=ENVIRON)
    check_subprocess(p)


def run_flirt_feat(task_fmri, gm_file):
    gm_feat_file = replace_extension(gm_file, '_feat.nii.gz')  # TEST: same affine as bold compare
    p = run([
        'flirt',
        '-in', str(gm_file),
        '-ref', str(task_fmri.filename),
        '-usesqform',
        '-applyxfm',
        '-out', str(gm_feat_file),
        ], stdout=PIPE, stderr=PIPE, env=ENVIRON)
    check_subprocess(p)
    return gm_feat_file


def run_fslmaths_threshold(gm_file, threshold):
    gm_bin_file = replace_extension(gm_file, '_bin.nii.gz')
    p = run([
        'fslmaths',
        gm_file,
        '-thr', str(threshold),
        '-bin',
        gm_bin_file
        ], stdout=PIPE, stderr=PIPE)
    check_subprocess(p)
    return gm_bin_file
