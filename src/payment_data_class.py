from abstract_data_class import abstract_data_class
from datetime import datetime

class payment_data_class(abstract_data_class):
    fname = "data/p1.csv"
    dtype = {
            "paymentKey": 'int',
            "paymentType": 'str',
            "date": 'str',
            "amount": 'float',
            "studentKey": 'str',
            "invoiceKey": 'int',
            }
    parse_dates = ['date']

# pdc = session_data_class()
# sdc.insert_new(["George", datetime(2022, 10, 11, 11, 11), 1.25, "MATH", 60, 0])
# print(sdc.find_single(3))

# print(sdc._data.iloc[[1,3]])

# sdc._data.loc[sdc._data.shape[0]] = [sdc._data.shape[0], "George", datetime(2022, 10, 11, 11, 11), 1.25, "MATH", 60, 0]
# sdc._data.loc[sdc._data.shape[0]] = [sdc._data.shape[0], "BANANANSSSSS", datetime(2022, 10, 11, 11, 11), 1.25, "MATH", 60, 0]

# for i in range(0,len(sdc.dtype.keys())):
#     print(type(sdc._data.iloc[6][i]))
# print(pdc._data.to_string())
# sdc.save_dataframe()