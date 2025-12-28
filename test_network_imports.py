import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

try:
    from core import config, reactor
    from network import Connection, UrlConnection, Identification, Sock, Receiver, Sender, Archiver, DatabaseLink
    print("Imports successful")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
