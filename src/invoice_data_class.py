from abstract_data_class import abstract_data_class
from datetime import datetime as dt
import numpy as np
import pandas as pd

class invoice_data_class(abstract_data_class):
    fname = "data/invoices.csv"
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

    def get_unpaid_invoices(self, df = pd.DataFrame()):
        if df.empty:
            df = self._data
        return df[df.totalPaid < df.total]

    def update_invoice_with_payment_amount(self, invoiceKey, amount):
        self._data.at[invoiceKey, 'totalPaid']+=amount

    def make_invoice(self, sKey: int, startDate: dt, endDate: dt, df: pd.DataFrame):
        cost = (df['duration'] * df['rate']).sum()
        # print(df.to_string())
        # print(cost)
        row = []
        row.append(sKey)
        row.append(startDate)
        row.append(endDate)
        row.append(cost)
        row.append(0)
        invoice = self.insert_new(row)
        return invoice.at['invoiceKey']

    def get_invoices_by_month(self, startDate):
        df = self._data
        return df[df['startDate'] == startDate]

    def get_total_income(self):
        return self._data['totalPaid'].sum()

    def get_monthly_income(self, year: int, month: int):
        df = self._data
        df = df[df['startDate'].dt.year == year]
        df = df[df['startDate'].dt.month == month]
        return (df['total'].sum(), df['totalPaid'].sum())