import numpy as np
from pathlib import Path
import logging

import save
from visualization.graph import generate_graphs, generate_size_graphs

def generate_benchmark_graphs(results_dir, path_csv_benchmark, mechanisms_dict):
    """
    Generates all graphs for the experiment, including algorithm performance
    and simulator results.

    Args:
        results_dir (str or Path): The main results directory.
        mechanisms_dict (dict): A dictionary of the mechanisms used.
    """
    results_dir = Path(results_dir)
    dir_benchmark = results_dir / save.DIR_BENCHMARK

    # Generate graphs for algorithm performance
    path_csv_sign = dir_benchmark / "time-evaluation-mean-std.csv"
    if path_csv_sign.exists():
        logging.info("")
        logging.info("Generating benchmark plots:")
        
        generate_graphs(
            path_csv=str(path_csv_sign),
            results_dir=str(dir_benchmark),
            mechanisms_dict=mechanisms_dict,
            columns=[
                ("mean_sign", "std_sign", "Signature"),
                ("mean_verify", "std_verify", "Verification"),
            ],
            show_legend=True,
            values_offset=0.2,
            error_offset=1.05,
            log_xticks=np.logspace(-3, 4, num=8, base=10),
            log_xlim=(1e-3, 1e4),
        )

        generate_size_graphs(
            path_csv=str(path_csv_sign),
            results_dir=str(dir_benchmark),
            mechanisms_dict=mechanisms_dict
        )
    else:
        logging.warning(f"Warning: Algorithm CSV file not found, skipping algorithm graphs: {path_csv_sign}")
    logging.info("")

def generate_simulator_graphs(results_dir, path_csv_simulator, mechanisms_dict, simulator_was_run=False):

    # Generate graphs for simulator results
    dir_simulator = results_dir / save.DIR_SIMULATOR
    # path_csv_simulator = dir_simulator / "blocksim-mean-std.csv"
    path_csv = Path(path_csv_simulator)
    if path_csv.exists():
        logging.info("")
        logging.info("Generating simulator plots:")
        
        generate_graphs(
            path_csv=str(path_csv),
            results_dir=str(dir_simulator),
            mechanisms_dict=mechanisms_dict,
            columns=[
                ("mean_verify", "std_verify", "Verification"),
            ],
            values_offset=0.2,
            error_offset=1.05,
            log_xticks=np.logspace(-2, 4, num=7, base=10),
            log_xlim=(1e-2, 1e4),
        )
    else:
        if simulator_was_run:
            logging.warning(f"Warning: Simulator output CSV not found, skipping simulator graphs: {path_csv}")
        else:
            logging.info("Simulator not executed, skipping simulator graphs.")