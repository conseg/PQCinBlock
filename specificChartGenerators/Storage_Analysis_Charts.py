from re import match

import pandas as pd
import matplotlib.pyplot as plt

def select_pretty_name(variant):
    match variant:
        case 'MAYO-2': return 'MAYO - Lv 1'
        case 'MAYO-3': return 'MAYO - Lv 3'
        case 'MAYO-5': return 'MAYO - Lv 5'
        case 'Falcon-padded-512': return 'Falcon-padded - Lv 1'
        case 'Falcon-padded-1024': return 'Falcon-padded - Lv 5'
        case 'ML-DSA-44': return 'ML-DSA - Lv 1'
        case 'ML-DSA-65': return 'ML-DSA - Lv 3'
        case 'ML-DSA-87': return 'ML-DSA - Lv 5'
        case 'P-256': return 'ECDSA - Lv 1'
        case 'P-384': return 'ECDSA - Lv 3'
        case 'P-521': return 'ECDSA - Lv 5'
        case _: return variant
        
def plot_scenario_comparison(path_csv, config_plot, break_even_pairs, max_transactions=10, fig_name=None):
    desired_columns = ['variant', 'mean_sigSize', 'mean_publicKeySize']
    try:
        df = pd.read_csv(path_csv, usecols=desired_columns)
    except ValueError as e:
        print(f"Error reading CSV. Check the header: {e}")
        return

    plt.figure(figsize=(12, 7))
    x_axis = list(range(1, max_transactions + 1))
    
    plotted_lines = {}

    # 1. Plot the curves according to the chosen scenario.
    for variant, scenario, style, color in config_plot:
        algorithm_data = df[df['variant'] == variant]
        
        if algorithm_data.empty:
            print(f"Warning: '{variant}' not found in CSV. Skipping...")
            continue
            
        sig = float(algorithm_data['mean_sigSize'].values[0])
        pk = float(algorithm_data['mean_publicKeySize'].values[0])
        
        variant_pretty = select_pretty_name(variant)
        
        match scenario:
            case 1:
        # if scenario == 1:
                # Scenario 1: sig * n
                cost = [n * sig for n in x_axis]
                label = f"{variant_pretty} - scenario 1"
                a, b = sig, 0
                marker = 'o'
            case 2:
        # elif scenario == 2:
                # Scenario 2: (sig + pubkey) * n
                cost = [n * (sig + pk) for n in x_axis]
                label = f"{variant_pretty} - scenario 2"
                a, b = (sig + pk), 0
                marker = 's'
            case 3:
        # elif scenario == 3:
                # Scenario 3: pubkey + (sig * n)
                cost = [pk + (n * sig) for n in x_axis]
                label = f"{variant_pretty} - scenario 3"
                a, b = sig, pk
                marker = '^'
            case _:
        # else:
                print(f"Scenario {scenario} unknown. Use 1, 2 or 3.")
                continue
            
        line_id = f"{variant}_C{scenario}"
        plt.plot(x_axis, cost, marker, linestyle=style, color=color, linewidth=2, label=label)
        plotted_lines[line_id] = {'a': a, 'b': b, 'cost': cost, 'color': color}

    # 2. Calculate and plot the break-even points.
    for id_algorithm1, id_algorithm2 in break_even_pairs:
        if id_algorithm1 in plotted_lines and id_algorithm2 in plotted_lines:
            l1, l2 = plotted_lines[id_algorithm1], plotted_lines[id_algorithm2]
            
            # Equating the equations: a1*x + b1 = a2*x + b2
            if (l1['a'] - l2['a']) != 0:
                intersection_point = (l2['b'] - l1['b']) / (l1['a'] - l2['a'])
                
                if 0 < intersection_point <= max_transactions:
                    id_algorithm1_pretty = select_pretty_name(id_algorithm1.split('_')[0])
                    id_algorithm2_pretty = select_pretty_name(id_algorithm2.split('_')[0])
                    plt.axvline(x=intersection_point, color='#b41f1f', linestyle='-.', alpha=0.9, 
                                label=f'Inflection Point {id_algorithm1_pretty} vs {id_algorithm2_pretty} (n ≈ {intersection_point:.1f})')

    # Visual chart settings
    # plt.title('Scenario 3', fontsize=14, pad=15)
    plt.xlabel('Transactions (n)', fontsize=12)
    plt.ylabel('Total Size Accumulated (Bytes)', fontsize=12)
    plt.xticks(x_axis)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(fontsize=10, loc='upper left')
    
    plt.tight_layout()
    plt.savefig(fig_name, dpi=300)
    print(f"Exported chart: {fig_name}")
    plt.show()

