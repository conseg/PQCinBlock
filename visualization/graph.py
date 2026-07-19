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

def generate_size_graphs(path_csv, results_dir, mechanisms_dict, simulation=False):
    try:
        df = pd.read_csv(path_csv)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    from visualization import utils
    import os
    
    size_graphics_dir = os.path.join(results_dir, "size_graphics")
    os.makedirs(size_graphics_dir, exist_ok=True)
    
    # get_variants_by_level expects the dataframe to have 'variant' as index
    df_indexed = df.set_index("variant")
    variants_by_level = utils.get_variants_by_level(df_indexed, mechanisms_dict)
    
    title = ""
    
    for level, variants in variants_by_level.items():
        variants_dict = {v["variant"]: v["algorithm"] for v in variants}
        output_filename = os.path.join(size_graphics_dir, f'sizes_level_{level}.pdf')
        plots.create_bar_chart(df, level, variants_dict, title, output_filename, simulation=simulation)
