from pathlib import Path
from datetime import datetime
import logging

DIR_RESULTS = "results"
DIR_BENCHMARK = "benchmark"
DIR_GRAPH = "graphs"
DIR_SIMULATOR = "simulator"

def _create_directory(root_directory, directory_name=None):
    if directory_name:
        directory = Path(root_directory) / directory_name
        directory.mkdir(parents=True, exist_ok=True)
        return directory
    else:
        Path(root_directory).mkdir(parents=True, exist_ok=True)
        return Path(root_directory)

def _mount_results_directory(timestamp, algorithms_dict, levels):

    mechanisms = set()
    for module_mechanisms in algorithms_dict.values():
        mechanisms.update(module_mechanisms.keys())
    mechanisms_str = "_".join(sorted(mechanisms))

    levels_str = "-".join(str(level) for level in sorted(levels))

    base_dir = f"{timestamp}_{mechanisms_str}_levels-{levels_str}"
    
    path = Path(DIR_RESULTS) / base_dir

    return path

def create_results_directory(timestamp, algorithms_dict, levels):
    path = _mount_results_directory(timestamp, algorithms_dict, levels)
    return _create_directory(path)

def create_benchmark_directory(root_directory):
    return _create_directory(root_directory, DIR_BENCHMARK)

def create_graphics_directory(root_directory):
    return _create_directory(root_directory, DIR_GRAPH)

def create_simulator_directory(root_directory):
    return _create_directory(root_directory, DIR_SIMULATOR)
