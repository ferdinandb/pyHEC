"""
Parallel processing module
--------------------------
A convenient way of using the full CPU power when processing large amounts of data.
Read more: https://pyhec.gitbook.io/pyhec/modules/parallel-processing-module
"""

from typing import Optional, List, Union, Callable

from multiprocessing import Pool, cpu_count
from functools import partial
from glob import glob
import numpy as np
import pandas as pd
from pyhec.core.util.parallel_processing_util import read_csv


def parallelize(func: Callable,
                iterable: Union[List, np.array, pd.DataFrame],
                n_cores: Optional[Union[int, None, str]] = None,
                return_as: Optional[str] = 'list',
                **kwargs) -> Union[List, pd.DataFrame, bool]:
    """
    Uses Python's multiprocessing package to parallelize tasks on both local machines and
    high-performance computing clusters. The approach of this function is very naive while
    simple to implement from a user's perspective. The performance increase is limited by
    the number of CPU cores on the executing machine. Please see the docs when using more
    than one computing node (a bit more complex).

    :param func: The function that will be executed in parallel to process iterable.
    :param iterable: A list, a NumPy array or a pandas DataFrame that should be processed
        in parallel.
    :param n_cores: The number of worker processes, i.e., the number of desired vCPU cores,
        to use when running the function func. Setting n_cores to None returns the maximum
        number of vCPU cores of the machine as defined be os.cpu_count().
    :param return_as: The multiprocessing module returns a list by default. If, however,
        the return value is supposed to be a pandas DataFrame, set the value to 'dataframe'.
    :param kwargs: Optional arguments for func.

    :return: Returns either a list or a pandas DataFrame with the returned values of func.
    """
    if n_cores == 'max' or n_cores is None:
        n_cores = cpu_count()  # Run with maximum number of CPU cores if desired

    # Create 2x more chunks than CPU cores on the system (improves handling of data)
    factor = 2 if len(iterable) > (n_cores * 4) else 1
    iterable = np.array_split(iterable, n_cores * factor)

    # Use the map() function to batch-process a large number of items. This approach is
    # preferred to using starmap() or apply() as it is more efficient when working with
    # huge amounts of data. We convert func to a partial object with the keyword arguments
    # **kwargs. The iterable will be passed as the first positional argument. In practice,
    # this should accommodate all potential research applications/needs.
    if len(kwargs):
        func = partial(func, **kwargs)

    p = Pool(n_cores)
    output = p.map(func, iterable)
    p.close()
    p.join()

    if return_as == 'dataframe':
        # Assemble the returned DataFrame
        return pd.concat(output)

    # Flatten list of lists
    return [item for sublist in output for item in sublist or []]


def batch_read_csv(glob_path: str, **kwargs) -> pd.DataFrame:
    """
    Reads a large number of CSV files using all CPU cores to speed up the process. This
    requires all CSV files to have the identical structure (i.e., the same column names).

    :param glob_path: A string containing a glob.glob()-like filepath. See the Python
        docs for more information on the use of wildcards.
    :param kwargs: Optional keyword arguments for pandas DataFrame.read_csv() function.

    :return: A pandas DataFrame with the concatenated contents of the CSV files.
    """
    files = glob(glob_path)
    if len(files) < 1:
        raise ValueError(f'(pyHEC error) No files found.')

    return parallelize(read_csv, files, **kwargs, n_cores=2, return_as='dataframe')
