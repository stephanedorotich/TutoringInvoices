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

'invoices/invoiceManager.py' 	loads, TODO modifies, generates, TODO deletes, and saves invoices
'sessions/sessioneManager.py' 	loads, TODO modifies, generates, TODO deletes, and saves sessions
'students/studentManager.py' 	loads, modifies, generates, TODO deletes, and saves students
'pdfs/pdfManager.py' 		writes a pdf for a given invoice, uses LaTeX



NOTES TO USER (CONTINUED):
- Invoices have some weird functionality around the 'invoiced' field of sessions,
and the 'printed' field of invoices. Consequently, the createNewInvoiceForStudent()
and generateInvoice() functions only work if those fields are False respectively.
- If not in TEST mode, if either of those functions are called and programs Quits and
Saves, then these functions will not produce anything unless new data is added or the
csv files are modified by hand.

TODO:
- need to document dependencies for:
	- sessionManager
	- invoiceManager
	- helpers
- need to write missing documentation
- need to protect payment type of session so that it is only 'cash', 'e-transfer', or 'cheque'
- need to modify sm.editStudent() to have a better print statement to display changes.
- need to modify pm.printPDF(invoice) so that any session that has already been
  paid shows up with a rate = 0.
- need to add autoGenerateInvoices():
	- user command? --> generate invoices for all students for a given month ~
	- printPDFs for all generated invoices.
- need functionality to pay an invoice/session
- need functionality to indicate if a session has been paid for on input


MAKE NEW INVOICE
Present functionality...
	asks user to indicate student
	asks user to indicate month of the invoice
	- generates invoice by grabbing the student's sessions for the related month
	- d.n. care if session has already been invoiced.
	- d.n. check if there already exists an invoice for this month.
What I want...
	should only ever be 1 invoice for a given month.
	so...
	- needs to 're-write' invoice if one already exists.
		- maybe invoices could have a 'month' field
		*becomes billing period*
	- checks student invoices to see if one already exists for the given month.
		
	- if does... edits instead of makes new...
		invoice = None
		for key in student.invoices:
		    if findInvoice(key).datetime.month == month:
		        invoice = findInvoice(key)
		if invoice == None:
		    invoice = Invoice()
	- else:
	- compiles sessions for the requested month. if sessions is empty(), raise Error



NOTES TO SELF:
1.Include A README file that contains
	- A brief description of the project
	- Installation instructions
	- A short example/tutorial