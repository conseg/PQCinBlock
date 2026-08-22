#!/bin/bash

# Define the algorithm list
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

python main.py --algorithm "${ALGORITHMS[@]}" \
    --benchmark 100 \
    --warm-up 10 \
    --levels 1 2 3 5
