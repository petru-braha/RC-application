#!/bin/bash

# The execution is defaulted to start with a integrated GUI.
$GUI_MODE="gui"
$GUI_WEB_OPT="--web"

$mode=$GUI_MODE
$web_enabled=false

if [ "$#" -gt 2 ]; then
    echo "Error: Too many arguments provided."
    echo "Usage: $0 [--cli]"
    exit 1

elif [ "$#" -eq 2 ]; then
    if [ $1 == "--cli" ]; then
        $mode="cli"
    fi

    if [ $1 == $GUI_WEB_OPT ]; then
        $web_enabled=true
    fi
    
    echo "Error: Invalid argument '$1'. Expected: '--cli' or '--web'."
    exit 2
fi

# It is not enough to directly run the script.
# A positional argument is required for the application to load.
if [ $mode -eq $GUI_MODE ]; then
    echo "Starting application in GUI mode..."
    if [ $web_enabled == true ]; then
        flet run --web
    else
        flet run
    fi
else
    echo "Starting application in CLI mode..."
    python3 src/main.py --cli
fi
