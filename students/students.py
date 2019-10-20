# students.py
from dataclasses import dataclass
import helpers as h

@dataclass
class Student:
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