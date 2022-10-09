---
author: Stéphane Dorotich
title: Assignment 1 - Refactoring
date: Oct 7th, 2022
---

# Code Source

The original code can be found on [my personal github](https://github.com/stephanedorotich/TutoringInvoices). I use it to track my high school tutoring business. Development began in fall 2019.

The program helps me manage my Students, Sessions, and Invoices. I use it to automatically generate PDF invoices to send to my clients. 

Generating PDFs is beyond the scope of this assignment. It's fairly straightforward to set up, but requires installing LaTeX and moving a CLS style sheet to a particular directory.

# Usage

```python3 src/ui.py```

While the program is running, there are two keywords that can be used at anytime:
- `Q`: Quits the program. First saves data to `.csv` files.
- `MAIN`: Returns the user to the main menu.

# Commits

| Branch | Refactor | Commit Title | Short Hash |
| ------ |:--------:| -------------- |:-----------:|
| R4     | 4 | R4: Updating Tests | 06961de5 |
| R4     | 4 | R4: Analyzer.py absorbed into ui_operations | 1787a5cc |
| R4     | 4 | R4: Moved invoiceManager ui operations | cf2f677d |
| R4     | 4 | R4: Implemented SessionMenu operations in ui_operations.py | e5d6a0f7 |
| R4     | 4 | R4: Migrated all Student Menu options into ui_operations. | 8d9b5692 |
| R4     | 4 | R4: Created ui_services.py | 0225345e |
| master | 3 | Refactor 3: Extract methods from newSessionUI() | 60043ba5 |
| master | 3 | Refactor 3: Extract method from newStudentUI() | 8c985f18 |
| master | 2 | Refactor 2: Removing calls to mainMenu() | 40e5d594 |
| master | 2 | Refactor 2: Tests | f2b3fd32 |
| master | 2 | Refactor 2: Added global state to ui.py | ab243851 |
| master | 2 | Refactor 2: Fixing a typo | e9246cb2 |
| master | 2 | Refactor 2: Feature Envy | 8768859f |
| master | 1 | Refactor 1: Dead Code | 11b36dbd |

# Testing

All testing was done using `PyTest`. Tests can be run with the command
```
python3 -m pytest
```

`PyTest` can be installed with pip using one of the following three commands (on Linux):
- `pip install pytest`
- `pip3 install pytest`
- `python3 -m pip install pytest`


# Refactor 1

## Code Smell: Dead Code

I developed a variety of utilities for my program. Over years of continued use, these utilities were seldom used. The code was reachable and functional, but not needed.

Some truly "dead" code was located in the `run()`, pertaining to `recoveryMode` whose purpose was to safely load my `.csv` files in the event that I accidentally ran the program from Command Prompt which would insert additional newline characters to my `.csv` files and be an absolute headache to fix manually. I later updated the regular `loadX()` methods to handle this case, rendering the `recoveryMode` section "dead".

## Solution: Delete Code

The methods for these utilities were all removed. The menus from which these utilities were invoked were updated accordingly.

## Resulting Code


The following files and methods were affected.

### Commit `11b36dbd`

- `invoiceManager.py`
    - Removed: `openRecentInvoiceUI()`
- `pdfManager.py`
    - Removed: `openPDF()`
- `studentManager.py`
    - Removed: `printEmailList()`
    - Removed: `editStudentUI()`
- `ui.py`
    - Updated: `studentMenu()`
    - Updated: `invoiceMenu()`
    - Updated: `run()`

## Testing

No testing was done because the removed methods/code were only invoked from a single location in `ui.py` and so the functionality of my program was unaffected by their removal.

## Justification

Removing the `recoveryMode` section prevents potential **runtime errors**. The section invoked methods that no longer existed, which would cause a runtime error.

Removing `editStudentUI()` helps ensure the integrity of my Student data entries. The ability to edit was a big risk because the method allowed me to modify the `Session` list whose integrity is paramount to integrity of the program.

Removing `openRecentInvoiceUI()` reduced some coupling between `invoiceManager.py` and `pdfManager.py`. The pdfManager file now **exclusively** deals with generating PDFs and has no UI methods.


# Refactor 2

## Code Smell: Feature Envy 

A class called `uihelpers.py` was developed for my program. It contained methods responsible for handling user input, displaying menus and getting user choices, for listening for the keywords `Q`, `TEST`, and `MAIN`, and for terminating the program.

Each of these features is heavily used by `ui.py` and are responsible for the smooth operation of the program. They are not *helpers*, they are a core part of the user interface.

A big concern was the `listener` method, which served as the termination point of the program (it called `quit()` when `Q` was entered.) `uihelpers.py` maintained state about whether the program was in Test mode or not, and would exit the program. It is "smelly" that the methods responsible for **closing** the program are not part of the class that is responsible for **running** the program.

## Solution: Move Method

All methods and global variables from `uihelpers.py` were moved to `ui.py`. All methods in other files that called on `uihelpers` were updated so they call on `ui` instead.

A new method `get_input()` was added. It standardizes the way input is received by the program and guarantees that everything passes through the `listener()`, which updates the program state and throws a custom exception `RenewStateException` as needed.

The `run()` method in `ui.py` was updated so that it uses global state variables and the new custom exception.

## Resulting Code

The following files and methods were affected.

### Commit `8768859f`

- `uihelpers.py` content moved to `ui.py`.
    - Migrated `listener()`
    - Migrated `quit()`
    - Migrated `quitTest()`
    - Migrated `doubleCheck()`
    - Migrated `getChoice()`
    - Migrated `menuDisplay()`
    - Migrated `validateChoice()`
    - Migrated `printItems()`
    - Migrated `printItem()`
    - Migrated global vars `isTest` and `yn` (list of "y", "n", and "")
- `ui.py`
    - All instances of `uih` removed.
    - New method `get_input()` defined, it passes user input through the `listener()`.
- `pdfManager.py`
    - Unused import statement removed
- `invoiceManager.py`, `sessionManager.py`, `studentManager.py`
    - All instances of `uih` replaced with `ui`
    - 5 instances of getting user input via `listener(input(...))` replaced with new method `ui.get_input()`

### Commit `ab243851`

- `ui.py`
    - Added a new custom exception `RenewStateException` to replace the previously used `StopIteration`.
    - Changed `isRunning` from a local variable in the `run()` method to a global variable.
    - Changed `listener()` so that it sets the global `isRunning` variable to `False` if 'Q' is input.
    - Moved the calls to `quit()` and `quitTest` from `listener()` to `run()` method instead.
    - Updated `run()` method accordingly.

### Commit `f2b3fd32`

- Added `ui_test.py` (see below)

### Commit `40e5d594`

- `ui.py`
    - Removed the calls to `mainMenu()` from each of the sub-menus. The previous implementation would "extend" the call stack indefinitely. Now - more appropriately - the `run()` method is solely responsible for calling the `mainMenu()` method.

## Testing

Tested the initialization of the global variables.

Tested the new method `get_input()`.
4 cases were tested. Each of the 3 keywords 'MAIN', 'Q',and 'TEST' which all produce a `RenewStateException`, 'Q' sets `isRunning` to `False` and `TEST` sets `isTest` to `True`.

## Justification

One of the objectives of refactoring my project is to better separate the UI components of my program from the functional components. Part of this movement involves aggregating all aspects of the UI. Merging `uihelpers` and `ui` helps achieve this, and is especially useful since so many of the `uihelpers`' methods are regularly used in the UI.

Another major change is the addition of state variables, a custom exception, and a better process for quitting the program. Previously, the `quit()` method (which saves data and terminates the program) was *hidden* in `uihelpers`. The way the program terminated was not obvious because it was indirectly invoked by a `listener()` method which was itself out-of-sight. This updated control flow is substantially more central which makes it easier to understand and update in the future. (For instance, if I add a GUI to the program.)


# Refactor 3

## Code Smell: Long Method

The methods `newStudentUI()` and `newSessionUI()` were 34 and 62 lines respectively. Both of them guides the user through the creation of a new object.

The primary concern is that these methods handle getting user input **and** using that input to create an object and store it in the program's data structures.

In general, methods should accomplish **one** thing at a time, so this is a bad smell.

## Solution: Extract Method

To improve my design, I separated the functionality of user interaction from data handling. The result was extracting two methods from each of the originals.

## Resulting Code

The following files and methods were affected.

### Commit `8c985f18`

- `studentManager.py`
    - `newStudentUI()` replaced by `ui_new_student()` and `insert_new_student()`. The `ui` method interacts with the user and once the appropriate fields have been populated, calls the `insert` method to create and add the new student.
    - `pickStudent()` were `findStudent()` merged to make `ui_pick_student()` as their functionality was coupled.
- `invoiceManager.py`
    - All instances of `pickStudent()` replaced with more generic `ui_pick_student()`.
- `ui.py`
    - In `studentMenu()` replaced call to `newStudentUI()` with `ui_new_student()`.
    - All instances of `pickStudent()` replaced with more generic `ui_pick_student()`

### Commit `60043ba5`

- `sessionManager.py`
    - `newSessionUI()` replaced by `ui_new_session()` and `insert_new_session()`.
- `ui.py`
    - Added `get_integer_input()`
    - Added `get_datetime_input()`
    - Added `get_float_input()`
    - In `sessionMenu()` replaced call to `newSessionUI()` with `ui_new_session()`
- `studentManager.py`
    - Updated `ui_new_student()` to use the new `get_integer_input()` method. Bug fixed bad call to the fields of the Student class.

## Testing

Tested the parsing methods in `helpers.py` file that are used by the new `get_integer_input()`, `get_float_input()`, and `get_datetime_input()` in `ui.py`.

Tested the `insert_new_session()` method and the `insert_new_student()` methods.

## Justification

One of the goals of refactoring this project is to de-couple the UI aspects of the program from the data aspects of the program.

Taking these two core methods of the program and splitting them into ones that are clearly in different domains facilitates the next major refactoring of dividing my code base into these two domains.

Additionally, the new naming convention creates more clarity as to what the methods do. `ui_X` indicates that there will be user interaction while `insert_X` indicates that there will be some sort of data addition (harkening to the INSERT SQL statement.)


# Refactor 4 - MAJOR

## Code Smell: Large Class

The previous refactorings have been preparing for the decoupling of user interactions from the data classes. In my program, the `studentManager`, `sessionManager`, and `invoiceManager` all have a combination of UI oriented methods and data oriented methods. These classes are doing two different things and is not conduscive to the future development of a GUI or a proper database backend system.

## Solution: Extract Class

The goal is to aggreggate the user interaction methods, instead of leaving them scattered around my program. Two new classes will be created.

- All UI methods (ones that print to stdout and read from stdin) are moved to `ui_service.py`.
- All user functions (ones that are defined as part of the menus) are either created or moved to `ui_operations.py`. This class will interface with the data classes to fulfill user needs.

## Resulting Code

### Commit: `0225345e`
- Created empty `ui_service.py` file

### Commit: `cd26ac43`
- `ui.py`
    - All code relating to getting user input was moved to `ui_services.py`
    - The `isTest` global variable was removed.
    - The keywords "Q" and "MAIN" now throw unique exceptions that determine how they are handled
- `ui_services.py`
    - Where all user input methods were relocated.
- `exceptions.py`
    - Created two custom exceptions used for program flow. `Quit` and `GoToMain`.

### Commit: `8d9b5692`
- `studentManager.py`
    - Moved `ui_new_student()` to `uop`
    - Moved `ui_pick_student()` to `uop`
    - Moved `ui_view_student()` to  `uop`
- `ui.py`
    - Earlier attempt to pass `ui_services` as an object were inneffective. Reverted to making regular calls to the file instead.
    - Updated `studentMenu` to **only** make calls to `uop`.
- Created `ui_operations.py` (`uop`)
    - Added `new_student()`
    - Added `pick_student()`
    - Added `view_student()`
    - Added `view_single_student()`
- `ui_service.py` removed comments

### Commit: `e5d6a0f7`
- `sessionManager.py`
    - Moved `ui_new_session()` to `uop`
    - Moved `findSession()` to `uop`
    - Deleted `getSessionsByStudent()` because it was effectively an alias for `findSessions()`.
- `ui.py`
    - Updated `sessionMenu()` to **only** make calls to `uop`
- `ui_operations.py`
    - Added `new_session()`
    - Added `view_all_sessions()`
    - Added `view_sessions_by_student()`

### Commit: `cf2f677d`
- `invoiceManager.py`
    - Moved `newInvoiceUI()` to `uop`
    - Moved `payInvoiceUI()` to `uop`
    - Removed obsolete `changeAttribute()`
    - Renamed `createMonthlyInvoice()` to `insert_new_invoice`
- `ui.py`
    - Updated `invoiceMenu()` to **only** make calls to `uop`
    - Removed obsolete import statements
    - Updated `quit()` to get `uop` to save data
    - Updated `run()` to get `uop` to load data
- `ui_operations.py`
    - Updated `new_student()` to remove obscurity - it no longer depends on the Student dataclass
    - Added `new_invoice_for_student()`
    - Added `view_all_invoices()`
    - Added `view_invoices_by_student()`
    - Added `generate_monthly_invoices()`
    - Added `print_student_invoice()`
    - Added `print_monthly_invoices()`
    - Added `pay_invoice`
    - Added `load()`
    - Added `save()`
- `paymentManager.py` bugfix
- `sessionManager.py` bugfix
- `studentManager.py` bugfix
- `ui_service.py`
    - Added `get_date_input()`
    - Bugfix `get_float_input()`
    - Bugfix `validateChoice()`

### Commit: `1787a5cc`
- `analyzer.py`
    - Moved `getTotalIncome` to `uop`
    - Moved `getIncomeByMonth` to `uop`
- `ui.py`
    - Updated `analysisMenu()` to **only** make calls to `uop`
    - Removed obsolete import statements
- `ui_operations.py`
    - Added `get_total_income()`
    - Added `get_monthly_income()`
- `paymentManager.py`
    - Removed dead code
- `invoiceManager.py` removed obsolete import statements
- `sessionManager.py` removed obsolete import statements
- `studentManager.py` removed obsolete import statements
- `helpers.py` removed unused global variables

### Commit: `06961de5`
- `Session_test.py` updated (see below)
- `Student_test.py` updated (see below)
- `ui_serivice_test.py` renamed (from `ui_test.py`) and updated (see below)
- `invoiceManager.py`
    - Simplified `findInvoice()`
    - Simplified `findInvoices()`
    - Removed `getInvoicesByStudent()` - two usages, alias for `findInvoices()`
    - Updated `printInvoiceByStudent()`
- `pdfManager.py` bugfix
- `sessionManager.py`
    - Simplified `findSessions()`
- `studentManager.py`
    - Simplified `findSudent()`
- `ui_operations.py`
    - Updated `view_invoices_by_student()` to accomodate  removal of `getInvoicesByStudent()`

## Testing

Existing tests were updated to test the newly migrated code. Setup/teardown was added to most test modules. New tests were developped for `findSessions()` and `findStudent()`. The `ui_test.py` file was no longer effective. Foremost, because all of the methods it previously tested had been moved to `ui_service.py` and secondly, because the control flow of the program had changed. Consequently, this group of tests were renamed to `ui_service_test.py` and redesigned to account for the changes.

Extensive unit testing was not feasible for this stage of refactoring. The entirety of `ui_operations.py` consists of heavy UI methods. Almost every method requires multiple user inputs - and simulating multiple user inputs is conflated and difficult using PyTest.

Instead of unit testing, I methodically called each of the 15 menu options and ensured that they:
- a) Executed without error
- b) Produced the expected output // created the correct data

The bugfixes noted in commit `cf2f677d` were all detected using this testing method.


## Justification

Oh my god! It's like I redecorated my entire bedroom!!!

SO FRESH!

In seriousness though, this refactoring was amazing. Here are some of the things that it achieved:

1. `ui.py` has no awareness of the data classes now, all import statements were removed.
2. `_Manager.py` classes have no UI methods.
3. `ui.py` is now 100% focused on the control flow of the program.
4. `ui_service.py` contains all UI methods.
5. `ui_operations.py` contains all methods responsible for handling interaction between the *app* and the *data*.

One of the things that I'm happy about is how much I was able to clean up the import statements. Not so long ago, `ui` imported `studentManager` which imported `ui`. I had these really weird circular import statements where files depended on each other for a bunch of features. I am really pleased to have isolated these features.

These changes have a huge positive impact on the ease of *future development*. Functionality of the program is now reasonably allocated with little to no cross over between domains. Developing a proper backend actually seems like something I can do now :) Adding new features is trivial now, I can:

- modify a menu in `ui`,
- write a method in `ui_operations` for the feature, and
- leverage any of the UI utilities from `ui_service`

# Refactor 5

Not actually written yet.

## Code Smell: 

## Solution:

## Resulting Code

## Testing

## Justification