#!/bin/bash

# Check if a CSV path was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_csv>"
    exit 1
fi

CSV_FILE="$1"

# 1. Definindo a lista de algoritmos como um array
ALGORITHMS=(
    ecdsa
    mldsa
    dilithium
    falcon
    falcon-padded
    mayo
    sphincs-sha-s
    sphincs-sha-f
    sphincs-shake-s
    sphincs-shake-f
    cross-rsdp-small
    cross-rsdpg-small
    cross-rsdp-balanced
    cross-rsdpg-balanced
    cross-rsdp-fast
    cross-rsdpg-fast
)

# 2. Variando o parâmetro de cenário de 1 a 3
for SCENARIO in {1..3}; do
    
    echo "======================================================"
    echo "Iniciando execução para simulation-scenario $SCENARIO..."
    echo "======================================================"

    python main.py --algorithm "${ALGORITHMS[@]}" \
        --levels 1 2 3 5 \
        --input-file "$CSV_FILE" \
        --blockchain-model 1 2 \
        --simulation 1000 \
        --simulation-scenario "$SCENARIO"
        
done

echo "Execuções concluídas!"