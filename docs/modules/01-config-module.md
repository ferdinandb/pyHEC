# Config module

Using parameters in models allows for the quick testing of different assumptions. Rather than hard-coding values or setting a battery of variables at the beginning of a file, this module provides an easy solution to loading the parameter values from different sources.

The set of parameter values can be provided in individual YAML files \(one file equals one model run\) or in one consolidated CSV file \(one row equals a model run\). This way, one code execution can run several models one after another.

{% hint style="info" %}
**Tip:** Use`read_yaml()` when first developing your model and `read_csv()` when running the code on the cluster.
{% endhint %}

## Import module

Run the command to import the config module.

```python
from pyhec import config as c
```

## `read_yaml()`

Loads a YAML file and returns the model parameters as key-value pairs.

**`c.read_yaml`**`(config_file, as_list)`

* `config_file` **str, PathLike**
  * The YAML config file that contains all relevant parameter values for the current model run. 
* `as_list` **bool, default: True**
  * By default, the function returns a single set of parameter values. Setting as\_list True returns a list of length one instead. This equals to loading a CSV file with only one row and allows to test the code for production. Setting as\_list True requires a YAML file with only one hierarchy level. 
* **`Return`** **Dict, List**
  * A dictionary with one set of parameters, i.e., values for one model run. 

The YAML file is more helpful when developing a first prototype of the model as it is a more structured way of storing and describing the parameter. The following example shows the use of a YAML file to run one model.

```python
config = c.read_yaml('./data/single-model-run.yaml')
print('Output destination: ' + config['output_dir'])
```

## `read_csv()`

Loads a CSV file that contains the parameter keys in the header and the parameter values in the following rows \(hence, one row equals one model run\).

**`c.read_csv`**`(config_file, **kwargs)`

* `config_file` **str, PathLike**
  * The CSV file that contains all relevant parameter values for the different model runs. 
* `**kwargs`
  * See the [Pandas docs](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html) for a list of available parameters. 
* **`Return`** **pandas.DataFrame**
  * A pandas DataFrame with the structure of the CSV file. 

When working with the HEC, we want to run multiple models in one job submission. This can be achieved by either saving multiple YAML files and looping over them \(see [examples](https://github.com/ferdinandb/pyHEC/tree/master/examples/config)\) or by using a single CSV file. The CSV file can be saved either locally or remotely such as on network or shared drives \(e.g., Google Drive, OneDrive, etc.\). This way, you can run multiple models by simply updating the remote CSV file without changing anything on the HEC.

```python
configs = c.read_csv('https://github.com/ferdinandb/pyHEC/raw/master/examples/config/data/multiple-model-runs.csv')

for config in configs:
    print('Output destination: ' + config['output_dir'])
```

## `yaml2csv()`

Converts a YAML file to a CSV file that can be used as a template.

{% hint style="warning" %}
Converting a YAML file to a CSV file requires a YAML file with only one hierarchy level.
{% endhint %}

**`c.yaml2csv`**`(yaml_file, output_file, **kwargs)`

* `yaml_file` **str, PathLike**
  * The location of the YAML file. 
* `output_file` **str, PathLike**
  * The location where the CSV file should be saved. 
* `**kwargs`
  * See the [Pandas docs](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html) for a list of available parameters. 
* **`Return`** **None**

## Examples

More examples can be found on [GitHub](https://github.com/ferdinandb/pyHEC/tree/master/examples/config) or in the examples section.

