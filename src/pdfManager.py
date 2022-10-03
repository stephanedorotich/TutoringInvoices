# invoicePDFGenerator.py
import sys
import os,glob,subprocess,shutil
import invoiceManager as im
import sessionManager as xm
import studentManager as sm

def getFileName(invNum, studentName):
	return f'TutoringInvoice{invNum}-{studentName.split(" ")[0]}'

def getInvNum(invKey):
	invNum = ''
	for _ in range(4-len(str(invKey))):
		invNum+='0'
	invNum+=str(invKey)
	return invNum

def printPDF(invoice):
	student = sm.findStudent(invoice.student)
	sessions = xm.findSessions(invoice.sessions)
	invoiceNumber = getInvNum(invoice.key)
	filename = f'TutoringInvoice{invoiceNumber}-{student.name.split(" ")[0]}'

	header = r'''\documentclass{invoice}
\renewcommand{\familydefault}{\sfdefault}
\def \tab {\hspace*{3ex}}
\begin {document}
\begin{center}
{\huge\sc St\'ephane Dorotich}\\
{\Large\sc Tutoring}
\end{center}
\bigskip
Invoice Number: INVOICENUMBER
\hrule
St\'ephane Dorotich \hfill 587-434-7693 \\
10 West Beynon Rise, Cochrane, AB \hfill stephanedorotich@gmail.com \\

{\large \sc Invoice To:} \hfill {\sc Billing Period:} INVOICEDATE\\
NAME PHONENUM EMAIL ADDRESS'''
	header = fillHeader(header, student, invoice)

	footer = r'''Payable by: cash, cheque, or e-transfer
\end{document}'''

	main = fillMain(student, sessions)

	content = header + main + footer

	with open(f'{filename}.tex','w') as f:
		f.write(content)

	commandLine = subprocess.Popen(['pdflatex', f'{filename}.tex'])
	commandLine.communicate()

	os.unlink(f'{filename}.aux')
	os.unlink(f'{filename}.log')
	os.unlink(f'{filename}.tex')
	shutil.move(f'{filename}.pdf', f'pdfs/{filename}.pdf')

def fillHeader(header,student,invoice):
	NAME = ''
	if len(student.pName) == 0:
		NAME = student.name
	else:
		NAME = student.pName

	PHONENUM = student.pPhoneNum
	EMAIL = student.pEmail
	ADDRESS = student.pAddress
	INVOICENUMBER = getInvNum(invoice.key)

	temp = r'''\tab NAME \\'''
	header = header.replace("NAME",temp.replace("NAME",NAME))
	header = header.replace("INVOICENUMBER", f'{INVOICENUMBER}')

	if not len(PHONENUM) == 0:
		temp = r'''\tab PHONENUM \\'''
		header = header.replace("PHONENUM",temp.replace("PHONENUM",PHONENUM))
	else:
		header = header.replace("PHONENUM",'')

	if not len(EMAIL) == 0:
		temp = r'''\tab EMAIL \\'''
		print("_" in EMAIL)
		if "_" in EMAIL:
			EMAIL = EMAIL.replace("_",'''\_''')
		header = header.replace("EMAIL",temp.replace("EMAIL",EMAIL))
	else:
		header = header.replace("EMAIL",'')

	if not len(ADDRESS) == 0:
		temp = r'''\tab ADDRESS \\'''
		header = header.replace("ADDRESS",temp.replace("ADDRESS",ADDRESS))
	else:
		header = header.replace("ADDRESS",'')

	header = header.replace("INVOICEDATE",str(str(invoice.billingPeriod[0]) + " to " + str(invoice.billingPeriod[1])))
	return header

def fillMain(student,sessions):
	main = r'''\\\\
{\sc Tutoring - STUDENTNAME}
\begin{invoiceTable}
\feetype{Tutoring Services}                          
SESSIONS
\end{invoiceTable}'''
	main = main.replace('''STUDENTNAME''',f'{student.name}')
	body = ''''''
	for session in sessions:
		RATE = session.rate
		DATE = session.datetime
		DURATION = session.duration
		line = f'''\\hourrow{{{DATE}}}{{{DURATION}}}{{{RATE}}}
'''
		body = str(body + line)
	return main.replace('''SESSIONS''',body)