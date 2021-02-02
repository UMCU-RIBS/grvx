from .plot.histogram import plot_histogram
from .plot.gaussian import plot_gaussian
from .plot.fmri import plot_fmri
from .plot.scatter import plot_scatter
from .plot.smooth import plot_smooth


def plot_results(parameters):

    plot_dir = parameters['paths']['output'] / 'plots'
    plot_dir.mkdir(exist_ok=True, parents=True)

    """
    plot_fmri()
    plot_gaussian(wd)
    plot_scatter(wd)
    """
    plot_histogram(plot_dir, parameters)
    plot_smooth(plot_dir, parameters)
