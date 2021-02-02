from subprocess import run

def plot_fmri(PLOT_PATH):
    output_png = PLOT_PATH / 'mri.png'

    cmd = [
        'freeview',
        '-v', '/Fridge/users/giovanni/projects/grvx/derivatives/nipype/grvx/fmri/_subject_bunnik/bet/sub-bunnik_ses-UMCU3Tdaym42_acq-wholebrain_T1w_brain.nii.gz',
        '-v', '/Fridge/users/giovanni/projects/grvx/derivatives/nipype/grvx/fmri/_subject_bunnik/fmri_compare/sub-bunnik_ses-UMCU3Tdaym42_task-motorHandRight_run-1_bold_compare.nii.gz:colormap=heat:heatscale=0,15:heatscaleoptions=truncate',
        '-f', '/Fridge/users/giovanni/projects/freesurfer/sub-bunnik/surf/lh.pial:edgecolor=255,182,193',
        '-f', '/Fridge/users/giovanni/projects/freesurfer/sub-bunnik/surf/rh.pial:edgecolor=255,182,193',
        '--layout', '1',
        '--viewport', 'coronal',
        '--ras', '-24.77', '-2', '15.24',
        '--screenshot', str(output_png), '6',
        ]

    run(cmd)
