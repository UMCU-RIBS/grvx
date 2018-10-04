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


"""
    node_corr_plot = Node(function_corr_plot, name='corr_fmri_ecog_plot')
    node_corr_plot.inputs.pvalue = PARAMETERS['corr']['pvalue']
    node_corr_plot.inputs.image = PARAMETERS['image_format']

    node_corr_plot_all = JoinNode(function_corr_plot_all, name='corr_fmri_ecog_plot_all', joinsource='bids', joinfield='in_files')
    node_corr_plot_all.inputs.image = PARAMETERS['image_format']
"""
