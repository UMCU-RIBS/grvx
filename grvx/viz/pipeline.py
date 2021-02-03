from .histogram import plot_histogram
from .gaussian import plot_gaussian
from .fmri import plot_fmri
from .scatter import plot_scatter
from .smooth import plot_smooth
from .surfaces import plot_surfaces


def plot_results(parameters):

    plot_dir = parameters['paths']['output'] / 'plots'
    plot_dir.mkdir(exist_ok=True, parents=True)

    """
    plot_fmri()
    plot_scatter(wd)
    """
    plot_gaussian(plot_dir)
    plot_surfaces(plot_dir, parameters)
    plot_histogram(plot_dir, parameters)
    plot_smooth(plot_dir, parameters)
