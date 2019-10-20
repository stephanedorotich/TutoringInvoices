# invoiceManager.py
import sys
sys.path.insert(0, '../')
import csv
from datetime import date
from .invoices import Invoice
from sessions import sessionManager as xm
from pdfs import pdfManager as pm
import helpers as h

invoices = []
invoiceKey = 0

def loadInvoices(destination = 'invoices'):
	filename = f'{destination}.csv'
	try:
		with open(filename, 'r') as csv_file:
			csv_reader = csv.reader(csv_file,delimiter=',',quotechar='"')
			for row in csv_reader:
				invoice = Invoice(
					key = h.importIntegerFromString(row[0]),
					student = row[1],
					date = h.importDateFromString(row[2]),
					total = h.importFloatFromString(row[3]),
					sessions = h.importListFromString(row[4]),
					paid = h.importBooleanFromString(row[5]),
					printed = h.importBooleanFromString(row[6]))
				invoices.append(invoice)
			global invoiceKey
			invoiceKey = invoices[-1].key
	except FileNotFoundError:
		print(f'File({filename}) does not exist')

def saveInvoices(destination = 'invoices'):
	filename = f'{destination}.csv'
	with open(filename, 'w') as csv_file:
		csv_writer = csv.writer(csv_file,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
		for invoice in invoices:
			csv_writer.writerow(exportInvoice(invoice))

def exportInvoice(i):
	return [i.key, i.student, i.date, i.total, i.sessions, i.paid, i.printed]

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
	global invoiceKey
	invoiceKey+=1
	dateOfInvoice = date.today()
	total = 0
	sessionKeys = []
	sessions = xm.findSessions(student.sessions)
	for session in sessions:
		if not session.invoiced:
			total += session.duration*student.rate
			sessionKeys.append(session.key)
			session.invoiced = True
	if not sessionKeys:
		print("No new sessions to invoice for this Student\n")
		return
	invoice = Invoice(invoiceKey,student.name,dateOfInvoice,total,sessionKeys,paid)
	invoices.append(invoice)
	if not invoiceKey in student.invoices:
		student.invoices.append(invoiceKey)
	return invoiceKey

def deleteInvoice(key):
	invoice = findInvoice(key)[0]
	#TODO do stuff

def generatePDF(key):
	invoice = findInvoice(key)
	if not invoice.printed:
		pm.generatePDF(invoice)
		invoice.printed = True
