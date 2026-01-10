#!/bin/bash

# Ensure that the virtual environment is activated.
source ./.venv/bin/activate

python3 -m coverage run -m unittest discover tst
python3 -m coverage report -m
