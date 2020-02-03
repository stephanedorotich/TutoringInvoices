# analyzer.py
import sessions.sessionManager as xm
import students.studentManager as sm
import invoices.invoiceManager as im
import uihelpers as uih
import calendar

def getTotalIncome(sessions):
	totalPaid = 0
	totalUnpaid = 0
	for session in sessions:
		if session.paid:
			totalPaid += session.duration * sm.findStudent(session.student).rate
		else:
			totalUnpaid += session.duration * sm.findStudent(session.student).rate

	print(f'\nTotal Income: {totalPaid}')
	print(f'Total Unpaid: {totalUnpaid}')

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
		monthlyIncomes[year][month][0] += session.duration * sm.findStudent(session.student).rate
		monthlyIncomes[year][month][1]+=1
	for year in [*monthlyIncomes]:
		print(year)
		for month in [*monthlyIncomes[year]]:
			print(f'\t{calendar.month_abbr[month]}: {monthlyIncomes[year][month]}')
