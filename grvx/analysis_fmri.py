from shutil import copyfile
from time import sleep


from bidso import Task
from boavus.freesurfer import run_freesurfer
from boavus.fsl import run_feat
from boavus.fsl.feat import coreg_feat2freesurfer


from .core.constants import (PARAMETERS,
                             FEAT_PATH,
                             FREESURFER_PATH,
                             DATA_PATH,
                             )
from .core.log import with_log


@with_log
def Run_FreeSurfer(lg, img_dir):
    FREESURFER_PATH.mkdir(exist_ok=True)

    for task in layout.get(modality='anat', extensions='.nii.gz'):
        run_freesurfer(FREESURFER_PATH, task)


@with_log
def Run_fMRI_feat(lg, img_dir):
    FEAT_PATH.mkdir(exist_ok=True)

    feats = []
    for fmri_path in DATA_PATH.rglob('*_bold.nii.gz'):
        task = Task(fmri_path)
        feat_path = run_feat(FEAT_PATH, task)
        print(feat_path)
        feats.append(feat_path)

    _move_tsplot(feats, img_dir)

    # _move_tsplot waits until all the feat processes have ended
    for feat_path in feats:
        coreg_feat2freesurfer(feat_path, FREESURFER_PATH)


def _move_tsplot(feats, img_dir):

    while True:
        tsplots = [(x / 'tsplot' / 'tsplot_zstat1.png').exists() for x in feats]
        if all(tsplots):
            break
        sleep(1)

    for feat in feats:
        png_in = feat / 'tsplot' / 'tsplot_zstat1.png'
        png_out = img_dir / (feat.stem + '.png')
        copyfile(str(png_in), str(png_out))
