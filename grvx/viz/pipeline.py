from .histogram import plot_histogram
from .gaussian import plot_gaussian
from .fmri import plot_fmri
from .scatter import plot_scatter
from .smooth import plot_smooth
from .surfaces import plot_surface
from .utils import to_html

from shutil import rmtree


def plot_results(parameters):

    plot_dir = parameters['paths']['output'] / 'plots'
    try:
        rmtree(plot_dir)
    except OSError:
        pass
    plot_dir.mkdir(exist_ok=True, parents=True)

    div = plot_gaussian()
    to_html([div, ], plot_dir / 'gaussian.html')

    divs = plot_histogram(parameters)
    to_html(divs, plot_dir / 'histogram.html')

    subjects = [x.stem[4:] for x in parameters['paths']['input'].glob('sub-*')]

    for subject in subjects:
        print(subject)
        divs = []
        divs.extend(
            plot_smooth(parameters, subject))

        divs.append(
            plot_scatter(parameters, subject))

        divs.append(
            plot_surface(parameters, subject))

        to_html(divs, plot_dir / f'{subject}.html')

    """
    plot_fmri()
    """
