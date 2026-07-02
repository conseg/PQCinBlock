import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import logging
import math

from visualization import utils

def _compute_figsize(n_items):
    """Calcula a altura ideal baseada no número de itens no eixo Y."""
    return (16, max(6.0, n_items * 0.7))

def _adaptive_fontsize(n_items, base=24, shrink_factor=0.4, floor=12, ceiling=26):
    """Calcula um fontsize adaptativo que encolhe suavemente com muitos itens."""
    fs = base - (n_items * shrink_factor)
    return max(floor, min(ceiling, fs))

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
    
    if figsize is None:
        figsize = _compute_figsize(n_variants)

    # Adaptive font sizes
    fs_tick   = _adaptive_fontsize(n_variants, base=26, shrink_factor=0.4, floor=14, ceiling=26)
    fs_label  = fs_tick + 2
    fs_title  = fs_label + 6
    fs_value  = _adaptive_fontsize(n_variants, base=20, shrink_factor=0.3, floor=12, ceiling=20)
    fs_error  = fs_value - 1
    fs_legend = _adaptive_fontsize(n_variants, base=20, shrink_factor=0.3, ceiling=22)
    
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
            error_kw={"capsize": 3, "ecolor": "red", "elinewidth": 1.5}
        )

        # Annotate values and errors — positioned AFTER the error bar cap
        if show_values or show_errors:
            for bar_idx, bar in enumerate(bars):
                value = values.iloc[bar_idx] if hasattr(values, 'iloc') else values[bar_idx]
                error = errors.iloc[bar_idx] if hasattr(errors, 'iloc') else errors[bar_idx]
                
                # Check for NaN or Inf before attempting to format
                if pd.isna(value) or math.isinf(value):
                    continue

                right_edge = value + (error if (show_errors and not pd.isna(error)) else 0)
                y_pos = bar.get_y() + bar.get_height() / 2

                parts = []
                if show_values:
                    parts.append(f"{value:.3f}")
                if show_errors and not pd.isna(error):
                    parts.append(f"±{error:.3f}")
                label_text = "  ".join(parts)

                if xscale == "log" and right_edge > 0:
                    x_pos = right_edge * 1.15
                else:
                    x_pos = right_edge + 0.5

                ax.text(
                    x_pos,
                    y_pos,
                    label_text,
                    va="center",
                    ha="left",
                    fontsize=fs_value,
                    color="black",
                    fontweight=500,
                )

    ax.set_yticks(y)
    ax.set_yticklabels(df_all[yticklabels].to_list(), rotation=0, va="center")

    if ylabel:
        ax.set_ylabel(ylabel, fontsize=fs_label)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=fs_label)
    if title:
        ax.set_title(title, fontsize=fs_title)

    ax.set_xscale(xscale)
    if xscale == "log" and xticks is not None:
        ax.set_xticks(xticks)
    if xscale == "linear" and xlim:
        ax.set_xlim(*xlim)

    if len(y) > 0:
        ax.set_ylim(y[0] - 0.5, y[-1] + 0.5)

    ax.tick_params(axis="y", labelsize=fs_tick)
    ax.tick_params(axis="x", labelsize=fs_tick)

    if show_legend:
        ax.legend(loc="upper right", fontsize=fs_legend)

    ax.grid(True, axis="x", linestyle="--", linewidth=0.5, alpha=0.7)
    plt.tight_layout()

    filename = f"level-{level}" if level else "all_level"

    for ext in save_formats:
        file = f"{graphics_directory}/{filename}.{ext}"
        plt.savefig(file, format=ext, bbox_inches='tight')
        logging.info(f"\t{file}")

    if show_graph:
        plt.show()
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
    ylabel=None,
    figsize=None,
    save_formats=["pdf"],
):
    df = pd.read_csv(path_csv, index_col="variant")
    variants_by_level = utils.get_variants_by_level(df, variants_dict)

    for level, mechanisms in variants_by_level.items():
        variant_to_algorithm = {m["variant"]: m["algorithm"] for m in mechanisms}
        variant_names = [m["variant"] for m in mechanisms]
        df_subset = df.loc[variant_names].copy()
        df_subset["algorithm"] = df_subset.index.map(variant_to_algorithm)

        effective_xscale = xscale
        if xscale == "log":
            has_positive_data = False
            for val_col, _, _ in columns:
                if val_col in df_subset.columns and (df_subset[val_col].dropna() > 0).any():
                    has_positive_data = True
                    break
            if not has_positive_data:
                effective_xscale = "linear"
                logging.warning(f"\nWarning: No positive data for level {level} to plot with log scale.")
        
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
    legend_kwargs=None
):
    """
    Plota múltiplos gráficos horizontais em uma única figura.
    No modo invertido (TrustCom), as barras principais (eixo Y) são as operações (ex: Keypair, Sign, Verify)
    e os agrupamentos são os algoritmos. No modo padrão (BCRA), o eixo Y são os algoritmos e agrupamentos são redes.
    """
    n_plots = len(dfs)
    
    if figsize is None:
        if yticklabels == "operation":
            algorithms = dfs[0]['algorithm'].unique()
            n_rows = len(columns) * len(algorithms)
        else:
            y_items = dfs[0][yticklabels].unique() if yticklabels in dfs[0].columns else dfs[0].index
            n_rows = len(y_items) * len(columns)
        figsize = _compute_figsize(n_rows)

    fig, axes = plt.subplots(1, n_plots, figsize=figsize, squeeze=False)
    axes = axes.flatten()

    for idx, df in enumerate(dfs):
        ax = axes[idx]
        
        # Decide the grouping logic based on yticklabels
        if yticklabels == "operation":
            # TrustCom style: Y-axis is operation, Groups are Algorithms
            algorithms = df['algorithm'].unique()
            n_algorithms = len(algorithms)
            n_operations = len(columns)
            
            width_bar = width / n_algorithms
            y = np.arange(n_operations)
            palette = sns.color_palette("muted", n_colors=n_algorithms + pallet_start)

            # Para manter largura razoável mesmo com poucos algoritmos
            width_bar = max(0.04, min(width_bar, 0.2))

            for algo_idx, algorithm in enumerate(algorithms):
                color = palette[algo_idx + pallet_start]
                algo_data = df[df['algorithm'] == algorithm]
                if len(algo_data) == 0:
                    continue

                values = []
                errors = []
                for i, (val_col, err_col, label) in enumerate(columns):
                    values.append(algo_data[val_col].iloc[0] if len(algo_data) > 0 else 0)
                    errors.append(algo_data[err_col].iloc[0] if len(algo_data) > 0 else 0)

                bars = ax.barh(
                    y + ((n_algorithms - 1 - algo_idx) - (n_algorithms - 1) / 2) * width_bar,
                    values,
                    height=width_bar,
                    xerr=errors if show_errors else None,
                    label=algorithm,
                    color=color,
                    error_kw={"capsize": 2, "ecolor": "red", "elinewidth": 1.5}
                )

                if show_values or show_errors:
                    for bar_idx, bar in enumerate(bars):
                        value = values[bar_idx]
                        error = errors[bar_idx]
                        if pd.isna(value) or value == 0:
                            if show_values:
                                ax.text(
                                    0.1, bar.get_y() + bar.get_height() / 2, "N/A",
                                    va="center", ha="left", fontsize=14, color="black"
                                )
                            continue
                        
                        right_edge = value + (error if show_errors else 0)
                        
                        parts = []
                        if show_values:
                            parts.append(f"{value:.3f}")
                        if show_errors:
                            parts.append(f"±{error:.3f}")
                        label_text = "  ".join(parts)
                        
                        x_pos = right_edge * 1.15 if (xscale == "log" and right_edge > 0) else right_edge + max(0.1, right_edge*0.05)
                        
                        ax.text(
                            x_pos, bar.get_y() + bar.get_height() / 2, label_text,
                            va="center", ha="left", fontsize=14, color="black"
                        )

            ax.set_yticks(y)
            operation_names = [col[2] for col in columns]
            ax.set_yticklabels(operation_names, rotation=0, va="center", fontsize=18)
            
        else:
            # BCRA style: Y-axis is Algorithm, Groups are columns (e.g. Ethereum vs Bitcoin)
            y_items = df[yticklabels].unique() if yticklabels in df.columns else df.index
            n_items = len(y_items)
            n_columns = len(columns)
            
            width_bar = width / n_columns
            y = np.arange(n_items)
            palette = sns.color_palette("muted", n_colors=n_columns + pallet_start)

            width_bar = max(0.04, min(width_bar, 0.2))

            for i, (val_col, err_col, label) in enumerate(columns):
                color = palette[i + pallet_start]
                values = df[val_col].values
                errors = df[err_col].values

                reverse_i = n_columns - 1 - i
                
                bars = ax.barh(
                    y + (reverse_i - (n_columns - 1) / 2) * width_bar,
                    values,
                    height=width_bar,
                    xerr=errors if show_errors else None,
                    label=label,
                    color=color,
                    error_kw={"capsize": 2, "ecolor": "red", "elinewidth": 1.5}
                )

                if show_values or show_errors:
                    for bar_idx, bar in enumerate(bars):
                        value = values[bar_idx]
                        error = errors[bar_idx]
                        if pd.isna(value) or value == 0:
                            if show_values:
                                ax.text(
                                    0.1, bar.get_y() + bar.get_height() / 2, "N/A",
                                    va="center", ha="left", fontsize=14, color="black"
                                )
                            continue
                        
                        right_edge = value + (error if show_errors else 0)
                        
                        parts = []
                        if show_values:
                            parts.append(f"{value:.3f}")
                        if show_errors:
                            parts.append(f"±{error:.3f}")
                        label_text = "  ".join(parts)
                        
                        x_pos = right_edge * 1.15 if (xscale == "log" and right_edge > 0) else right_edge + max(0.1, right_edge*0.05)
                        
                        ax.text(
                            x_pos, bar.get_y() + bar.get_height() / 2, label_text,
                            va="center", ha="left", fontsize=14, color="black"
                        )

            ax.set_yticks(y)
            ax.set_yticklabels(y_items, rotation=0, va="center", fontsize=18)

        if ylabel:
            ax.set_ylabel(ylabel, fontsize=20)
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=20)
        if titles and idx < len(titles):
            ax.set_title(titles[idx], fontsize=22)

        ax.set_xscale(xscale)
        if xscale == "log" and xticks is not None:
            ax.set_xticks(xticks)
        if xscale == "linear" and xlim:
            ax.set_xlim(*xlim)

        if len(y) > 0:
            ax.set_ylim(y[0] - 0.5, y[-1] + 0.5)

        ax.tick_params(axis="x", labelsize=18)
        
        if show_legend:
            if legend_kwargs:
                ax.legend(**legend_kwargs)
            else:
                ax.legend(loc="upper right", fontsize=16)
                
        ax.grid(True, axis="x", linestyle="--", linewidth=0.5, alpha=0.7)

    plt.tight_layout()

    for ext in save_formats:
        file = f"{graphics_directory}/{file_name}.{ext}"
        plt.savefig(file, format=ext, bbox_inches='tight')
        print(f"Saved: {file}")

    if show_graph:
        plt.show()
    plt.close()