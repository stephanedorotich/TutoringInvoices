# sessionManager.py
import csv
from datetime import datetime, date
import Session
import Student
import helpers as h

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


def saveSessions(filename = 'data/sessions.csv'):
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

def insert_new_session(
		student : Student.Student, time : datetime,
		duration : float, subject : str, rate: int
		) -> Session.Session:
	# Create session
	sessionKey = len(sessions)+1
	session = Session.Session(sessionKey, student.name, time, duration, subject, rate, 0)
	sessions.append(session)
	student.sessions.append(sessionKey)
	return session

def findSessions(keys):
	return h.findMultiple(sessions,keys)
