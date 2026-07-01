

import pandas as pd
from utils import filter_algorithms
from visualization.utils import get_variants_by_level

from visualization.plots import plot_horizontal_multiple_inverted

def generate_bcra_plots(
    results,
    all_algorithms,
    levels,
    output_dir,
    sign_list,
):
    """
    Prepara os dados e define as regras específicas para os gráficos do artigo BCRA.
    """
    print("Gerando gráficos com as configurações do paper BCRA...")
    print("All algorithms loaded:", list(all_algorithms.keys()))
    
    filtered_algorithms = filter_algorithms(all_algorithms, sign_list, levels)
    print("Filtered algorithms:", filtered_algorithms)
    
    combined_mechanisms = {}
    for algorithm in filtered_algorithms.values():
        combined_mechanisms.update(algorithm)

    print("Combined mechanisms:", combined_mechanisms)

    for m in ["scenario1", "scenario2", "scenario3"]:
     
        if m not in results:
            print(f"Aviso: Cenário {m} não encontrado nos resultados. Pulando...")
            continue
            
        df_ethereum = results[m]["blocksim-model-2-mean-std"]
        df_bitcoin = results[m]["blocksim-model-1-mean-std"]
        variants_by_level = get_variants_by_level(df_ethereum, combined_mechanisms)
        
        print("Variants by level:", variants_by_level)
        
        for level, variants in variants_by_level.items():
            print(f"\tProcessing level {level} with variants: {variants}")
            variant_to_algorithm = {v["variant"]: v["algorithm"] for v in variants}
            variant_names = [v["variant"] for v in variants]
            
            # Copy the subsets of each network.
            df_ethereum_subset = df_ethereum.loc[variant_names].copy()
            df_bitcoin_subset = df_bitcoin.loc[variant_names].copy()

            # Map the algorithms
            df_ethereum_subset["algorithm"] = df_ethereum_subset.index.map(variant_to_algorithm)
            
            # 1. Rename the Ethereum columns to avoid conflicts.
            df_combined = df_ethereum_subset.rename(columns={
                "mean_artifacts_size": "eth_mean_size",
                "std_artifacts_size": "eth_std_size"
            })
            
            # 2. Get the Bitcoin columns with unique names.
            df_combined["btc_mean_size"] = df_bitcoin_subset["mean_artifacts_size"]
            df_combined["btc_std_size"] = df_bitcoin_subset["std_artifacts_size"]
            
            # Add missing algorithms (N/A) BEFORE creating algorithm2
            for s in sign_list:
                if s not in df_combined["algorithm"].values:
                    
                    new_row = {col: 0.0 for col in df_combined.columns if col != "algorithm"}
                    new_row["algorithm"] = s
                    new_row["variant"] = f"N/A-{s}"
                    new_row_df = pd.DataFrame([new_row]).set_index("variant")
                    df_combined = pd.concat([df_combined, new_row_df])
             
            # Create algorithm2
            df_combined["algorithm2"] = df_combined.apply(
                lambda x: f"{x['algorithm']}\n({x.name})" if "N/A" not in str(x.name) 
                         else x['algorithm'],
                axis=1
            )

            # Sort and categorize
            df_combined["algorithm"] = pd.Categorical(
                df_combined["algorithm"], 
                categories=sign_list, 
                ordered=True
            )
            df_combined = df_combined.sort_values("algorithm")
            
            # 3. Updates the columns that will be passed to the plotter.
            plot_columns = [
                ("eth_mean_size", "eth_std_size", "Ethereum"),
                ("btc_mean_size", "btc_std_size", "Bitcoin"),
            ]

            xlims = {1: None, 3: None, 5: None}
            
            # 4. Call the plotter genérico!
            plot_horizontal_multiple_inverted(
                dfs=[df_combined],
                columns=plot_columns,
                graphics_directory=output_dir,
                values_offset=3,
                error_offset=0,
                levels=levels,
                figsize=(9, 6),
                xscale="linear",
                xlabel="Cryptographic Artifacts Size (KiB)",
                xlim=(0, xlims.get(level, None)),
                yticklabels="algorithm",
                width=0.7,
                titles=None,
                ylabel=None,
                show_graph=False,
                show_values=True,
                show_errors=True,
                show_legend=True,
                save_formats=["pdf"],
                file_name=f"sim_{m}_level-{level}",
                pallet_start=0,
                legend_location="lower right" 
            )