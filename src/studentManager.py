# studentManager.py
import sys
import csv
import Student
import helpers as h
import uihelpers as uih

students = []

def loadStudents(filename = 'data/students.csv'):
	"""Reads the csv file and generates a list of Student objects

	For every row in the csv file, generate a Student object with the attributes specified in the row and append it to the 'students' list

	When 'students' has been populated, updates the Minimum_Search_Query_Length (the # of chars necessary for a search of the students to yield a unique result)

	Args:
		filename (str): the filename to load (default is 'students.csv')

	Returns:
		None
	"""
	try:
		with open(filename, 'r') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
			for row in csv_reader:
				if len(row) != 0:
					try:
						student = Student.Student(
							name = row[0],
							sPhoneNum = row[1],
							sEmail = row[2],
							pName = row[3],
							pPhoneNum = row[4],
							pEmail = row[5],
							pAddress = row[6],
							rate = h.importIntegerFromString(row[7]),
							invoices = h.importListFromString(row[8]),
							sessions = h.importListFromString(row[9]),
							payments = h.importListFromString(row[10]))
						students.append(student)
					except ValueError as e:
						print(f'Error in line {csv_reader.line_num} of {filename}\n')
						raise e
	except FileNotFoundError:
		print(f'File({filename}) does not exist')

def saveStudents(filename = 'data/students.csv'):
	"""Saves all Student objects in students to a csv file with given filename

	Args:
		filename (str): the destination to save sessions (default is students.csv)

	Returns:
		None
	"""
	with open(filename, 'w') as csv_file:
		writer = csv.writer(csv_file, delimiter=',', quotechar = '"', quoting =csv.QUOTE_MINIMAL)
		for student in students:
			writer.writerow(exportStudent(student))

def exportStudent(s):
	"""Given a Student, returns a list of its attributes.

	Args:
		s (Student): the Student whose attributes are to be exported as a list

	Returns:
		list: a list of s's attributes
	"""	
	return [s.name, s.sPhoneNum, s.sEmail, s.pName, s.pPhoneNum, s.pEmail, s.pAddress, s.rate, s.invoices, s.sessions, s.payments]

def printEmailList():
	i = 0;
	print("Student Email List:")
	for s in students:
		if not s.sEmail == "":
			i+=1
			print(f'{s.sEmail}; ', end = '')

	print("\nParent Email List:")
	for s in students:
		if not s.pEmail == "":
			i+=1
			print(f'{s.pEmail}; ', end = '')
	print(f'\n\n{i} emails on file')

def findStudent(name):
	"""Given a name (str) search query, returns the corresponding Student. Raises a ValueError if the search query is not at least the length of the MINIMUM_SEARCH_QUERY_LENGTH

	Args:
		name (str): a name fragment to search students for (can be an entire name, but expected to be just a few chars)
	
	Raises:
		ValueError

	Returns:
		Student: the student that matches the given search query
	"""
	results = []
	for s in students:
		if name.lower() in s.name.lower():
			results.append(s)
	if not results:
		raise ValueError(f'There is no student that matches the query: {name}')
	if len(results) == 1:
		return results[0]
	else:
		print(f'There are multiple students who match the query: {name}')
		return results[uih.menuDisplay(None,[s.name for s in results])-1]

def newStudentUI():
	"""Guides the user through the creation of a new Student object

	1. Prompts the user to input the values of a Student's attributes. These values are validated and the Student's attributes are set to them.

	2. Displays the created Student and asks the user if they want to save the Student. If YES, this Student is appended to the 'students' list to be saved when the program Quits.

	# INTERFACE
	"""
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
	student.invoices = []
	student.sessions = []
	student.payments = []
	if x == 'y' or x == '':
		students.append(student)
		print("Student saved...\n")

def editStudentUI():
	"""Guides the user through the editing of a Student

	1. Prompts the user to pick a student 'to edit'

	2. Prompts the user to input a value for any attribute they wish to edit.

	3. Displays the edits proposed by the user, and asks the user to confirm that they would like to save these edits. If YES, all the Student's attributes are updated to the new values. If NO, no changes are saved.

	# INTERFACE
	"""
	fields = [*Student.__annotations__][:-2]
	# last 2 fields of Student are omited so user cannot edit 'sessions' or 'invoices'
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

def pickStudent(op):
	"""Prompts the user to select a Student on which to perform the given operation (op).

	Args:
		op (str): A message for the user to indicate what operation the Student is being selected for.

	Returns:
		Student: The student selected by the user

	# INTERFACE
	"""
	while True:
		userInput = uih.listener(input(f'Which Student would you like {op}? '))
		try:
			student = findStudent(userInput)
		except ValueError as e:
			print(e)
			continue
		if uih.doubleCheck(student.name):
			return student	

def viewStudentUI():
	"""Guides the user through the selection of a Student to view

	1. Prompts the user to select a Student 'to view'

	2. Prints out the selected Student's Attributes

	# INTERFACE
	"""
	student = pickStudent("to view")
	uih.printItem(student)

def addSessionKey(student,key):
	"""Adds the given Session Key to the given Student's Session Keys

	Args:
		student (Student): the student to add the given Session Key to
		key (int): the Session Key to add to the given Student
	"""
	if student.sessions:
		student.sessions.append(key)
	else:
		student.sessions = [key]

def changeAttribute(self,attributeName,newValue):
	"""Given a Student and attributeName, sets the value of that attribute to the new Value.

	Args:
		self (Student): A Student to be modified
		attributeName (str): The name of the attribute to modify
		newValue (str): The new value to set the attribute to
	"""
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