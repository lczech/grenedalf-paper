# grenedalf-paper
Code for tests and benchmarks of the paper on our tool [grenedalf](https://github.com/lczech/grenedalf)

We here provide tests scripts to benchmark [grenedalf](https://github.com/lczech/grenedalf) against 
[PoPoolation 1](https://sourceforge.net/projects/popoolation/) and 
[PoPoolation 2](https://sourceforge.net/projects/popoolation/).
For these tests to run, you need to make sure that all tools in `software` are
working by [downloading the git submodules](https://www.atlassian.com/git/tutorials/git-submodule), 
and in particular compile grenedalf first.

In particular:

  * `benchmark-random`: Benchmarks based on randomly generated files.
  * `benchmark-real`: Benchmarks based on real world data.
  * `bug-exam`: Examination of the two bugs in PoPoolation Tajima's D implementation.

See the subdirectories for details.
