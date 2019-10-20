# TutoringInvoices

*****THIS PROGRAM IS UNDER CONSTRUCTION*****

NOTES TO USER:
- The INVOICE part of this program is not implemented in the UI yet and has some weird
behaviour. Scroll to bottom for more info.
- 'uihelpers.py' is the go-to place to make your own tests. They can be easily run by
the quitTest() function.



Description:
This program keeps track of STUDENTS, SESSIONS, and INVOICES for my tutoring business
and can generate pdf invoices for all the un-invoiced sessions of a given student.



To Run: >> python ui.py
- Typing 'python ui.py' in Terminal or Command Prompt will launch the User Interface
- Inputing 'Q' at any point will quit the program
	quit() quits the program and saves all STUDENTS, SESSIONS, and INVOICES
	to their respective csv files.
- Inputing 'TEST' at any point will set the var isTest = True (found in uihelpers.py)
	if isTest == True, then the 'Q' command calls quitTest()
	quitTest() quits the program without saving any changes.
	It also	runs any programmer written lines of code
	Some options are written as comments for convenience



File Descriptions:
'students.csv', 'sessions.csv', invoices.csv' are the save files for the program

'ui.py' 	runs the User Interface that guides a user through the program
'uihelpers.py' 	helps elicit and validate userInput, it also listens to userInput
		for COMMAND keys and executes the exit() and exitTest() functions.

'invoices/invoices.py' 		is the data class file that defines an INVOICE
'sessions/sessions.py' 		is the data class file that defines a SESSION
'students/students.py' 		is the data class file that defines a STUDENT

'invoices/invoiceManager.py' 	loads, TODO modifies, generates, and saves invoices
'sessions/sessioneManager.py' 	loads, TODO modifies, generates, and saves sessions
'students/studentManager.py' 	loads, modifies, generates, and saves students
'pdfs/pdfManager.py' 		writes a pdf for a given invoice, uses LaTeX



NOTES TO USER (CONTINUED):
- Invoices have some weird functionality around the 'printed' field of invoices,
and the 'invoiced' field of sessions. Consequently, the generateInvoice() and
createNewInvoiceForStudent() functions only work if those fields are False respectively.
- If not in TEST mode, if either of those functions are called and programs Quits and
Saves, then these functions will not produce anything unless new data is added or the
csv files are modified by hand.


NOTES TO SELF:
1.Include A README file that contains
	- A brief description of the project
	- Installation instructions
	- A short example/tutorial