# Overview

The workflow of the application:

- open_gui()
- connect_redis()
- send_hello()

- read_gui()
- encode_input()
- send_tcp()
- recv_tcp()
- decode_output()
- write_gui()

- close_redis()
- close_gui()

## Assumptions/Decisions

the overall purpose is to make indexing work and achieve constant time retrieval of a variable

## Modules

0. frontend (gui for connecting, terminal, html, files)
0. io (reading/writing)
0. network (session managemnt)
0. protocol (resp parser, encoder, decoder)
0. transport (reading/write to socket)

Workflow: frontend -> io.fronend.input.connecting -> network -> io.frontend.input -> protocol -> transport -> protocol -> io.fronend.output -> frontend

## Future

- i/o operations should be abstracted by a class (gui/cli/file)
- future allow multiple connections
- deploy it as a web app (html gui)
- commands:
  - run
  - tst

## Issues:

0. RESP, CONN
0. GUI
0. CRUD Strings, Lists, Sets
0. CRUD Hashes, Sorted Sets

an issue is complete when the following items are achieved:

0. code
0. logs
0. tests
0. errors
0. documentation

# cool?

```sh

# Activate the project's virtual environment from any path available.

# We need to find the path of the .venv directory.
# This can be done by analysing the terminal path.
# The terminal path always end with either bin/build.sh or build.sh.

# First case: the script was lauched from outside of bin.
# We need to cut the bin/build.sh suffix.
# Second case: the script was launched from the bin.
# We assign "../"

terminal_path=$0
script_suffix="bin/build.sh"
# 
# # The script path must be a suffix of the terminal path.
# # Its length must be smaller or equal than the terminal path.
# ter_path_len=${#terminal_path}
# scr_path_len=${#script_suffix}
# 
# project_path="./../"
# 
# if [ $scr_path_len -gt $ter_path_len ]; then
#     offset=$ter_path_len - $scr_path_len
#     project_path=${terminal_path:offset:$ter_path_len}
# fi
# 
# venv_directory=".venv/bin/python3"
# expected_interpreter="${project_path}${venv_directory}"
# 
# actual_interpreter=${which python3}
# 
# if [ expected_interpreter -ne actual_interpreter ]; then
#     source "${project_path}/.venv/bin/activate"
# fi


```