# Overview

This file contains personal notes.

App workflow:

- open_gui()
- connect_redis()
- send_hello()
- input_workflow()
- close_redis()
- close_gui()

User input workflow:

- frontend
- network
- input
- protocol
- transmission
- protocol
- output

Ideas for future development can be seen in the `Issues` section in of this GitHub repository.

## Modules

0. core (common utilities used across the entire codebase)
1. frontend (GUI)
2. network (session managemnt)
3. protocol (resp parser, encoder, decoder)
4. transmission (reading/writing)

A module is complete when the following items are achieved:

0. implementation
1. documentation
2. tests
3. logs
