# ui.py
from datetime import datetime as dt
import sessionManager as xm
import studentManager as sm
import invoiceManager as im
from helpers import prettyPrint as pp
import uihelpers as uih

isTest = True

today = dt.today()

def run():
	running = True
	im.loadInvoices()
	xm.loadSessions()
	sm.loadStudents()
	invoices = im.invoices
	sessions = xm.sessions
	students = sm.students
	while running:
		im.createNewInvoiceForStudent(sm.findStudent("Ste")[0])
		im.generatePDF(0)
		pp(im.invoices)
		pp(sessions)
		pp(sm.students)
		running = False
	#dostuff while not Q:
	if not isTest:
		im.saveInvoices()
		xm.saveSessions()
		sm.saveStudents()
		

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