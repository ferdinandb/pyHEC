# pyHEC

**pyHEC** is a Python package that facilitates the use of the university's high-end computing (HEC) cluster. It provides higher-level tools to easily parallelize code execution on both a local computer and a multi-node computing cluster. The tool aims to compile the functionality of popular Python packages to accomplish common tasks without requiring a deep understanding of all the technical aspects of high-performance computing (HPC).

pyHEC is optimized for Lancaster University's HEC cluster. Please refer to the [ISS help page](https://answers.lancaster.ac.uk/display/ISS/High+End+Computing+(HEC)+help) to find out more about the cluster.

---

## How to use
While submitting a job is straight-forward, it is more challenging to set up a locally developed project on the cluster without code changes. Mainly the duplication of local Python environments, a lack of automation when deploying the code and the technical aspects of parallelization might be perceived as the greatest bottlenecks. 

pyHEC aims to automatize these tasks in the background. The package consists of three main components: the config library, the parallel processing library and the HEC job submission generator. Please see below for detailed explanations on the three components.

### Installing and loading pyHEC

The Python package is hosted on GitHub and can be installed with the following pip command.

````shell script
pip install git+https://github.com/ferdinandb/pyHEC.git@master#egg=pyhec
````

Not all modules of pyHEC might be of same interest in a project. As such, it is recommended to only load the corresponding module as shown below. Please also refer to the [examples](https://github.com/ferdinandb/pyHEC/#) to see further applications and use cases of the different modules.

### Config module

Using parameters in models allows the quick testing of different assumptions. Rather than hard-coding values or setting a battery of variables at the beginning of a file, this module provides an easy solution to loading the parameter values from different sources. 

Run the command to import the config module.

````python
from pyhec import config as c
````

The set of parameter values can be provided in individual YAML files (one file equals one model run) or in one consolidated CSV file (one row equals a model run). This way, one code execution can run several models one after another.

The YAML file is more helpful when developing a first prototype of the model as it is a more structured way of storing and describing the parameter. The following example shows the use of a YAML file to run one model.

````python
config = c.read_yaml('./data/single-model-run.yaml')
print(f'Output destination as defined in the YAML file: {config["output_dir"]}')
````

When working with the HEC, we want to run multiple models in one job submission. This can be achieved by either saving multiple YAML files and looping over them (see [examples](https://github.com/ferdinandb/pyHEC/tree/master/examples/config)) or by using a single CSV file. The CSV file can be saved either locally or remotely such as on network or shared drives (e.g., Google Drive, OneDrive, etc.). This way, you can run multiple models by simply updating the remote CSV file without changing anything on the HEC.

````python
configs = c.read_csv('https://github.com/ferdinandb/pyHEC/raw/master/examples/config/data/multiple-model-runs.csv')

for config in configs:
    print(f'Output destination: {config["output_dir"]}')
````

More examples can be found [here](https://github.com/ferdinandb/pyHEC/tree/master/examples/config).


### Parallel processing module

By default, Python uses one CPU core when executing code. This behaviour is caused by the global interpreter lock (GIL) that limits the Python interpreter to using only one core. Such behavior is counterproductive for HPC applications and limits the scope of research projects that are computational demanding. This module offers an easy (and slightly naive) way to bypass the GIL to executed the code in parallel on multiple CPU cores.

The parallel-processing module works "out of the box" on both local machines and HPC clusters. The module can be integrated quickly and does not require significant code changes or a deep understanding of parallel processing. The approach represents a balance between easy usability and high processing efficiency. The solution works for most research tasks. It lacks in performance compared to optimized HPC applications. See the [examples](https://github.com/ferdinandb/pyHEC/tree/master/examples/parallel-processing) for different use cases of the parallel processing module.
 
Run the command to import the parallel processing module.

````python
from pyhec import parallel_processing as pp
````

There are two options when using the parallel processing module. Both options bypass the GIL and can speed up the code execution significantly. While the first option is relatively easy to implement, it only works on a single computing node. It is ideal for local development and works out of the box on both local machines and computing clusters. No additional installations are required. The increase in processing speed is limited by the maximum number of cores of the given computing node (probably something around 8 to 64 cores). For most applications, such increase in speed should already be sufficient. The second option requires a HPC cluster and works with multiple nodes (this option is still in development).

The first option is likely to be the default case for most applications. Refer to the [examples](https://github.com/ferdinandb/pyHEC/tree/master/examples/parallel-processing) for more information.