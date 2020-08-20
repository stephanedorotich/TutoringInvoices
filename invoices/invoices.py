# invoices.py
from dataclasses import dataclass
from datetime import date

@dataclass
class Invoice:
	"""
	A class that represents a Tutoring Invoice

	Includes the student's name, when the invoice was created, a list of session keys, and whether or not it has been printed as a pdf.

	Attributes
	----------
	key : int
		a unique identifier for the invoice
	student : str
		the student's name > 'First Last'
	date : date
		the date when the invoice was generated > YYYY-MM-DD
	billingMonth : date
		the first day of the invoice's billing month
	sessions : list
		a list of session keys that belong to this invoice
	printed : bool
		if True, the invoice has been printed as a PDF document
	"""
	key: int
	student: str = ''
	billingPeriod: date = (date.today(), date.today())
	sessions: list = None
	payments: list = None
	total: float = 0
	totalPaid: float = 0