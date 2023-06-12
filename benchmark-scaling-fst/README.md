# Benchmark of the strong scaling properties of grenedalf on a large dataset

In `benchmark-scaling`, we tested strong and weak scaling on a relatively small dataset, and found that we did not gain any speedups, likely due to thread synchronization overhead and Amdahl's law.
Hence, we here test how grenedalf scales when using multiple threads for the execution, on a large dataset. Indeed, on larger datasets, we do observe significant speedups. This was tested on a pairwise FST computation with 2415 samples from our GrENE-net project.
