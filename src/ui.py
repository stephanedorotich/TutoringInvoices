# ui.py
import sys, os
import dataclasses as dataclass
import sessionManager as xm
import studentManager as sm
import invoiceManager as im
import paymentManager as pm
import analyzer

isRunning = True
isTest = False
yn = ['y','n','']

class RenewStateException(Exception):
	pass

# MENUS
def mainMenu():
	name = "MAIN MENU"
	options = ['students','sessions','invoices','analysis']
	choice = menuDisplay(name, options)
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
	choice = menuDisplay(name, options)
	if choice == 1:
		sm.ui_new_student()
	if choice == 2:
		printItems(sm.students)
	if choice == 3:
		sm.viewStudentUI()

def sessionMenu():
	name = "SESSION MENU"
	options = ['Add New','View All', 'View by Student']
	choice = menuDisplay(name, options)
	if choice == 1:
		xm.newSessionUI()
	if choice == 2:
		printItems(xm.sessions)
	if choice == 3:
		printItems(xm.getSessionsByStudent(sm.ui_pick_student()))

def invoiceMenu():
	name = "INVOICE MENU"
	options = ['View All', 'View by Student','Create Invoice by Student',
				'Print Invoice by Student','Generate Invoices by Month','Print Invoices by Month','Pay Invoice']
	choice = menuDisplay(name, options)
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
	choice = menuDisplay(name, options)
	if choice == 1:
		analyzer.getTotalIncome(pm.payments)
	if choice == 2:
		analyzer.getIncomeByMonth(xm.sessions, im.invoices)

# listener:
# listends for COMMAND keys
# every userinput is is listened to.
# If userinput = 'Q', initiates quit or quitTest (depending on whether isTest = True).
# If userinput = 'TEST', sets var isTest to True, then returns input() to enable user
# to input new information with no response from the calling function.
# If not userinput = 'Q' or 'TEST' returns userinput to calling function.
# >> case sensitive
def listener(userinput):
	if userinput == 'Q':
		global isRunning
		isRunning = False
		raise RenewStateException
	elif userinput == 'TEST':
		global isTest
		isTest = True
		raise RenewStateException
	elif userinput == 'MAIN':
		raise RenewStateException
	else:
		return userinput

def get_input(prompt : str) -> str:
	return listener(input(prompt))

# quit:
# called when user inputs Q
# saves all invoices, students, and sessions to their csv files. Exits the program.
def quit():
	im.saveInvoices()
	sm.saveStudents()
	xm.saveSessions()
	pm.savePayments()
	sys.exit()

# quitTest:
# called when user inputs Q and when var isTest = True (which occurs when user inputs TEST)
# does not save invoices, students, or sessions
def quitTest():
	sys.exit()

# doubleCheck
# Asks the user to confirm their previous input.
# Looks for 'y, n, enter'
# Will continue if userinput =  enter or y
# Will ask the previous query if userinput = n
def doubleCheck(userinput):
	# if userinput was 'enter' then skips this one and assumes no input
	if userinput == '':
		return True
	query = f'Is \"{userinput}\" correct?'
	options = yn
	choice = getChoice(query,options)
	if choice == options[0] or choice == '':
		return True

# getChoice
# prompts the user to input one of the options in choices
# userinputs must match an item in choices to continue (or be a COMMAND key)
# >> not case sensitive
# RETURNS: userinput, must be one of the options in choices
def getChoice(query,choices):
	prompt = f'{query} >> '
	while True:
		userinput = get_input(prompt)
		try:
			choice = validateChoice(userinput,choices)
			return choice
		except ValueError as e:
			print(e)

def menuDisplay(name, options):
	query = ''
	if name:
		query+=f'\n{name}:\t\t(Q: quit)\nSelect one of the following:'
	else:
		query+='Select one of the following:'
	for n in range(len(options)):
		query+=f'\n\t{n+1}. {options[n]}'

	choices = [str(n+1) for n in range(len(options))]

	return int(getChoice(query, choices))


# validateChoice
# checks to see if userinput.lower() is one of the options in choices
# if not, raises ValueError
# note: if last char in choices is '', appends the word 'enter' to the
# string that gets displayed to the user.
### TODO this has changed. it can now return choice as int
def validateChoice(userinput,choices):
	for choice in choices:
		try:
			if userinput.lower() in choice:
				return choice.lower()
		except TypeError:
			if int(userinput) == choice:
				return choice
	else:
		raise ValueError(f'\"{userinput}\" is not one of the options: {choices}\n')

# printItems:
# Takes a list of Students, Sessions, or Invoices (any kind of dataclass)
# and prints them out individually
def printItems(items):
	if not len(items) == 0:
		output = ''
		itemKeys = [*items[0].__annotations__]
		totalItems = len(items)
		for n in range(totalItems):
			printItem(items[n], n+1, totalItems)

# printItem:
# Prints out a dataclass. Starts with dataclass name, followed by all of its fields
def printItem(item, itemNum = 1, totalItems = 1):
	itemKeys = [*item.__annotations__]
	### ex: type(student) = <class 'students.students.Student'>
	itemType = f'{str(type(item)).split(".")[-1][:-2]}'
	itemAsDict = dataclass.asdict(item)
	output=f'\n{itemType} ({itemNum}/{totalItems}):\n'
	for key in itemKeys:
		output+=f'\t{key}: {itemAsDict[key]}\n'
	print(output[:-1])

def run():
	if not os.path.isdir("data"):
		os.mkdir("data")
	if not os.path.isdir("pdfs"):
		os.mkdir("pdfs")
	im.loadInvoices()
	xm.loadSessions()
	sm.loadStudents()
	pm.loadPayments()
	global isRunning
	global isTest
	while isRunning:
		try:
			mainMenu()
		except RenewStateException as e:
			if isRunning == True:
				continue
			else:
				break
	if isTest:
		quitTest()
	quit()

if __name__ == "__main__":
	if len(sys.argv) == 1:
		run()