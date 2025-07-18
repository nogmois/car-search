# tests/test_cli.py

from app.cli.main import main

# Simula uma sessão onde o usuário aperta Ctrl+D de cara
class DummySession:
    def __init__(self, *args, **kwargs):
        pass

    def prompt(self, *args, **kwargs):
        raise EOFError  # simula "sair" logo de cara

def test_cli_exit(monkeypatch):
    # Substitui a PromptSession do prompt_toolkit por nossa dummy
    monkeypatch.setattr("app.cli.main.PromptSession", DummySession)

    # Só testa se o main() roda sem explodir ao receber EOF
    main()
