from nipype import Function


def wrapper_prepare_design(func, anat, active_conditions):
    from pathlib import Path
    from grvx.nodes.fsl.feat import prepare_design

    output = prepare_design(
        Path(func),
        Path(anat),
        active_conditions,
        Path('.').resolve())
    return str(output)


function_prepare_design = Function(
    input_names=[
        'func',
        'anat',
        'active_conditions',
    ],
    output_names=[
        'fsf_file',
    ],
    function=wrapper_prepare_design,
    )
