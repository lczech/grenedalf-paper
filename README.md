# grenedalf-paper

Code for tests and benchmarks of the paper on our tool [grenedalf](https://github.com/lczech/grenedalf)

We here provide tests scripts to benchmark [grenedalf](https://github.com/lczech/grenedalf) against existing tools:

  * [grenedalf](https://github.com/lczech/grenedalf)
  * [PoPoolation 1](https://sourceforge.net/projects/popoolation/)
  * [PoPoolation 2](https://sourceforge.net/projects/popoolation/)
  * [poolfstat](https://cran.r-project.org/web/packages/poolfstat/index.html)
  
See the `software` directory here for their setup.

With all tools available, we run the following tests here:

  * `benchmark-grenenet`:
  * `benchmark-random`: Benchmarks based on randomly generated files.
  
Furthermore, we have some auxiliary tests and comparisons:
  
  * `benchmark-real`: Quick test to assess overall gain of grenedalf for our GrENE-net project.
  * `bug-exam`: Examination of the two bugs in PoPoolation Tajima's D implementation.

See the respective subdirectories for details.
