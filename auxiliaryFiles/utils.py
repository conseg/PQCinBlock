import argparse
import os
import importlib
import logging
import shlex
import subprocess
import inspect
from typing import Callable, Any
import pandas as pd

def positive_int(value: int):
    """
    Validates that the provided value is a positive integer.

    Parameters:
        value (int): The value to validate.

    Returns:
        int: The validated positive integer.

    Raises:
        argparse.ArgumentTypeError: If the value is not a positive integer.
    """
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    return ivalue

def non_negative_int(value: int):
    """
    Validates that the provided value is a non-negative integer.

    Parameters:
        value (int): The value to validate.

    Returns:
        int: The validated non-negative integer.

    Raises:
        argparse.ArgumentTypeError: If the value is negative.
    """
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(f"{value} is not a non-negative integer")
    return ivalue

def compute_mean_std(df, group_by, columns):
    """
    Compute mean and standard deviation for specified columns grouped by a key.

    Parameters:
    - df: The input DataFrame.
    - group_by: Column name to group by (e.g., 'variant').
    - columns: List of column names to compute mean and std for.

    Returns:
    - pd.DataFrame: DataFrame with mean and std columns.
    """
    grouped = df.groupby(group_by)

    result = pd.DataFrame()
    for col in columns:
        result[f'mean_{col}'] = grouped[col].mean()
        result[f'std_{col}'] = grouped[col].std()

    # Transform the index into a column
    result = result.reset_index()
    return result

def _load_from_modules(package: str, attribute_name: str, filter_func: Callable[[Any], bool] = lambda x: True):
    result = {}
    package_path = package.replace('.', '/')

    for file in os.listdir(package_path):
        if file.endswith('.py') and not file.startswith('__'):
            module_name = file[:-3]
            full_module_name = f"{package}.{module_name}"
            module = importlib.import_module(full_module_name)

            attr = getattr(module, attribute_name, None)
            if attr is not None and filter_func(attr):
                result[module_name] = attr

    return result

def load_algorithms(package: str):
    return _load_from_modules(package, "ALGORITHMS")

def load_functions(package: str):
    return _load_from_modules(package, "time_evaluation", inspect.isfunction)

def extract_algorithms(all_algorithms: dict):
    algorithms = set()
    for module, algorithm in all_algorithms.items():
        algorithms.update(algorithm.keys())
    return algorithms

def filter_algorithms(algorithms: dict, selected_algorithms: list = None, selected_levels: list = None) -> dict:
    selected_algorithms = selected_algorithms or []
    selected_levels = selected_levels or []

    filtered = {}

    for module, algos in algorithms.items():
        for algorithm, variants in algos.items():
            if selected_algorithms and algorithm not in selected_algorithms:
                continue

            selected_variants = {
                level: name for level, name in variants.items()
                if not selected_levels or level in selected_levels
            }

            if selected_variants:
                filtered.setdefault(module, {})[algorithm] = selected_variants

    return filtered

def run_cmd(cmd, shell=False):
    """
    Executes a shell/system command with logging, respecting dry-run mode.

    Parameters
    ----------
    cmd : str
        The shell command to execute.
    shell : bool
        Whether to execute the command within a shell environment.

    Notes
    -----
    - Logs both the raw command and the parsed array (if applicable).
    - Supports dry-run mode via args.dryrun.
    """
    logging.info("Command line: {}".format(cmd))
    cmd_array = shlex.split(cmd)
    logging.debug("Command array: {}".format(cmd_array))
    logging.info("")
    # if not arguments.dryrun:
    subprocess.run(cmd_array, check=True, shell=shell)