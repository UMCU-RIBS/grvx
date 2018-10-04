from subprocess import run

def plot_fmri(PLOT_PATH):
    output_png = PLOT_PATH / 'mri.png'

    cmd = [
        'freeview',
        '-v', '/Fridge/users/giovanni/projects/grvx/derivatives/nipype/grvx/fmri/_subject_arnhem/bet/sub-arnhem_ses-UMCU3Tdaym31_acq-wholebrain_T1w_brain.nii.gz',
        '-v', '/Fridge/users/giovanni/projects/grvx/derivatives/nipype/grvx/fmri/_subject_arnhem/compare/sub-arnhem_ses-UMCU3Tdaym31_task-motorHandRight_run-1_bold_compare.nii.gz:colormap=heat:heatscale=0,15:heatscaleoptions=truncate',
        '-f', '/Fridge/users/giovanni/projects/grvx/derivatives/freesurfer/sub-arnhem/surf/lh.pial:edgecolor=255,182,193',
        '-f', '/Fridge/users/giovanni/projects/grvx/derivatives/freesurfer/sub-arnhem/surf/rh.pial:edgecolor=255,182,193',
        '--layout', '1',
        '--viewport', 'coronal',
        '--ras', '-24.77', '-2', '15.24',
        '--screenshot', str(output_png), '6',
        ]

    run(cmd)
