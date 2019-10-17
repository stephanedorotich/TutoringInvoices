# invoiceManager.py
import csv
from datetime import date
from invoices.invoices import Invoice
import sessionManager as xm
import pdfManager as pm
import helpers as h

invoices = []

def loadInvoices(destination = 'invoices'):
	filename = f'{destination}.csv'
	try:
		with open(filename, 'r') as csv_file:
			csv_reader = csv.reader(csv_file,delimiter=',',quotechar='"')
			for row in csv_reader:
				invoice = Invoice(
					key = h.importIntegerFromString(row[0]),
					student = row[1],
					datetime = importDateTimeFromString(row[2]),
					total = importFloatFromString(row[3]),
					sessions = importListFromString(row[4]),
					paid = importBooleanFromString(row[5]),
					printed = importBooleanFromString(row[6]))
				invoices.append(invoice)
	except FileNotFoundError:
		print(f'File({filename}) does not exist')

def saveInvoices(destination = 'invoices'):
	filename = f'{destination}.csv'
	with open(filename, 'w') as csv_file:
		csv_writer = csv.writer(csv_file,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
		for invoice in invoices:
			csv_writer.writerow(exportInvoice(invoice))

def exportInvoice(i):
	return [i.key, i.student, i.datetime, i.total, i.sessions, i.paid, i.printed]

def findInvoice(key):
	try:
		results = h.findSingle(invoices,key)
		return results
	except ValueError as e:
		print(e)

def findInvoices(keys):
	try:
		results = h.findMultiple(invoices,keys)
		return results
	except ValueError as e:
		print(e)

def createNewInvoiceForStudent(student, paid = False):
	if not invoices:
		key = 0
	else:
		key = (invoices[-1].key) + 1
	dateOfInvoice = date.today()
	total = 0
	sessionKeys = []
	sessions = xm.findSessions(student.sessions)
	for session in sessions:
		if not session.invoiced:
			total += session.duration*student.rate
			sessionKeys.append(session.key)
			session.invoiced = True
	invoice = Invoice(key,student.name,dateOfInvoice,total,sessionKeys,paid)
	invoices.append(invoice)
	if not key in student.invoices:
		student.invoices.append(key)
	return key

def deleteInvoice(key):
	invoice = findInvoice(key)[0]
	#TODO do stuff

def generatePDF(key):
	invoice = findInvoice(key)[0]
	if not invoice.printed:
		pm.generatePDF(invoice)
		invoice.printed = True
