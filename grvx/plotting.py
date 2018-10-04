from exportimages import Webdriver

from .core.log import with_log
from .core.constants import PLOT_PATH

from .plot.gaussian import plot_gaussian
from .plot.fmri import plot_fmri


@with_log
def Plot_Results(lg):

    plot_fmri(PLOT_PATH)

    with Webdriver(PLOT_PATH) as wd:
        plot_gaussian(wd)
