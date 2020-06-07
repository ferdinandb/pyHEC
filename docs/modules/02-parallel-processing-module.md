# Parallel processing module

By default, Python uses one CPU core when executing code. This behaviour is caused by the global interpreter lock \(GIL\) that limits the Python interpreter to using only one core. Such behavior is counterproductive for HPC applications and limits the scope of research projects that are computational demanding. This module offers an easy \(and slightly naive\) way to bypass the GIL to executed the code in parallel on multiple CPU cores.

The parallel-processing module works "out of the box" on both local machines and HPC clusters. The module can be integrated quickly and does not require significant code changes or a deep understanding of parallel processing. The approach represents a balance between easy usability and high processing efficiency. The solution works for most research tasks. It lacks in performance compared to optimized HPC applications. See the [examples](https://github.com/ferdinandb/pyHEC/tree/master/examples/parallel-processing) for different use cases of the parallel processing module.

## Import module

Run the command to import the parallel processing module.

```python
from pyhec import parallel_processing as pp
```

There are two options when using the parallel processing module. Both options bypass the GIL and can speed up the code execution significantly. While the first option is relatively easy to implement, it only works on a single computing node. It is ideal for local development and works out of the box on both local machines and computing clusters. No additional installations are required. The increase in processing speed is limited by the maximum number of cores of the given computing node \(probably something around 8 to 64 cores\). For most applications, such increase in speed should already be sufficient. The second option requires a HPC cluster and works with multiple nodes \(this option is still in development\).

The first option is likely to be the default case for most applications. Refer to the [examples](https://github.com/ferdinandb/pyHEC/tree/master/examples/parallel-processing) for more information.

