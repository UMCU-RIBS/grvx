from logging import getLogger
from subprocess import run

from bidso.find import find_in_bids

from ..utils import ENVIRON

lg = getLogger(__name__)


def main(analysis_dir, freesurfer_dir):
    """
    coreg feat with freesurfer

    Parameters
    ----------
    analysis_dir : path

    freesurfer_dir : path

    """

    for feat_path in find_in_bids(analysis_dir, generator=True, extension='.feat'):
        lg.debug(f'Reading {feat_path}')
        coreg_feat2freesurfer(feat_path, freesurfer_dir)


def coreg_feat2freesurfer(feat_file, FREESURFER_PATH):
    """This needs to be improved with object-oriented feat"""
    cmd = ['reg-feat2anat', '--feat', str(feat_file), '--subject', feat_file.name.split('_')[0]]
    run(cmd,
        env={**ENVIRON, 'SUBJECTS_DIR': str(FREESURFER_PATH)},
        cwd=str(feat_file.parent))
