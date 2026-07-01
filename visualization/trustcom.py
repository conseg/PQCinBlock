import pandas as pd
from visualization.plots import plot_horizontal_multiple_inverted

def generate_benchmark_trustcom_plots(
    results_df,       # Recebe a tabela de dados diretamente
    all_algorithms,
    levels,
    output_dir,
    sign_list
):
    """
    Prepara os dados de tempo (Keypair, Sign, Verify) para os gráficos do TrustCom.
    """
    print("Gerando gráficos com as configurações do paper TrustCom...")
    
    # 1. Filtra apenas os algoritmos que o usuário pediu no terminal/notebook
    df_filtered = results_df[results_df['algorithm'].isin(sign_list)].copy()
    
    # 2. Adiciona N/A para algoritmos faltantes (Regra do TrustCom)
    for s in sign_list:
        if s not in df_filtered["algorithm"].values:
            new_row = {col: 0.0 for col in df_filtered.columns if col != "algorithm"}
            new_row["algorithm"] = s
            df_filtered = pd.concat([df_filtered, pd.DataFrame([new_row])], ignore_index=True)

    # 3. Ordena na exata ordem que o usuário digitou
    df_filtered["algorithm"] = pd.Categorical(df_filtered["algorithm"], categories=sign_list, ordered=True)
    df_filtered = df_filtered.sort_values("algorithm")

    # 4. Define as colunas do TrustCom (as operações criptográficas)
    plot_columns = [
        ("mean_keypair", "std_keypair", "Keypair"),
        ("mean_sign", "std_sign", "Sign"),
        ("mean_verify", "std_verify", "Verify")
    ]

    # 5. Chama o Pintor Genérico (plots.py)
    plot_horizontal_multiple_inverted(
        dfs=[df_filtered],
        columns=plot_columns,
        graphics_directory=output_dir,
        # Aumente ou diminua este valor se os números estiverem batendo na barra de erro (tente 0.1, 0.5, 1.0)
        values_offset=0.2, 
        error_offset=0,
        levels=levels,
        
        # MUDANÇA PRINCIPAL: Aumentamos a largura (14) e a altura (12) da tela!
        figsize=(14, 12), 
        
        xscale="linear",
        xlabel="Average time (ms)",
        yticklabels="operation",  
        
        # MUDANÇA 2: Deixa as barras um pouco mais finas para terem respiro entre elas
        width=0.8, 
        
        show_graph=False,
        show_values=True,
        show_errors=True,
        show_legend=True,
        save_formats=["pdf"],
        file_name=f"trustcom_benchmark_level-{levels[0]}",
        pallet_start=0,
        
        # Se a legenda estiver cobrindo as barras, você pode tentar "upper right" ou "center right"
        legend_location="lower right" 
    )