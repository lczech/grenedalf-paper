# Benchmark of the strong and weak scaling properties of grenedalf

Here, we test how grenedalf scales when using multiple threads for the execution.
Strong scaling uses a fixed problem size, and tests how the runtime of the program changes when using more threads for the computation. Here, we expect the program to run faster when more cores are used.
Weak scaling on the other hand scales the number of threads _and_ the number of threads at the same time. Here, we hence expect the execution time to remain constant.

In both cases, on the relatively small dataset used here, we currently find that grenedalf does not optimally scale when using more threads. This is likely due to the statistics computation being a bottleneck, as it is hard to parallelize that part. There is still benefit from using multiple threads, as the file reading can be done asynchronously that way.

Furthermore, we ran scaling tests using the big all-to-all pairwise fst matrix computation, see `benchmark-scaling-fst` for details on that. On that large test, we actually observe significant speedups when using multiple threads
