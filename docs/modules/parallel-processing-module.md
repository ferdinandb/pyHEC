# Parallel processing module

By default, Python uses one CPU core when executing code. This behavior is caused by the global interpreter lock \(GIL\) that limits the Python interpreter to using only one core. Such behavior is counterproductive for high-performance computing \(HPC\) applications and limits the scope of research projects that are computational demanding. This module offers an easy \(and slightly naive\) way to bypass the GIL to execute the code in parallel on multiple CPU cores.

The parallel-processing module works "out of the box" on both local machines and HPC clusters. The module can be integrated quickly and does not require significant code changes or a deep understanding of parallel processing. The approach represents a balance between easy usability and high processing efficiency. The solution works for most research tasks. It lacks in performance compared to optimized HPC applications. See the examples for different use cases of the parallel processing module.

There are two options when using the parallel processing module. Both options bypass the GIL and can speed up the code execution significantly. While the first option is relatively easy to implement, it only works on a single computing node. It is ideal for local development and works out of the box on both local machines and computing clusters. No additional installations are required. The increase in processing speed is limited by the maximum number of cores of the given computing node \(probably something around 8 to 64 cores\). For most applications, such an increase in speed should already be sufficient.

The second option requires an HPC cluster and works with multiple nodes. This option is still in development and will follow soon.

{% hint style="info" %}
**Tip:** The first option is likely to be the default case for most applications. Refer to the examples for more information.
{% endhint %}

## Import module

Run the command to import the parallel processing module.

```python
from pyhec import parallel_processing as pp
```

## `parallelize()`

Uses Python's multiprocessing package to parallelize tasks on local machines and HPC clusters. The approach of this function is very naive while simple to implement from a user's perspective. The performance increase is limited by the number of CPU cores of the computing node.

{% hint style="warning" %}
Only run `pp.parallelize` within the `if name == 'main'` statement. Not doing so can result in weird behavior.
{% endhint %}

**`pp.parallelize`**`(func, iterable, n_core, return_as, **kwargs)`

* `func` **Callable**
  * The function that will be executed in parallel to process iterable. 
* `iterable` **List, numpy.array, pands.DataFrame**
  * A list, NumPy array, or pandas DataFrame that should be processed in parallel. 
* `n_core` **int, str, None, default: None**
  * The number of worker processes, i.e., the number of desired vCPU cores, to use when running the function func. Setting n\_cores to None returns the maximum number of vCPU cores of the machine as defined be os.cpu\_count\(\). 
* `return_as` **str, default: 'list'**
  * The multiprocessing module returns a list by default. If, however, the return value is supposed to be a pandas DataFrame, set the value to 'dataframe'. 
* `**kwargs`
  * Optional arguments for func. 
* **`Return` List, pandas.DataFrame**
  * Returns either a list or a pandas DataFrame with the results of func. 

The function takes a list \(`iterable`\), splits it into multiple chunks and submits the chunks to `func`. As such, you need a for-loop to process the items per chunk. Please see the example below.

The following example can be found [here](https://github.com/ferdinandb/pyHEC/blob/master/examples/parallel-processing/batch-load-csv-files.py).

{% code title="main.py" %}
```python

```
{% endcode %}

## `batch_read_csv()`

Reads a large number of CSV files using all CPU cores to speed up the process.

{% hint style="warning" %}
The CSV files must have the same structure, i.e. they must have the same column names.
{% endhint %}

**`pp.batch_read_csv`**`(glob_path, **kwargs)`

* `glob_path` **str**
  * A string containing a glob.glob\(\)-like file path. See the [Python docs](https://docs.python.org/3/library/glob.html#glob.glob) for more information on the use of wildcards. 
* `**kwargs` 
  * Optional keyword arguments for pandas DataFrame.read\_csv\(\) function. See the [pandas docs](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html) for more information. 
* **`Return` pandas.DataFrame**
  * A pandas DataFrame with the concatenated contents of the CSV files. 

The following example can be found [here](https://github.com/ferdinandb/pyHEC/blob/master/examples/parallel-processing/batch-load-csv-files.py). It shows how to load multiple CSV files with just one line of code.

{% code title="main.py" %}
```python
"""
Batch load CSV files
--------------------

A simple example of how to batch load a bunch of CSV files with just 
one line of code. The CSV files must have the same structure, i.e. 
they must have the same column names.

You can pass all available keyword arguments of pandas' read_csv() 
function.
"""
from pyhec import parallel_processing as pp


if __name__ == '__main__':

    df = pp.batch_read_csv('./data/*.csv', error_bad_lines=False)

    print(f'Loaded {len(df)} CSV files. See head() below:')
    print(df.head())
```
{% endcode %}

## Examples

More examples can be found on [GitHub](https://github.com/ferdinandb/pyHEC/tree/master/examples/parallel-processing) or in the examples section.

