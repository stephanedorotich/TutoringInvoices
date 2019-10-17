# sessionManager.py
import sys
sys.path.insert(0, '../')
import csv
from datetime import datetime
from .sessions import Session
import helpers as h

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
					invoiced = h.importBooleanFromString(row[5]))
				sessions.append(session)
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

def addNewSession(student,datetime,duration):
	key = 0
	if not sessions:
		key = 0
	else:
		key = (sessions[-1].key) + 1
	session = Session(key,student,datetime,duration)
	sessions.append(session)
	return key


