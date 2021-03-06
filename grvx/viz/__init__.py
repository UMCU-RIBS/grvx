from .pipeline import plot_results as plot_pipeline
from .paper import plot_results as plot_paper
from .summary import summary_info


def plot_results(parameters):
    plot_pipeline(parameters)
    plot_paper(parameters)
    summary_info(parameters)
