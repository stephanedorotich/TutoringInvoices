# invoiceManager.py
import csv
from datetime import date
import calendar
import Invoice
import sessionManager as xm
import pdfManager as pdfm
import helpers as h

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

def printInvoiceByStudent(student, month, year):
	invoices = getInvoicesByStudent(student)
	for i in invoices:
		if (i.billingPeriod[0].month == month) & (i.billingPeriod[0].year == year):
			pdfm.printPDF(i)

def generateInvoicesByMonth(students, month, year):
	for student in students:
		if not insert_new_invoice(student, month, year) == -1:
			print(f"Made invoice for {student.name}")

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

def insert_new_invoice(student, month, year):
	if not hasSessionsToInvoiceForMonth(student, month, year):
		return -1
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

def getInvoicesByStudent(student):
	return findInvoices(student.invoices)
