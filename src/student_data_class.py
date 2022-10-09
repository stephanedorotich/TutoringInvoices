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

# sdc = student_data_class()
# print(sdc.find_single(2))

# print(sdc._data.iloc[[1,3]])

# sdc._data.loc[sdc._data.shape[0]] = [sdc._data.shape[0], "George", datetime(2022, 10, 11, 11, 11), 1.25, "MATH", 60, 0]
# sdc._data.loc[sdc._data.shape[0]] = [sdc._data.shape[0], "BANANANSSSSS", datetime(2022, 10, 11, 11, 11), 1.25, "MATH", 60, 0]

# for i in range(0,len(sdc.dtype.keys())):
#     print(type(sdc._data.iloc[6][i]))
# print(sdc._data.to_string())
# sdc.save_dataframe()