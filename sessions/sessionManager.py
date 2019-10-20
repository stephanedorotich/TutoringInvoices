# sessionManager.py
import sys
sys.path.insert(0, '../')
import csv
from datetime import datetime, date, timedelta
from .sessions import Session
from students import studentManager as sm
import helpers as h
import uihelpers as uih

sessions = []
sessionKey = 0

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
					invoiced = h.importBooleanFromString(row[5]))
				sessions.append(session)
			global sessionKey
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
	return [s.key, s.student, s.datetime, s.duration, s.subject, s.invoiced]

def findSession(key):
	try:
		results = h.findSingle(sessions,key)
		return results
	except ValueError as e:
		print(e)

def findSessions(keys):
	try:
		results = h.findMultiple(sessions,keys)
		return results
	except ValueError as e:
		print(e)

def newSessionUI():
	fields = [*Session.__annotations__][1:-1]
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
			if uih.doubleCheck(userinput):
				try:
					changeAttribute(session,f,userinput)
					break
				except ValueError as e:
					print(e)
			else:
				continue
	print('''
******************************
SESSION GENERATED SUCCESSFULLY
******************************''')
	uih.printItem(session)
	print('******************************\n******************************\n')
	x = uih.getChoice('Would you like to save this Session?',uih.yn)
	if x == 'y' or x == '':
		sessions.append(session)
		sm.addSessionKey(student,session.key)
		print("Session saved...\n")

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

def newSession():
	global sessionKey
	sessionKey+=1
	return Session(sessionKey)


