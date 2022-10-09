from abstract_data_class import abstract_data_class
from datetime import datetime
import numpy as np

class session_data_class(abstract_data_class):
    fname = "data/x1.csv"
    dtype = {
            "sessionKey": 'int',
            "studentKey": 'int',
            "datetime": 'str',
            "duration": 'float',
            "subject": 'str',
            "rate": 'int',
            "invoiceKey": 'int'
            }
    parse_dates = ['datetime']

    def get_sessions_by_student_key(self, sKey: np.int64):
        return self._data[self._data.studentKey == sKey]