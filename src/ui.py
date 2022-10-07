# ui.py
import sys, os
import sessionManager as xm
import invoiceManager as im
import paymentManager as pm
import analyzer
import exceptions as ex
import ui_service as use
import ui_operations as uop

# MENUS
def mainMenu():
	name = "MAIN MENU"
	options = [
		'students',
		'sessions',
		'invoices',
		'analysis']
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
	options = [
		'Add New',
		'View All',
		'View Student']
	choice = use.menuDisplay(name, options)
	if choice == 1:
		uop.new_student()
	if choice == 2:
		uop.view_all_students()
	if choice == 3:
		uop.view_single_student()

def sessionMenu():
	name = "SESSION MENU"
	options = [
		'Add New',
		'View All',
		'View by Student']
	choice = use.menuDisplay(name, options)
	if choice == 1:
		uop.new_session()
	if choice == 2:
		uop.view_all_sessions()
	if choice == 3:
		uop.view_sessions_by_student()

def invoiceMenu():
	name = "INVOICE MENU"
	options = [
		'Add New',
		'View All',
		'View by Student',
		'Generate Monthly Invoices',
		'Print Invoice by Student',
		'Print Invoices by Month',
		'Pay Invoice']
	choice = use.menuDisplay(name, options)
	if choice == 1:
		uop.new_invoice_for_student()
	if choice == 2:
		uop.view_all_invoices()
	if choice == 3:
		uop.view_student_invoices()
	if choice == 4:
		uop.generate_monthly_invoices()
	if choice == 5:
		uop.print_student_invoice()
	if choice == 6:
		uop.print_monthly_invoices()
	if choice == 7:
		uop.pay_invoice()

def analysisMenu():
	name = "ANALYSIS MENU"
	options = ['Total Income', 'Monthly Incomes']
	choice = use.menuDisplay(name, options)
	if choice == 1:
		analyzer.getTotalIncome(pm.payments)
	if choice == 2:
		analyzer.getIncomeByMonth(xm.sessions, im.invoices)

def quit():
	uop.save()
	sys.exit()

def run():
	uop.load()
	while True:
		try:
			mainMenu()
		except ex.GoToMain:
			continue
		except ex.Quit:
			quit()

if __name__ == "__main__":
	run()