from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pyhec',
    version='0.0.1',
    author='Ferdinand Bratek',
    author_email='566392+ferdinandb@users.noreply.github.com',
    description='Python package that facilitates the use of the university\'s high-end computing cluster (HEC)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ferdinandb/pyHEC',
    python_requires='>=3.6',
    install_requires=[
        'yaml',
        'pandas>=0.19.2',
        'numpy'
    ],
    packages=find_packages(include=['pyhec', 'pyhec.*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
    ],
)
