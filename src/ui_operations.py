import calendar
import os
import subprocess
from time import sleep
from datetime import datetime, date
import ui_service as use
import helpers as h
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
        row.append(use.get_input("Please enter their parent's email: ")) #email
        row.append(use.get_input("Please enter their address: ")) # pAddress
        row.append(use.get_integer_input("Please enter their rate: ")) #rate
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
        rate = use.get_integer_input("Please enter their rate: ", True)
        if rate == 0:
            rate = student.at['rate']
        row.append(rate)
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
        startDate = h.get_first_date_of_month(year, month)
        endDate = h.get_last_date_of_month(year, month)

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
        if df.empty:
            print(f"{student.at['name']} has no invoices")
            return False
        print(f"\n{student.at['name']}'s invoices")

        for invoiceKey, invoice in df.iterrows():
            print(f"\nInvoice - {invoiceKey}")
            sessions = self._xdc.get_sessions_by_invoice_key(invoiceKey)
            print(sessions)
            print(invoice)
        return True

    def generate_monthly_invoices(self):
        month = use.getChoice("What month would you like to invoice for?", [n+1 for n in range(12)])
        year = use.getChoice("What year would you like to invoice for?", [n+1 for n in range(2018,2099)])
        startDate = h.get_first_date_of_month(year, month)
        endDate = h.get_last_date_of_month(year, month)

        print(f"\nStart:\t{startDate.strftime('%Y-%m-%d')}\nEnd:\t{endDate.strftime('%Y-%m-%d')}")

        df = self._xdc.get_sessions_by_month(startDate, endDate)
        df = self._xdc.get_uninvoiced_sessions(df)

        if df.empty:
            print("There are no sessions to invoice for the selected month.")
            return

        student_keys = df['studentKey'].unique().tolist()

        for sKey in student_keys:
            invoiceKey = self._idc.make_invoice(sKey, startDate, endDate, df[df['studentKey'] == sKey])
            session_keys = df.loc[df['studentKey'] == sKey]['sessionKey'].tolist()
            self._xdc.update_sessions_with_invoice_key(session_keys, invoiceKey)


    def print_student_invoice(self):
        raise NotImplementedError("Generating PDF invoices is not currently supported")
        # im.printInvoiceByStudent(pick_student(),
        #     use.getChoice("What month is the invoice for?", [n+1 for n in range(12)]),
        #     use.getChoice("What year would you like to invoice for?", [n+1 for n in range(2018,2099)]))

    def print_monthly_invoices(self):
        # raise NotImplementedError("Generating PDF invoices is not currently supported")
        month = use.getChoice("What month would you like to invoice for?", [n+1 for n in range(12)])
        year = use.getChoice("What year would you like to invoice for?", [n+1 for n in range(2018,2099)])
        startDate = h.get_first_date_of_month(year, month)

        df = self._idc.get_invoices_by_month(startDate)

        # for invoiceKey,invoice in df.iterrows():
        #     print(f"hello: {invoiceKey}")


        for invoiceKey,invoice in df.iterrows():
            f = open("inv_data.md", "w")
            invoiceDate = invoice['endDate'].strftime("%Y-%m-%d")

            student = self._sdc.get_student_by_key(invoice['studentKey'])
            sessions = self._xdc.get_sessions_by_invoice_key(invoiceKey)

            parentName = student['pName'].values[0]
            parentPhone = student['pPhoneNum'].values[0]
            parentEmail = student['email'].values[0]
            parentAddr = student['pAddress'].values[0]
            studentName = student['name'].values[0]

            f.write(f"\def\invoiceID{{{invoiceKey}}}\n")
            f.write(f"\def\invoiceDate{{{invoiceDate}}}\n")
            f.write(f"\def\parentName{{{parentName}}}\n")
            f.write(f"\def\parentPhone{{{parentPhone}}}\n")
            f.write(f"\def\parentEmail{{{parentEmail}}}\n")
            f.write(f"\def\parentAddr{{{parentAddr}}}\n")
            f.write(f"\def\studentName{{{studentName}}}\n")

            balanceDue = 0
            f.write("\def\sessions{")
            for sessionKey, session in sessions.iterrows():
                sessionDatetime = session['datetime'].strftime("%Y-%m-%d %H:%M")
                sessionDuration = session['duration']
                sessionRate = session['rate']
                cost = sessionDuration * sessionRate
                f.write(f" {sessionDatetime} & {sessionDuration:.2f} & \\${sessionRate}/hr & \\${cost:.2f} \\\\")
                balanceDue += cost
            f.write("}\n")
            f.write(f"\def\\balanceDue{{{balanceDue:.2f}}}\n")
            f.close()

            filename = "pdfs/TutoringInvoice{:04d}-{}.pdf".format(invoiceKey, studentName.replace(" ", "_"))
            command = "pandoc inv_data.md inv.md --pdf-engine=pdflatex -o {}".format(filename)
            subprocess.run(command.split())
            os.remove("inv_data.md")

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

        payment = self._pdc.insert_new(row)
        self._idc.update_invoice_with_payment_amount(invoice['invoiceKey'],payment['amount'])
    # ==================================== #



    # ==================================== #
    #||         Analysis Services
    def get_total_income(self):
        print(f"Grand Total: {self._idc.get_total_income()}")

    def get_monthly_income(self):
        current_year = date.today().year
        current_month = date.today().month
        for y in range(2019, current_year+1):
            print(f"\n{y}")
            total = 0
            totalPaid = 0
            for m in range(1,13):
                mi = self._idc.get_monthly_income(y, m)
                if mi[0] == 0:
                    continue
                total+= mi[0]
                totalPaid+= mi[1]
                if (mi[0] != mi[1]):
                    print(f"\t{calendar.month_abbr[m]:>3}:{mi[1]:>10}\t({mi[1]-mi[0]})")
                else:
                    print(f"\t{calendar.month_abbr[m]:>3}:{mi[1]:>10}")
            print(f"\t==============\n\tTotal:{total:>8}")

        total_uninvoiced = self._xdc.get_total_uninvoiced()
        print(f"\nUninvoiced:\t{total_uninvoiced:>6}")
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
        self._idc.save_dataframe()
        self._pdc.save_dataframe()
        self._sdc.save_dataframe()
        self._xdc.save_dataframe()
    # ==================================== #
