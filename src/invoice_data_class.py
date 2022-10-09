from abstract_data_class import abstract_data_class
from datetime import datetime
import numpy as np
import pandas as pd

class invoice_data_class(abstract_data_class):
    fname = "data/i1.csv"
    dtype = {
            "invoiceKey": 'int',
            "studentKey": 'int',
            "startDate": 'str',
            "endDate": 'str',
            "total": 'float',
            "totalPaid": 'float'
            }
    parse_dates = ['startDate', 'endDate']

    def get_invoices_by_student_key(self, sKey: np.int64):
        return self._data[self._data.studentKey == sKey]

    def make_invoice(self, sKey: int, startDate: str, endDate: str, df: pd.DataFrame):
        cost = (df['duration'] * df['rate']).sum()
        row = []
        row.append(sKey)
        row.append(startDate)
        row.append(endDate)
        row.append(cost)
        row.append(0)
        invoice = self.insert_new(row)
        return invoice.at['invoiceKey']
