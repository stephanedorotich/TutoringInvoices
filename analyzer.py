# analyzer.py
import sessions.sessionManager as xm
import students.studentManager as sm
import invoices.invoiceManager as im
import payment.paymentManager as pm
import uihelpers as uih
import calendar

def getTotalIncome(payments):
	totalCash = 0
	totalEtransfer = 0
	totalCheque = 0
	for payment in payments:
		if payment.paymentType == 'cash':
			totalCash += payment.amount
		if payment.paymentType == 'e-transfer':
			totalEtransfer += payment.amount
		if payment.paymentType == 'cheque':
			totalCheque += payment.amount

	print(f'\nTotal cash: {totalCash}')
	print(f'Total e-transfer: {totalEtransfer}')
	print(f'Total cheque: {totalCheque}')
	print(f'\nGrand Total: {totalCash + totalEtransfer + totalCheque}')

def getIncomeByMonth(sessions):
	print()
	monthlyIncomes = {}
	for session in sessions:
		month = session.datetime.month
		year = session.datetime.year
		if not year in monthlyIncomes:
			monthlyIncomes[year] = {}
		if not month in monthlyIncomes[year]:
			monthlyIncomes[year][month] = [0,0]
		monthlyIncomes[year][month][0] += session.duration * session.rate
		monthlyIncomes[year][month][1]+=1
	for year in [*monthlyIncomes]:
		print(year)
		for month in [*monthlyIncomes[year]]:
			print(f'\t{calendar.month_abbr[month]}: {monthlyIncomes[year][month]}')
