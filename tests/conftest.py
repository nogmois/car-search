# tests/conftest.py

import os
import sys

# Adiciona a raiz do projeto (pasta acima de tests/) no path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
