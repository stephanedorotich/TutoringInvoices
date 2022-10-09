import pandas as pd
import abc

from typing import List

class abstract_data_class(metaclass=abc.ABCMeta):
    fname: str = NotImplemented
    dtype: dict = NotImplemented
    parse_dates: list = NotImplemented

    def __new__(cls, *args, **kwargs):
        if cls is abstract_data_class:
            raise TypeError(f"Only children of '{cls.__name__}' may be instantiated")
        return super().__new__(cls)
    
    def __init__(self):
        self.load_dataframe()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.fname is NotImplemented:
            raise NotImplementedError("Please implement the `fname` class variable")
        if cls.dtype is NotImplemented:
            raise NotImplementedError("Please implement the `dtype` class variable")
        if cls.parse_dates is NotImplemented:
            raise NotImplementedError("Please implement the `parse_dates` class variable")

    def load_dataframe(self):
        """Load in the data"""
        self._data = pd.read_csv(self.fname, header=None, names=self.dtype.keys(), dtype=self.dtype, parse_dates=self.parse_dates)

    def save_dataframe(self):
        """Save the data"""
        self._data.to_csv(self.fname, header=None, index=None)
        print(f"Saved {self.__class__.__name__}")

    def insert_new(self, row: list):
        """Add a new object to the data"""
        i = self._data.shape[0]
        row.insert(0, i)
        self._data.loc[i] = row
        print(self._data.iloc[-1])

    def find_single(self, key: int):
        """Return the object in data that matches the key"""
        return self._data.iloc[key]

    def find_multiple(self, keys: list):
        """Return the objects in data that match the key"""
        return self._data.iloc[keys]