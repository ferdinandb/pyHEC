"""
Batch load CSV files
--------------------

A simple example of how to batch load a bunch of CSV files with just one line of code. The
CSV files must have the same structure, i.e. they must have the same column names.

You can pass all available keyword arguments of pandas' read_csv() function.
"""

from pyhec import parallel_processing as pp


if __name__ == '__main__':
    df = pp.batch_read_csv('./data/*.csv', error_bad_lines=False)
    print(f'Loaded {len(df)} CSV files. See head() below:')
    print(df.head())
