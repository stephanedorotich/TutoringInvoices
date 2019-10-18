# students.py
from dataclasses import dataclass

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
				self.rate = int(newValue)