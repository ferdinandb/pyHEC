# Config module

Using parameters in models allows for the quick testing of different assumptions. Rather than hard-coding values or setting a battery of variables at the beginning of a file, this module provides an easy solution to loading the parameter values from different sources. 

## Import module
Run the command to import the config module.

```python
from pyhec import config as c
```

## Read YAML file

The set of parameter values can be provided in individual YAML files (one file equals one model run) or in one consolidated CSV file (one row equals a model run). This way, one code execution can run several models one after another.

The YAML file is more helpful when developing a first prototype of the model as it is a more structured way of storing and describing the parameter. The following example shows the use of a YAML file to run one model.

```python
config = c.read_yaml('./data/single-model-run.yaml')
print(f'Output destination as defined in the YAML file: {config["output_dir"]}')
```

## Run multiple models 

When working with the HEC, we want to run multiple models in one job submission. This can be achieved by either saving multiple YAML files and looping over them (see [examples](https://github.com/ferdinandb/pyHEC/tree/master/examples/config)) or by using a single CSV file. The CSV file can be saved either locally or remotely such as on network or shared drives (e.g., Google Drive, OneDrive, etc.). This way, you can run multiple models by simply updating the remote CSV file without changing anything on the HEC.

```python
configs = c.read_csv('https://github.com/ferdinandb/pyHEC/raw/master/examples/config/data/multiple-model-runs.csv')

for config in configs:
    print(f'Output destination: {config["output_dir"]}')
```

## Examples

More examples can be found [here](https://github.com/ferdinandb/pyHEC/tree/master/examples/config).
