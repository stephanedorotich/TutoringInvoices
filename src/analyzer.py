# analyzer.py
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

def getIncomeByMonth(sessions,invoices):
	print()
	monthlyIncomes = {}
	yearlyIncomes = {}
	for session in sessions:
		month = session.datetime.month
		year = session.datetime.year
		if not year in monthlyIncomes:
			monthlyIncomes[year] = {}
		if not month in monthlyIncomes[year]:
			monthlyIncomes[year][month] = [0,0,0,0]
		if not year in yearlyIncomes:
			yearlyIncomes[year] = [0,0,0,0]
		yearlyIncomes[year][0] += session.duration * session.rate
		yearlyIncomes[year][2] += session.duration
		yearlyIncomes[year][3] += 1
		monthlyIncomes[year][month][0] += session.duration * session.rate
		monthlyIncomes[year][month][2] += session.duration
		monthlyIncomes[year][month][3] += 1
	for invoice in invoices:
		month = invoice.billingPeriod[0].month
		year = invoice.billingPeriod[0].year
		yearlyIncomes[year][1] += invoice.totalPaid
		monthlyIncomes[year][month][1] += invoice.totalPaid
	for year in [*monthlyIncomes]:
		print(year)
		for month in [*monthlyIncomes[year]]:
			print(f'\t{calendar.month_abbr[month]}:\t{monthlyIncomes[year][month]}')
		print(f'Total:\t\t{yearlyIncomes[year]}\n')
