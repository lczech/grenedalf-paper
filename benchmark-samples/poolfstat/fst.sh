#!/bin/bash

OUT=${1}
DATA=${@:2}

mkdir -p fst
mkdir -p logs

# We could not install poolfstat directly from within R,
# so we need a conda environment instead, using
# conda create --name poolfstat
# conda install -c r r-poolfstat r=
# mamba env create -f env.yaml -n poolfstat

# Also, activating a conda env from with a script apparently
# has its issues, and does not work right away, see
# https://stackoverflow.com/a/56155771/4184258
# conda activate base
# conda init bash
eval "$(conda shell.bash hook)"
conda activate poolfstat

echo "Start `date`"
START=$(date +%s.%N)

./fst.R \
    ${DATA} "fst/fst-${OUT}.txt" \
    > logs/fst-${OUT}.log 2>&1

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "End `date`"
echo "Internal time: ${DIFF}"
