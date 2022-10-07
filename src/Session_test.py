import pytest
import sessionManager as xm
import Student
import Session
from datetime import datetime

def test_insert_new_session():
    student = Student.Student()
    student.sessions = []
    tSession = xm.insert_new_session(
        student,
        datetime(2022, 10, 7, 11, 11),
        1.25,
        "MATH20",
        60)
    
    eSession = Session.Session(1)
    eSession.student = student.name
    eSession.datetime = datetime(2022, 10, 7, 11, 11)
    eSession.duration = 1.25
    eSession.subject = "MATH20"
    eSession.rate = 60
    eSession.invoiceKey = 0

    assert tSession == eSession

def test_insert_new_session_student_updated():
    student = Student.Student()
    student.sessions = []
    tSession = xm.insert_new_session(
        student, datetime(2022, 10, 7, 11, 11), 1.25,
        "MATH20", 60)
    assert len(student.sessions) == 1
