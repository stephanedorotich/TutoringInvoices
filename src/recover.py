import pandas as pd

## CLEAN STUDENTS
# dtype = {
#         "name": 'str',
#         "sPhoneNum": 'str',
#         "sEmail": 'str',
#         "pName": 'str',
#         "pPhoneNum": 'str',
#         "email": 'str',
#         "pAddress": 'str',
#         "rate": 'int',
#         "invoices": 'str',
#         "sessions": 'str',
#         "payments": 'str',
#         }
# df = pd.read_csv("backups/22-10/students.csv", header=None, names=dtype.keys(), dtype=dtype)
# # df = df.reset_index(level=0)
# df.drop("invoices", inplace=True, axis=1)
# df.drop("sessions", inplace=True, axis=1)
# df.drop("payments", inplace=True, axis=1)
# df.drop("sPhoneNum", inplace=True, axis=1)
# df.drop("sEmail", inplace=True, axis=1)
# df.to_csv("data/students.csv")

# Student Data type
# sdtype = {
#         "studentKey": 'int',
#         "name": 'str',
#         "pName": 'str',
#         "pPhoneNum": 'str',
#         "email": 'str',
#         "pAddress": 'str',
#         "rate": 'int',
#         }
# sdf = pd.read_csv("data/students.csv", header=0, names=sdtype.keys(), dtype=sdtype)
# print(df.to_string())

#Payments
# pdtype = {
#         "paymentKey": 'int',
#         "paymentType": 'str',
#         "date": 'str',
#         "amount": 'float',
#         "student": 'str',
#         "invoiceKey": 'int',
#         }
# parse_dates = ['date']

# pdf = pd.read_csv("backups/22-10/payments.csv", header=None, names=pdtype.keys(), dtype=pdtype, parse_dates=parse_dates)

# for i in range(0, pdf.shape[0]):
#         pdf.at[i, 'paymentKey']-=1
#         pdf.at[i, 'invoiceKey']-=1

#         skey = sdf.index[sdf["name"] == pdf.at[i, 'student']].tolist()[0]
#         pdf.at[i, 'student'] = skey

# # print(pdf.to_string())
# pdf.to_csv("data/payments.csv", index=None)

# Invoices
# idtype = {
#         "invoiceKey": 'int',
#         "student": 'str',
#         "startDate": 'str',
#         "endDate": 'str',
#         "sessions": 'str',
#         "payments": 'str',
#         "total": 'float',
#         "totalPaid": 'float'
#         }
# parse_dates = ['startDate', 'endDate']

# idf = pd.read_csv("backups/22-10/invoices.csv", header=None, names=idtype.keys(), dtype=idtype, parse_dates=parse_dates)
# idf.drop("sessions", inplace=True, axis=1)
# idf.drop("payments", inplace=True, axis=1)
# for i in range(0, idf.shape[0]):
#         idf.at[i, 'invoiceKey']-=1
# for i in range(0, idf.shape[0]):
#         idf.at[i, 'student'] = sdf.index[sdf["name"] == idf.at[i, 'student']].tolist()[0]

# idf.to_csv("data/invoices.csv", index=None)
# print(idf.to_string())


# Sessions
xdtype = {
        "sessionKey": 'int',
        "studentKey": 'str',
        "datetime": 'str',
        "duration": 'float',
        "subject": 'str',
        "rate": 'int',
        "invoiceKey": 'int'
        }
xdf = pd.read_csv("data/sessions.csv", header=0, names=xdtype.keys(), dtype=xdtype)
# # for i in range(0, xdf.shape[0]):
# #         xdf.at[i, 'invoiceKey']-=1
# for i in range(0,xdf.shape[0]):
#         xdf.at[i, 'studentKey'] = sdf.index[sdf["name"] == xdf.at[i, 'studentKey']].tolist()[0]
for i in range(0, xdf.shape[0]):
        xdf.at[i, 'sessionKey']-=1
# # print(xdf.to_string())
xdf.to_csv("data/sessions.csv", index=None)

# print(sdf.index[sdf["name"] == "Liam Moore"].tolist()[0])