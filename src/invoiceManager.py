# invoiceManager.py
import sys
import csv
from datetime import date
import calendar
import Invoice
import sessionManager as xm
import studentManager as sm
import paymentManager as pm
import pdfManager as pdfm
import helpers as h
import uihelpers as uih

invoiceKey = 0
invoices = []

def loadInvoices(filename = 'data/invoices.csv'):
	try:
		with open(filename, 'r') as csv_file:
			csv_reader = csv.reader(csv_file,delimiter=',',quotechar='"')
			for row in csv_reader:
				if len(row) != 0:
					invoice = Invoice.Invoice(
						key = h.importIntegerFromString(row[0]),
						student = row[1],
						billingPeriod = h.importDateTupleFromString(row[2]),
						sessions = h.importListFromString(row[3]),
						payments = h.importListFromString(row[4]),
						total = h.importFloatFromString(row[5]),
						totalPaid = h.importFloatFromString(row[6])
						)
					invoices.append(invoice)
			global invoiceKey
			if not len(invoices) == 0:
				invoiceKey = invoices[-1].key
	except FileNotFoundError:
		print(f'File({filename}) does not exist')

def saveInvoices(filename = 'data/invoices.csv'):
	with open(filename, 'w') as csv_file:
		csv_writer = csv.writer(csv_file,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
		for invoice in invoices:
			csv_writer.writerow(exportInvoice(invoice))

def exportInvoice(i):
	return [i.key, i.student, str(str(i.billingPeriod[0])+','+str(i.billingPeriod[1])), i.sessions, i.payments, i.total, i.totalPaid]

def findInvoice(key):
	try:
		result = h.findSingle(invoices,key)
		return result
	except ValueError as e:
		print(e)

def findInvoices(keys):
	results = h.findMultiple(invoices,keys)
	return results

def newInvoiceUI():
	createMonthlyInvoice(
		sm.pickStudent('to generate invoice for'),
		uih.getChoice("What month would you like to invoice for?", [n+1 for n in range(12)]),
		uih.getChoice("What year would you like to invoice for?", [n+1 for n in range(2019,2099)]))

def printInvoiceByStudent(student, month, year):
	invoices = getInvoicesByStudent(student)
	for i in invoices:
		if (i.billingPeriod[0].month == month) & (i.billingPeriod[0].year == year):
			pdfm.printPDF(i)

def generateInvoicesByMonth(students, month, year):
	for student in students:
		if hasSessionsToInvoiceForMonth(student, month, year):
			createMonthlyInvoice(student, month, year)

def printInvoicesByMonth(month, year):
	for invoice in invoices:
		if invoice.billingPeriod[0].month == month and invoice.billingPeriod[0].year == year:
			pdfm.printPDF(invoice)

def hasSessionsToInvoiceForMonth(student, month, year):
	sessions = xm.findSessions(student.sessions)
	for session in sessions:
		if session.invoiceKey == 0 and session.datetime.month == month and session.datetime.year == year:
			return True
	return False

def createMonthlyInvoice(student, month, year):
	global invoiceKey
	invoiceKey+=1
	global invoices
	sessionKeys = []
	total = 0
	sessions = xm.findSessions(student.sessions)

	for session in sessions:
		if session.datetime.month == month and session.datetime.year == year and session.invoiceKey == 0:
			sessionKeys.append(session.key)
			session.invoiceKey = invoiceKey
			total += session.rate * session.duration
	invoice = Invoice.Invoice(invoiceKey,student.name,(date(year, month, 1),date(year, month, calendar.monthrange(year, month)[1])), sessionKeys, [], total)
	invoices.append(invoice)
	student.invoices.append(invoiceKey)
	return invoice.key

def openRecentInvoiceUI():
	student = sm.pickStudent("to open the most recent invoice of")
	if not len(student.invoices) == 0:
		try:
			invoice = findInvoice(student.invoices[-1])
			pdfm.openPDF(invoice)
		except ValueError as e:
			print(e)
	else:
		raise ValueError('This student has no invoices')

def getInvoicesByStudent(student):
	return findInvoices(student.invoices)

def payInvoiceUI():
	student = sm.pickStudent('to pay an Invoice for')
	invoice = findInvoice(uih.getChoice(f'Please select an invoice: {student.invoices}',student.invoices))
	uih.printItem(invoice)

	paymentAmount = uih.listener(input("Please enter the payment amount: "))
	if (uih.doubleCheck(paymentAmount)):
		if paymentAmount == "":
			amount = invoice.total
		else:
			amount = h.importFloatFromString(paymentAmount)

	paymentType = uih.getChoice(f'Please indicate the payment type',['cash','e-transfer','cheque'])
	while True:
		paymentDate = uih.listener(input("Please enter the payment date: "))
		if 'today' in paymentDate:
			paymentDate = str(date.today())
		if 'yesterday' in paymentDate:
			paymentDate = date.strftime(date.today() - timedelta(1), '%Y-%m-%d')
		try:
			paymentDate = h.importDateFromString(paymentDate)
			break
		except ValueError as e:
			print(e)
			continue
	newPaymentKey = pm.newPayment(paymentType, paymentDate, amount, student.name, invoice.key)
	student.payments.append(newPaymentKey)
	invoice.payments.append(newPaymentKey)
	invoice.totalPaid += amount

def changeAttribute(self,attributeName,newValue):
	switch = [*Invoice.__annotations__]
	if attributeName == switch[4]:
		self.sessions = newValue