#!/bin/bash

# Check if a CSV path was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_csv>"
    exit 1
fi

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
    --simulation-scenario 2

