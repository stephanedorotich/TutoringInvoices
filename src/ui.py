# ui.py
import sys, os
import dataclasses as dataclass
import sessionManager as xm
import studentManager as sm
import invoiceManager as im
import paymentManager as pm
import helpers as h
import analyzer
from datetime import datetime
import exceptions as ex
import ui_service as use
import ui_operations as uop

# MENUS
def mainMenu():
	name = "MAIN MENU"
	options = ['students','sessions','invoices','analysis']
	choice = use.menuDisplay(name, options)
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
	options = ['Add New','View All','View Student']
	choice = use.menuDisplay(name, options)
	if choice == 1:
		uop.new_student()
	if choice == 2:
		uop.view_all_students()
	if choice == 3:
		uop.view_single_student()

def sessionMenu():
	name = "SESSION MENU"
	options = ['Add New','View All', 'View by Student']
	choice = use.menuDisplay(name, options)
	if choice == 1:
		xm.ui_new_session()
	if choice == 2:
		printItems(xm.sessions)
	if choice == 3:
		printItems(xm.getSessionsByStudent(sm.ui_pick_student()))

def invoiceMenu():
	name = "INVOICE MENU"
	options = ['View All', 'View by Student','Create Invoice by Student',
				'Print Invoice by Student','Generate Invoices by Month','Print Invoices by Month','Pay Invoice']
	choice = use.menuDisplay(name, options)
	if choice == 1:
		printItems(im.invoices)
	if choice == 2:
		printItems(im.getInvoicesByStudent(sm.ui_pick_student()))
	if choice == 3:
		im.newInvoiceUI()
	if choice == 4:
		im.printInvoiceByStudent(sm.ui_pick_student(),
			getChoice("What month is the invoice for?", [n+1 for n in range(12)]),
			getChoice("What year would you like to invoice for?", [n+1 for n in range(2019,2099)]))
	if choice == 5:
		im.generateInvoicesByMonth(sm.students,
			getChoice("What month would you like to invoice for?", [n+1 for n in range(12)]),
			getChoice("What year would you like to invoice for?", [n+1 for n in range(2019,2099)]))
	if choice == 6:
		im.printInvoicesByMonth(getChoice("What month would you like to invoice for?", [n+1 for n in range(12)]),
			getChoice("What year would you like to invoice for?", [n+1 for n in range(2019,2099)]))
	if choice == 7:
		im.payInvoiceUI()

def analysisMenu():
	name = "ANALYSIS MENU"
	options = ['Total Income', 'Monthly Incomes']
	choice = use.menuDisplay(name, options)
	if choice == 1:
		analyzer.getTotalIncome(pm.payments)
	if choice == 2:
		analyzer.getIncomeByMonth(xm.sessions, im.invoices)

# quit:
# called when user inputs Q
# saves all invoices, students, and sessions to their csv files. Exits the program.
def quit():
	im.saveInvoices()
	sm.saveStudents()
	xm.saveSessions()
	pm.savePayments()
	sys.exit()

def run():
	if not os.path.isdir("data"):
		os.mkdir("data")
	if not os.path.isdir("pdfs"):
		os.mkdir("pdfs")
	im.loadInvoices()
	xm.loadSessions()
	sm.loadStudents()
	pm.loadPayments()
	while True:
		try:
			mainMenu()
		except ex.GoToMain:
			continue
		except ex.Quit:
			quit()

if __name__ == "__main__":
	run()