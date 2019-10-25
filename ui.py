# ui.py
import sys
import sessions.sessionManager as xm
import students.studentManager as sm
import invoices.invoiceManager as im
import uihelpers as uih
#	Must be able ot generate new invoices. - TODO
#		Functionality uncertain. Perhaps iterates through all students and prints invoices,
#		maybe automatically does so at the end of the month?


# MENUS
def mainMenu():
	print("MAIN MENU:\t\t(Q: quit)")
	query = '''\tstudents
\tsessions
\tinvoices'''
	options = ['students','sessions','invoices', '1', '2', '3']
	choice = uih.getChoice(query,options)
	if choice == options[0] or choice == options[3]:
		studentMenu()
	if choice == options[1] or choice == options[4]:
		sessionMenu()
	if choice == options[2] or choice == options[5]:
		invoiceMenu()

def studentMenu():
	print("\nSTUDENT MENU:\t\t(Q: quit)")
	query = '''Would you like to:
\t1. Add New
\t2. Edit
\t3. View Student
\t4. View All'''
	options = ['1','2','3','4']
	choice = uih.getChoice(query,options)
	if choice == options[0]:
		sm.newStudentUI()
	if choice == options[1]:
		sm.editStudentUI()
	if choice == options[2]:
		sm.viewStudentUI()
	if choice == options[3]:
		uih.printItems(sm.students)
	mainMenu()

def sessionMenu():
	name = "SESSION MENU"
	options = ['Add New','View All']

	query = f'\n{name}:\t\t(Q: quit)\nWould you like to:'
	listener = []

	for n in range(len(options)):
		query+=f'\n\t{n+1}. {options[n]}'
		listener.append(str(n+1))

	choice = uih.getChoice(query,listener)

	if choice == listener[0]:
		xm.newSessionUI()
	if choice == listener[1]:
		uih.printItems(xm.sessions)
	mainMenu()

def invoiceMenu():
	print("\nINVOICE MENU:\t\t(Q: quit)")
	query = '''Would you like to:
\t1. Open PDF
\t2. View All
\t3. Create Invoice
\t4. Print Invoice
\t5. Generate Invoices
\t6. Pay Invoice'''
	options = ['1','2','3','4','5','6']
	choice = uih.getChoice(query,options)
	if choice == options[0]:
		try:
			im.openRecentInvoiceUI()
		except ValueError as e:
			print(e)
	if choice == options[1]:
		uih.printItems(im.invoices)
	if choice == options[2]:
		try:
			im.newInvoiceUI()
		except ValueError as e:
			print(e)
	if choice == options[3]:
		try:
			im.printRecentInvoice()
		except ValueError as e:
			print(e)
	if choice == options[4]:
		im.generateInvoicesByMonth(sm.students,
			uih.getChoice("What month would you like to invoice for?", [n+1 for n in range(12)]))
	if choice == options[5]:
		im.payInvoiceUI()
	mainMenu()

def run():
	im.loadInvoices()
	xm.loadSessions()
	sm.loadStudents()
	isRunning = True
	while isRunning:
		try:
			mainMenu()
		except StopIteration as e:
			print(e)
			continue

run()

#-->Sessions
#	-->Delete
#		-->Recent?
#		-->Search
#	-->Edit
#		-->[*Sessions.__annotations__]
#-->Students
#	-->Delete
#		-->Recent?
#		-->Search