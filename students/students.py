# students.py
from dataclasses import dataclass

@dataclass
class Student:
	name: str
	sPhoneNum: str
	sEmail: str
	pName: str
	pPhoneNum: str
	pEmail: str
	pAddress: str
	rate: int
	invoices: list
	sessions: list