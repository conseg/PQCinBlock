# PQCinBlock

**PQCinBlock** is a modular and extensible benchmark tool for evaluating post-quantum digital signature (PQC) algorithms in blockchain environments.
It allows for the direct measurement of cryptographic operation performance and the impact of cryptographic artifact sizes, as well as realistic blockchain network simulations, through integration with the BlockSim simulator.

[Demo Video](https://youtu.be/lVWv9Dv7tQk)

## Table of Contents / Estrutura do readme.md

- [Considered Badges / Selos Considerados](#considered-badges--selos-considerados)
- [Basic Information / Informações Básicas](#basic-information--informações-básicas)
- [Security Concerns / Preocupações com Segurança](#security-concerns--preocupações-com-segurança)
- [Objectives / Objetivos](#objectives--objetivos)
- [Tool Structure / Estrutura da Ferramenta](#tool-structure--estrutura-da-ferramenta)
  - [Directory Structure / Estrutura de Diretórios](#directory-structure--estrutura-de-diretórios)
- [Requirements / Dependências](#requirements--dependências)
- [Installation / Instalação](#installation--instalação)
- [Execution Environment / Ambiente de Execução](#execution-environment--ambiente-de-execução)
- [Minimal Test / Teste Mínimo](#minimal-test--teste-mínimo)
- [Reproducing the Experiments Described in the Paper / Experimentos](#reproducing-the-experiments-described-in-the-paper--experimentos)
  - [Claim #1: Performance / Reivindicação #1: Desempenho](#claim-1-performance--reivindicação-1-desempenho)
  - [Claim #2: Storage / Reivindicação #2: Armazenamento](#claim-2-storage--reivindicação-2-armazenamento)
- [Argument List / Lista de Argumentos](#argument-list--lista-de-argumentos)
- [Other Execution Flow / Outro Fluxo de Execução (optional/opcional)](#other-execution-flow--outro-fluxo-de-execução-optionalopcional)
- [Adding New Algorithms / Adicionando Novos Algoritmos](#adding-new-algorithms--adicionando-novos-algoritmos)
- [License / LICENSE](#license--license)

## Considered Badges / Selos Considerados

The authors consider the following badges for the evaluation process:

- Artefatos Disponíveis (SeloD)
- Artefatos Funcionais (SeloF)
- Artefatos Sustentáveis (SeloS)
- Experimentos Reprodutíveis (SeloR)

Based on the code and documentation provided in this and related repositories.

## Basic Information / Informações Básicas

The tool consists of Python scripts and uses the `liboqs` library to perform post-quantum cryptographic operations. It requires a Linux or macOS environment (or Docker). Detailed hardware requirements used for the paper's experiments are listed in the [Execution Environment / Ambiente de Execução](#execution-environment--ambiente-de-execução) section.

## Security Concerns / Preocupações com Segurança

There are no security risks associated with executing this artifact. It runs locally and performs cryptographic benchmarks and network simulations without requiring special privileges.

## Objectives / Objetivos

- Compare classical algorithms (e.g., ECDSA) and post-quantum algorithms (e.g., ML-DSA, Dilithium, Falcon, SPHINCS+).
- Simulate the systemic impact of algorithms in blockchain networks.
- Tests on different computing environments.

## Tool Structure / Estrutura da Ferramenta

The tool consists of three main modules, each responsible for a specific part of the evaluation process.

1. **`benchmark`**: Executes algorithms and measures signing, verification, and key generation times and sizes.
2. **`simulator`**: It simulates blockchain networks using collected timing and size data.
3. **`graph`**: Generates charts from the data of the previous two modules.

### Directory Structure / Estrutura de Diretórios
```bash
PQCinBlock/
├── algorithms/           # PQC algorithm implementations (with ALGORITHMS and time_evaluation)
├── auxiliaryFiles/       # Auxiliary files used across the modules
├── BlockSim/             # Blockchain simulator source code (BlockSim)
├── results-paper/        # Complete results used in the papers
├── results/              # Execution results in CSV and charts (not versioned)
├── scripts-SBSeg26/      # Scripts used in the paper's experiments
├── Scripts-execution/    # Scripts used to evaluate the algorithms
├── specificChartGenerators/ # Auxiliary files used to generate specific views
├── visualization/        # Chart generation from execution results
├── venv/                 # Python virtual environment (not versioned)
├── benchmark.py          # Signature algorithms benchmarking module
├── docker-compose.yml    # Docker services configuration
├── Dockerfile            # Docker image definition
├── graph.py              # Auxiliary chart generation script
├── install.sh            # Main installation script
├── LICENSE               # License file
├── main.py               # Main script orchestrating all steps
├── README.md             # This documentation file
├── requirements.txt      # Required Python dependencies
├── simulator.py          # BlockSim interface and execution with collected data
```

## Requirements / Dependências

- [Python >= 3.11.2](https://www.python.org/downloads/release/python-3112/) < 3.14.x
- [liboqs](https://github.com/open-quantum-safe/liboqs)
- [liboqs-python](https://github.com/open-quantum-safe/liboqs-python)
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) *(optional, for containerized execution)*

## Installation / Instalação

### Native Installation / Instalação Nativa

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

#### Virtual Environment / Ambiente Virtual

Activate the virtual environment before running PQCinBlock.

Activate:
```bash
source venv/bin/activate
```

Deactivate:
```bash
deactivate
```

### Using Docker / Usando Docker

Make sure you have Docker and Docker Compose installed.

Clone this repository:
```bash
git clone https://github.com/conseg/PQCinBlock.git
cd PQCinBlock
```

Build the Docker image:
```bash
docker-compose build
```
Alternatively, use the command:
```bash
docker compose build
```

To run the tool via Docker, simply prefix any `python main.py` command shown in this documentation with `docker-compose run --rm pqcinblock`, or `docker compose run --rm pqcinblock`.

**Examples:**
Instead of running: `python main.py --help`
You run: `docker-compose run --rm pqcinblock python main.py --help`
Or: `docker compose run --rm pqcinblock python main.py --help`

For a complete benchmark run:
```bash
docker-compose run --rm pqcinblock python main.py --algorithm ecdsa mldsa --benchmark 5 --warm-up 5 --levels 3
```
Or:
```bash
docker compose run --rm pqcinblock python main.py --algorithm ecdsa mldsa --benchmark 5 --warm-up 5 --levels 3
```

*(Generated results are persisted in your local folder)*

## Execution Environment / Ambiente de Execução

The experiments were performed in the following hardware configurations:

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

- **Raspberry PI4** (performance & storage evaluation)
  - Cortex-A72
  - Raspberry Pi OS 12 (bookworm) Linux Kernel 6.12.62-v8+
  - 4 GB RAM
  - 32 GB disk space

- **Desktop with WSL** (performance & storage evaluation)
  - Intel Pentium G5400 
  - WSL: Ubuntu 24.04.4 LTS Linux Kernel 6.18.33.2-microsoft Host: Windows 11 Pro 10.0.22631
  - WSL: 8 GB Host: 16 GB
  - 500 GB disk space

## Minimal Test / Teste Mínimo

To quickly verify that the tool is installed correctly, you can list the available algorithms:
```bash
python main.py --list-algorithm
```
*(This command will output the list of supported PQC algorithms and indicates a successful setup).*

For a better visualization of the tool's capabilities:

```bash
python main.py --algorithm \
    ecdsa \
    mldsa \
    mayo \
    --benchmark 10 \
    --warm-up 5 \
    --levels 3 5 \
    --blockchain-model 1 2 \
    --simulation 10
```
*(This command will execute one classical and two PQC algorithms with very fast execution).*

## Reproducing the Experiments Described in the Paper / Experimentos

This section describes the step-by-step process for reproducing the experiments in the paper. The experiments are automated and organized to allow independent validation of the experimental results.


> Complete results used in the paper are available in [`results-paper`](./results-paper/)


### Installation and Setup / Instalação e Configuração

Follow the [installation guide in the previous section](#installation--instalação).

### Scripts used in the research paper

To view the exact commands used in the research paper, see the scripts in the [scripts-SBSeg26](scripts-SBSeg26/) folder.

### Claim #1: Performance / Reivindicação #1: Desempenho

**Goal:** Simulate the impact of algorithms on block verification times in a blockchain network, using BlockSim, for NIST security levels 1, 3, and 5. This command generates figures similar to the Figures 2 and 4 of the paper. 

The results are located in `results/*/benchmark/` for raw and consolidated data for `benchmark`.

**Command:**

Use the `run_benchmark_and_simulator.sh` script or the following command:

```bash
python main.py --algorithm \
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
    --benchmark 100 \
    --warm-up 10 \
    --levels 1 2 3 5 \
    --blockchain-model 1 2 \
    --simulation 10
```

**Setup:**

- Flags used: `--algorithm`, `--benchmark`, `--warm-up`, `--levels`, `--blockchain-model`, `--simulation`.
- Estimated runtime: 10–16 hours depending on the machine used.
- The actual runtime and performance results are highly dependent on the used hardware.
- Results: located at `results/*/benchmark/`.

### Claim #2: Storage / Reivindicação #2: Armazenamento

**Goal:** Evaluate the impact of cryptographic artifact sizes on storage.

**Command**

Run a benchmark using the `run_benchmark_only.sh` script, and then use the `run_multiples_simulation_scenarios.sh <path_to_CSV_FILE>` script or the following command, pointing the CSV_FILE variable to the file generated by the benchmark and changing the simulation-scenario variable to the desired scenario. This command generates figures similar to the Figures 2 and 4 (with the first script) and to the Figures 3 and 5 (with the second script) of the paper. 

The `CSV_FILE` to be used is located at `results/*/benchmark/time-evaluation-mean-std.csv`. Use a file previously generated in a benchmark execution.

The results are located in `results/*/benchmark/` for raw and consolidated data for `benchmark` and in `results/*/simulator/` for raw and consolidated data for `simulation`.

```bash
CSV_FILE="$1"

python main.py --algorithm \
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
    --blockchain-model 1 2 \
    --simulation 100 \
    --simulation-scenario 2
```
**Notes**
- Estimated runtime: ~4 hours to benchmark and ~16 hours to each simulation (based on the storage evaluation desktop machine). 
- The actual runtime and performance results are highly dependent on the used hardware.
- Results: located at `results/*/benchmark/` and at `results/*/simulator/`.

## Argument List / Lista de Argumentos

| Arguments          | Description                                          |
| ------------------ | ---------------------------------------------------- |
| `--help`           | Shows the help message with the description of all available arguments and usage instructions. |
| `--list-algorithm`      | Displays all available signature algorithms in the tool. |
| `--algorithm`           | List of digital signature algorithms to evaluate. Supports multiple values, including classical algorithms (e.g., ECDSA) and post-quantum ones (e.g., ML-DSA, Dilithium, Falcon, SPHINCS+). |
| `--benchmark`           | Number of executions of each algorithm. |
| `--warm-up`        | Number of warm-up runs before the main measurement, for performance stabilization.   |
| `--levels`         | Defines the NIST security levels (1 to 5) of the algorithms to be tested. Can receive multiple values. |
| `--blockchain-model` | Defines the *BlockSim* model to use (1: Bitcoin, 2: Ethereum). Can receive multiple values. |
| `--simulation` | Number of simulation runs in *BlockSim*. |
| `--simulation-scenario` | Defines the cryptographic artifact sizes simulation scenario (1: digital signature size only; 2: digital signature + public keys sizes; 3: n * digital signatures + 1 * public key).


## Other Execution Flow / Outro Fluxo de Execução (optional/opcional)

Check available arguments with:
```bash
python main.py --help
```

```text
usage: main.py [-h] [--blockchain-model {1,2} [{1,2} ...]]
               [--algorithm {cross-rsdpg-small,sphincs-shake-s,cross-rsdp-small,cross-rsdpg-fast,cross-rsdpg-balanced,ecdsa,cross-rsdp-fast,falcon,falcon-padded,mldsa,sphincs-shake-f,dilithium,mayo,cross-rsdp-balanced,sphincs-sha-f,sphincs-sha-s} [{cross-rsdpg-small,sphincs-shake-s,cross-rsdp-small,cross-rsdpg-fast,cross-rsdpg-balanced,ecdsa,cross-rsdp-fast,falcon,falcon-padded,mldsa,sphincs-shake-f,dilithium,mayo,cross-rsdp-balanced,sphincs-sha-f,sphincs-sha-s} ...]]
               [--levels {1,2,3,4,5} [{1,2,3,4,5} ...]] [--benchmark BENCHMARK]
               [--warm-up WARM_UP] [--list-algorithm]
               [--simulation SIMULATION] [--input-file INPUT_FILE]
               [--verbosity VERBOSITY]

PQCinBlock

options:
  -h, --help            show this help message and exit 
  --blockchain-model {1,2} [{1,2} ...], -bm {1,2} [{1,2} ...]
                        BlockSim model to use (1: Bitcoin, 2: Ethereum)
                        (default: [2])
 --algorithm {cross-rsdpg-small,sphincs-shake-s,cross-rsdp-small,cross-rsdpg-fast,cross-rsdpg-balanced,ecdsa,cross-rsdp-fast,falcon,falcon-padded,mldsa,sphincs-shake-f,dilithium,mayo,cross-rsdp-balanced,sphincs-sha-f,sphincs-sha-s} [{cross-rsdpg-small,sphincs-shake-s,cross-rsdp-small,cross-rsdpg-fast,cross-rsdpg-balanced,ecdsa,cross-rsdp-fast,falcon,falcon-padded,mldsa,sphincs-shake-f,dilithium,mayo,cross-rsdp-balanced,sphincs-sha-f,sphincs-sha-s} ...], -a {cross-rsdpg-small,sphincs-shake-s,cross-rsdp-small,cross-rsdpg-fast,cross-rsdpg-balanced,ecdsa,cross-rsdp-fast,falcon,falcon-padded,mldsa,sphincs-shake-f,dilithium,mayo,cross-rsdp-balanced,sphincs-sha-f,sphincs-sha-s} [{cross-rsdpg-small,sphincs-shake-s,cross-rsdp-small,cross-rsdpg-fast,cross-rsdpg-balanced,ecdsa,cross-rsdp-fast,falcon,falcon-padded,mldsa,sphincs-shake-f,dilithium,mayo,cross-rsdp-balanced,sphincs-sha-f,sphincs-sha-s} ...]
                        Input list of digital signature algorithms (space-
                        separated) (default: None)
  --levels {1,2,3,4,5} [{1,2,3,4,5} ...], -l {1,2,3,4,5} [{1,2,3,4,5} ...]
                        Nist levels (space-separated) (default: [1, 2, 3, 4,
                        5])
  --benchmark BENCHMARK, -b BENCHMARK  Number of executions (default: 1)
  --warm-up WARM_UP, -wp WARM_UP
                        Number of executions warm up (default: 0)
  --list-algorithm           List of variants digital signature algorithms
                        (default: False)
  --simulation SIMULATION
                        Number of simulator runs (default: 0)
  --input-file INPUT_FILE, -i INPUT_FILE
                        Input CSV file for the simulator to run independently
                        of benchmark. (default: None)
  --verbosity VERBOSITY, -v VERBOSITY
                        verbosity logging level (INFO=20 DEBUG=10) (default:
                        20)

```

### Listing Algorithms and Variants / Listando Algoritmos e Variantes

Show all available digital signature algorithms:
```bash
python main.py --list-algorithm
```

Filter by specific NIST security levels:
```bash
python main.py --list-algorithm --levels <nist_levels>
```

**Example:**
```bash
python main.py --list-algorithm --levels 1 3 5
```

### Running Algorithm Benchmarks / Executando Benchmarks de Algoritmos

Run performance tests (sign, verify) for desired algorithms:
```bash
python main.py --algorithm <algorithms> --benchmark <n> --warm-up <n> --levels <nist_levels>
```

**Example**
```bash
python main.py --algorithm ecdsa mldsa falcon sphincs-sha-s sphincs-shake-f --benchmark 5 --warm-up 5 --levels 3 5
```

### Running Blockchain Simulations / Executando Simulações Blockchain

Use `--simulation` to define how many times each variant will be executed in the simulator:
```bash
python main.py --algorithm ecdsa mldsa falcon sphincs-sha-s sphincs-shake-f --benchmark 5 --warm-up 5 --levels 1 3 5 --simulation 5
```

## Adding New Algorithms / Adicionando Novos Algoritmos

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


## License / LICENSE

This project is distributed under the MIT license. See [`LICENSE`](./LICENSE) for details.
