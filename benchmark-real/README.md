2021-01-29-ath-greneone-release-01

snakemake --use-conda --cores 8 --conda-prefix /home/lucas/Software/conda-envs/ --directory /home/lucas/Projects/grenedalf-paper/benchmark-real all_pileups

gunzip -k *.gz

./grenedalf sync-file --pileup-file /home/lucas/Projects/grenedalf-paper/benchmark-real/mpileup/S1.mpileup.gz --out-dir /home/lucas/Projects/grenedalf-paper/benchmark-real/sync --file-prefix S1_
./grenedalf sync-file --pileup-file /home/lucas/Projects/grenedalf-paper/benchmark-real/mpileup/S2.mpileup.gz --out-dir /home/lucas/Projects/grenedalf-paper/benchmark-real/sync --file-prefix S2_

./diversity.sh
