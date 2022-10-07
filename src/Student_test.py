import pytest
import studentManager as sm
import Student

def test_insert_new_student():
    tStudent = sm.insert_new_student(
        "name",
        "sPhoneNum",
        "sEmail",
        "pName",
        "pPhoneNum",
        "pEmail",
        "pAddress",
        60)
    
    eStudent = Student.Student()
    eStudent.name = "name"
    eStudent.sPhoneNum = "sPhoneNum"
    eStudent.sEmail = "sEmail"
    eStudent.pName = "pName"
    eStudent.pPhoneNum = "pPhoneNum"
    eStudent.pEmail = "pEmail"
    eStudent.pAddress = "pAddress"
    eStudent.rate = 60
    eStudent.invoices = []
    eStudent.sessions = []
    eStudent.payments = []

    assert tStudent == eStudent
