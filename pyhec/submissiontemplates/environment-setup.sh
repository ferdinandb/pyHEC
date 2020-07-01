# Change to the project dir and run all commands from there
cd "$1" || exit

# Either activate + update OR create + activate the environment
ENV=$(head -n 1 environment.yml | cut -f2 -d ' ')

source activate "$ENV"
if [ $? -eq 0 ]; then
  # Conda environment exists: update packages
  echo "Updating environment"
  conda env update -f environment.yml --prune --quiet
else
  # Create a new environment and activate it
  echo "Creating new environment"
  conda env create -f environment.yml --quiet
  source activate "$ENV"
fi

# Install the remaining packages (work-around to make setup platform compatible)
cat requirements.txt | cut -f1 -d"#" | sed '/^\s*$/d' | xargs -n 1 pip install

echo "Environment updated."
