# grenedalf-paper

Code for tests and benchmarks of the paper on our tool [grenedalf](https://github.com/lczech/grenedalf)

We here provide tests scripts to benchmark [grenedalf](https://github.com/lczech/grenedalf) against existing tools:

  * [grenedalf](https://github.com/lczech/grenedalf)
  * [PoPoolation 1](https://sourceforge.net/projects/popoolation/) (diversity)
  * [PoPoolation 2](https://sourceforge.net/projects/popoolation/) (FST)
  * [poolfstat](https://cran.r-project.org/web/packages/poolfstat/index.html) (FST)
  * [npstat](https://github.com/lucaferretti/npstat) (diversity)

See the `software` directory here for their setup.

With all tools available, we run the following tests here:

  * `benchmark-grenenet`: Benchmarks on real-world data from GrENE-net, subsetting one or two files to increasing numbers of positions to show scaling with respect to the genome length.
  * `benchmark-random`: Simple benchmarks based on randomly generated files, as a lower boundary of how much faster grenedalf is compared to its competitors.
  * `benchmark-samples`: Benchmarks on real-world data from GrENE-net, increasing the number of files to show scaling wrt number of samples.
  * `benchmark-scaling`: Benchmarks for strong and weak scaling of grenedalf on multi-core systems.

Furthermore, we have some auxiliary tests and comparisons:

  * `eval-bug-exam`: Examination of the two bugs in PoPoolation Tajima's D implementation.
  * `eval-correlation`: Test how the results from grenedalf correlate with those of other tools.
  * `eval-fst-biases`: Evaluation of the biases of different Pool-seq estimators of FST.
  * `eval-grenenet`: Quick test to assess the overall gain of grenedalf for our GrENE-net project.

See the respective subdirectories for details.
