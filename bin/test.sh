#!/bin/bash

# Ensure that the virtual environment is activated.
source ./.venv/bin/activate

coverage run -m unittest discover -s ./tst -t ./
coverage report
