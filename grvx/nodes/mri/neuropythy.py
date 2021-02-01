from nipype import Function


def wrapper_neuropythy_atlas(subject_id, subjects_dir=None):
    from pathlib import Path
    from neuropythy.commands import atlas

    if subjects_dir is not None:
        subject_id = str(Path(subjects_dir).resolve() / subject_id)

    output_path = str(Path('.').resolve() / subject_id)

    atlas.main([
        subject_id,
        '--overwrite',
        '--verbose',
        '--create-directory',
        '--output-path',
        output_path,
        ])

    return output_path


function_neuropythy_atlas = Function(
    input_names=[
        'subject_id',
        'subjects_dir',
    ],
    output_names=[
        'output_dir',
    ],
    function=wrapper_neuropythy_atlas,
    )
