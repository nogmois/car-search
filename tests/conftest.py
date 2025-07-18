# tests/conftest.py

import os
import sys

# Garante que a pasta raiz do projeto está no sys.path
# Isso permite importar app.*, mesmo rodando os testes diretamente
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
