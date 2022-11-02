from abstract_data_class import abstract_data_class
import pandas as pd

class student_data_class(abstract_data_class):
    fname = "data/students.csv"
    dtype = {
            "studentKey": 'int',
            "name": 'str',
            "pName": 'str',
            "pPhoneNum": 'str',
            "email": 'str',
            "pAddress": 'str',
            "rate": 'int'
            }
    parse_dates = None

    def find_by_name(self, name: str):
        return self._data[self._data.name.str.contains(name, case=False)]

    def get_student_by_key(self, key):
        return self._data[self._data.studentKey == key]
