from .histogram import plot_histogram
from .gaussian import plot_gaussian
from .fmri import plot_fmri
from .scatter import plot_scatter
from .smooth import plot_smooth
from .surfaces import plot_surface


def plot_results(parameters):

    plot_dir = parameters['paths']['output'] / 'plots'
    plot_dir.mkdir(exist_ok=True, parents=True)

    subjects = [x.stem[4:] for x in parameters['paths']['input'].glob('sub-*')]

    divs = {}
    for subj in subjects:
        divs_subj = []
        divs_subj.append(
            plot_surface(parameters, subject))
        break

    """
    plot_fmri()
    plot_scatter(wd)
    """
    plot_gaussian(plot_dir)
    plot_histogram(plot_dir, parameters)
    plot_smooth(plot_dir, parameters)
