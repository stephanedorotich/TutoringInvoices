import ui_service as use
import studentManager as sm
from Student import Student

# ==================================== #
#||         Student Services
def new_student():
	"""
	Prompts the user to input a Student's details
	Validates that an integer was entered for rate, the rest are strings.
	"""
	fields = [*Student.__annotations__][:-3]
	res = {}

	for f in fields:
		while True:
			if f == "rate":
				res[f] = use.get_integer_input("Please enter their rate")
			else:
				res[f] = use.get_input(f'Please enter their {f}: ')
			if use.doubleCheck(res[f]):
				break
	student = sm.insert_new_student(res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7])
	print("******************************")
	print("      NEW STUDENT ADDED       ")
	print("******************************")
	use.printItem(student)
	print("******************************")

def pick_student():
	"""
	Prompts the user to select a student
	"""
	while True:
		name = use.get_input(f'Please select a student: ')
		results = []
		for s in sm.students:
			if name.lower() in s.name.lower():
				results.append(s)
		if not results:
			print(f'There is no student matching: {name}')
			continue
		if len(results) == 1:
			student = results[0]
		else:
			student = results[use.menuDisplay(f'Multiple students match the query <{name}>',[s.name for s in results])-1]
		if use.doubleCheck(student.name):
			return student
		else:
			continue

def view_all_students():
    use.printItems(sm.students)

def view_single_student():
	use.printItem(pick_student())
# ==================================== #



# ==================================== #
#||         Session Services

# ==================================== #



# ==================================== #
#||         Invoice Services

# ==================================== #