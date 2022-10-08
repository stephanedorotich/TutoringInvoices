# ui_test

import pytest
import ui_service as use
import exceptions as ex

def test_get_input_reg(monkeypatch):
    # monkeypatch the "input" function, so that it returns "hello".
    # This simulates the user entering "hello" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "hello")
    output = use.get_input("")
    assert output == "hello"

def test_get_input_keyword_main(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "MAIN")
    with pytest.raises(ex.GoToMain):
        use.get_input("")

def test_get_input_keyword_quit(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Q")
    with pytest.raises(ex.Quit):
        use.get_input("")
