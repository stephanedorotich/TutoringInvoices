# invoices.py
from dataclasses import dataclass
from datetime import date

@dataclass
class Invoice:
	key: int
	student: str = ''
	date: date = date.today()
	sessions: list = None
	printed: bool = False
#	sent: bool = False