# pyHEC
**pyHEC** is a Python package that facilitates the use of the university's high-end computing (HEC) cluster. It provides tools to easily parallelize code execution on both a local computer and a multi-node computing cluster.

pyHEC is optimized for Lancaster University's HEC cluster. Please refer to the [ISS help page](https://answers.lancaster.ac.uk/display/ISS/High+End+Computing+(HEC)+help) to find out more about the cluster.

## How to use
While submitting a job is straight-forward, it is more challenging to set up a locally developed project on the cluster without code changes. Mainly the duplication of local Python environments, a lack of automation when deploying the code and the technical aspects of parallelization might be perceived as the greatest bottlenecks. 

pyHEC aims to automatize these tasks in the background. The package consists of three main components: the config library, the parallel processing library and the HEC job submission generator. Please see below for detailed explanations on the three components.

### Install and import pyHEC

````python
import pyhec as hec
````

### Config

````python
config = hec.load_config('test')
````