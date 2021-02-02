from .viz.histogram import plot_histogram
from .viz.gaussian import plot_gaussian
from .viz.fmri import plot_fmri
from .viz.scatter import plot_scatter
from .viz.smooth import plot_smooth


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
