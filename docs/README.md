# pyHEC Documentation

While submitting a job is straight-forward, it is more challenging to set up a locally developed project on the cluster without code changes. Especially the duplication of local Python environments, a lack of automation when deploying the code and the technical aspects of parallelization might be perceived as the greatest bottlenecks.

pyHEC aims to automatize these tasks in the background. The package consists of three main components: the config module, the parallel processing module and the HEC job submission generator.

This documentation contains explanations for the available modules and functions, and provides several examples and use cases.

{% hint style="info" %}
**Tip:** The different modules can be loaded independently of each other. Please see code below.
{% endhint %}

## Installing and loading pyHEC

The Python package is hosted on GitHub and can be installed with the following pip command.

```bash
pip install git+https://github.com/ferdinandb/pyHEC.git@master#egg=pyhec
```

The Python package can be imported as follows

```python
import pyhec as hec
```

Not all modules of pyHEC might be of same interest in a project. As such, it is recommended to only load the corresponding module as shown below.

```python
from pyhec import config as c
from pyhec import parallel_processing as pp
```

## Additional notes

Please also refer to the [examples](https://github.com/ferdinandb/pyHEC/tree/master/examples) to see further applications and use cases of the different modules.

Find the project source code on [GitHub](https://github.com/ferdinandb/pyHEC).

