# ui.py
import sys
import sessions.sessionManager as xm
import students.studentManager as sm
import invoices.invoiceManager as im
import payment.paymentManager as pm
import uihelpers as uih
import helpers as h
import analyzer
from datetime import date
import calendar

# MENUS
def mainMenu():
	name = "MAIN MENU"
	options = ['students','sessions','invoices','analysis']
	choice = uih.menuDisplay(name, options)
	if choice == 1:
		studentMenu()
	if choice == 2:
		sessionMenu()
	if choice == 3:
		invoiceMenu()
	if choice == 4:
		analysisMenu()

def studentMenu():
	name = "STUDENT MENU"
	options = ['Add New','View All','View Student','Edit']
	choice = uih.menuDisplay(name, options)
	if choice == 1:
		sm.newStudentUI()
	if choice == 2:
		uih.printItems(sm.students)
	if choice == 3:
		sm.viewStudentUI()
	if choice == 4:
		sm.editStudentUI()
	mainMenu()

def sessionMenu():
	name = "SESSION MENU"
	options = ['Add New','View All', 'View by Student']
	choice = uih.menuDisplay(name, options)
	if choice == 1:
		xm.newSessionUI()
	if choice == 2:
		uih.printItems(xm.sessions)
	if choice == 3:
		uih.printItems(xm.getSessionsByStudent(sm.pickStudent("to view the sessions of")))
	mainMenu()

def invoiceMenu():
	name = "INVOICE MENU"
	options = ['Open PDF','View All', 'View by Student','Create Invoice','Generate Invoices','Pay Invoice']
	choice = uih.menuDisplay(name, options)
	if choice == 1:
		try:
			im.openRecentInvoiceUI()
		except ValueError as e:
			print(e)
	if choice == 2:
		uih.printItems(im.invoices)
	if choice == 3:
		uih.printItems(im.getInvoicesByStudent(sm.pickStudent("to view the invoices of")))
	if choice == 4:
		im.newInvoiceUI()
	if choice == 5:
		im.generateInvoicesByMonth(sm.students,
			uih.getChoice("What month would you like to invoice for?", [n+1 for n in range(12)]))
	if choice == 6:
		im.payInvoiceUI()
	mainMenu()

def analysisMenu():
	name = "ANALYSIS MENU"
	options = ['Total Income', 'Monthly Incomes']
	choice = uih.menuDisplay(name, options)
	if choice == 1:
		analyzer.getTotalIncome(pm.payments)
	if choice == 2:
		analyzer.getIncomeByMonth(xm.sessions)
	mainMenu()

def printParentsEmails():
	emails = ""
	for s in sm.students:
		emails += s.pEmail + "; "
	print(emails)

def updateSessionInvoiceKeys():
	for session in xm.sessions:
		if session.datetime.month == 4:
			session.invoiceKey = 0

def run():
	im.loadInvoices()
	xm.loadSessions()
	sm.loadStudents()
	pm.loadPayments()
	isRunning = True
	while isRunning:
		try:
			mainMenu()
		except StopIteration as e:
			continue

run()