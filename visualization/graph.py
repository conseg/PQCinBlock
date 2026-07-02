import pandas as pd
import numpy as np

# Internal imports
from visualization import plots
import save

def generate_graphs(
    path_csv,
    results_dir,
    columns,
    mechanisms_dict,
    values_offset,
    error_offset,
    log_xticks,
    log_xlim,
    show_graph=False,
    show_values=True,
    show_erros=True,
    show_legend=False, 
):

    try:
        df = pd.read_csv(path_csv)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    graphics_directory = save.create_graphics_directory(results_dir)
    
    plots.generate_plots_from_csv(
        path_csv=path_csv,
        variants_dict=mechanisms_dict,
        graphics_directory=graphics_directory,
        columns = columns,
        xscale="log",
        xticks=log_xticks,
        xlim=log_xlim,
        values_offset=values_offset,
        error_offset=error_offset,
        show_graph=show_graph,                
        show_values=show_values,
        show_erros=show_erros,
        show_legend=show_legend, 
    )
