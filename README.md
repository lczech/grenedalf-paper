# grenedalf-paper
Code for tests and benchmarks of the paper on our tool [grenedalf](https://github.com/lczech/grenedalf)

We here provide tests scripts to benchmark [grenedalf](https://github.com/lczech/grenedalf) against 
[PoPoolation 1](https://sourceforge.net/projects/popoolation/) and 
[PoPoolation 2](https://sourceforge.net/projects/popoolation/).
For these tests to run, you need to make sure that all tools in `software` are
working by [downloading the git submodules](https://www.atlassian.com/git/tutorials/git-submodule), 
and in particular compile grenedalf first.
Then, generate the random test data as described in `data`.
Lastly, call the `measure.sh` script to run the benchmarks.
