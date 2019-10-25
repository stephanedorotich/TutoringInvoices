# TutoringInvoices

*****THIS PROGRAM IS UNDER CONSTRUCTION*****


Description:
This program keeps track of STUDENTS, SESSIONS, and INVOICES for my tutoring business
Given a month, it will automatically populate an invoice for a student and generate a pdf invoice for each student.

Notes to User:
- Inputing 'TEST' at any point will enter a test mode, whereupon inputing 'Q' will
result in the program quitting WITHOUT SAVING ANY CHANGES.
- Each of the Student, Session, and Invoice Menu have a 'View All' option. This is an
easy way to verify any changes you made to objects or any new objects you create.
- Presently, when generating the invoice pdf, any paid session will pass a 'RATE' of 0$/hr so that it doesn't get added to the total amount owing. This is not the desired functionality, but a consequence of the invoice template that I'm using not being able to record a downpayment on the invoice.
- Presently, I've modified the invoices.csv file so that all the 'printed' fields are False. This allows the user to generate fresh pdf invoices by running the GenerateInvoices command.

To Run: >> python ui.py
- Typing 'python ui.py' in Terminal or Command Prompt will launch the User Interface
- Inputing 'Q' at any point will quit the program
	quit() quits the program and saves all STUDENTS, SESSIONS, and INVOICES
	to their respective csv files.
- Inputing 'TEST' at any point will set the var isTest = True (found in uihelpers.py)
	if isTest == True, then the 'Q' command calls quitTest()
	which quits the program without saving any changes.


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


TODO:
- need to write missing documentation
- need to protect payment type of session so that it is only 'cash', 'e-transfer', or 'cheque'
- need to modify newSessionUI() so that it does not ask for the 'paid' or 'paymentType' fields
- need functionality to indicate if a session has been paid for on input
- need to modify sm.editStudent() to have a better print statement to display changes.
- need to find a new invoice template so I can handle 'paid' sessions more effectively


NOTES TO SELF:
1.Include A README file that contains
	- A brief description of the project
	- Installation instructions
	- A short example/tutorial