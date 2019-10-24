# studentManager.py
import sys
sys.path.insert(0, '../')
import csv
from .students import Student
import helpers as h
import uihelpers as uih
import copy

MINIMUM_SEARCH_QUERY_LENGTH = 3
students = []

def loadStudents(destination = 'students'):
	filename = f'{destination}.csv'
	try:
		with open(filename, 'r') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
			for row in csv_reader:
				student = Student(
					name = row[0],
					sPhoneNum = row[1],
					sEmail = row[2],
					pName = row[3],
					pPhoneNum = row[4],
					pEmail = row[5],
					pAddress = row[6],
					rate = h.importIntegerFromString(row[7]),
					invoices = h.importListFromString(row[8]),
					sessions = h.importListFromString(row[9]))
				students.append(student)
			updateMinimumSearchQueryLength()
	except FileNotFoundError:
		print(f'File({filename}) does not exist')

def saveStudents(destination = 'students'):
	filename = f"{destination}.csv"
	with open(filename, 'w') as csv_file:
		writer = csv.writer(csv_file, delimiter=',', quotechar = '"', quoting =csv.QUOTE_MINIMAL)
		for student in students:
			writer.writerow(exportStudent(student))

def exportStudent(s):
	return [s.name, s.sPhoneNum, s.sEmail, s.pName, s.pPhoneNum, s.pEmail, s.pAddress, s.rate, s.invoices, s.sessions]

def findStudent(name):
	if len(name) < MINIMUM_SEARCH_QUERY_LENGTH:
		raise ValueError(f'Search queries must be at least {MINIMUM_SEARCH_QUERY_LENGTH} in length')
	else:
		results = []
		for student in students:
			if name.lower() in student.name.lower():
				results.append(student)
		if not results:
			raise ValueError(f'There is no student that matches the query: {name}')
		elif len(results) == 1:
			return results[0]
		else:
			raise ValueError(f'There are multiple students that match the query: {name}')

# >> gonna have to move to a new file
def newStudentUI():
	fields = [*Student.__annotations__][:-2]
	student = Student()
	for f in fields:
		while True:
			userinput = uih.listener(input(f'Please enter their {f}: '))
			if uih.doubleCheck(userinput):
				try:
					changeAttribute(student,f,userinput)
					break
				except ValueError as e:
					print(e)
			else:
				continue
	print('''
******************************
STUDENT GENERATED SUCCESSFULLY
******************************''')
	uih.printItem(student)
	print('******************************\n******************************\n')
	x = uih.getChoice('Would you like to save this Student?',uih.yn)
	if x == 'y' or x == '':
		students.append(student)
		print("Student saved...\n")
		updateMinimumSearchQueryLength()

# >> gonna have to move to a new file
def editStudentUI():
	fields = [*Student.__annotations__][:-2]
	## so user cannot edit 'sessions' or 'invoices' (last 2 fields for a Student)
	student = pickStudent("to edit")
	edits = []
	for f in fields:
		while True:
			userinput = uih.listener(input(f'Please enter their {f}: '))
			if uih.doubleCheck(userinput):
				#### TODO WARNING! delete's field without double checking
				#### should get moved below.
				if userinput == 'delete':
					try:
						changeAttribute(student,f,'')
						break
					except ValueError as e:
						print(e)
				elif not userinput == '':
					try:
						edits.append((f,userinput))
						break
					except ValueError as e:
						print(e)
				break
			else:
				continue
#### TODO	
#### CAN DO SOME WORK HERE. MAKE THE PRINT STATEMENT MORE
#### INFORMATIVE
	print("EDITS:")
	for edit in edits:
		print(f'\t{edit[0]}: {edit[1]}')
	choice = uih.getChoice('Would you like to save these edits?',uih.yn)
	if choice == 'y' or choice == '':
		for edit in edits:
			changeAttribute(student,edit[0],edit[1])
		print('''
*******************************
  STUDENT EDITED SUCCESSFULLY
*******************************''')
		uih.printItem(student)
		print('*******************************\n*******************************\n')
	

# >> gonna have to move to a new file
def viewStudentUI():
	student = pickStudent("to view")
	uih.printItem(student)

# >> gonna have to move to a new file
def pickStudent(op):
	while True:
		userInput = uih.listener(input(f'Which Student would you like {op}? '))
		try:
			student = findStudent(userInput)
		except ValueError as e:
			print(e)
			continue
		if uih.doubleCheck(student.name):
			return student

def addSessionKey(student,key):
	student.sessions.append(key)

def updateMinimumSearchQueryLength():
	global MINIMUM_SEARCH_QUERY_LENGTH
	initial = MINIMUM_SEARCH_QUERY_LENGTH
	for student in students:
		for n in range(len(student.name)-MINIMUM_SEARCH_QUERY_LENGTH+1):
			val = student.name[n:n+MINIMUM_SEARCH_QUERY_LENGTH]
			try:
				findStudent(val)
			except ValueError as e:
				print(e)
				MINIMUM_SEARCH_QUERY_LENGTH+=1
				updateMinimumSearchQueryLength()
				break
		if initial < MINIMUM_SEARCH_QUERY_LENGTH:
			print(f'New minimum search query length is: {MINIMUM_SEARCH_QUERY_LENGTH}')
			break

def changeAttribute(self,attributeName,newValue):
	switch = [*Student.__annotations__]
	if attributeName == switch[0]:
		self.name = newValue
	elif attributeName == switch[1]:
		self.sPhoneNum = newValue
	elif attributeName == switch[2]:
		self.sEmail = newValue
	elif attributeName == switch[3]:
		self.pName = newValue
	elif attributeName == switch[4]:
		self.pPhoneNum = newValue
	elif attributeName == switch[5]:
		self.pEmail = newValue
	elif attributeName == switch[6]:
		self.pAddress = newValue
	elif attributeName == switch[7]:
		if not newValue == '':
			try:
				self.rate = h.importIntegerFromString(newValue)
			except ValueError as e:
				print('Rate could not be edited because',e)