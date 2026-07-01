import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import logging


from visualization import utils

def plot_horizontal(
    df_all, 
    columns,
    graphics_directory,
    values_offset,
    error_offset,
    level, 
    xscale,
    xlabel,
    xlim,
    xticks, 
    yticklabels,
    figsize, 
    width,
    title=None,
    ylabel=None,
    show_graph=False,
    show_values=True,
    show_errors=True,
    show_legend=True,
    save_formats=("svg", "png")
):
    n_variants = len(df_all)
    n_columns = len(columns)
    
    width_bar = width / n_columns

    y = np.arange(n_variants)

    fig, ax = plt.subplots(figsize=figsize)

    palette = sns.color_palette("muted", n_colors=n_columns)

    for i, (val_col, err_col, label) in enumerate(columns):
        values = df_all[val_col]
        errors = df_all[err_col]
        
        reverse_i = n_columns - 1 - i

        bars = ax.barh(
            y + (reverse_i - (n_columns - 1) / 2) * width_bar,
            values,
            height=width_bar,
            xerr=errors if show_errors else None,
            label=label,
            color=palette[i],
            error_kw={"capsize": 5, "ecolor": "red", "elinewidth": 2}
        )

        # values
        if show_values:
            for bar, value in zip(bars, values):
                offset = values_offset
                ax.text(
                    value * (1 - offset),
                    bar.get_y() + bar.get_height() / 2,
                    f"{value:.3f}",    
                    va="center_baseline",
                    ha="right",
                    fontsize=22,
                    color="black",
                    fontweight=600,
                )

        # error
        if show_errors:
            for bar, value, error in zip(bars, values, errors):
                right = value + error
                offset = error_offset
                ax.text(
                    right * offset,
                    bar.get_y() + bar.get_height() / 2,
                    f"±{error:.3f}",
                    va="center_baseline",
                    ha="left",
                    fontsize=20,
                    color="red",
                )

    ax.set_yticks(y)
    ax.set_yticklabels(df_all[yticklabels].to_list(), rotation=0, va="center")

    if ylabel:
        ax.set_ylabel(ylabel, fontsize=24)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=24)
    if title:
        ax.set_title(title, fontsize=32)

    ax.set_xscale(xscale)
    
    if xscale == "log":
        ax.set_xticks(xticks)
    
    if xscale == "linear" and xlim:
        ax.set_xlim(*xlim)

    ax.set_ylim(y[0] - 0.5, y[-1] + 0.5)

    ax.tick_params(axis="y", labelsize=28)
    ax.tick_params(axis="x", labelsize=28)

    if show_legend:
        ax.legend(loc="upper right", fontsize=28)

    ax.grid(True, axis="x", linestyle="--", linewidth=0.5, alpha=0.7)

    plt.tight_layout()

    filename = f"level-{level}" if level else "all_level"

    for ext in save_formats:
        file = f"{graphics_directory}/{filename}.{ext}"
        plt.savefig(file, format=ext)
        logging.info(f"\t{file}")

    if show_graph:
        plt.show()
    else:
        plt.close()


def generate_plots_from_csv(
    path_csv,
    graphics_directory,
    variants_dict,
    columns,
    show_graph,
    show_values,
    show_erros,
    show_legend,
    values_offset,
    error_offset,
    xscale,
    xlim,
    xticks,
    width=0.85,
    xlabel="Average time (ms)",
    ylabel="Algorithms",
    figsize=(16, 9),
    save_formats=["pdf"],
):
    """
    Generates bar plots with error bars from a benchmark CSV file.
    """
    df = pd.read_csv(path_csv, index_col="variant")

    variants_by_level = utils.get_variants_by_level(df, variants_dict)

    for level, mechanisms in variants_by_level.items():

        variant_to_algorithm = {m["variant"]: m["algorithm"] for m in mechanisms}
        variant_names = [m["variant"] for m in mechanisms]

        df_subset = df.loc[variant_names]
        df_subset["algorithm"] = df_subset.index.map(variant_to_algorithm)

        # Check for positive data if log scale is requested for this subset
        effective_xscale = xscale
        if xscale == "log":
            has_positive_data = False
            for val_col, _, _ in columns:
                # Drop NaN values before checking for positive data
                if val_col in df_subset.columns and (df_subset[val_col].dropna() > 0).any():
                    has_positive_data = True
                    break
            if not has_positive_data:
                effective_xscale = "linear"
                logging.warning(f"\nWarning: No positive data for level {level} to plot with log scale. Switching to linear scale.")
        
        plot_horizontal(
            df_all=df_subset, 
            columns=columns,
            graphics_directory=graphics_directory,
            values_offset=values_offset,
            error_offset=error_offset,
            level=level, 
            xlabel=xlabel,
            xlim=xlim,
            xticks=xticks, 
            yticklabels="algorithm",
            figsize=figsize,
            width=width,
            xscale=effective_xscale,
            show_graph=show_graph,
            show_values=show_values,
            show_errors=show_erros,
            show_legend=show_legend,
            save_formats=save_formats
        )


