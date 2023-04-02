# Software

These are the tools that we test in this repository.

grenedalf, PoPoolation, PoPoolation2, and npstat are included here as git submodules.
To use them, [download the git submodules](https://www.atlassian.com/git/tutorials/git-submodule).

Then, grenedalf needs to be compiled; see [here](https://github.com/lczech/grenedalf) for instructions.
Furthermore, npstat needs to be compiled, and the GSL needs to be present. See the npstat directory for instructions.

Lastly, poolfstat is available via [conda](https://docs.conda.io/en/latest/)/[mamba](https://github.com/mamba-org/mamba).
To install the package, use

    conda env create -f poolfstat/env.yaml

After that, all tools should be ready to go.
