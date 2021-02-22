from .histogram import plot_histogram
from .gaussian import plot_gaussian
from .fmri import plot_fmri
from .scatter import plot_scatter
from .smooth import plot_smooth, plot_gradient
from .surfaces import plot_surface
from .utils import to_html, to_div
from .allfreq import plot_allfreq
from .compare_freq import plot_freq_comparison

from shutil import rmtree


def plot_results(parameters):

    plot_dir = parameters['paths']['output'] / 'plots'
    try:
        rmtree(plot_dir)
    except OSError:
        pass
    plot_dir.mkdir(exist_ok=True, parents=True)

    subjects = [x.stem[4:] for x in parameters['paths']['input'].glob('sub-*')]
    # subjects = set(subjects) - {'ommen', 'vledder', 'arnhem', 'boxtel'}

    fig = plot_gaussian()
    to_html([to_div(fig), ], plot_dir / 'gaussian.html')

    figs = plot_freq_comparison(parameters)
    divs = [to_div(fig) for fig in figs]
    to_html(divs, plot_dir / 'compare_frequencies.html')

    for subject in subjects:
        divs = plot_allfreq(parameters, subject)
        if divs is not None:
            to_html(divs, plot_dir / 'allfreq' / f'{subject}.html')

    surf = {}
    for frequency_band in parameters['ieeg']['ecog_compare']['frequency_bands']:

        freq_name = f'frequency_{frequency_band[0]}_{frequency_band[1]}'
        figs = plot_histogram(parameters, frequency_band)
        divs = [to_div(fig) for fig in figs]
        to_html(divs, plot_dir / freq_name / 'histogram.html')

        for subject in subjects:
            divs = []

            fig = plot_scatter(parameters, frequency_band, subject)
            if fig is not None:
                divs.append(fig)

            fig = plot_smooth(parameters, frequency_band, subject)
            if fig is not None:
                divs.append(to_div(fig))

            fig = plot_gradient(parameters, frequency_band, subject)
            if fig is not None:
                divs.append(to_div(fig))

            div = plot_surface(parameters, frequency_band, subject, surf)
            if div is not None:
                divs.append(div)

            to_html(divs, plot_dir / freq_name / f'{subject}.html')

    """
    plot_fmri()
    """
