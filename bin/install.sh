#!/bin/bash

# Set up the virtual environment.
# https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
python3 -m venv ./.venv
source ./.venv/bin/activate

# Check for a relative path.
which python

python3 -m pip install -r requirements.txt

echo "Environment setup complete."
