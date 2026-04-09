# PQCinBlock

<!-- [Demo Video](https://youtu.be/CNKmvOyZqm0) -->

**PQCinBlock** is a modular and extensible benchmark tool for evaluating post-quantum digital signature (PQC) algorithms in blockchain environments.
It allows for the direct measurement of cryptographic operation performance and the impact of cryptographic artifact sizes, as well as realistic blockchain network simulations, through integration with the BlockSim simulator.

## Table of Contents

- [Objectives](#objectives)
- [Tool Structure](#tool-structure)
- [Directory Structure](#directory-structure)
- [Requirements](#requirements)
- [Argument List](#argument-list)
- [Execution](#execution)
- [Adding New Algorithms](#adding-new-algorithms)
- [Reproducing the Experiments Described in the Paper](#reproducing-the-experiments-described-in-the-paper)
- [License](#license)


## Objectives

- Compare classical algorithms (e.g., ECDSA) and post-quantum algorithms (e.g., ML-DSA, Dilithium, Falcon, SPHINCS+).
- Allow continuous and modular integration of new algorithms.
- Simulate the systemic impact of algorithms in blockchain networks.

## Tool Structure

The tool consists of three main modules, each responsible for a specific part of the evaluation process.

1. **`benchmark`**: Executes algorithms and measures signing, verification, and key generation times and sizes.
2. **`simulator`**: It simulates blockchain networks using collected timing and size data.
3. **`graph`**: Generates charts from the data of the previous two modules.

### Directory Structure
```bash
PQCinBlock/
├── algorithms/           # PQC algorithm implementations (with ALGORITHMS and time_evaluation)
├── BlockSim/             # Blockchain simulator source code (BlockSim)
├── results-paper/        # Complete results used in the papers (v1 and v2)
├── results/              # Execution results in CSV and charts (not versioned)
├── visualization/        # Chart generation from execution results
├── venv/                 # Python virtual environment (not versioned)
├── benchmark.py          # Signature algorithms benchmarking module
├── graph.py              # Auxiliary chart generation script
├── info.py               # Auxiliary metadata collector
├── install.sh            # Main installation script
├── LICENSE               # License file
├── main.py               # Main script orchestrating all steps
├── README.md             # This documentation file
├── requirements.txt      # Required Python dependencies
├── run_benchmark_and_simulator.sh     # Runs all experiments described in the paper (v1)
├── run_benchmark_only.sh # Run all algorithms, but no simulations
├── run_simulator_only.sh # Run only the simulator using data from an input file
├── save.py               # Result saving functions
├── simulator.py          # BlockSim interface and execution with collected data
├── utils.py              # Auxiliary utility functions
├── Storage_Analysis_Charts.py  # Auxiliary chart generation script tailored to storage analysis
```

## Requirements

- [Python 3.11.2+](https://www.python.org/downloads/release/python-3112/)
- [liboqs](https://github.com/open-quantum-safe/liboqs)
- [liboqs-python](https://github.com/open-quantum-safe/liboqs-python)

### Installation:

Clone this repository:
```bash
git clone https://github.com/conseg/PQCinBlock.git
cd PQCinBlock
```

Make the installation script executable:
```bash
chmod +x install.sh
```

Install the requirements:
```bash
./install.sh
```

>It is recommended to use the same version of `liboqs` and `liboqs-python`. By default, we use version `0.12.0`, defined in the variables at the beginning of [install.sh](./install.sh).

#### Virtual Environment

Activate the virtual environment before running PQCinBlock.

Activate:
```bash
source venv/bin/activate
```

Deactivate:
```bash
deactivate
```

## Argument List

| Arguments          | Description                                          |
| ------------------ | ---------------------------------------------------- |
| `--help`           | Shows the help message with the description of all available arguments and usage instructions. |
| `--list-sign`      | Displays all available signature algorithms in the tool. |
| `--sign`           | List of digital signature algorithms to evaluate. Supports multiple values, including classical algorithms (e.g., ECDSA) and post-quantum ones (e.g., ML-DSA, Dilithium, Falcon, SPHINCS+). |
| `--runs`           | Number of executions of each algorithm. |
| `--warm-up`        | Number of warm-up runs before the main measurement, for performance stabilization.   |
| `--levels`         | Defines the NIST security levels (1 to 5) of the algorithms to be tested. Can receive multiple values. |
| `--model` | Defines the *BlockSim* model to use (1: Bitcoin, 2: Ethereum). Can receive multiple values. |
| `--runs-simulator` | Number of simulation runs in *BlockSim*. |
| `--simulation-scenario` | Defines the cryptographic artifact sizes simulation scenario (1: digital signature size only ,2: digital signature + public keys sizes, 3: n * digital signatures + 1 * public key)


## Execution

Check available arguments with:
```bash
python main.py --help
```

```text
usage: main.py [-h] [--model {1,2} [{1,2} ...]]
               [--sign {cross-rsdpg-small,sphincs-shake-s,cross-rsdp-small,cross-rsdpg-fast,cross-rsdpg-balanced,ecdsa,cross-rsdp-fast,falcon,falcon-padded,mldsa,sphincs-shake-f,dilithium,mayo,cross-rsdp-balanced,sphincs-sha-f,sphincs-sha-s} [{cross-rsdpg-small,sphincs-shake-s,cross-rsdp-small,cross-rsdpg-fast,cross-rsdpg-balanced,ecdsa,cross-rsdp-fast,falcon,falcon-padded,mldsa,sphincs-shake-f,dilithium,mayo,cross-rsdp-balanced,sphincs-sha-f,sphincs-sha-s} ...]]
               [--levels {1,2,3,4,5} [{1,2,3,4,5} ...]] [--runs RUNS]
               [--warm-up WARM_UP] [--list-sign]
               [--runs-simulator RUNS_SIMULATOR] [--input-file INPUT_FILE]
               [--verbosity VERBOSITY]

PQCinBlock

options:
  -h, --help            show this help message and exit
  --model {1,2} [{1,2} ...], -m {1,2} [{1,2} ...]
                        BlockSim model to use (1: Bitcoin, 2: Ethereum)
                        (default: [2])
  --sign {cross-rsdpg-small,sphincs-shake-s,cross-rsdp-small,cross-rsdpg-fast,cross-rsdpg-balanced,ecdsa,cross-rsdp-fast,falcon,falcon-padded,mldsa,sphincs-shake-f,dilithium,mayo,cross-rsdp-balanced,sphincs-sha-f,sphincs-sha-s} [{cross-rsdpg-small,sphincs-shake-s,cross-rsdp-small,cross-rsdpg-fast,cross-rsdpg-balanced,ecdsa,cross-rsdp-fast,falcon,falcon-padded,mldsa,sphincs-shake-f,dilithium,mayo,cross-rsdp-balanced,sphincs-sha-f,sphincs-sha-s} ...], -s {cross-rsdpg-small,sphincs-shake-s,cross-rsdp-small,cross-rsdpg-fast,cross-rsdpg-balanced,ecdsa,cross-rsdp-fast,falcon,falcon-padded,mldsa,sphincs-shake-f,dilithium,mayo,cross-rsdp-balanced,sphincs-sha-f,sphincs-sha-s} [{cross-rsdpg-small,sphincs-shake-s,cross-rsdp-small,cross-rsdpg-fast,cross-rsdpg-balanced,ecdsa,cross-rsdp-fast,falcon,falcon-padded,mldsa,sphincs-shake-f,dilithium,mayo,cross-rsdp-balanced,sphincs-sha-f,sphincs-sha-s} ...]
                        Input list of digital signature algorithms (space-
                        separated) (default: None)
  --levels {1,2,3,4,5} [{1,2,3,4,5} ...], -l {1,2,3,4,5} [{1,2,3,4,5} ...]
                        Nist levels (space-separated) (default: [1, 2, 3, 4,
                        5])
  --runs RUNS, -r RUNS  Number of executions (default: 1)
  --warm-up WARM_UP, -wp WARM_UP
                        Number of executions warm up (default: 0)
  --list-sign           List of variants digital signature algorithms
                        (default: False)
  --runs-simulator RUNS_SIMULATOR
                        Number of simulator runs (default: 0)
  --input-file INPUT_FILE, -i INPUT_FILE
                        Input CSV file for the simulator to run independently
                        of benchmark. (default: None)
  --verbosity VERBOSITY, -v VERBOSITY
                        verbosity logging level (INFO=20 DEBUG=10) (default:
                        20)

```

### Listing Algorithms and Variants

Show all available digital signature algorithms:
```bash
python main.py --list-sign
```

Filter by specific NIST security levels:
```bash
python main.py --list-sign --levels <nist_levels>
```

**Example:**
```bash
python main.py --list-sign --levels 1 3 5
```

### Running Algorithm Benchmarks

Run performance tests (sign, verify) for desired algorithms:
```bash
python main.py --sign <algorithms> --runs <n> --warm-up <n> --levels <nist_levels>
```

**Example**
```bash
python main.py --sign ecdsa mldsa falcon sphincs-sha-s sphincs-shake-f --runs 5 --warm-up 5 --levels 3 5
```

### Running Blockchain Simulations

Use `--runs-simulator` to define how many times each variant will be executed in the simulator:
```bash
python main.py --sign ecdsa mldsa falcon sphincs-sha-s sphincs-shake-f --runs 5 --warm-up 5 --levels 1 3 5 --runs-simulator 5
```

## Adding New Algorithms

To add a new algorithm, create a `.py` file in `algorithms/` with the following structure:

```python
import pandas as pd

ALGORITHMS = {
    # The levels (1 to 5) can be defined according to the algorithm’s availability.
    # It is not mandatory to fill in all levels.
    "algorithm_name": {
        <level_1>: "variant_name",
        <level_2>: "variant_name",
        <level_3>: "variant_name",
        <level_4>: "variant_name",
        <level_5>: "variant_name",
    }, ...
}

def time_evaluation(variant: str, runs: int):
    
    # Implement the benchmark logic for the given algorithm variant.
    # This function should return a DataFrame with 'sign' and 'verify' execution times.

    return pd.DataFrame({
        'variant': [variant] * runs,
        'sign': time_sign,
        'verify': time_verify
    })
```

## Reproducing the Experiments Described in the Paper

This section describes the step-by-step process for reproducing the experiments in the paper. The experiments are automated and organized to allow independent validation of the experimental.


> Complete results used in the paper are available in [`results-paper`](./results-paper/)


### Execution Environment

The experiments were performed in three hardware configurations:

- **Laptop ARM** (performance evaluation)
  - Apple M1
  - macOS Darwin Kernel 24.0.0
  - 8 GB RAM

- **Laptop x64** (performance evaluation)
  - Intel Core i7-1360P
  - Ubuntu 22.04.1 LTS Linux Kernel 6.8.0-65-generic
  - 32 GB RAM

- **Desktop** (performance evaluation)
  - AMD Ryzen 7 5800X
  - Ubuntu 24.04.2 LTS Linux Kernel 6.8.0-64-generic
  - 80 GB RAM

- **Desktop** (storage evaluation)
  - Intel Core i5-8500
  - Ubuntu 25.10 Linux Kernel 6.17.0-20-generic
  - 16 GB RAM
  - 234 GB disk space


### Installation and Setup

1. Clone this repository:
```bash
git clone https://github.com/conseg/PQCinBlock.git
cd PQCinBlock
```

2. Grant execution permission to the script:
```bash
chmod +x install.sh
```

3. Install the requirements:
```bash
./install.sh
```

4. Activate the virtual environment:
```bash
source venv/bin/activate
```

### Evaluating the Impact of Algorithms on Blockchain Simulation

**Goal:** Simulate the impact of algorithms on block verification times in a blockchain network, using BlockSim, for NIST security levels 1, 3, and 5.

#### Performance

**Command:**

Use the `run_benchmark_and_simulator.sh` scrip or the following command:
```bash
python main.py --sign \
    ecdsa \
    mldsa \
    dilithium \
    falcon \
    falcon-padded \
    mayo \
    sphincs-sha-s \
    sphincs-sha-f \
    sphincs-shake-s \
    sphincs-shake-f \
    cross-rsdp-small \
    cross-rsdpg-small \
    cross-rsdp-balanced \
    cross-rsdpg-balanced \
    cross-rsdp-fast \
    cross-rsdpg-fast \
    --runs 10000 \
    --warm-up 1000 \
    --levels 1 2 3 5 \
    --model 1 2 \
    --runs-simulator 1000
```

**Setup:**

- Flags used: `--sign`, `--runs`, `--warm-up`, `--levels`, `--model`, `--runs-simulator`.
- Estimated runtime: 10–16 hours depending on the machine used.
- Results: CSV files and charts in `./results/`.

#### Storage

**Command**

Run a benchmark using the `run_benchmark_only.sh` script, and then use the `run_multiples_simulation_scenarios.sh` script or the following command, pointing the CSV_FILE variable to the file generated by the benchmark and changing the simulation-scenario variable to the desired scenario.

```

CSV_FILE="$1"

python main.py --sign \
    ecdsa \
    mldsa \
    dilithium \
    falcon \
    falcon-padded \
    mayo \
    sphincs-sha-s \
    sphincs-sha-f \
    sphincs-shake-s \
    sphincs-shake-f \
    cross-rsdp-small \
    cross-rsdpg-small \
    cross-rsdp-balanced \
    cross-rsdpg-balanced \
    cross-rsdp-fast \
    cross-rsdpg-fast \
    --levels 1 2 3 5 \
    --input-file "$CSV_FILE" \
    --model 1 2 \
    --runs-simulator 2 \
    --simulation-scenario 1
```
**Notes**
- Estimated runtime: ~4 hours to benchmar and ~16 hours to each simulation (based on the storage evaluation desktop machine).
- Results: CSV files and charts in `./results/`.

## License

This project is distributed under the MIT license. See [`LICENSE`](./LICENSE) for details.
