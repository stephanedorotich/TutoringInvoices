import calendar
import os
from datetime import datetime
import ui_service as use
import helpers as h
import studentManager as sm
import sessionManager as xm
import invoiceManager as im
import paymentManager as pm

import invoice_data_class
import payment_data_class
import session_data_class
import student_data_class

class ui_operations():
    # ==================================== #
    #||         Student Services
    def new_student(self):
        """
        Prompts the user to input a Student's details
        Validates that an integer was entered for rate, the rest are strings.
        """
        row = []
        row.append(use.get_input("Please enter their name: ")) # name
        row.append(use.get_input("Please enter their parent's name: ")) # pName
        row.append(use.get_input("Please enter their parent's phone number: ")) #pPhone
        row.append(use.get_input("Please enter their parent's email: ")) #pEmail
        row.append(use.get_input("Please enter their address: ")) # pAddress
        row.append(use.get_integer_input("Please entier their rate: ")) #rate
        self._sdc.insert_new(row)
        
    def pick_student(self):
        """
        Prompts the user to select a student
        """
        while True:
            name = use.get_input(f'Please select a student: ')
            df = self._sdc.find_by_name(name)
            if df.empty:
                print(f"There is no student matching: {name}")
                continue
            if df.shape[0] == 1:
                student = df.iloc[0]
            else:
                options = df['name'].tolist()
                choice = use.menuDisplay(f'Multiple students match the query <{name}>', options)
                choice-=1 # subtract 1 for proper indexing
                student = df.iloc[choice]
            print(f"Selected <{student.at['name']}>")
            return student

    def view_all_students(self):
        print(self._sdc._data.to_string())

    def view_single_student(self):
        print(self.pick_student().to_string())
    # ==================================== #



    # ==================================== #
    #||         Session Services
    def new_session(self):
        """
        Prompts the user to input a Student's details
        Validates each input.
        """
        student = self.pick_student()
        row = []
        row.append(student.at['studentKey']) # studentKey
        row.append(use.get_datetime_input("Please enter the datetime: ")) # datetime
        row.append(use.get_float_input("Please enter the duration: ")) # duration
        row.append(use.get_input("Please enter the subject: ").upper()) # subject
        row.append(use.get_integer_input("Please enter their rate: ")) # rate
        if row[-1] == 0:
            row[-1] = student.rate
        row.append(-1) # invoiceKey
        self._xdc.insert_new(row)

    def view_all_sessions(self):
        print(self._xdc._data.to_string())

    def view_sessions_by_student(self):
        student = self.pick_student()
        sKey = student.at['studentKey']
        df = self._xdc.get_sessions_by_student_key(sKey)
        print(f"\n{student.at['name']}'s sessions")
        print(df)
    # ==================================== #



    # ==================================== #
    #||         Invoice Services
    def new_invoice_for_student(self):
        student = self.pick_student()
        sKey = student.at['studentKey']
        month = use.getChoice("What month would you like to invoice for?", [n+1 for n in range(12)])
        year = use.getChoice("What year would you like to invoice for?", [n+1 for n in range(2018,2099)])
        startDate = str(datetime(year, month, 1))
        if month == 12:
            endDate = str(datetime(year+1, 1, 1))
        else:
            endDate = str(datetime(year, month+1, 1))

        student_sessions = self._xdc.get_sessions_by_student_key(sKey)
        df = self._xdc.get_sessions_by_month(startDate, endDate, student_sessions)
        df = self._xdc.get_uninvoiced_sessions(df)

        if df.empty:
            print(f"{student.at['name']} has no sessions to invoice for the selected month.")
            return False

        invoiceKey = self._idc.make_invoice(sKey, startDate, endDate, df)
        session_keys = df['sessionKey'].tolist()
        self._xdc.update_sessions_with_invoice_key(session_keys, invoiceKey)
        return True

    def view_all_invoices(self):
        print(self._idc._data.to_string())

    def view_invoices_by_student(self):
        student = self.pick_student()
        sKey = student.at['studentKey']
        df = self._idc.get_invoices_by_student_key(sKey)
        print(f"\n{student.at['name']}'s invoices")
        print(df)

    def generate_monthly_invoices(self):
        month = use.getChoice("What month would you like to invoice for?", [n+1 for n in range(12)])
        year = use.getChoice("What year would you like to invoice for?", [n+1 for n in range(2018,2099)])
        startDate = str(datetime(year, month, 1))
        if month == 12:
            endDate = str(datetime(year+1, 1, 1))
        else:
            endDate = str(datetime(year, month+1, 1))

        df = self._xdc.get_sessions_by_month(startDate, endDate)
        df = self._xdc.get_uninvoiced_sessions(df)

        student_keys = df['studentKey'].unique().tolist()

        for sKey in student_keys:
            df = self._xdc.get_sessions_by_student_key(sKey)
            invoiceKey = self._idc.make_invoice(sKey, startDate, endDate, df)
            session_keys = df['sessionKey'].tolist()
            self._xdc.update_sessions_with_invoice_key(session_keys, invoiceKey)


    def print_student_invoice(self):
        raise NotImplementedError("Generating PDF invoices is not currently supported")
        # im.printInvoiceByStudent(pick_student(),
        #     use.getChoice("What month is the invoice for?", [n+1 for n in range(12)]),
        #     use.getChoice("What year would you like to invoice for?", [n+1 for n in range(2018,2099)]))

    def print_monthly_invoices(self):
        raise NotImplementedError("Generating PDF invoices is not currently supported")
        # im.printInvoicesByMonth(
        #     use.getChoice("What month would you like to invoice for?", [n+1 for n in range(12)]),
        #     use.getChoice("What year would you like to invoice for?", [n+1 for n in range(2018,2099)]))

    def pay_invoice(self):
        student = self.pick_student()
        sKey = student.at['studentKey']

        df = self._idc.get_invoices_by_student_key(sKey)
        df = self._idc.get_unpaid_invoices(df)
        if df.empty:
            print(f"{student.at['name']} has no unpaid invoices")

        iKeys = df['invoiceKey'].tolist()
        choice = use.menuDisplay(f'Please select the', iKeys)
        choice-=1 # subtract 1 for proper indexing
        invoice = df.iloc[choice]
        print(invoice)
        print(invoice['invoiceKey'])

        row = []
        row.append(use.getChoice(f'Please enter the payment type: ',['cash','e-transfer','cheque']))
        row.append(use.get_date_input("Please enter the payment date: "))
        row.append(use.get_float_input("Please enter the payment amount: "))
        row.append(sKey)
        row.append(invoice['invoiceKey'])

        self._pdc.insert_new(row)
    # ==================================== #



    # ==================================== #
    #||         Analysis Services
    def get_total_income(self):
        totalCash = 0
        totalEtransfer = 0
        totalCheque = 0
        for payment in pm.payments:
            if payment.paymentType == 'cash':
                totalCash += payment.amount
            elif payment.paymentType == 'e-transfer':
                totalEtransfer += payment.amount
            elif payment.paymentType == 'cheque':
                totalCheque += payment.amount
        print(f'\nTotal cash: {totalCash}')
        print(f'Total e-transfer: {totalEtransfer}')
        print(f'Total cheque: {totalCheque}')
        print(f'\nGrand Total: {totalCash + totalEtransfer + totalCheque}')

    def get_monthly_income(self):
        monthlyIncomes = {}
        yearlyIncomes = {}
        for session in xm.sessions:
            month = session.datetime.month
            year = session.datetime.year
            if not year in monthlyIncomes:
                monthlyIncomes[year] = {}
            if not month in monthlyIncomes[year]:
                monthlyIncomes[year][month] = [0,0,0,0]
            if not year in yearlyIncomes:
                yearlyIncomes[year] = [0,0,0,0]
            yearlyIncomes[year][0] += session.duration * session.rate
            yearlyIncomes[year][2] += session.duration
            yearlyIncomes[year][3] += 1
            monthlyIncomes[year][month][0] += session.duration * session.rate
            monthlyIncomes[year][month][2] += session.duration
            monthlyIncomes[year][month][3] += 1
        for invoice in im.invoices:
            month = invoice.billingPeriod[0].month
            year = invoice.billingPeriod[0].year
            yearlyIncomes[year][1] += invoice.totalPaid
            monthlyIncomes[year][month][1] += invoice.totalPaid
        for year in [*monthlyIncomes]:
            print(year)
            for month in [*monthlyIncomes[year]]:
                print(f'\t{calendar.month_abbr[month]}:\t{monthlyIncomes[year][month]}')
            print(f'Total:\t\t{yearlyIncomes[year]}\n')
    # ==================================== #



    # ==================================== #
    #||         Data Services
    def load(self):
        if not os.path.isdir("data"):
            os.mkdir("data")
        if not os.path.isdir("pdfs"):
            os.mkdir("pdfs")
        if not os.path.isfile("data/sessions.csv"):
            open("data/sessions.csv", "w")
        if not os.path.isfile("data/students.csv"):
            open("data/students.csv", "w")
        if not os.path.isfile("data/invoices.csv"):
            open("data/invoices.csv", "w")
        if not os.path.isfile("data/payments.csv"):
            open("data/payments.csv", "w")
        self._idc = invoice_data_class.invoice_data_class()
        self._pdc = payment_data_class.payment_data_class()
        self._sdc = student_data_class.student_data_class()
        self._xdc = session_data_class.session_data_class()
        
    def save(self):
        # self._idc.save_dataframe()
        self._pdc.save_dataframe()
        self._sdc.save_dataframe()
        self._xdc.save_dataframe()
    # ==================================== #