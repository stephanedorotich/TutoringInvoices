---
author: Stéphane Dorotich
title: Assignment 1 - Refactoring
date: Oct 8th, 2022
---

You will find this report and project at these repositories:

-  [https://github.com/stephanedorotich/TutoringInvoices](https://github.com/stephanedorotich/TutoringInvoices)
- [https://gitlab.cpsc.ucalgary.ca/stephane.dorotich/501](https://gitlab.cpsc.ucalgary.ca/stephane.dorotich/501)

# Code Source

This code is my own. I use it to track my high school tutoring business. Development began in fall 2019. I have updated my personal repository concurrently with this assignment. The original code can be viewed on [this commit](https://github.com/stephanedorotich/TutoringInvoices/tree/357dcf909d14191ccf62a33de2512f05dfcbadb7).

The program helps me manage my Students, Sessions, and Invoices. I use it to automatically generate PDF invoices to send to my clients. Generating PDFs is beyond the scope of this assignment. Due to the complexity of the final refactor, this feature has been disabled.

# Usage

To run the program, use the command: ```python3 src/ui.py```

While the program is running, there are two keywords that can be used at anytime:
- `Q`: Saves data and exits the program.
- `MAIN`: Returns the user to the main menu.

# Commits

| Branch | Refactor | Commit Title | Short Hash |
| ------ |:--------:| -------------- |:-----------:|
| master | 5 | Merge branch 'R5' | ff05978a |
| R5     | 5 | Adding fake data | a327ef6d |
| R5     | 5 | R5: Removing obsolete code :) | b1d59951 |
| R5     | 5 | R5: Updated invoice_data_class to update with payment | de098c44 |
| R5     | 5 | R5: Bugfix pay_invoice | e383c096 |
| R5     | 5 | R5: Finished implementation of Invoice Menu | c0572cd8 |
| R5     | 5 | R5: Invoice Menu functionality | aabd1e01 |
| R5     | 5 | R5: Updated abstract_data_class | bd905800 |
| R5     | 5 | R5: Student & Session Menus functional | aba6babb |
| R5     | 5 | R5: Creationg of data classes | 5a47cde8 |
| master | 4 | Merge branch 'R4' into 'master' | 60035dfa |
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

<details>
<summary>Refactor 1 Commit History</summary>

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
</details>

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

<details>
<summary>Refactor 2 Commit History</summary>

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
</details>

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

<details>
<summary>Refactor 3 Commit History</summary>
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
</details>

## Testing

Tested the parsing methods in `helpers.py` file that are used by the new `get_integer_input()`, `get_float_input()`, and `get_datetime_input()` in `ui.py`.

Tested the `insert_new_session()` method and the `insert_new_student()` methods.

## Justification

One of the goals of refactoring this project is to de-couple the UI aspects of the program from the data aspects of the program.

Taking these two core methods of the program and splitting them into ones that are clearly in different domains facilitates the next major refactoring of dividing my code base into these two domains.

Additionally, the new naming convention creates more clarity as to what the methods do. `ui_X` indicates that there will be user interaction while `insert_X` indicates that there will be some sort of data addition (harkening to the INSERT SQL statement.)


# Refactor 4 - Major

## Code Smell: Large Class

The previous refactorings have been preparing for the decoupling of user interactions from the data classes. In my program, the `studentManager`, `sessionManager`, and `invoiceManager` all have a combination of UI oriented methods and data oriented methods. These classes are doing two different things and is not conduscive to the future development of a GUI or a proper database backend system.

## Solution: Extract Class

The goal is to aggreggate the user interaction methods, instead of leaving them scattered around my program. Two new classes will be created.

- All UI methods (ones that print to stdout and read from stdin) are moved to `ui_service.py`.
- All user functions (ones that are defined as part of the menus) are either created or moved to `ui_operations.py`. This class will interface with the data classes to fulfill user needs.

## Resulting Code

<details>
<summary>Refactor 4 Commit History</summary>

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
</details>

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

# Refactor 5 - Major

## Code Smell: Alternative Classes with Different Interfaces

After the previous refactorings, it became apparent that each of the classes: `sessionManager`, `studentManager`, `invoiceManager`, and `paymentManager` all had the same basic functionality. They all needed to be able to `load` from file, `save` to file, and `insert_new` elements.

This resulted in a lot of duplicated code (even though the load methods were each unique) that was tricky to modify if there was any change to the underlying structure of the data.

Also, due to the complex load/save methods, there was lots of opportunity for mistakes to be made.

## Solution: Extract Superclass

The solution is the extract a superclass, called `abstract_data_class` which can be extended for `session`, `student`, `invoice`, and `payment`.

In doing so, the functionality of those classes can be rigorously controlled to ensure they all meet the same specifications.

As I extracted the superclass, I realized that the `load` and `save` methods were not going to generalize well. To remedy this, I decided to entirely reconstruct the backend of my program using the `pandas` library and its `DataFrames`. The data design changed significantly.

## Resulting Code

The resulting code is a complete reworking of the data driven aspects of my code. I removed the `object` based design that I had before, where each type (student, session, invoice, payment) was stored like an object whose fields were easily accessed.

Instead, each data type is stored in a DataFrame, which is akin to the tables in a relational database. Each entry, or row, represents a single object.

Previously, my Student objects had Lists that stored the keys of the Sessions, Invoices, and Payments that belonged to them. This made finding those objects quite straightforward, however, storing a list as an entry in a table is **not good practice**. Instead, I realized that each table row for sessions, invoices, and payments, could instead store the studentKey of who they belong to.

The program functions much more like a relational database that is being queried. This is aligned with my original intentions when developing the code. At the time, I lacked the knowledge and expertise to build it in this way.

<details>
<summary>Commit History</summary>

### Commit `5a47cde8`

- Created `abstract_data_class`
    - With methods `__new__`, `__init__`, `__init_subclass__`, `load_dataframe`, `save_dataframe`, `insert_new`, `find_single`, `find_multiple`
- Created `invoice_data_class`, `payment_data_class`, `session_data_class`, `student_data_class`
    - Each one implements the required global vars `fname`, `dtype`, and `parse_dates`

### Commit `aba6babb`

- `abstract_data_class`
    - added print statements to `save_dataframe` and `insert_new`
- `session_data_class`
    - added `get_sessions_by_student_key`
- `student_data_class`
    - added `find_by_name`
- `ui_operations`
    - turned `ui_operations` into a class, updated calls accordingly.
    - updated `load()` to call on new dataclasses
    - update `save()` to call on new dataclasses
    - rewrote `new_student()` to work with pandas DataFrames
    - rewrote `pick_student()` to work with pandas DataFrames
    - rewrote `view_all_students()` to work with pandas DataFrames
    - rewrote `view_single_student()` to work with pandas DataFrames
    - rewrote `new_session()` to work with pandas DataFrames
    - rewrote `view_all_sessions()` to work with pandas DataFrames
    - rewrote `view_sessions_by_student()` to work with pandas DataFrames
- `ui`
    - Turned `ui` into a class, updated calls accordingly.

### Commit `bd905800`

- `abstract_data_class`
    - Call the `load_dataframe` method from the `__init__` method
    - Ensure that all `superclass` methods **return** something
  
### Commit `aabd1e01`

- `invoice_data_class`
    - added `get_invoices_by_student_key`
    - added `make_invoice`
- `session_data_class`
    - added `get_sessions_by_month`
    - added `get_uninvoiced_sessions`
    - added `update_sessions_with_invoice_key`
- `ui_operations`
    - updated `pick_student` with a print statement
    - rewrote `new_invoice_for_student` to work with pandas DataFrames
    - rewrote `view_all_invoices` to work with pandas DataFrames
    - rewrote `view_invoices_by_student` to work with pandas DataFrames
    - rewrote `generate_monthly_invoices` to work with pandas DataFrames
    - removed obsolete calls to `*Manager.py` files

### Commit `c0572cd8`

- `invoice_data_class`
    - added `get_unpaid_invoices`
- `ui`
    - updated `run()` method to catch `NotImplementedError`
- `ui_operations`
    - rewrote `pay_invoice` to work with pandas DataFrames
    - updated `print_student_invoices` to throw `NotImplementedError`
    - updated `print_monthly_invoices` to throw `NotImplementedError`

### Commit `e383c096`

- `ui_operations`
    - removed obsolete import statements
    - updated `view_invoices_by_student` to print statement if user has no invoices to view
    - updated `pay_invoice` so that it updates the invoice's totalPaid amount in addition to creating a new payment.
    - updated `get_total_income` to throw `NotImplementedError`
    - updated `get_monthly_income` to throw `NotImplementedError`

### Commit `de098c44`

- `invoice_data_class`
    - added `update_invoice_with_payment_amount` to complete functionality of previous commit.

### Commit `b1d59951`

- Deleted `Invoice.py`
- Deleted `Payment.py`
- Deleted `Session.py`
- Deleted `Student.py`
- Deleted `Session_test.py`
- Deleted `Student_test.py`
- Deleted `invoiceManager.py`
- Deleted `paymentManager.py`
- Deleted `pdfManager.py`
- Deleted `sessionManager.py`
- Deleted `studentManager.py`
- `helpers`
    - removed `findSingle()`
    - removed `findMultiple()`

### Commit `a327ef6d`

- Added fake data.

</details>

## Testing

Unfortunately, rigorous unit testing was not an option for this refactoring. The main reason for this is limitations in "budget." I designed 15 testable methods in my data_classes and updated 12/16 methods in `ui_operations` about 7 are or can be made to be testable.

Developing rigorous unit tests for 22 methods is not feasible given the timeline for this assignment (and given that I started this final refactoring late.)

Instead, to ensure the integrity of my code (because I **do** use this for my business) I methodically reviewed each of the 15 menu options to ensure that my program produces correct output and does not crash on any inputs.

## Justification

Making this change protects my data. The complexity of data storage and manipulation is hidden inside of data classes and behaves much more like queries on a relational database. This design style supports future changes such as using a SQLite database to store my data - as SQLite interfaces well with Pandas.

The overhaul elimited the complexity of my save and load, it turned them from a dangerous and possibly buggy mess to **very clean one-liners**.

Using pandas DataFrames opens up a powerful suite of data manipulation and analysis opportunities. I know longer need to build clunky methods that deal with my hacked-together lists of data.

Using keys to indicate relationships allowed me to remove the improper use of "lists within lists" that my program relied on.

Additionally, going through this process allowed me to learn about:

- creating Classes,
- extending Classes,
- using Classes as Objects, and
- using Pandas DataFrames

This refactoring assignment as a whole allowed me to think critically about my code and iteratively develop a solid design for a substantial collection of code. I am very pleased with the results :)
