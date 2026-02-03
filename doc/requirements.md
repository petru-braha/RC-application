The original link https://gdt050579.github.io/python-course-fii/projects_a/14.html.

### Phase 1: RESP Protocol Implementation

Implement the Redis Serialization Protocol (RESP) for communication with a Redis server.

Parse and serialize RESP message types (Simple Strings, Errors, Integers, Bulk Strings, Arrays)
Validate message format and error handling
Functional Output: RESP messages can be sent and received correctly without using external libraries.

### Phase 2: Connection Management and Command Execution

Implement connection handling to a local Redis server and basic command sending/receiving.

Establish TCP socket connection
Send commands following RESP format
Receive and parse responses
Functional Output: Client can execute basic Redis commands and receive correct responses.

### Phase 3: CRUD for Strings and Lists

Implement GUI support for basic operations on Strings and Lists.

Create, read, update, delete elements
Display contents in the GUI
Handle edge cases (non-existent keys, empty lists)
Functional Output: Users can perform all CRUD operations on Strings and Lists via GUI.

### Phase 4: CRUD for Sets and Hashes

Extend GUI to support Sets and Hashes operations.

Add, remove, retrieve members/fields
Display current state of Sets and Hashes
Validate input types and errors
Functional Output: Users can manage Sets and Hashes entirely through the GUI with correct RESP handling.

### Phase 5: CRUD for Sorted Sets and Additional Features

Implement operations for Sorted Sets and enhance GUI usability.

Add elements with scores, retrieve range, remove elements
Update GUI layout and sorting
Error handling for score conflicts or invalid ranges
Functional Output: Full CRUD operations for Sorted Sets with live GUI updates.

Phase 6: Testing, Logging, and GUI Refinement
Add comprehensive tests, logging, and polish GUI design.

Unit/integration tests for RESP and CRUD
Verbose logging of commands and responses
Improve GUI responsiveness and error messages
Functional Output: Stable, fully tested Redis GUI client with proper logs and smooth user experience.
