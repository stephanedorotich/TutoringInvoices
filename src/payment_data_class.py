from abstract_data_class import abstract_data_class
from datetime import datetime

class payment_data_class(abstract_data_class):
    fname = "data/payments.csv"
    dtype = {
            "paymentKey": 'int',
            "paymentType": 'str',
            "date": 'str',
            "amount": 'float',
            "studentKey": 'str',
            "invoiceKey": 'int',
            }
    parse_dates = ['date']