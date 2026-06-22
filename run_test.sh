#!/bin/bash

python main.py --algorithms \
    ecdsa \
    mldsa \
    --levels 3 5 \
    --benchmark 3 \
    --warm-up 2 \
    --runs-simulator 2 \
    --model 1 2