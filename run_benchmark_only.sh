#!/bin/bash

python main.py --algorithms \
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
    --benchmark 10000 \
    --warm-up 1000 \
    --levels 1 2 3 5
