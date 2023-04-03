# grenedalf-paper

Code for tests and benchmarks of the paper on our tool [grenedalf](https://github.com/lczech/grenedalf)

We here provide tests scripts to benchmark [grenedalf](https://github.com/lczech/grenedalf) against existing tools:

  * [grenedalf](https://github.com/lczech/grenedalf)
  * [PoPoolation 1](https://sourceforge.net/projects/popoolation/)
  * [PoPoolation 2](https://sourceforge.net/projects/popoolation/)
  * [poolfstat](https://cran.r-project.org/web/packages/poolfstat/index.html)
  * [npstat](https://github.com/lucaferretti/npstat)

See the `software` directory here for their setup.

With all tools available, we run the following tests here:

  * `benchmark-random`: Simple benchmarks based on randomly generated files, as a lower boundary.
  * `benchmark-grenenet`: Benchmarks on real-world data from GrENE-net, subsetting one or two files to increasing numbers of positions to show scaling wrt genome length.
  * `benchmark-samples`: Benchmarks on real-world data from GrENE-net, increasing the number of files to show scaling wrt number of samples.

Furthermore, we have some auxiliary tests and comparisons:

  * `eval-grenenet`: Quick test to assess the overall gain of grenedalf for our GrENE-net project.
  * `bug-exam`: Examination of the two bugs in PoPoolation Tajima's D implementation.

See the respective subdirectories for details.
