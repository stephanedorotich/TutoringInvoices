import pytest
import studentManager as sm
import Student

@pytest.fixture
def setup():
    student = make_student("Bananas")
    yield student
    teardown()

def teardown():
    sm.students.clear()

def make_student(name):
    student = Student.Student()
    student.name = name
    student.sPhoneNum = "sPhoneNum"
    student.sEmail = "sEmail"
    student.pName = "pName"
    student.pPhoneNum = "pPhoneNum"
    student.pEmail = "pEmail"
    student.pAddress = "pAddress"
    student.rate = 60
    student.invoices = []
    student.sessions = []
    student.payments = []
    sm.students.append(student)
    return student

def test_insert_new_student(setup):
    tStudent = sm.insert_new_student(
        "Bananas",
        "sPhoneNum",
        "sEmail",
        "pName",
        "pPhoneNum",
        "pEmail",
        "pAddress",
        60)
    assert tStudent == setup

def test_find_student(setup):
    assert sm.find_student("Bananas") == setup.student

def test_find_student(setup):
    with pytest.raises(ValueError):
        sm.find_student("Apples")

