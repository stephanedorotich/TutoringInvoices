# uihelpers.py
import sys
import dataclasses as dc
from students.students import Student
from sessions.sessions import Session
from invoices.invoices import Invoice
import sessions.sessionManager as xm
import students.studentManager as sm
import invoices.invoiceManager as im

isTest = False
yn = ['y','n','']

def exit():
	im.saveInvoices()
	sm.saveStudents()
	xm.saveSessions()
	sys.exit()

def exitTest():
	print(asString(im.invoices))
	print(asString(xm.sessions))
	print(asString(sm.students))
	sys.exit()

def listener(userinput):
	global isTest
	if userinput == 'Q':
		if isTest:
			exitTest()
		else:
			exit()
	elif userinput == 'TEST':
		isTest = True
		return userinput
	else:
		return userinput

def doubleCheck(userinput):
	if userinput == '':
		return True
	options = yn
	query = f'Is \"{userinput}\" correct? '
	choice = getChoice(query,options)
	if choice == options[0] or choice == '':
		return True

def getChoice(query,options):
	prompt = f'{query} >> '
	while True:
		userinput = listener(input(prompt))
		if userinput == 'TEST':
			userinput = listener(input())
		try:
			choice = validateUserInput(userinput,options)
			return choice
		except ValueError as e:
			print(e)

def validateUserInput(userinput,options):
	if not userinput == None:
		if userinput.lower() in options:
			return userinput.lower()
		else:
			temp = ", ".join(options)
			if temp[-1]==' ':
				temp+='enter'
			raise ValueError(f'\"{userinput}\" is not one of the options: ({temp})\n')

def asString(items):
	output = ''
	if not (type(items) == Student or type(items) == Session or type(items) == Invoice):
		itemKeys = [*items[0].__annotations__]
		for n in range(len(items)):
			itemType = f'{type(items[0])}'.split(' ')[-1].split('.')[-1][:-2]
			output+=f'{itemType} ({n+1}/{len(items)}):\n'
			item = dc.asdict(items[n])
			for key in itemKeys:
				output+=f'\t{key}: {item[key]}\n'
	else:
		itemKeys = [*items.__annotations__]
		itemType = f'\n{type(items)}'.split(' ')[-1].split('.')[-1][:-2]
		output+=f'\n{itemType}:\n'
		item = dc.asdict(items)
		for key in itemKeys:
			output+=f'\t{key}: {item[key]}\n'
	return output
