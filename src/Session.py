# sessions.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Session:
	"""
	A class that represents a Tutoring Session

	Includes the student's name, when the session occured, how long it was, what subject it was, and whether or not it's been paid for.

	Attributes
	----------
	key : int
		a unique identifier for the session
	student : str
		the student's name > 'First Last'
	datetime : datetime
		the sessions date and start-time > YYYY-MM-DD HH:mm:ss
	duration : float
		the duration of the session, units are hours
	subject : str
		the subject of the session > 'MATH20' (or CHEM, PHYS, etc.)
	rate : int
		the rate per hour of the session
	invoice key : int
		what invoice this session belongs to (0 indicates none)
	"""
	key: int
	student: str = ''
	datetime: datetime = None
	duration: float = 1.0
	subject: str = ''
	rate: int = 0
	invoiceKey: int = 0