from shutil import rmtree

from .gaussian import plot_gaussian
from .scatter import plot_scatter
from .smooth import plot_smooth, plot_gradient
from .histogram import plot_histogram
from .utils import merge
from .compare_freq import plot_freq_comparison

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

    freqA = parameters['ieeg']['ecog_compare']['frequency_bands'][parameters['plot']['compare']['freqA']]
    freqB = parameters['ieeg']['ecog_compare']['frequency_bands'][parameters['plot']['compare']['freqB']]

    for freq in (freqA, freqB):

        freq_dir = plot_dir / f"frequency_{freq[0]}_{freq[1]}"
        freq_dir.mkdir(exist_ok=True, parents=True)

        fig = paper_plot_scatter(parameters, freq)
        fig.write_image(str(freq_dir / 'scatter.svg'))

        fig = paper_plot_smooth(parameters, freq)
        fig.write_image(str(freq_dir / 'smooth.svg'))

        fig = paper_plot_gradient(parameters, freq)
        fig.write_image(str(freq_dir / 'gradient.svg'))

        figs = paper_plot_histogram(parameters, freq)
        for fig, value_type in zip(figs, ('r2_at_peak', 'size_at_peak', 'size_at_concave')):
            fig.write_image(str(freq_dir / f'{value_type}.svg'))

    figs = paper_plot_freq_comparison(parameters)
    names = (
        'comparefreq_r2_at_peak',
        'comparefreq_size_at_peak',
        'comparefreq_size_at_concave',
        )
    for fig, name in zip(figs, names):
        fig.write_image(str(plot_dir / f'{name}.svg'))


def paper_plot_scatter(parameters, freq):

    fig = plot_scatter(parameters, freq, parameters['plot']['subject'])

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


def paper_plot_smooth(parameters, freq):
    fig = plot_smooth(parameters, freq, parameters['plot']['subject'])

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


def paper_plot_gradient(parameters, freq):
    fig = plot_gradient(parameters, freq, parameters['plot']['subject'])

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


def paper_plot_histogram(parameters, freq):
    figs = plot_histogram(parameters, freq)

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


def paper_plot_freq_comparison(parameters):
    figs = plot_freq_comparison(parameters)

    layout = dict(
        title=dict(
            text='',
            ),
        width=300,
        height=300,
        )

    layout = merge(LAYOUT, layout)
    figs = [fig.update_layout(layout) for fig in figs]

    figs[3] = figs[3].update_layout(
        dict(
            xaxis=dict(
                showgrid=False,
            ),
            yaxis=dict(
                showgrid=False,
            ),
        ))

    return figs
