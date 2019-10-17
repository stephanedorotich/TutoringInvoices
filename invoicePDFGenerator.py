# invoicePDFGenerator.py
import os,glob,subprocess,shutil
import invoiceManager as im
import sessionManager as xm
import studentManager as sm

def generatePDF(invoice):
	student = sm.findStudent(invoice.student)[0]
	sessions = xm.findSessions(invoice.sessions)
	filename = f'invoice{invoice.key}'


	header = r'''\documentclass{invoice}
	\def \tab {\hspace*{3ex}}
	\begin {document}

	\hfil{\Huge\bf SD Tutoring}\hfil
	\bigskip\break
	\hrule

	10 West Beynon Rise \hfill 587-434-7693 \\
	Cochrane, AB \hfill stephanedorotich@gmail.com \\
	\hrule
	{\bf Invoice To:} \hfill {\bf Date:} INVOICEDATE \\
	NAME PHONENUM EMAIL ADDRESS \\
	'''
	header = fillHeader(header, student, invoice)

	footer = r'''
	Payable by: cash, cheque, or e-transfer
	\end{document}'''


	main = '''\\begin{invoiceTable}
	\\feetype{Tutoring Services}
	SESSION\\end{invoiceTable}
	'''
	main = fillMain(main, student, sessions)

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

	if len(student.pPhoneNum) == 0:
		PHONENUM = student.sPhoneNum
	else:
		PHONENUM = student.pPhoneNum

	if len(student.pEmail) == 0:
		EMAIL = student.sEmail
	else:
		EMAIL = student.pEmail

	if len(student.pAddress) == 0:
		ADDRESS = ''
	else:
		ADDRESS = student.pAddress

	temp = r'''\tab NAME \\'''
	header = header.replace("NAME",temp.replace("NAME",NAME))

	if not len(PHONENUM) == 0:
		temp = r'''\tab PHONENUM \\'''
		header = header.replace("PHONENUM",temp.replace("PHONENUM",PHONENUM))
	else:
		header = header.replace("PHONENUM",'')

	if not len(EMAIL) == 0:
		temp = r'''\tab EMAIL \\'''
		header = header.replace("EMAIL",temp.replace("EMAIL",EMAIL))
	else:
		header = header.replace("EMAIL",'')

	if not len(ADDRESS) == 0:
		temp = r'''\tab ADDRESS \\'''
		header = header.replace("ADDRESS",temp.replace("ADDRESS",ADDRESS))
	else:
		header = header.replace("ADDRESS",'')

	header = header.replace("INVOICEDATE",str(invoice.date))
	return header

def fillMain(main,student,sessions):
	body = ''''''
	RATE = student.rate
	for session in sessions:
		DATE = sessions[0].datetime
		DURATION = sessions[0].duration
		line = f'\\\\hourrow{DATE}{DURATION}{RATE}'
		print(line)
		body+=line
	print(main)
	main = main.replace("SESSSION",body)
	print(main)
	return main

