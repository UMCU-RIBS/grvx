from logging import getLogger
import collections

from copy import deepcopy
from plotly.offline import plot, get_plotlyjs

lg = getLogger(__name__)


LIGHT_COLOR = 'lightGray'

LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(
        l=0,
        t=0,
        b=0,
        r=0,
        pad=0,
        ),
    title=dict(
        font=dict(
            size=14,
            ),
        ),
    xaxis=dict(
        title=dict(
            font=dict(
                size=14,
                ),
            ),
        zerolinecolor='black',
        linecolor='black',
        gridcolor=LIGHT_COLOR,
        tickfont=dict(
            size=11,
            ),
        ),
    yaxis=dict(
        title=dict(
            font=dict(
                size=14,
                ),
            ),
        zerolinecolor='black',
        linecolor='black',
        gridcolor=LIGHT_COLOR,
        tickfont=dict(
            size=11,
            ),
        ),
    )


def to_div(fig):
    """Convert plotly FIG into an HTML div

    Parameters
    ----------
    fig : instance of plotly.Figure
        figure to convert

    Returns
    -------
    str
        html div, containing the figure as dynamic javascript plot
    """
    return plot(fig, output_type='div', show_link=False, include_plotlyjs=False)


def to_html(divs, filename):
    """Convert DIVs, obtained from 'to_div', into one HTML file

    Parameters
    ----------
    divs : list of divs
        list of the output of 'to_div'
    filename : path
        path of the file to write (extension should be .html). It overwrites if
        it exists
    """
    filename.parent.mkdir(exist_ok=True, parents=True)
    lg.debug(f'Saving {len(divs)} plots to {filename}')

    html = '''
        <html>
         <head>
             <script type="text/javascript">{plotlyjs}</script>
         </head>
         <body>
            {div}
         </body>
     </html>
    '''.format(plotlyjs=get_plotlyjs(), div='\n'.join(divs))

    with filename.open('w') as f:
        f.write(html)


def to_png(fig, png_name):
    """Convert image to png directly

    Parameters
    ----------
    fig : instance of plotly.Figure
        figure to convert
    png_name : path
        path of the file to write (extension should be .png). It overwrites if
        it exists

    Notes
    -----
    It crashes easily, especially if it's called multiple times, because it relies
    on plotly calling an external function to do the actual plotting (orca)
    """
    fig = fig.update_layout(width=1600, height=900)
    png_name.parent.mkdir(exist_ok=True, parents=True)
    with png_name.open('wb') as f:
        f.write(fig.to_image('png'))


def merge(dict1, dict2):
    """Return a new dictionary by merging two dictionaries recursively.

    https://stackoverflow.com/a/43228384
    """
    result = deepcopy(dict1)

    for key, value in dict2.items():
        if isinstance(value, collections.Mapping):
            result[key] = merge(result.get(key, {}), value)
        else:
            result[key] = deepcopy(dict2[key])

    return result
