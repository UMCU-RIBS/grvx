from shutil import rmtree

from .gaussian import plot_gaussian
from .scatter import plot_scatter
from .smooth import plot_smooth, plot_gradient
from .histogram import plot_histogram
from .utils import merge

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
    xaxis=dict(
        title=dict(
            font=dict(
                size=10,
                ),
            ),
        linecolor='black',
        gridcolor=LIGHT_COLOR,
        tickfont=dict(
            size=8,
            ),
        ),
    yaxis=dict(
        title=dict(
            font=dict(
                size=10,
                ),
            ),
        linecolor='black',
        gridcolor=LIGHT_COLOR,
        tickfont=dict(
            size=8,
            ),
        ),
    )


def plot_results(parameters):

    plot_dir = parameters['paths']['output'] / 'paper'
    try:
        rmtree(plot_dir)
    except OSError:
        pass
    plot_dir.mkdir(exist_ok=True, parents=True)

    fig = plot_gaussian()
    layout = dict(
        width=250,
        height=180,
        )
    fig.update_layout(merge(LAYOUT, layout))
    fig.write_image(str(plot_dir / 'gaussian.svg'))

    fig = paper_plot_scatter(parameters)
    fig.write_image(str(plot_dir / 'scatter.svg'))

    fig = paper_plot_smooth(parameters)
    fig.write_image(str(plot_dir / 'smooth.svg'))

    fig = paper_plot_gradient(parameters)
    fig.write_image(str(plot_dir / 'gradient.svg'))

    figs = paper_plot_histogram(parameters)
    for i, value_type in enumerate(('r2_at_peak', 'size_at_peak', 'size_at_concave')):
        figs[i].write_image(str(plot_dir / f'{value_type}.svg'))


def paper_plot_scatter(parameters):

    fig = plot_scatter(parameters, [65, 95], parameters['plot']['subject'])

    layout = dict(
        width=500,
        height=200,
        xaxis=dict(
            showline=False,
            showgrid=False,
            title=dict(
                text='ECoG (<i>z</i>-statistics)',
                standoff=4,
                ),
            ),
        yaxis=dict(
            showline=False,
            showgrid=False,
            title=dict(
                text='fMRI (<i>z</i>-statistics)',
                standoff=8,
                ),
            ),
        shapes=[
            dict(
                type='line',
                x0=0,
                x1=1,
                xref='paper',
                y0=0,
                y1=0,
                layer='below',
                line=dict(
                    width=2,
                    color='gray',
                ),
            ),
            dict(
                type='line',
                x0=0,
                x1=0,
                y0=0,
                y1=1,
                yref='paper',
                layer='below',
                line=dict(
                    width=2,
                    color='gray',
                ),
            )

        ]
    )

    fig.update_layout(merge(LAYOUT, layout))

    return fig


def paper_plot_smooth(parameters):
    fig = plot_smooth(parameters, [65, 95], parameters['plot']['subject'])

    layout = dict(
        width=500,
        height=200,
        xaxis=dict(
            title=dict(
                text='kernel σ (mm)',
                standoff=4,
                ),
            ),
        yaxis=dict(
            title=dict(
                text='explained variance',
                standoff=8,
                ),
            dtick=0.1,
            ),
        )

    fig.update_layout(merge(LAYOUT, layout))

    return fig


def paper_plot_gradient(parameters):
    fig = plot_gradient(parameters, [65, 95], parameters['plot']['subject'])

    layout = dict(
        width=500,
        height=200,
        xaxis=dict(
            title=dict(
                text='kernel σ (mm)',
                ),
            ),
        yaxis=dict(
            title=dict(
                text='Concavity',
                ),
            dtick=0.002,
            ),
        )

    fig.update_layout(merge(LAYOUT, layout))

    return fig


def paper_plot_histogram(parameters):
    figs = plot_histogram(parameters, [65, 95])

    layout = dict(
        width=500,
        height=200,
        xaxis=dict(
            title=dict(
                standoff=4,
            ),
            linecolor='black',
            gridcolor='lightGray',
            ),
        yaxis=dict(
            title=dict(
                text='# participants',
                standoff=8,
            ),
            linecolor='black',
            gridcolor='lightGray',
            dtick=2,
            ),

        )

    XAXIS = (
        'explained variance (r<sup>2</sup>)',
        'kernel σ (mm)',
        'kernel σ (mm)',
        )

    layout = merge(LAYOUT, layout)
    for i, xaxis in enumerate(XAXIS):
        xaxis_title = dict(xaxis=dict(title=dict(text=xaxis)))
        figs[i] = figs[i].update_layout(merge(layout, xaxis_title))

    return figs
