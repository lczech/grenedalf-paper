#!/bin/bash

for c in `seq 1 5` ; do
  mkdir -p chr-${c}

  for x in xaa xab xac ; do

        echo "At $c $x"
        zcat ../counts-${x}.sync.gz | egrep "^${c}" | gzip > chr-${c}/counts-${x}.sync.gz

  done
done

