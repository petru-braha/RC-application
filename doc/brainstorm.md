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

0. ui (gui for connecting, terminal, html, files)
0. io (reading/writing)
0. network (session managemnt)
0. protocol (resp parser, encoder, decoder)
0. transport (reading/write to socket)

Workflow: ui -> io.fronend.input.connecting -> network -> io.ui.input -> protocol -> transport -> protocol -> io.fronend.output -> ui

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
