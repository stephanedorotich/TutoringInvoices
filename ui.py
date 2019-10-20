# ui.py
import sys
import sessions.sessionManager as xm
import students.studentManager as sm
import invoices.invoiceManager as im
import uihelpers as uih
# Basic functionality:
#
#	Must be able to add a new student - DONE
# 		Must prompt user to provide responses for each of the field values.
#
#	Must be able to add new invoice - DONE
#		Must allow the user to search for a student
#		Must prompt user to provide responses for each of the field values.
#	
#	Must be able ot generate new invoices. - TODO
#		Functionality uncertain. Perhaps iterates through all students and prints invoices,
#		maybe automatically does so at the end of the month?


isTest = False

# listener:
# listends for COMMAND keys
# every userinput is is listened to.
# If userinput = 'Q', initiates exit or exitTest (depending on whether isTest = True).
# If userinput = 'TEST', sets var isTest to True, then returns input() to enable user
# to input new information with no response from the calling function.
# If not userinput = 'Q' or 'TEST' returns userinput to calling function.
# >> case sensitive
def listener(userinput):
	global isTest
	if userinput == 'Q':
		if isTest:
			exitTest()
		else:
			exit()
	elif userinput == 'TEST':
		isTest = True
		return listener(input())
	else:
		return userinput

def mainMenu():
	print("MAIN MENU:\t    (Q: quit)")
	query = '''Would you like to:
\t1. Add a new student
\t2. Add a new session
\t3. Edit a student'''
	options = ['1','2','3']
	choice = uih.getChoice(query,options)
	if choice == options[0]:
		newStudent()
	if choice == options[1]:
		newSession()
	if choice == options[2]:
		editStudent()

def newStudent():
	sm.newStudentUI()
	mainMenu()

def newSession():
	xm.newSessionUI()
	mainMenu()

def editStudent():
	sm.editStudentUI()
	mainMenu()

# exit:
# called when user inputs Q
# saves all invoices, students, and sessions to their csv files
def exit():
	im.saveInvoices()
	sm.saveStudents()
	xm.saveSessions()
	sys.exit()

# exitTest:
# called when user inputs Q and when var isTest = True (which occurs when user inputs TEST)
# does not save invoices, students, or sessions
# performs various programmer defined actions.
# TODO: enable user control do perform various operations
def exitTest():
#	im.createNewInvoiceForStudent(sm.findStudent("Ste"))
	uih.printItem(sm.findStudent("Ste"))
	im.saveInvoices()
	sys.exit()

def run():
	im.loadInvoices()
	xm.loadSessions()
	sm.loadStudents()
	#im.generatePDF(0)
	mainMenu()

run()
#LISTENER:
#	--> Q to Quit
#	--> TEST:
#			Changes isTest to True, runs alternate Exit code (with options you can select) when
#			command Q is heard







#-->Sessions
#	DONE-->AddNew: 	Need to choose student
#				-->Recent
#				-->Search
#				Need to specify datetime
#				-->today
#				-->custom
#				Need to specifiy duration (as float)
#	-->Delete
#		-->Recent?
#		-->Search
#	-->View
#		-->Recent
#		-->Recents?(such as 5 most recent)
#		-->Search
#	-->Edit
#		-->[*Sessions.__annotations__]
#-->Students
#	DONE-->AddNew
#	-->Delete
#		-->Recent?
#		-->Search
#	-->View
#		-->Recent
#		-->Search
#	DONE-->Edit