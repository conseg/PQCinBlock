import pandas as pd
from visualization.plots import plot_horizontal_multiple_inverted
from visualization.utils import get_variants_by_level
from auxiliaryFiles.utils import filter_algorithms

def generate_trustcom_plots(
    results,
    all_algorithms,
    levels,
    output_dir,
    sign_list
):
    """
    Generates TrustCom plots with inverted axes (operations on Y-axis).
    """
    print("Generating TrustCom plots...")
    
    filtered_algorithms = filter_algorithms(all_algorithms, sign_list, levels)
    combined_mechanisms = {}
    for algorithm in filtered_algorithms.values():
        combined_mechanisms.update(algorithm)

    plot_columns = [
        ("mean_verify", "std_verify", "Verify"),
        ("mean_sign", "std_sign", "Sign"),
        ("mean_keypair", "std_keypair", "Keypair")
    ]

    for m in results.keys():
        if "time-evaluation-mean-std" not in results[m]:
            continue
            
        df = results[m]["time-evaluation-mean-std"]
        variants_by_level = get_variants_by_level(df, combined_mechanisms)

        for level, variants in variants_by_level.items():
            variant_to_algorithm = {v["variant"]: v["algorithm"] for v in variants}
            variant_names = [v["variant"] for v in variants]

            df_subset = df.loc[variant_names].copy()
            df_subset["algorithm"] = df_subset.index.map(variant_to_algorithm)

            for s in sign_list:
                if s not in df_subset["algorithm"].values:
                    new_row = {col: 0.0 for col in df_subset.columns if col != "algorithm"}
                    new_row = {**new_row, "algorithm": s, "variant": f"N/A-{s}"}
                    new_row_df = pd.DataFrame([new_row]).set_index("variant")
                    df_subset = pd.concat([df_subset, new_row_df])

            df_subset["algorithm"] = pd.Categorical(
                df_subset["algorithm"],
                categories=sign_list,
                ordered=True
            )
            df_subset = df_subset.sort_values("algorithm")

            n_algorithms = len(df_subset["algorithm"].unique())

            plot_horizontal_multiple_inverted(
                dfs=[df_subset],
                columns=plot_columns,
                graphics_directory=output_dir,
                values_offset=0,
                error_offset=0,
                xscale="log",
                xlabel="Time (ms)",
                xlim=(1e-3, 1e4),
                xticks=[10**i for i in range(-3, 5)],
                yticklabels="operation",
                figsize=None,
                width=0.7,
                show_graph=False,
                show_values=True,
                show_errors=True,
                show_legend=True,
                save_formats=["pdf", "png"],
                file_name=f"bench_{m}_level-{level}",
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
                }
            )