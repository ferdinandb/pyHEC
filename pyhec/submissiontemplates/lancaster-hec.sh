#$ -S /bin/bash
# Template file for Lancaster University's HEC

# Run the job on x nodes with 16 cores each
#$ -q parallel
#$ -l node_type=10Geth*

source /etc/profile

# Helper function by https://github.com/chdoig/conda-auto-env
function conda_auto_env() {
  if [ -e "environment.yml" ]; then
    # echo "environment.yml file found"
    ENV=$(head -n 1 environment.yml | cut -f2 -d ' ')
    # Check if you are already in the environment
    if [[ $PATH != *$ENV* ]]; then
      # Check if the environment exists
      source activate $ENV
      if [ $? -eq 0 ]; then
        :
      else
        # Create the environment and activate
        echo "Conda env '$ENV' doesn't exist."
        conda env create -q
        source activate $ENV
      fi
    fi
  fi
}


# Change to storage dir and run all commands from there
cd $global_storage || exit

# Either set up or update environment
conda env create -f environment.yml --yes
conda env update --f environment.yml --prune --yes

# Run
python "$1"
