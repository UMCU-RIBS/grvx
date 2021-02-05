from nipype import Function


def wrapper_corr(fmri_file, ecog_file, output_dir='./corr_values', pvalue=0.05):
    from pathlib import Path
    from grvx.nodes.corr.corrfmri import compute_corr_ecog_fmri

    results_tsv, fmri_file, ecog_file = compute_corr_ecog_fmri(
        Path(fmri_file).resolve(),
        Path(ecog_file).resolve(),
        Path(output_dir).resolve(),
        pvalue)

    return str(results_tsv), str(fmri_file), str(ecog_file)


def wrapper_corr_allfreq(fmri_file, ecog_file, min_n_sign_elec, pvalue=0.05, output_dir='./corr_values'):
    from pathlib import Path
    from grvx.nodes.corr.corrfmri import compute_corr_ecog_fmri_allfreq

    results_pkl  = compute_corr_ecog_fmri_allfreq(
        Path(fmri_file).resolve(),
        Path(ecog_file).resolve(),
        min_n_sign_elec,
        pvalue,
        Path(output_dir).resolve(),
        )

    return str(results_pkl)


def wrapper_summary(in_files, ecog_files, fmri_files, output_dir='./output'):
    from pathlib import Path
    from grvx.nodes.corr.summary import collect_corr

    collect_corr(in_files, ecog_files, fmri_files, Path(output_dir).resolve())


function_corr = Function(
    input_names=[
        'fmri_file',
        'ecog_file',
        'output_dir',
        'pvalue',
    ],
    output_names=[
        'out_file',
        'fmri_file',
        'ecog_file',
    ],
    function=wrapper_corr,
    )


function_corr_allfreq = Function(
    input_names=[
        'fmri_file',
        'ecog_file',
        'min_n_sign_elec',
        'pvalue',
        'output_dir',
    ],
    output_names=[
        'out_file',
    ],
    function=wrapper_corr_allfreq,
    )


function_corr_summary = Function(
    input_names=[
        'in_files',
        'ecog_files',
        'fmri_files',
    ],
    function=wrapper_summary,
    )
