# testStudents.py
import unittest
import students.students as students

class TestAddThis(unittest.TestCase):
	"""docstring for TestSum"""
		
	def test_add_this(self):
		self.assertEqual(students.addThis([1,3,4]), 8)

class TestSum(unittest.TestCase):
	"""docstring for TestSum"""
		
	def test_sum(self):
		self.assertEqual(sum([1, 2, 3]), 6)

	def test_sum_tuple(self):
		self.assertEqual(sum((1,2,3)), 6)

def createMe():
	s1 = Student("Stephane Dorotich",80,"587-434-7693","stephanedorotich@gmail.com"
		,"Paul Dorotich","10 West Beynon Rise, Cochrane, AB","403-921-2721"
		,"pdorotich@shaw.ca",[],[1,2])
	return s1

if __name__ == "__main__":
	unittest.main()