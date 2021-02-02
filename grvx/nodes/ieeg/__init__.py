from nipype import Function

def wrapper_read_ieeg_block(ieeg, electrodes, active_conditions, baseline_conditions, minimalduration):
    from pathlib import Path
    from grvx.nodes.ieeg.read import read_ieeg_block

    conditions = {
        'active': active_conditions,
        'baseline': baseline_conditions,
        }

    outputs = read_ieeg_block(
        Path(ieeg),
        Path(electrodes),
        conditions,
        minimalduration,
        Path('.').resolve())
    return [str(x) for x in outputs]


def wrapper_preprocess(ieeg, reref, duration, offset):
    from pathlib import Path
    from grvx.nodes.ieeg.preprocessing import preprocess_ecog

    output = preprocess_ecog(
        Path(ieeg),
        reref,
        duration,
        offset,
        Path('.').resolve())
    return str(output)


def wrapper_powerspectrum(ieeg, method, taper, duration):
    from pathlib import Path
    from grvx.nodes.ieeg.psd import compute_powerspectrum

    output = compute_powerspectrum(
        Path(ieeg),
        method,
        taper,
        duration,
        Path('.').resolve())
    return str(output)


def wrapper_ieeg_compare(in_files, frequency, baseline=False, method='dh2012',
                         measure='dh2012_r2'):
    from pathlib import Path
    from grvx.nodes.ieeg.compare import compare_ieeg_freq

    output = compare_ieeg_freq(
        Path(in_files[0]),
        Path(in_files[1]),
        frequency,
        baseline,
        method,
        measure,
        Path('.').resolve())
    return str(output)


function_ieeg_read = Function(
    input_names=[
        'ieeg',
        'electrodes',
        'active_conditions',
        'baseline_conditions',
        'minimalduration',
    ],
    output_names=[
        'ieeg',
    ],
    function=wrapper_read_ieeg_block,
    )


function_ieeg_preprocess = Function(
    input_names=[
        'ieeg',
        'reref',
        'duration',
        'offset',
    ],
    output_names=[
        'ieeg',
    ],
    function=wrapper_preprocess,
    )


function_ieeg_powerspectrum = Function(
    input_names=[
        'ieeg',
        'method',
        'taper',
        'duration',
    ],
    output_names=[
        'ieeg',
    ],
    function=wrapper_powerspectrum,
    )


function_ieeg_compare = Function(
    input_names=[
        'in_files',
        'frequency',
        'baseline',
        'method',
        'measure',
    ],
    output_names=[
        'tsv_compare',
    ],
    function=wrapper_ieeg_compare,
    )
