# sessionManager.py
import sys
import csv
from datetime import datetime, date, timedelta
import Session
import studentManager as sm
import helpers as h
import ui

sessionKey = 0
sessions = []

def loadSessions(filename = 'data/sessions.csv'):
	"""Reads the csv file and generates a list of Session objects

	For every row in the csv file, generate a Session object with the attributes specified in the row and appends it to the 'sessions' list

	Args:
		filename (str): the filename to load (default is sessions.csv)
	
	Returns:
		None
	"""
	try:
		with open(filename, 'r') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
			for row in csv_reader:
				if len(row) != 0:
					try:
						session = Session.Session(
							key = h.importIntegerFromString(row[0]),
							student = row[1],
							datetime = h.importDateTimeFromString(row[2]),
							duration = h.importFloatFromString(row[3]),
							subject = row[4],
							rate = h.importFloatFromString(row[5]),
							invoiceKey = h.importIntegerFromString(row[6])
							)
						sessions.append(session)
					except ValueError as e:
						print(f'Error in line {csv_reader.line_num} of {filename}')
						print(row)
						print(e)
			global sessionKey
			if not len(sessions) == 0:
				sessionKey = sessions[-1].key
	except FileNotFoundError:
		print(f'File({filename}) does not exist')


def saveSessions(filename = 'data/	sessions.csv'):
	"""Saves all Session objects in sessions to a csv file with given filename

	Args:
		filename (str): the destination to save sessions (default is sessions.csv)

	Returns:
		None
	"""
	with open(filename, 'w') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for session in sessions:
			csv_writer.writerow(exportSession(session))

def exportSession(s):
	"""Given a Session, returns a list of its attributes.

	Args:
		s (Session): the Session whose attributes are to be exported as a list

	Returns:
		list: a list of s's attributes
	"""
	return [s.key, s.student, s.datetime, s.duration, s.subject, s.rate, s.invoiceKey]

def findSession(key):
	"""Given a key, returns the Session which belongs to that key. Catches a ValueError in the case where multiple Sessions exist with the given key, or no Sessions exist with the given key.

	Args:
		key (int): A positive integer to search the sessions for

	Returns:
		Session: The session matching the given key
	"""
	try:
		result = h.findSingle(sessions,key)
		return result
	except ValueError as e:
		print(e)

def findSessions(keys):
	"""Given a list of keys, returns a list of sessions corresponding to the list of keys. Catches a ValueError in the case where there are no sessions, or where no sessions correspond to any of the given keys

	Args:
		keys (list): A list of positive integers to search the sessions for

	Returns:
		list (Session): A list of sessions corresponding to the list of keys
	"""
	try:
		results = h.findMultiple(sessions,keys)
		return results
	except ValueError as e:
		print(e)

def newSessionUI():
	"""Guides the user through the creation of a new Session object.

	1. Prompts the user to input values for each of a Session's attributes. These values are validated and the Session's attributes are set to them.

	2. Displays the created Session and asks the user if they want to save the Session. If YES, this Session's Key is added to the Student's Session Keys, and this Session is appended to the 'sessions' list to be saved when the program quits. If NO, this Session is set to None, the global sessionKey is decremented.

	3. The user is asked if they would like to input another Session. If YES, this method recurs.

	# INTERFACE
	"""
	fields = [*Session.__annotations__][1:-1]
	session = newSession()
	for f in fields:
		while True:
			userinput = ui.get_inpute(f'Please enter the {f}: ')

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
			if f == 'rate':
				if userinput == '':
					userinput = student.rate	
			if f == 'invoiceKey':
				break

			if ui.doubleCheck(userinput):
				if f == 'duration' and userinput == '':
					break
				try:
					changeAttribute(session,f,userinput)
					break
				except ValueError as e:
					print(e)
					continue
			else: continue
	print('''
******************************
SESSION GENERATED SUCCESSFULLY
******************************''')
	ui.printItem(session)
	print('******************************\n')
	choice = ui.getChoice('Would you like to save this Session?',ui.yn)
	if choice == 'y' or choice == '':
		sessions.append(session)
		sm.addSessionKey(student,session.key)
		print("Session saved...")
	if choice == 'n':
		global sessionKey
		sessionKey-=1
		session = None
	choice = ui.getChoice('Would you like to input another Session?', ui.yn)
	if choice == 'y' or choice == '':
		newSessionUI()

def getSessionsByStudent(student):
	"""Prompts the user to select a student that they would like to view the sessions of. Returns a list of the sessions belonging to that student.

	Returns:
		list (Session): A list of sessions belonging to the student selected
	"""
	return findSessions(student.sessions)

def changeAttribute(self,attributeName,newValue):
	"""Given a Session and attributeName, sets the value of that attribute to the new Value.

	Args:
		self (Session): A session to be modify
		attributeName (str): The name of the attribute to modify
		newValue (str): The new value to set the attribute to
	"""
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
		self.rate = h.importIntegerFromString(newValue)
	elif attributeName == switch[6]:
		self.invoiceKey = h.importIntegerFromString(newValue)

def newSession():
	"""Returns a new Session object with a unique Key.

	Returns:
		Session: a new Session object, all attributes are set to default values except for the Key which is a unique integer.
	"""
	global sessionKey
	sessionKey+=1
	return Session(sessionKey)


