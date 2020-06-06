"""
Helper functions for the parallel processing module
"""

import pandas as pd
import sys
import csv

def read_csv(files, **kwargs):
    """
    Reads a list of CSV files. This function is used for the overarching wrapper to read
    CSV files in parallel.

    :param files: A list of files that should be loaded.
    :param kwargs: Keyword arguments for pandas' DataFrame.read_csv()

    :return: A concatenated pandas DataFrame
    """
    max_int = sys.maxsize
    while True:
        # Reading large CSV files might raise an OverflowError. Decrease the maxInt
        # value by factor 10 as long as the OverflowError occurs
        try:
            csv.field_size_limit(max_int)
            break
        except OverflowError:
            max_int = int(max_int/10)

    return pd.concat((pd.read_csv(f, engine='python', **kwargs) for f in files), ignore_index=True)
