"""
Config module
-------------
A convenient and simple way of working with parameters when running models.

Using parameters in models allows the quick testing of different assumptions. Rather than
hard-coding values or setting a battery of variables at the beginning of a file, this
module provides an easy solution to loading the parameter values from external sources.
The set of parameter values can be provided in individual YAML files (one file equals one
model run) or in one consolidated CSV file (one row equals a model run). This way, one
code execution can run several models (one after another).
"""

from typing import Optional, List, Dict, Union
from os import PathLike

import yaml
import os
import pandas as pd


def read_yaml(config_file: Union[PathLike, str, bytes],
              as_list: Optional[bool] = False) -> Union[Dict, List]:
    """
    Loads a YAML file and returns the model parameters as key-value pairs.

    :param as_list: By default, the function returns a single set of parameter values.
        Setting as_list True returns a list of length one instead. This equals to loading
        a CSV file with only one row and allows to test the code for production. Setting
        as_list True requires a YAML file with only one hierarchy level.
    :param config_file: The YAML config file that contains all relevant parameter values
        for the current model run.

    :return: A dictionary with one set of parameters, i.e., values for one model run.
    """
    if config_file is not None and os.path.exists(config_file) is False:
        raise ValueError(f'(pyHEC error) config file not found.\n'
                         f'Specified file location: {config_file}')

    with open(config_file, 'r') as f:
        items = yaml.load(f, Loader=yaml.FullLoader)

    return [items] if as_list else items


def read_csv(config_file: Union[PathLike, str, bytes], **kwargs) -> pd.DataFrame:
    """
    Loads a CSV file that contains the parameter keys in the header and the parameter
    values in the following rows (hence, one row equals one model run).

    :param config_file: The CSV file that contains all relevant parameter values for the
        different model runs.
    :param kwargs: See Pandas documentation for a list of available parameters.

    :return: A pandas data frame with the structure of the CSV file
    """
    return pd.read_csv(config_file, header=0, **kwargs)


def yaml2csv(yaml_file: Union[PathLike, str, bytes], output_file: Union[PathLike, str, bytes], **kwargs) -> None:
    """
    Converts a YAML file to a CSV file that can be used as a template.

    :param yaml_file: The location of the YAML file.
    :param output_file: The location where the CSV file should be saved.

    :return: Returns True when the CSV file was saved.
    """
    pd.Series(read_yaml(yaml_file)).to_frame().T.to_csv(output_file, index=False, **kwargs)
