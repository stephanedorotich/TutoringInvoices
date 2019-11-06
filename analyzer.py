# analyzer.py
import sessions.sessionManager as xm
import students.studentManager as sm
import invoices.invoiceManager as im
import uihelpers as uih

def getTotalIncome(sessions):
	total = 0
	for session in sessions:
		if session.paid:
			total += session.duration * sm.findStudent(session.student).rate
	print(f'Total Income: {total}')