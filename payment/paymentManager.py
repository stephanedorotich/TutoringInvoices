import sys
sys.path.insert(0, '../')
import csv
from .payment import Payment
import helpers as h

payments = []
validPaymentTypes = ['e-transfer', 'cash', 'cheque']

def loadPayments(filename = 'payments.csv'):
	try:
		with open(filename, 'r') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
			for row in csv_reader:
				if len(row) != 0:
					try:
						payment = Payment(
							key = h.importIntegerFromString(row[0]),
							paymentType = row[1],
							date = h.importDateFromString(row[2]),
							amount = h.importFloatFromString(row[3]),
							studentName = row[4],
							invoiceNumber = h.importIntegerFromString(row[5]))
						payments.append(payment)
					except ValueError as e:
						print(f'Error in line {csv_reader.line_num} of {filename}\n')
						raise e
	except FileNotFoundError:
		print(f'File({filename}) does not exist')

def savePayments(filename = 'payments.csv'):
	with open(filename, 'w') as csv_file:
		writer = csv.writer(csv_file, delimiter=',', quotechar = '"', quoting =csv.QUOTE_MINIMAL)
		for p in payments:
			writer.writerow([p.key, p.paymentType, p.date, p.amount, p.studentName, p.invoiceNumber])

def newPayment(paymentType, paymentDate, amount, studentName, invoiceNumber) -> int:
	paymentKey = len(payments)+1
	newPayment = Payment(paymentKey,
		paymentType,
		paymentDate,
		amount,
		studentName,
		invoiceNumber)
	payments.append(newPayment)
	return paymentKey

def isValidPaymentType(newPaymentType: str) -> bool:
	return (newPaymentType in validPaymentTypes)

def sumPayments() -> float:
	total = 0
	for p in payments:
		total += p.amount
	return total