import pytest
import sessionManager as xm
import Student
import Session
from datetime import datetime

@pytest.fixture
def setup_and_teardown():
    session = make_session(1)
    yield session
    teardown()

def make_session(key):
    session = Session.Session(key)
    session.student = ""
    session.datetime = datetime(2022, 10, 7, 11, 11)
    session.duration = 1.25
    session.subject = "MATH20"
    session.rate = 60
    session.invoiceKey = 0
    return session

def teardown():
    xm.sessions.clear()

def test_insert_new_session(setup_and_teardown):
    student = Student.Student()
    student.sessions = []
    tSession = xm.insert_new_session(
        student,
        datetime(2022, 10, 7, 11, 11),
        1.25,
        "MATH20",
        60)
    assert tSession == setup_and_teardown

def test_insert_new_session_student_sessions_updated(setup_and_teardown):
    student = Student.Student()
    student.sessions = []
    tSession = xm.insert_new_session(
        student, datetime(2022, 10, 7, 11, 11), 1.25,
        "MATH20", 60)
    sessionKey = xm.sessions[0].key
    assert student.sessions[0] == sessionKey

def test_findSessions_found(setup_and_teardown):
    xm.sessions.append(make_session(2))
    xm.sessions.append(make_session(3))
    xm.sessions.append(make_session(4))
    assert xm.findSessions([2])[0] == xm.sessions[1]

def test_findSessions_found(setup_and_teardown):
    xm.sessions.append(make_session(1))
    xm.sessions.append(make_session(2))
    xm.sessions.append(make_session(3))
    with pytest.raises(ValueError):
        xm.findSessions([13,12])