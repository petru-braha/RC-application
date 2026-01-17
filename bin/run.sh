#!/bin/bash

# The execution is defaulted to start with a integrated GUI.
GUI_MODE="gui"
GUI_WEB_OPT="--web"

mode="$GUI_MODE"
web_enabled=false

if [ "$#" -gt 2 ]; then
    echo "Error: Too many arguments provided."
    echo "Usage: $0 [--cli] [--web]"
    exit 1
fi

for arg in "$@"; do
    case "$arg" in
        --cli)
            mode="cli"
            ;;
        --web)
            web_enabled=true
            ;;
        *)
            echo "Error: Invalid argument '$arg'."
            echo "Expected: --cli or --web"
            exit 2
            ;;
    esac
done

# It is not enough to directly run the script.
# A positional argument is required for the application to load.
if [ "$mode" = "$GUI_MODE" ]; then
    echo "Starting application in GUI mode..."
    if [ "$web_enabled" = true ]; then
        flet run --web
    else
        flet run
    fi
else
    echo "Starting application in CLI mode..."
    python3 src/main.py --cli
fi