def plot_horizontal_multiple_inverted(
    dfs,               
    columns,
    graphics_directory,
    values_offset,
    error_offset,
    levels=None,        
    xscale="linear",
    xlabel=None,
    xlim=None,
    xticks=None,
    yticklabels="operation",  
    figsize=None,
    width=0.7,
    titles=None,       
    ylabel=None,
    show_graph=False,
    show_values=True,
    show_errors=True,
    show_legend=True,
    save_formats=("pdf", "png"),
    file_name="multiples",
    pallet_start=0,
    legend_location="best"
):
    """
    Plota múltiplos gráficos horizontais em uma única figura, um para cada DataFrame da lista.
    Agora cada barra representa uma operação e os grupos representam os algoritmos.
    """
    n_plots = len(dfs)
    fig, axes = plt.subplots(1, 1, figsize=figsize, squeeze=False)
    axes = axes.flatten()
    fontsize = 25
    
    for idx, df in enumerate(dfs):
        algorithms = df['algorithm'].unique()
        n_algorithms = len(algorithms)
        n_operations = len(columns)  
        
        width_bar = width / n_algorithms
        y = np.arange(n_operations) 
        ax = axes[idx]
        palette = sns.color_palette("muted", n_colors=len(algorithms) + pallet_start)
        
        
        for algo_idx, algorithm in enumerate(algorithms):
            color = palette[algo_idx + pallet_start]
            
    
            algo_data = df[df['algorithm'] == algorithm]
            if len(algo_data) == 0:
                continue
                
           
            values = []
            errors = []
            operation_labels = []
             
            for i, (val_col, err_col, label) in enumerate(columns):
                if len(algo_data) > 0:
                    values.append(algo_data[val_col].iloc[0])
                    errors.append(algo_data[err_col].iloc[0])
                    operation_labels.append(label)
            
            bars = ax.barh(
                y + ((n_algorithms - 1 - algo_idx) - (n_algorithms - 1) / 2) * width_bar,
                values,
                height=width_bar,
                xerr=errors if show_errors else None,
                label=algorithm, 
                color=color,
                error_kw={"capsize": 1, "ecolor": "red", "elinewidth": 4}
            )

            if show_values:
                for bar, value in zip(bars, values):
                    if value == 0:
                        ax.text(
                            0.1,
                            bar.get_y() + bar.get_height() / 2,
                            f"N/A",
                            va="center",
                            ha="right",
                            fontsize=fontsize-5,
                            color="black",
                        )
                    else:
                        ax.text(
                            value + values_offset,
                            bar.get_y() + bar.get_height() / 2,
                            f"{value:.2f}",
                            va="center",
                            ha="left",
                            fontsize=fontsize-5,
                            color="black",
                        )

       
        ax.set_yticks(y)
        operation_names = [col[2] for col in columns] 
        ax.set_yticklabels(operation_names, rotation=90, va="center", fontsize=fontsize)

        if ylabel:
            ax.set_ylabel(ylabel, fontsize=fontsize)
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=fontsize)
        if titles and idx < len(titles):
            ax.set_title(titles[idx], fontsize=fontsize)

        ax.set_xscale(xscale)
        if xscale == "log" and xticks is not None:
            ax.set_xticks(xticks)
        if xscale == "linear" and xlim:
            ax.set_xlim(*xlim)
        
        if len(y) > 0:
            ax.set_ylim(y[0] - 0.5, y[-1] + 0.5)
        
        ax.tick_params(axis="y", labelsize=fontsize)
        ax.tick_params(axis="x", labelsize=fontsize)
        if show_legend:
            ax.legend(loc=legend_location, fontsize=fontsize-2)
        ax.grid(True, axis="x", linestyle="--", linewidth=0.5, alpha=0.7)

    plt.tight_layout()
    
    for ext in save_formats:
        file = f"{graphics_directory}/{file_name}.{ext}"
        plt.savefig(file, format=ext, bbox_inches='tight')
        print(f"Saved: {file}")

    if show_graph:
        plt.show()
    plt.close()