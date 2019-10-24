# sessionManager.py
import sys
sys.path.insert(0, '../')
import csv
from datetime import datetime, date, timedelta
from .sessions import Session
from students import studentManager as sm
import helpers as h
import uihelpers as uih

sessionKey = 0
sessions = []

def loadSessions(destination = 'sessions'):
	filename = f'{destination}.csv'
	try:
		with open(filename, 'r') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
			for row in csv_reader:
				session = Session(
					key = h.importIntegerFromString(row[0]),
					student = row[1],
					datetime = h.importDateTimeFromString(row[2]),
					duration = h.importFloatFromString(row[3]),
					subject = row[4],
					paid = h.importBooleanFromString(row[5]),
					paymentType = row[6])
				sessions.append(session)
			global sessionKey
			if not len(sessions) == 0:
				sessionKey = sessions[-1].key
	except FileNotFoundError:
		print(f'File({filename}) does not exist')

def saveSessions(destination = 'sessions'):
	filename = f'{destination}.csv'
	with open(filename, 'w') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for session in sessions:
			csv_writer.writerow(exportSession(session))

def exportSession(s):
	return [s.key, s.student, s.datetime, s.duration, s.subject, s.paid, s.paymentType]

def findSession(key):
	try:
		result = h.findSingle(sessions,key)
		return result
	except ValueError as e:
		print(e)

def findSessions(keys):
	results = h.findMultiple(sessions,keys)
	return results

# >> gonna have to move to a new file
def newSessionUI():
	fields = [*Session.__annotations__][1:]
	session = newSession()
	done = False
	for f in fields:
		while not done:
			userinput = uih.listener(input(f'Please enter the {f}: '))
			if f == 'student':
				try:
					student = sm.findStudent(userinput)
					userinput = student.name
				except ValueError as e:
					print(e)
					continue
			if f == 'datetime':
				if 'today' in userinput:
					userinput = userinput.replace('today',str(date.today()))
				if 'yesterday' in userinput:
					userinput = userinput.replace('yesterday',date.strftime(date.today() - timedelta(1), '%Y-%m-%d'))
			if f == 'paid':
				if userinput == '' or userinput == 'y':
					userinput = 'True'
				if userinput == 'n':
					userinput = 'False'
			if uih.doubleCheck(userinput):
				if f == 'duration' and userinput == '':
					break
				try:
					changeAttribute(session,f,userinput)
					break
				except ValueError as e:
					print(e)
					continue
	print('''
******************************
SESSION GENERATED SUCCESSFULLY
******************************''')
	uih.printItem(session)
	print('******************************\n******************************\n')
	choice = uih.getChoice('Would you like to save this Session?',uih.yn)
	if choice == 'y' or choice == '':
		sessions.append(session)
		sm.addSessionKey(student,session.key)
		print("Session saved...")
	choice = uih.getChoice('Would you like to input another Session?', uih.yn)
	if choice == 'y' or choice == '':
		newSessionUI()

def changeAttribute(self,attributeName,newValue):
	switch = [*Session.__annotations__]
	if attributeName == switch[1]:
		self.student = newValue
	elif attributeName == switch[2]:
		self.datetime = h.importDateTimeFromString(newValue)
	elif attributeName == switch[3]:
		self.duration = h.importFloatFromString(newValue)
	elif attributeName == switch[4]:
		self.subject = newValue.upper()
	elif attributeName == switch[5]:
		self.paid = h.importBooleanFromString(newValue)
	elif attributeName == switch[6]:
		self.paymentType = newValue

def newSession():
	global sessionKey
	sessionKey+=1
	return Session(sessionKey)


