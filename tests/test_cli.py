# tests/test_cli.py

from app.cli.main import main

class DummySession:
    def __init__(self, *args, **kwargs):
        pass

    def prompt(self, *args, **kwargs):
        raise EOFError

def test_cli_exit(monkeypatch):
    # Monkeypatcha a classe PromptSession usada no módulo app.cli.main
    monkeypatch.setattr(
        'app.cli.main.PromptSession',
        DummySession
    )

    # main() deve usar DummySession e capturar o EOFError sem crashar
    main()
