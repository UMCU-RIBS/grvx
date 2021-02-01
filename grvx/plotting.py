from .plot.histogram import plot_histogram
from .plot.gaussian import plot_gaussian
from .plot.fmri import plot_fmri
from .plot.scatter import plot_scatter
from .plot.smooth import plot_smooth


def plot_results(parameters):

    wd = None
    plot_fmri()
    plot_gaussian(wd)
    plot_histogram(wd)
    plot_scatter(wd)
    plot_smooth(wd)
