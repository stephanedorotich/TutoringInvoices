# invoices.py
from dataclasses import dataclass
from datetime import date

validPaymentTypes = ['e-transfer', 'cash', 'cheque']

@dataclass
class Payment():
	"""
	A class that represents payment for services.

	Attributes
	----------
	key : int
		a unique identifier for the payment
	paymentType : str
		The type of the payment. Must be one of validPaymentTypes
	date : date
		The date the payment was acknowledged.
	amount : float
		The amount of the payment
	studentName : str
		The name of the student for whom the payment is made
	invoiceNumber : int
		The number of the invoice this payment is related to
	"""
	key: int
	paymentType: str
	date: date
	amount: float
	studentName: str
	invoiceNumber: int
