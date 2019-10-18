# studentManager.py
import sys
sys.path.insert(0, '../')
import csv
from .students import Student
import helpers as h
import uihelpers as uih

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

def addNewStudent(name,sPhoneNum='',sEmail='',pName='',pPhoneNum='',pEmail='',pAddress='',rate=50,sessions=[],invoices=[]):
		student = Student(name,sPhoneNum,sEmail,pName,pPhoneNum,pEmail,pAddress,rate,sessions,invoices)
		students.append(student)
		updateMinimumSearchQueryLength()

def newStudentUI():
	fields = [*Student.__annotations__][:-2]
	student = Student()
	for f in fields:
		while True:
			userinput = uih.listener(input(f'Please enter their {f}: '))
			if uih.doubleCheck(userinput):
				Student.changeAttribute(student,f,userinput)
				break
			else:
				continue		
	students.append(student)
	print('''
******************************
STUDENT GENERATED SUCCESSFULLY
******************************''')
	print(uih.asString(student))
	print('******************************\n******************************\n')

###WATCH OUT FOR THIS ONE NEEDS EXTERNAL HELP TO MAKE WORK
def addNewSessionKey(name):
	student.sessions.append(name)

def updateStudentName(student,name):
	student.name=name

def updateStudentPhoneNum(student,sPhoneNum):
	student.sPhoneNum=sPhoneNum

def updateStudentEmail(student,sEmail):
	student.sEmail=sEmail

def updateParentName(student,pName):
	student.pName=pName

def updateParentPhoneNum(student,pPhoneNum):
	student.pPhoneNum=pPhoneNum

def updateParentEmail(student,pEmail):
	student.pEmail=pEmail

def updateParentAddress(student,pAddress):
	student.pAddress=pAddress

def updateRate(student,rate):
	student.rate=rate

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
				print(f'Minimum search query length is: {MINIMUM_SEARCH_QUERY_LENGTH}')
				updateMinimumSearchQueryLength()
				break
		if initial < MINIMUM_SEARCH_QUERY_LENGTH:
			break
