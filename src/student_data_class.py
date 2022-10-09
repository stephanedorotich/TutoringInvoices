from abstract_data_class import abstract_data_class
import pandas as pd

class student_data_class(abstract_data_class):
    fname = "data/s1.csv"
    dtype = {
            "studentKey": 'int',
            "name": 'str',
            "pName": 'str',
            "pPhoneNum": 'str',
            "pEmail": 'str',
            "pAddress": 'str',
            "rate": 'int'
            }
    parse_dates = None

    def find_by_name(self, name: str):
        return self._data[self._data.name.str.contains(name, case=False)]