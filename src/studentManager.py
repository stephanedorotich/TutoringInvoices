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
	global students
	students.append(student)
	return student

def findStudent(name):
	try:
		result = h.findSingle(students,name)
		return result
	except ValueError as e:
		print(e)