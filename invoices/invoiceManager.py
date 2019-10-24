# invoiceManager.py
import sys
sys.path.insert(0, '../')
import csv
from datetime import date
from .invoices import Invoice
from sessions import sessionManager as xm
from students import studentManager as sm
from pdfs import pdfManager as pm
import helpers as h
import uihelpers as uih

invoiceKey = 0
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
					date = h.importDateFromString(row[2]),
					sessions = h.importListFromString(row[3]),
					printed = h.importBooleanFromString(row[4]))
				invoices.append(invoice)
			global invoiceKey
			if not len(invoices) == 0:
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
	return [i.key, i.student, i.date, i.sessions, i.printed]

def findInvoice(key):
	results = h.findSingle(invoices,key)
	return results
#try-except block now found in uihelpers.openRecentInvoice()
#	except ValueError as e:
#		print(e)

def findInvoices(keys):
	try:
		results = h.findMultiple(invoices,keys)
		return results
	except ValueError as e:
		print(e)

def newInvoiceUI():
	createMonthlyInvoice(sm.pickStudent('to generate invoice for'),
		uih.getChoice("What month would you like to invoice for?", [n+1 for n in range(12)]))

def createMonthlyInvoice(student, month):
	sessionKeys = []
	sessions = xm.findSessions(student.sessions)
	dateOfInvoice = date.today()

	for session in sessions:
		if session.datetime.month == month:
			sessionKeys.append(session.key)
	if not sessionKeys:
		print("No sessions to invoice this Student for this month")
		return

	invoice = None
	for key in student.invoices:
		temp = findInvoice(key)
		if temp.date.month == month:
			invoice = findInvoice(key)
			if not sessionKeys == invoice.sessions:
				changeAttribute(invoice,'sessions',sessionKeys)
				changeAttribute(invoice,'date',dateOfInvoice)
				changeAttribute(invoice,'printed',False)

	if invoice == None:
		global invoiceKey
		invoiceKey+=1
		invoice = Invoice(invoiceKey,student.name,dateOfInvoice,sessionKeys)
		invoices.append(invoice)

	if not invoiceKey in student.invoices:
		student.invoices.append(invoiceKey)

def openRecentInvoiceUI():
	student = sm.pickStudent("to open the most recent invoice of")
	if not len(student.invoices) == 0:
		try:
			invoice = findInvoice(student.invoices[-1])
			pm.openPDF(invoice)
		except ValueError as e:
			print(e)
	else:
		raise ValueError('This student has no recent invoice to open')

def printPDF(key):
	invoice = findInvoice(key)
	if not invoice.printed:
		pm.printPDF(invoice)
		invoice.printed = True

def printRecentInvoice():
	student = sm.pickStudent("to open the print the recent invoice of")
	if not len(student.invoices) == 0:
		try:
			invoice = findInvoice(student.invoices[-1])
			printPDF(invoice.key)
		except ValueError as e:
			print(e)
	else:
		raise ValueError('This student has no recent invoice to print')

def changeAttribute(self,attributeName,newValue):
	switch = [*Invoice.__annotations__]
	if attributeName == switch[2]:
		self.date = newValue
	if attributeName == switch[3]:
		self.sessions = newValue
	if attributeName == switch[4]:
		self.printed = newValue