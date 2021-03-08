from .pipeline import plot_results as plot1
from .paper import plot_results as plot2


def plot_results(parameters):
    plot2(parameters)
    plot1(parameters)

