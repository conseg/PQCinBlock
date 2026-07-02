import pandas as pd
from visualization.plots import plot_horizontal_multiple_inverted
from visualization.utils import get_variants_by_level
from utils import filter_algorithms

def generate_bcra_plots(
    results,
    all_algorithms,
    levels,
    output_dir,
    sign_list,
):
    """
    Processa e gera os gráficos para o formato BCRA (Comparação Ethereum vs Bitcoin).
    Agrupa por algoritmo e mostra as barras para Ethereum e Bitcoin.
    """
    print("Gerando gráficos BCRA...")
    
    filtered_algorithms = filter_algorithms(all_algorithms, sign_list, levels)
    combined_mechanisms = {}
    for algorithm in filtered_algorithms.values():
        combined_mechanisms.update(algorithm)

    for m in ["scenario1", "scenario2", "scenario3"]:
        if m not in results:
            continue
            
        df_ethereum = results[m]["blocksim-model-2-mean-std"]
        df_bitcoin = results[m]["blocksim-model-1-mean-std"]
        variants_by_level = get_variants_by_level(df_ethereum, combined_mechanisms)
        
        for level, variants in variants_by_level.items():
            variant_to_algorithm = {v["variant"]: v["algorithm"] for v in variants}
            variant_names = [v["variant"] for v in variants]
            
            df_ethereum_subset = df_ethereum.loc[variant_names].copy()
            df_bitcoin_subset = df_bitcoin.loc[variant_names].copy()

            df_ethereum_subset["algorithm"] = df_ethereum_subset.index.map(variant_to_algorithm)
            
            # Combine Ethereum and Bitcoin into one df for plotting
            df_combined = df_ethereum_subset.rename(columns={
                "mean_artifacts_size": "eth_mean_size",
                "std_artifacts_size": "eth_std_size"
            })
            df_combined["btc_mean_size"] = df_bitcoin_subset["mean_artifacts_size"]
            df_combined["btc_std_size"] = df_bitcoin_subset["std_artifacts_size"]
            
            # Fill missing algorithms with 0s for spacing
            for s in sign_list:
                if s not in df_combined["algorithm"].values:
                    new_row = {col: 0.0 for col in df_combined.columns if col != "algorithm"}
                    new_row["algorithm"] = s
                    new_row["variant"] = f"N/A-{s}"
                    new_row_df = pd.DataFrame([new_row]).set_index("variant")
                    df_combined = pd.concat([df_combined, new_row_df])
             
            df_combined["algorithm"] = pd.Categorical(
                df_combined["algorithm"], 
                categories=sign_list, 
                ordered=True
            )
            df_combined = df_combined.sort_values("algorithm")
            
            plot_columns = [
                ("eth_mean_size", "eth_std_size", "Ethereum"),
                ("btc_mean_size", "btc_std_size", "Bitcoin"),
            ]

            n_algorithms = len(df_combined["algorithm"].unique())

            plot_horizontal_multiple_inverted(
                dfs=[df_combined],
                columns=plot_columns,
                graphics_directory=output_dir,
                values_offset=0,
                error_offset=0,
                levels=levels,
                figsize=None,
                xscale="linear",
                xlabel="Cryptographic Artifacts Size (KiB)",
                xlim=None,
                yticklabels="algorithm",
                width=0.7,
                show_graph=False,
                show_values=True,
                show_errors=True,
                show_legend=True,
                save_formats=["pdf", "png"],
                file_name=f"sim_{m}_level-{level}",
                pallet_start=0,
                legend_kwargs={
                    "loc": "upper center",
                    "bbox_to_anchor": (0.5, -0.15),
                    "ncol": min(4, n_algorithms),
                    "fontsize": 14,
                    "frameon": True,
                    "borderpad": 0.8,
                    "handletextpad": 0.5,
                    "columnspacing": 1.2,
                },
            )
