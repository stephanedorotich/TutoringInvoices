# helpers.py
from datetime import datetime
import dataclasses

def findSingle(items,key):
	if items:
		results = []
		itemType = f'{type(items[0])}'.split(' ')[-1].split('.')[-1].replace("'",'').replace('>','')
		itemKeyName = [*items[0].__annotations__][0]
		for n in range(len(items)):
			item = dataclasses.asdict(items[n])
			if item[itemKeyName] == key:
				results.append(items[n])
		if not results:
			raise ValueError(f'There are no {itemType}s with this key: "{key}"')
		elif len(results) == 1:
			return results
		else:
			raise ValueError(f'There are multiple {itemType}s that share this key: {key}')
	else:
		raise ValueError(f'There are no items to search')

def findMultiple(items,keys):
	if items:
		results = []
		itemType = f'{type(items[0])}'.split(' ')[-1].split('.')[-1].replace("'",'').replace('>','')
		itemKeyName = [*items[0].__annotations__][0]
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
	try:
		if val == "True":
			return True
		elif val == "False":
			return False
	except ValueError: raise VaueError(f'Value: {val} is not a Boolean')

def importDateTimeFromString(val):
	try:
		return datetime.fromisoformat(val)
	except ValueError: raise ValueError(f'Value: {val} is not an ISO format Datetime')

def importFloatFromString(val):
	try:
		return float(val)
	except ValueError: raise ValueError(f'Value: {val} is not a Float')

def importIntegerFromString(val):
	try:
		return int(val)
	except ValueError: raise ValueError(f'Value: {val} is not an Integer')

def importListFromString(val):
	try:
		temp = val[1:len(val)-1]
		vals = []
		if not len(temp) == 0:
			for n in temp.split(','):
				vals.append(int(n))
		return vals
	except ValueError: raise ValueError(f'Value: {val} be parsed into a list of Integers')

def prettyPrint(items):
	if items:
		output = ''
		itemKeys = [*items[0].__annotations__]
		for n in range(len(items)):
			itemType = f'{type(items[0])}'.split(' ')[-1].split('.')[-1][:-2]
			output+=f'\n{itemType} ({n+1}/{len(items)}):\n'
			item = dataclasses.asdict(items[n])
			for key in itemKeys:
				output+=f'\t{key}: {item[key]}\n'
		print(output)

