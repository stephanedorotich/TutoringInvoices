# ui.py
import sys, os
import exceptions as ex
import ui_service as use
import ui_operations

class ui_app():
	# MENUS
	def mainMenu(self):
		name = "MAIN MENU"
		options = [
			'students',
			'sessions',
			'invoices',
			'analysis']
		choice = use.menuDisplay(name, options)
		if choice == 1:
			self.studentMenu()
		if choice == 2:
			self.sessionMenu()
		if choice == 3:
			self.invoiceMenu()
		if choice == 4:
			self.analysisMenu()

	def studentMenu(self):
		name = "STUDENT MENU"
		options = [
			'Add New',
			'View All',
			'View Student']
		choice = use.menuDisplay(name, options)
		if choice == 1:
			self._uop.new_student()
		if choice == 2:
			self._uop.view_all_students()
		if choice == 3:
			self._uop.view_single_student()

	def sessionMenu(self):
		name = "SESSION MENU"
		options = [
			'Add New',
			'View All',
			'View by Student']
		choice = use.menuDisplay(name, options)
		if choice == 1:
			self._uop.new_session()
		if choice == 2:
			self._uop.view_all_sessions()
		if choice == 3:
			self._uop.view_sessions_by_student()

	def invoiceMenu(self):
		name = "INVOICE MENU"
		options = [
			'Add New',
			'View All',
			'View by Student',
			'Generate Monthly Invoices',
			'Print Invoice by Student',
			'Print Invoices by Month',
			'Pay Invoice']
		choice = use.menuDisplay(name, options)
		if choice == 1:
			self._uop.new_invoice_for_student()
		if choice == 2:
			self._uop.view_all_invoices()
		if choice == 3:
			self._uop.view_student_invoices()
		if choice == 4:
			self._uop.generate_monthly_invoices()
		if choice == 5:
			self._uop.print_student_invoice()
		if choice == 6:
			self._uop.print_monthly_invoices()
		if choice == 7:
			self._uop.pay_invoice()

	def analysisMenu(self):
		name = "ANALYSIS MENU"
		options = [
			'Total Income',
			'Monthly Incomes']
		choice = use.menuDisplay(name, options)
		if choice == 1:
			self._uop.get_total_income()
		if choice == 2:
			self._uop.get_monthly_income()

	def quit(self):
		self._uop.save()
		sys.exit()

	def run(self):
		self._uop = ui_operations.ui_operations()
		self._uop.load()
		while True:
			try:
				self.mainMenu()
			except ex.GoToMain:
				continue
			except ex.Quit:
				self.quit()
			except NotImplementedError as e:
				print(e)
				continue

if __name__ == "__main__":
	app = ui_app()
	app.run()