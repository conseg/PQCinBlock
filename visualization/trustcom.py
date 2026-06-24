import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_horizontal_multiple_inverted(
    dfs,                # lista de DataFrames
    columns,
    graphics_directory,
    values_offset,
    error_offset,
    levels=None,        # lista de níveis (opcional)
    xscale="linear",
    xlabel=None,
    xlim=None,
    xticks=None,
    yticklabels="operation",  # Agora são as operações no eixo Y
    figsize=None,
    width=0.7,
    titles=None,        # lista de títulos (opcional)
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
        # Obter lista de algoritmos únicos
        algorithms = df['algorithm'].unique()
        n_algorithms = len(algorithms)
        n_operations = len(columns)  # keypair, sign, verify
        
        width_bar = width / n_algorithms
        y = np.arange(n_operations)  # Agora y representa as operações
        ax = axes[idx]
        palette = sns.color_palette("muted", n_colors=len(algorithms) + pallet_start)
        
        # Para cada algoritmo
        for algo_idx, algorithm in enumerate(algorithms):
            color = palette[algo_idx + pallet_start]
            
            # Encontrar os dados para este algoritmo
            algo_data = df[df['algorithm'] == algorithm]
            if len(algo_data) == 0:
                continue
                
            # Coletar valores para todas as operações deste algoritmo
            values = []
            errors = []
            operation_labels = []
            print(columns)
             
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
                label=algorithm,  # Label é o nome do algoritmo
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

        # Configurar labels do eixo Y com nomes das operações
        ax.set_yticks(y)
        operation_names = [col[2] for col in columns]  # Pega os nomes: "Keypair", "Sign", "Verify"
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
