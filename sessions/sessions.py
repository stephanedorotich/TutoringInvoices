# sessions.py
from dataclasses import dataclass
from datetime import datetime
import helpers as h

@dataclass
class Session:
	key: int
	student: str = ''
	datetime: datetime = None
	duration: float = 1.0
	subject: str = ''
	paid: bool = False
	paymentType: str = ''