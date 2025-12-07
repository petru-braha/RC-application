#!/bin/bash

# todo install python3 if it does not exist on this machine
# todo install venv if it does not exist on this machine
# todo install pip if it does not exist on this machine

# Set up the virtual environment.
# https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
python3 -m venv ./.venv
source ./.venv/bin/activate

# Check for a relative path.
which python

# Install the required dependencies.
python3 -m pip install frozendict
python3 -m pip install coverage

echo "Environment setup complete."
