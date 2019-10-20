# uihelpers.py
import sys
import dataclasses as dataclass
import sessions.sessionManager as xm
import students.studentManager as sm
import invoices.invoiceManager as im

###########################################################################
# Primary purpose is to validate userinput and listen for COMMAND keys
# Also provide a generic print for dataclass items
# 
# note: Ideally I want the quit & quitTest functions to be found in ui
# but importing ui from here seems to break the code. TODO ?
###########################################################################



yn = ['y', 'n', '']
isTest = False

# listener:
# listends for COMMAND keys
# every userinput is is listened to.
# If userinput = 'Q', initiates quit or quitTest (depending on whether isTest = True).
# If userinput = 'TEST', sets var isTest to True, then returns input() to enable user
# to input new information with no response from the calling function.
# If not userinput = 'Q' or 'TEST' returns userinput to calling function.
# >> case sensitive
def listener(userinput):
	global isTest
	if userinput == 'Q':
		if isTest:
			quitTest()
		else:
			quit()
	elif userinput == 'TEST':
		isTest = True
		return listener(input())
	else:
		return userinput

# quit:
# called when user inputs Q
# saves all invoices, students, and sessions to their csv files
def quit():
	im.saveInvoices()
	sm.saveStudents()
	xm.saveSessions()
	sys.quit()

# quitTest:
# called when user inputs Q and when var isTest = True (which occurs when user inputs TEST)
# does not save invoices, students, or sessions
# performs various programmer defined actions.
# TODO: enable user control do perform various operations
def quitTest():
#	printItems(im.invoices)
#	printItems(xm.sessions)
#	printItems(sm.students)
	printItem(sm.findStudent('Stephane'))
#	im.createNewInvoiceForStudent(sm.findStudent("Ste"))
#	im.createNewInvoiceForStudent(sm.findStudent("iba"))
#	im.generateInvoice(0)
	sys.exit()

# doubleCheck
# Asks the user to confirm their previous input.
# Looks for 'y, n, enter'
# Will continue if userinput =  enter or y
# Will ask the previous query if userinput = n
def doubleCheck(userinput):
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
		userinput = listener(input(prompt))
		try:
			choice = validateChoice(userinput,choices)
			return choice
		except ValueError as e:
			print(e)

# validateChoice
# checks to see if userinput.lower() is one of the options in choices
# if not, raises ValueError
# note: if last char in choices is '', appends the word 'enter' to the
# string that gets displayed to the user.
def validateChoice(userinput,choices):
	if userinput.lower() in choices:
		return userinput.lower()
	else:
		options = ", ".join(choices)
		if choices[-1]=='':
			options+='enter'
		raise ValueError(f'\"{userinput}\" is not one of the options: ({options})\n')

# printItems:
# Takes a list of Students, Sessions, or Invoices (any kind of dataclass)
# and prints them out individually
def printItems(items):
	output = ''
	itemKeys = [*items[0].__annotations__]
	totalItems = len(items)
	for n in range(totalItems):
		printItem(items[n], n+1, totalItems)

# printItem:
# Prints out a dataclass. Starts with dataclass name, followed by all of its fields
def printItem(item, itemNum = 1, totalItems = 1):
	itemKeys = [*item.__annotations__]
	itemType = f'{str(type(item)).split(".")[-1][:-2]}'
	### ex: type(student) = <class 'students.students.Student'>
	itemAsDict = dataclass.asdict(item)
	output=f'\n{itemType} ({itemNum}/{totalItems}):\n'
	for key in itemKeys:
		output+=f'\t{key}: {itemAsDict[key]}\n'
	print(output)
