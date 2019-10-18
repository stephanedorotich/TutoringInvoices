# ui.py
from datetime import datetime as dt
import dataclasses as dc
import sessions.sessionManager as xm
import students.studentManager as sm
import invoices.invoiceManager as im
from students.students import Student
import uihelpers as uih
# Basic functionality:
#	Must be able to add a new student
# 		Must prompt user to provide responses for each of the field values.
#	Must be able to add new invoice
#		Must allow the user to search for a student
#		Must prompt user to provide responses for each of the field values.
#	Must be able ot generate new invoices.
#		Functionality uncertain. Probably iterates through all students and prints invoices
	
today = dt.today()


def mainMenu():
	print("MAIN MENU:\t    (Q: quit)")
	query = 'Would you like to:\n\t1. Add a new student\n\t2. Add a new session'
	options = ['1','2']
	choice = uih.getChoice(query,options)
	if choice == options[0]:
		newStudent()
	if choice == options[1]:
		newSession()

def newStudent():
	sm.newStudentUI()
	mainMenu()

def newSession():
	return

def run():
	im.loadInvoices()
	xm.loadSessions()
	sm.loadStudents()
	#im.generatePDF(0)
	mainMenu()

run()
#LISTENER:
#	--> Q to Quit
#	--> MM for MainMenu
#-->Sessions
#	-->AddNew: 	Need to choose student
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
#	-->AddNew
#	-->Delete
#		-->Recent?
#		-->Search
#	-->View
#		-->Recent
#		-->Search
#	-->Edit
#		-->[*Students.__annotations__]