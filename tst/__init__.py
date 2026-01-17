import sys
import os

# Add `src` to the system path to allow imports of core.
_src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if _src_path not in sys.path:
    sys.path.insert(0, _src_path)
