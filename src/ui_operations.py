import calendar
import os
import ui_service as use
import helpers as h
import studentManager as sm
import sessionManager as xm
import invoiceManager as im
import paymentManager as pm

# ==================================== #
#||         Student Services
def new_student():
    """
	Prompts the user to input a Student's details
	Validates that an integer was entered for rate, the rest are strings.
	"""
    name = use.get_input("Please enter their name: ")
    sPhoneNum = use.get_input('Please enter their phone number: ')
    sEmail = use.get_input('Please enter their email: ')
    pName = use.get_input("Please enter their parent's name: ")
    pPhone = use.get_input("Please enter their parent's phone number: ")
    pEmail = use.get_input("Please enter their parent's email: ")
    pAddress = use.get_input("Please enter their address: ")
    rate = use.get_integer_input("Please entier their rate: ")
    student = sm.insert_new_student(name, sPhoneNum, sEmail, pName, pPhone, pEmail, pAddress, rate)
    print("******************************")
    print("      NEW STUDENT ADDED       ")
    print("******************************")
    use.printItem(student)
    print("******************************")

def pick_student():
	"""
	Prompts the user to select a student
	"""
	while True:
		name = use.get_input(f'Please select a student: ')
		results = []
		for s in sm.students:
			if name.lower() in s.name.lower():
				results.append(s)
		if not results:
			print(f'There is no student matching: {name}')
			continue
		if len(results) == 1:
			student = results[0]
		else:
			student = results[use.menuDisplay(f'Multiple students match the query <{name}>',[s.name for s in results])-1]
		if use.doubleCheck(student.name):
			return student
		else:
			continue

def view_all_students():
    use.printItems(sm.students)

def view_single_student():
	use.printItem(pick_student())
# ==================================== #



# ==================================== #
#||         Session Services
def new_session():
	"""
	Prompts the user to input a Student's details
	Validates each input.
	"""
	student = pick_student()
	time = use.get_datetime_input("Please enter the datetime: ")
	duration = use.get_float_input("Please enter the duration: ")
	subject = use.get_input("Please enter the subject: ").upper()
	rate = use.get_integer_input("Please enter their rate: ")
	if rate == 0:
		rate = student.rate
	session = xm.insert_new_session(student, time, duration, subject, rate)
	print("******************************")
	print("      NEW SESSION ADDED       ")
	print("******************************")
	use.printItem(session)
	print("******************************")

def view_all_sessions():
    use.printItems(xm.sessions)

def view_sessions_by_student():
	use.printItems(xm.findSessions(pick_student().sessions))
# ==================================== #



# ==================================== #
#||         Invoice Services
def new_invoice_for_student():
    student = pick_student()
    month = use.getChoice("What month would you like to invoice for?", [n+1 for n in range(12)])
    year = use.getChoice("What year would you like to invoice for?", [n+1 for n in range(2018,2099)])
    if im.insert_new_invoice(student, month, year) == -1:
        print(f"\n{student.name} has no sessions for {year}-{month}")

def view_all_invoices():
    printItems(im.invoices)

def view_invoices_by_student():
	use.printItems(im.getInvoicesByStudent(pick_student()))

def generate_monthly_invoices():
    im.generateInvoicesByMonth(sm.students,
		use.getChoice("What month would you like to invoice for?", [n+1 for n in range(12)]),
		use.getChoice("What year would you like to invoice for?", [n+1 for n in range(2018,2099)]))
	
def print_student_invoice():
    im.printInvoiceByStudent(pick_student(),
		use.getChoice("What month is the invoice for?", [n+1 for n in range(12)]),
		use.getChoice("What year would you like to invoice for?", [n+1 for n in range(2018,2099)]))

def print_monthly_invoices():
    im.printInvoicesByMonth(
        use.getChoice("What month would you like to invoice for?", [n+1 for n in range(12)]),
		use.getChoice("What year would you like to invoice for?", [n+1 for n in range(2018,2099)]))

def pay_invoice():
    student = pick_student()
    invoice = im.findInvoice(use.getChoice(f'Please select an invoice: {student.invoices}',student.invoices))
    use.printItem(invoice)

    paymentAmount = use.get_float_input("Please enter the payment amount: ")
    paymentType = use.getChoice(f'Please enter the payment type: ',['cash','e-transfer','cheque'])
    paymentDate = use.get_date_input("Please enter the payment date: ")

    newPaymentKey = pm.newPayment(paymentType, paymentDate, paymentAmount, student.name, invoice.key)
    student.payments.append(newPaymentKey)
    invoice.payments.append(newPaymentKey)
    invoice.totalPaid += paymentAmount
# ==================================== #



# ==================================== #
#||         Analysis Services
def get_total_income():
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

def get_monthly_income():
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

def load():
	if not os.path.isdir("data"):
		os.mkdir("data")
	if not os.path.isdir("pdfs"):
		os.mkdir("pdfs")
	im.loadInvoices()
	xm.loadSessions()
	sm.loadStudents()
	pm.loadPayments()

def save():
	im.saveInvoices()
	sm.saveStudents()
	xm.saveSessions()
	pm.savePayments()
# ==================================== #