# =======================================================
# EXAMPLE OF USE
# =======================================================
if __name__ == "__main__":
    path_csv = 'results-bcra/InputBenchmark/time-evaluation-mean-std.csv' 

    # fig_name = 'analise-nv3-edgecase1-pqc.pdf'
    output_dir = 'results-bcra/paper_graphics'
    max_transactions = 10

    configs = { 
    "All_Scenarios-lv1":[
        ('MAYO-2',  1, '-', '#2ca02c'),             # Green (scenario 1: Sig only)
        ('MAYO-2',  2, '-', '#2ca02c'),             # Green (scenario 2: Sig + PK)
        ('MAYO-2',  3, '-', '#2ca02c'),             # Green (scenario 3: 1 PK fixed + n*Sig)
        ('Falcon-padded-512', 1, '-', '#1f77b4'),  # Blue (scenario 1: Sig only)
        ('Falcon-padded-512', 2, '-', '#1f77b4'),  # Blue (scenario 2: Sig + PK)
        ('Falcon-padded-512', 3, '-', '#1f77b4'),  # Blue (scenario 3: 1 PK fixed + n*Sig)
        ('ML-DSA-44', 1, '-', '#ff7f0e'),            # Orange (scenario 1: Sig only)
        ('ML-DSA-44', 2, '-', '#ff7f0e'),            # Orange (scenario 2: Sig + PK)
        ('ML-DSA-44', 3, '-', '#ff7f0e'),            # Orange (scenario 3: 1 PK fixed + n*Sig)
        ('P-256', 1, '-', '#8c564b'),              # Brown (scenario 1: Sig only)
        ('P-256', 2, '-', '#8c564b'),             # Brown (scenario 2: Sig + PK)
        ('P-256', 3, '-', '#8c564b')              # Brown (scenario 3: 1 PK fixed + n*Sig)
    ],
    "All_Scenarios-lv3":[
        ('MAYO-3',  1, '-', '#2ca02c'),             # Green (scenario 1: Sig only)
        ('MAYO-3',  2, '-', '#2ca02c'),             # Green (scenario 2: Sig + PK)
        ('MAYO-3',  3, '-', '#2ca02c'),             # Green (scenario 3: 1 PK fixed + n*Sig)
        ('ML-DSA-65', 1, '-', '#ff7f0e'),            # Orange (scenario 1: Sig only)
        ('ML-DSA-65', 2, '-', '#ff7f0e'),            # Orange (scenario 2: Sig + PK)
        ('ML-DSA-65', 3, '-', '#ff7f0e'),            # Orange (scenario 3: 1 PK fixed + n*Sig)
        ('P-384', 1, '-', '#8c564b'),              # Brown (scenario 1: Sig only)
        ('P-384', 2, '-', '#8c564b'),             # Brown (scenario 2: Sig + PK)
        ('P-384', 3, '-', '#8c564b')              # Brown (scenario 3: 1 PK fixed + n*Sig)
    ],
    "All_Scenarios-lv5":[
        ('MAYO-5',  1, '-', '#2ca02c'),             # Green (scenario 1: Sig only)
        ('MAYO-5',  2, '-', '#2ca02c'),            # Green (scenario 2: Sig + PK)
        ('MAYO-5',  3, '-', '#2ca02c'),             # Green (scenario 3: 1 PK fixed + n*Sig)
        ('Falcon-padded-1024', 1, '-', "#1f77b4"),  # Blue (scenario 1: Sig only)
        ('Falcon-padded-1024', 2, '-', '#1f77b4'),  # Blue (scenario 2: Sig + PK)
        ('Falcon-padded-1024', 3, '-', '#1f77b4'),  # Blue (scenario 3: 1 PK fixed + n*Sig)
        ('ML-DSA-87', 1, '-', '#ff7f0e'),            # Orange (scenario 1: Sig only)
        ('ML-DSA-87', 2, '-', '#ff7f0e'),            # Orange (scenario 2: Sig + PK)
        ('ML-DSA-87', 3, '-', '#ff7f0e'),            # Orange (scenario 3: 1 PK fixed + n*Sig)
        ('P-521', 1, '-', '#8c564b'),              # Brown (scenario 1: Sig only)
        ('P-521', 2, '-', '#8c564b'),             # Brown (scenario 2: Sig + PK)
        ('P-521', 3, '-', '#8c564b')              # Brown (scenario 3: 1 PK fixed + n*Sig)
    ],
    
    "Edge_case_1(lv3)": [
        ('MAYO-3',  2, '-', '#2ca02c'),             # Green (scenario 2: Sig + PK)
        ('ML-DSA-65', 2, '-', '#ff7f0e')             # Orange (scenario 2: Sig + PK)
    ],

    "Edge_case_2(lv1)": [
        ('MAYO-2',  3, '-', '#2ca02c'),             # Green (scenario 2: Sig + PK)
        ('Falcon-padded-512', 3, '-', '#1f77b4')    # Blue (scenario 2: Sig + PK)
    ],
    
    "Edge_case_2(lv3)": [
        ('MAYO-3',  3, '-', '#2ca02c'),             # Green (scenario 3: 1 PK fixed + n*Sig)
        ('ML-DSA-65', 3, '-', '#ff7f0e')             # Orange (scenario 3: 1 PK fixed + n*Sig)
    ],

    "Edge_case_2(lv5)": [
        ('MAYO-5',  3, '-', '#2ca02c'),             # Green (scenario 3: 1 PK fixed + n*Sig)
        ('Falcon-padded-1024', 3, '-', '#1f77b4')    # Blue (scenario 3: 1 PK fixed + n*Sig)
    ]
    }
    
    # list_of_configs = [configs1, configs2, configs3, configs4, configs5, configs6, configs7]

    
    for name, configs in configs.items():
        if name.startswith("Edge_case"):
            # Break-even tuples use the format "Variant_C[scenario_number]" to allow comparing the same algorithm in different scenarios.
            pairs = [
                ('Falcon-padded-512_C3', 'MAYO-2_C3'),
                ('Falcon-padded-1024_C3', 'MAYO-5_C3'),
                ('ML-DSA-65_C3', 'MAYO-3_C3')
            ]
        else:
            pairs = []
        plot_scenario_comparison(path_csv, configs, pairs, max_transactions=max_transactions, fig_name=f"{output_dir}/{name}.pdf")