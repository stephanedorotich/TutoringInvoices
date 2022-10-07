# helpers_test

import pytest
import helpers as h
from datetime import datetime

def test_importIntegerFromString_int():
    val = h.importIntegerFromString("13")
    assert val == 13

def test_importIntegerFromString_int_and_char():
    with pytest.raises(ValueError):
        h.importIntegerFromString("78 and something else")
    
def test_importIntegerFromString_char():
    with pytest.raises(ValueError):
        h.importIntegerFromString("not a number")

def test_importIntegerFromString_float():
    with pytest.raises(ValueError):
        h.importIntegerFromString("12.34")



def test_importFloatFromString_float():
    val = h.importFloatFromString("12.34")
    assert val == 12.34

def test_importFloatFromString_float_and_char():
    with pytest.raises(ValueError):
        h.importIntegerFromString("98.76 and something else")
    
def test_importFloatFromString_char():
    with pytest.raises(ValueError):
        h.importIntegerFromString("not a number")

def test_importFloatFromString_int():
    val = h.importFloatFromString("13")
    assert val == 13.00


def test_importDateTimeFromString_datetime():
    val = h.importDateTimeFromString("2022-10-07 11:11")
    assert val == datetime(2022, 10, 7, 11, 11)

def test_importDateTimeFromString_date():
    val = h.importDateTimeFromString("2022-10-07")
    assert val == datetime(2022, 10, 7)

def test_importDateTimeFromString_char():
    with pytest.raises(ValueError):
        val = h.importDateTimeFromString("not a datetime")