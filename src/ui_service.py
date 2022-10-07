import dataclasses as dataclass
import datetime as datetime
import exceptions as ex

# ==================================== #
#||          Input Services
def listener(userinput):
    if userinput == 'Q':
        raise ex.Quit
    elif userinput == 'MAIN':
        raise ex.GoToMain
    else:
        return userinput

def get_input(prompt : str) -> str:
    return listener(input(prompt))

def get_integer_input(prompt : str) -> int:
    while True:
        try:
            return h.importIntegerFromString(get_input(prompt))
        except ValueError as e:
            print(e)
            continue

def get_datetime_input(prompt : str) -> datetime:
    while True:
        try:
            return h.importDateTimeFromString(get_input(prompt))
        except ValueError as e:
            print(e)
            continue

def get_float_input(prompt : str) -> float:
    while True:
        try:
            return h.importDateTimeFromString(get_input(prompt))
        except ValueError as e:
            print(e)
            continue

def validateChoice(userinput,choices):
    for choice in choices:
        try:
            if userinput.lower() in choice:
                return choice.lower()
        except TypeError:
            if int(userinput) == choice:
                return choice
    else:
        raise ValueError(f'\"{userinput}\" is not one of the options: {choices}\n')

def getChoice(query,choices):
    prompt = f'{query} >> '
    while True:
        userinput = get_input(prompt)
        try:
            return validateChoice(userinput,choices)
        except ValueError as e:
            print(e)

def doubleCheck(userinput):
    # if userinput was '\n' then does not ask for confirmation
    if userinput == '':
        return True
    query = f'Is \"{userinput}\" correct?'
    options = ['y','n','']
    choice = getChoice(query,options)
    if choice == options[0] or choice == '':
        return True
# ==================================== #



# ==================================== #
#||         Display Services
def menuDisplay(name, options):
    prompt = f'\n{name}:\t\t(Q: quit)\nSelect one of the following:'
    for n in range(len(options)):
        prompt+=f'\n\t{n+1}. {options[n]}'
    choices = [str(n+1) for n in range(len(options))]
    return int(getChoice(prompt, choices))

# printItems:
# Takes a list of Students, Sessions, or Invoices (any kind of dataclass)
# and prints them out individually
def printItems(items):
    if not len(items) == 0:
        output = ''
        itemKeys = [*items[0].__annotations__]
        totalItems = len(items)
        for n in range(totalItems):
            printItem(items[n], n+1, totalItems)

# printItem:
# Prints out a dataclass. Starts with dataclass name, followed by all of its fields
def printItem(item, itemNum = 1, totalItems = 1):
    itemKeys = [*item.__annotations__]
    itemType = f'{str(type(item)).split(".")[-1][:-2]}'
    itemAsDict = dataclass.asdict(item)
    output=f'\n{itemType} ({itemNum}/{totalItems}):\n'
    for key in itemKeys:
        output+=f'\t{key}: {itemAsDict[key]}\n'
    print(output[:-1])
# ==================================== #
