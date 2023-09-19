#!/bin/bash

GRENEDALF=/central/home/lczech/software/grenedalf-latest/bin/grenedalf

SAMPLES=/central/groups/carnegie_poc/lczech/grenephase1/hafpipe-231-fst-all/

${GRENEDALF} fst --sync-path ${SAMPLES} --window-type genome --method unbiased-nei --pool-sizes 100 --threads 8 --log-file fst.log

