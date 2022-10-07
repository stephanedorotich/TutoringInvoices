# studentManager.py
import sys
import csv
import Student
import helpers as h
import ui

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

def insert_new_student(
		name : str, sPhoneNum : str, sEmail : str,
		pName : str, pPhoneNum : str, pEmail : str,
		pAddress : str, rate : int
		) -> Student.Student:
	student = Student.Student(name, sPhoneNum, sEmail, pName, pPhoneNum, pEmail, pAddress, rate)
	student.invoices = []
	student.sessions = []
	student.payments = []
	students.append(student)
	return student

def ui_new_student():
	"""
	Prompts the user to input a Student's details
	Validates that an integer was entered for rate, the rest are strings.
	"""
	fields = [*Student.Student.__annotations__][:-3]
	res = {}

	for f in fields:
		while True:
			if f == "rate":
				res[f] = ui.get_integer_input("Please enter their rate")
			elif:
				res[f] = ui.get_input(f'Please enter their {f}: ')
			if ui.doubleCheck(res[f]):
				break
	student = insert_new_student(res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7])
	print("******************************")
	print("      NEW STUDENT ADDED       ")
	print("******************************")
	ui.printItem(student)
	print("******************************")

def ui_pick_student():
	"""
	Prompts the user to select a student
	"""
	while True:
		name = ui.get_input(f'Please select a student: ')
		results = []
		for s in students:
			if name.lower() in s.name.lower():
				results.append(s)
		if not results:
			print(f'There is no student matching: {name}')
			continue
		if len(results) == 1:
			student = results[0]
		else:
			print(f'There are multiple students who match the query: {name}')
			student = results[ui.menuDisplay(None,[s.name for s in results])-1]
		if ui.doubleCheck(student.name):
			return student
		else:
			continue

def ui_view_student():
	"""
	1. Prompts the user to select a Student
	2. Prints out the selected Student's Attributes
	"""
	ui.printItem(ui_pick_student())
