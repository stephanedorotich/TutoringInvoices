# invoices.py
from dataclasses import dataclass
from datetime import date

@dataclass
class Invoice:
	key: int
	student: str
	date: date
	total: float
	sessions: list
	paid: bool
	printed: bool = False