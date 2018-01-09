from plotly.offline import plot

from exportimages import export_plotly

from .constants import PARAMETERS


# FORMAT is only used when plot is not interactive (svg, png, jpeg)
FORMAT = PARAMETERS['plot_format']


def prepare_fig(fig, figure_path, driver=None):
    """Make either interactive figure or export to png.

    Parameters
    ----------
    fig : plotly figure
        figure
    figure_path : Path
        path to file (without extension)
    size : tuple of 2 int
        height and width in pixels

    Returns
    -------
    str
        either the javascript for interactive plot or path to png.
    """
    if PARAMETERS['plot_interactive']:
        txt = '\n'.join([figure_path.stem,
                         plot(fig, output_type='div', show_link=False,
                              include_plotlyjs=False)])
    else:
        output_fig = figure_path.with_suffix('.' + FORMAT)
        export_plotly(fig, output_fig, driver=driver)
        txt = '![{}]({})\n\\ '.format(figure_path.stem, output_fig)

    return txt
