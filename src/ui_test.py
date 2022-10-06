# ui_test

import pytest
import ui

def test_global_isRunning():
    assert ui.isRunning == True

def test_global_isTest():
    assert ui.isTest == False

def test_get_input_reg(monkeypatch):
    # monkeypatch the "input" function, so that it returns "hello".
    # This simulates the user entering "hello" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "hello")
    output = ui.get_input("")
    assert output == "hello"

def test_get_input_keyword_main(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "MAIN")
    with pytest.raises(ui.RenewStateException):
        ui.get_input("")

def test_get_input_keyword_quit(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Q")
    try:
        ui.get_input("")
    except ui.RenewStateException as e:
        assert ui.isRunning == False

def test_get_input_keyword_test(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "TEST")
    try:
        ui.get_input("")
    except ui.RenewStateException as e:
        assert ui.isTest == True
