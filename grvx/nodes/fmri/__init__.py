from nipype import Function


def wrapper_fmri_compare(feat_path, measure, normalize_to_mean):
    from pathlib import Path
    from boavus.fmri.compare import compare_fmri

    output = compare_fmri(
        Path(feat_path),
        measure,
        normalize_to_mean,
        Path('.').resolve())
    return str(output)


def wrapper_at_elec(in_file, electrodes, distance, kernel_sizes, graymatter=False):
    # measure_nii, electrodes, freesurfer_dir='', graymatter=False, distance='guassian', kernel_sizes):
    from pathlib import Path
    from boavus.fmri.at_electrodes import calc_fmri_at_elec

    output = calc_fmri_at_elec(
        Path(in_file),
        Path(electrodes),
        distance,
        kernel_sizes,
        graymatter,
        Path('.').resolve())
    return [str(x) for x in output]


def wrapper_fmri_graymatter(ribbon):
    from pathlib import Path
    from boavus.fmri.utils import ribbon2graymatter
    print(ribbon)

    output = ribbon2graymatter(
        ribbon,
        Path('.').resolve())
    return str(output)


function_fmri_compare = Function(
    input_names=[
        'feat_path',
        'measure',
        'normalize_to_mean',
    ],
    output_names=[
        'out_file',
    ],
    function=wrapper_fmri_compare,
    )


function_fmri_atelec = Function(
    input_names=[
        'in_file',
        'electrodes',
        'distance',
        'kernel_sizes',
        'graymatter',
    ],
    output_names=[
        'fmri_vals',
        'n_voxels',
    ],
    function=wrapper_at_elec,
    )


function_fmri_graymatter = Function(
    input_names=[
        'ribbon',
    ],
    output_names=[
        'out_file',
    ],
    function=wrapper_fmri_graymatter,
    )
