# sessions.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Session:
	key: int
	student: str
	datetime: datetime
	duration: float
	subject: str
	invoiced: bool = False