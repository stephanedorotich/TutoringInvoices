# students.py
from dataclasses import dataclass
import helpers as h

@dataclass
class Student:
	"""
	A class that represents a Tutoring Student

	Includes the contact information of a student, what rate I charge them, a list of session keys and invoice keys that belong to the student.

	Attributes
	----------
	name : str
		the student's name > 'First Last'
	sPhoneNum : str
		the student's phone number
	sEmail : str
		the student's e-mail address
	pName : str
		the student's parent's name
	pPhoneNum : str
		the parent's phone number
	pEmail : str
		the parent's e-mail address
	pAddress : str
		the billing address
	rate : int
		the student's rate per hour of tutoring
	invoices : list
		a list of invoice keys that belong to the student
	sessions : list
		a list of session keys that belong to the student
	"""
	name: str = ''
	sPhoneNum: str = ''
	sEmail: str = ''
	pName: str = ''
	pPhoneNum: str = ''
	pEmail: str = ''
	pAddress: str = ''
	rate: int = 0
	invoices: list = None
	sessions: list = None