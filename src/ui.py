# ui.py
import sys, os
import sessionManager as xm
import studentManager as sm
import invoiceManager as im
import paymentManager as pm
import uihelpers as uih
import analyzer

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
	options = ['Add New','View All','View Student']
	choice = uih.menuDisplay(name, options)
	if choice == 1:
		sm.newStudentUI()
	if choice == 2:
		uih.printItems(sm.students)
	if choice == 3:
		sm.viewStudentUI()
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
	options = ['View All', 'View by Student','Create Invoice by Student',
				'Print Invoice by Student','Generate Invoices by Month','Print Invoices by Month','Pay Invoice']
	choice = uih.menuDisplay(name, options)
	if choice == 1:
		uih.printItems(im.invoices)
	if choice == 2:
		uih.printItems(im.getInvoicesByStudent(sm.pickStudent("to view the invoices of")))
	if choice == 3:
		im.newInvoiceUI()
	if choice == 4:
		im.printInvoiceByStudent(sm.pickStudent("to print the invoice of"),
			uih.getChoice("What month is the invoice for?", [n+1 for n in range(12)]),
			uih.getChoice("What year would you like to invoice for?", [n+1 for n in range(2019,2099)]))
	if choice == 5:
		im.generateInvoicesByMonth(sm.students,
			uih.getChoice("What month would you like to invoice for?", [n+1 for n in range(12)]),
			uih.getChoice("What year would you like to invoice for?", [n+1 for n in range(2019,2099)]))
	if choice == 6:
		im.printInvoicesByMonth(uih.getChoice("What month would you like to invoice for?", [n+1 for n in range(12)]),
			uih.getChoice("What year would you like to invoice for?", [n+1 for n in range(2019,2099)]))
	if choice == 7:
		im.payInvoiceUI()
	mainMenu()

def analysisMenu():
	name = "ANALYSIS MENU"
	options = ['Total Income', 'Monthly Incomes']
	choice = uih.menuDisplay(name, options)
	if choice == 1:
		analyzer.getTotalIncome(pm.payments)
	if choice == 2:
		analyzer.getIncomeByMonth(xm.sessions, im.invoices)
	mainMenu()

def run():
	if not os.path.isdir("data"):
		os.mkdir("data")
	if not os.path.isdir("pdfs"):
		os.mkdir("pdfs")
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

if __name__ == "__main__":
	if len(sys.argv) == 1:
		run()