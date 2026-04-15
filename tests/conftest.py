import sys
from pathlib import Path

# Add the src dir to Pythons import path to allow module imports
SRC_DIR = Path(__file__).resolve().parents[1] / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
