# helpers.py
from datetime import datetime
from datetime import date
import dataclasses

def findSingle(items, key):
	"""Given a list of items, attempts to find one with the given key

	Args:
		items (list): a list of invoices, sessions, or students
		key (int or str): an integer or student_name search query

	Raises:
		ValueError: if no item matches the key, if multiple items do, or if the list of items is empty

	Returns:
		item: the invoice, student or session matching the search query
	"""
	if items:
		results = []
		itemType = f'{type(items[0])}'.split(' ')[-1].split('.')[-1].replace("'",'').replace('>','')
		# itemType yields 'student', 'session', or 'invoice'
		itemKeyName = [*items[0].__annotations__][0]
		# itemKeyName yields a list of the attributes of the given itemType
		for n in range(len(items)):
			item = dataclasses.asdict(items[n])
			if item[itemKeyName] == key:
				results.append(items[n])
		if not results:
			raise ValueError(f'There are no {itemType}s with this key: "{key}"')
		elif len(results) == 1:
			return results[0]
		else:
			raise ValueError(f'There are multiple {itemType}s that share this key: {key}')
	else:
		raise ValueError(f'There are no items to search')

def findMultiple(items, keys):
	"""Given a list of items and a list of keys, attempts to find all items that match any of the keys.

	Args:
		items (list): a list of invoices, sessions, or students
		keys (list): a list of integer or student_name search queries

	Raises:
		ValueError: if no items match any of the keys, or if items is empty

	Returns:
		list: a list of invoices, sessions, or students that match any of the keys
	"""
	if items:
		results = []
		itemType = f'{type(items[0])}'.split(' ')[-1].split('.')[-1].replace("'",'').replace('>','')
		# itemType yields 'student', 'session', or 'invoice'
		itemKeyName = [*items[0].__annotations__][0]
		# itemKeyName yields a list of the attributes of the given itemType
		for n in range(len(items)):
			item = dataclasses.asdict(items[n])
			if item[itemKeyName] in keys:
				results.append(items[n])
		if not results:
			raise ValueError(f'There are no {itemType}s with these keys: {keys}')
		else:
			return results
	else:
		raise ValueError(f'There are no items to search')

def importBooleanFromString(val):
	"""Converts a string to a boolean.
	Used when loading objects from csv files.

	Args:
		val (str): a string to be converted to a boolean

	Raises:
		ValueError: if the string cannot be converted to a boolean

	Returns:
		bool: True or False
	"""
	try:
		if val == "True":
			return True
		elif val == "False":
			return False
	except ValueError: raise ValueError(f'Value: \'{val}\' is not a Boolean')

def importDateFromString(val):
	"""Converts a string to a date, YYYY-MM-DD
	Used when loading objects from csv files.
	Used to validate user input while editing objects or creating new ones.

	Args:
		val (str): a string to be converted to a date

	Raises:
		ValueError: if the string cannot be converted to a date

	Returns:
		date: the date equivalent to the string, YYYY-MM-DD
	"""
	try:
		return date.fromisoformat(val)
	except ValueError: raise ValueError(f'Value: \'{val}\' is not an ISO format Date (YYYY-MM-DD)')

def importDateTupleFromString(val):
	try:
		dates = val.split(",")
		return (date.fromisoformat(dates[0]),date.fromisoformat(dates[1]))
	except ValueError: raise ValueError(f'Value: \'{val}\' is not an ISO format Date (YYYY-MM-DD)')

def importDateTimeFromString(val):
	"""Converts a string to a datetime, YYYY-MM-DD HH:mm:ss
	Used when loading objects from csv files.
	Used to validate user input while editing objects or creating new ones.

	Args:
		val (str): a string to be converted to a datetime

	Raises:
		ValueError: if the string cannot be converted to a datetime

	Returns:
		datetime: the datetime equivalent to the string, YYYY-MM-DD HH:mm:ss
	"""
	try:
		return datetime.fromisoformat(val)
	except ValueError: raise ValueError(f'Value: \'{val}\' is not an ISO format Datetime (YYYY-MM-DD HH:mm)')

def importFloatFromString(val):
	"""Converts a string to a float.
	Used when loading objects from csv files.
	Used to validate user input while editing objects or creating new ones.

	Args:
		val (str): a string to be converted to a float

	Raises:
		ValueError: if the string cannot be converted to a float

	Returns:
		float: the float equivalent to the string
	"""
	try:
		return float(val)
	except ValueError: raise ValueError(f'Value: \'{val}\' is not a Float')

def importIntegerFromString(val):
	"""Converts a string to an integer.
	Used when loading objects from csv files.
	Used to validate user input while editing objects or creating new ones.

	Args:
		val (str): a string to convert to an integer

	Raises:
		ValueError: if the string cannot be converted to an integer

	Returns
		int: the integer equivalent to the input
	"""
	try:
		return int(val)
	except ValueError: raise ValueError(f'Value: \'{val}\' is not an Integer')

def importListFromString(val):
	"""Converts a string to a list of integers.
	Used when loading objects from csv files.

	Args:
		val (str): a string to convert to a list of integers

	Raises:
		ValueError: if the string cannot be parsed into a list of integers

	Returns:
		list: a list of integers equivalent to the string
	"""
	if not (val[0] == '[' and val[-1] == ']'):
		print("I'm here!")
		raise ValueError(f"'{val}' cannot be parsed as a list of integers")
	try:
		temp = val[1:len(val)-1]
		vals = []
		if not len(temp) == 0:
			for n in temp.split(','):
				vals.append(int(n))
		return vals
	except ValueError:
		raise ValueError(f"'{val}' cannot be parsed as a list integers")

