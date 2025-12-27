#!/bin/bash

# todo decide if GUI or CLI
if [ "$#" -ne 1 ]; then
    echo "Invalid number of parameters."
    exit 1
fi



stage="${stage:-dev}"
tls="${tls:-false}"
conn_count_limit="${conn_count_limit:-1024}"

python3 src/main.py CLI --stage=${stage} --tls=${tls} --conn_count_limit=${conn_count_limit}