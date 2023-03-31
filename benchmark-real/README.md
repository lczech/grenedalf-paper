This is a small test using real world data from our GrENE-net dataset.

## Process

The test uses the samples from our data release `2021-01-29-ath-greneone-release-01`,
as specified in the `samples.tsv` table.

These reads were trimmed, mapped, and written as `mpileup` files 
by [grenepipe 0.4.0](https://github.com/moiexpositoalonsolab/grenepipe/releases/tag/v0.4.0),
using the `config.yaml` configuration file, and running with the command

    snakemake --use-conda --cores 8 --directory /path/to/grenedalf-paper/benchmark-real all_pileups

Then, the `mpileup` files were turned into `sync` files with grenedalf v0.1.0 with the commands

    ./grenedalf sync-file \
        --pileup-file /path/to/grenedalf-paper/benchmark-real/mpileup/S1.mpileup.gz \
        --out-dir     /path/to/grenedalf-paper/benchmark-real/sync \
        --file-prefix S1_
    ./grenedalf sync-file \
        --pileup-file /path/to/grenedalf-paper/benchmark-real/mpileup/S2.mpileup.gz \
        --out-dir     /path/to/grenedalf-paper/benchmark-real/sync \
        --file-prefix S2_

After that, the benchmarks of grenedalf and popoolation were run on these files.
The results of these runtimes are reported in `run.log`.
The `hist` files contain histograms of read coverage per position, for further examination of the data.

## Results

The main purpose of this test was to see how much time 
it would take to run PoPoolation on our whole GrENE-net dataset.
At the time of testing, we had ~1.7TB of fastq.gz files in the project, 
which is ~1,500 times the amount used for testing here.

That would require ~6.3TB mpileup files just so that PoPoolation could read them.
(Even though not all of them would have to be kept on disk,
but generating them would also cause overhead.)

With PoPoolation, we hence estimated the total runtime to be around 125 days.
With grenedalf, this would be reduced to a single day.
And this was with a restricted `mpilup` only containg up to 1000bp coverage per position;
more would have slowed PoPoolation down even more, massively.

