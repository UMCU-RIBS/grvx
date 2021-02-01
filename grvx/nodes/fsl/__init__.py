from nipype import Function


def wrapper_prepare_design(func, anat):
    from pathlib import Path
    from boavus.fsl.feat import prepare_design

    output = prepare_design(
        Path(func),
        Path(anat),
        Path('.').resolve())
    return str(output)


function_prepare_design = Function(
    input_names=[
        'func',
        'anat',
    ],
    output_names=[
        'fsf_file',
    ],
    function=wrapper_prepare_design,
    )
