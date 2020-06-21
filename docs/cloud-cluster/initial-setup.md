# Initial setup

Before being able to use pyHEC on the cluster, you have to go through some initial setup. There is no need to repeat the setup for new projects. 

## Lancaster University HEC

Login to the cluster as described on the [ISS help page](https://answers.lancaster.ac.uk/display/ISS/Logging+in+to+the+HEC). Execute the following commands:

```bash
module add anaconda3/2019.07
conda config
conda config --append envs_dirs "$global_storage/.conda/envs"
conda config --append pkgs_dirs "$global_storage/.conda/pkgs"
```

The HOME directory is very limited in size \(3GB\) and thus not suitable for a lot of scenarios. Instead, we save environments and packages in the storage directory \(30GB\) to overcome this bottleneck. 

{% hint style="info" %}
Please refer to the [ISS help pages](https://answers.lancaster.ac.uk/display/ISS/High+End+Computing+%28HEC%29+help) for more details.
{% endhint %}

## NYU Prince

Login to the cluster as described on the [HPC support page](https://sites.google.com/a/nyu.edu/nyu-hpc/documentation/hpc-access). Execute the following commands:

```bash
module add anaconda3/2019.10
conda config
conda config --append envs_dirs "$SCRATCH/.conda/envs"
conda config --append pkgs_dirs "$SCRATCH/.conda/pkgs"
```

The scratch directory is used to save environments and packages. Unused files are flushed after 60 days. In practice, that should be enough time for most scenarios and keeps the HPC storage clean. Either way, the required Python environment gets updated/checked before each run; missing files or incomplete environments are not an issue. 

{% hint style="info" %}
Please refer to the [HPC support pages](https://sites.google.com/a/nyu.edu/nyu-hpc/) for more details.
{% endhint %}

