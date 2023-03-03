from abstract_data_class import abstract_data_class
from datetime import datetime, date
import numpy as np
import pandas as pd

class session_data_class(abstract_data_class):
    fname = "data/sessions.csv"
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

    def get_sessions_by_invoice_key(self, iKey: np.int64):
        return self._data[self._data.invoiceKey == iKey]

    def get_sessions_by_month(self, startDate: datetime, endDate: datetime, df = pd.DataFrame()):
        if df.empty:
            df = self._data
        return df[(df.datetime >= startDate) & (df.datetime < endDate)]

    def get_uninvoiced_sessions(self, df = pd.DataFrame()):
        if df.empty:
            df = self._data
        return df[(df.invoiceKey == -1)]

    def update_sessions_with_invoice_key(self, session_keys, invoiceKey):
        for s in session_keys:
            self._data.at[s, 'invoiceKey'] = invoiceKey

    def get_total_uninvoiced(self):
        df = self._data
        df = df[df['invoiceKey'] == -1]
        return (df['duration'] * df['rate']).sum()

# xdc = session_data_class()