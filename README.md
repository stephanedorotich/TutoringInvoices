---
author: Stéphane Dorotich
title: Assignment 1 - Refactoring
date: Oct 7th, 2022
---

# Code Source

The original code can be found [here](https://github.com/stephanedorotich/TutoringInvoices). I started developing the program in 2019 to help me track my high school tutoring business.

The program provides a UI that helps me manage my Students, Sessions, and Invoices and also allows me to automatically generate monthly PDF invoices to send to my clients.

# Usage

```python3 src/ui.py```

# Commits

| Refactor | Commit Message | Short Hash |
| -------- | -------------- |:-----------:|
| 1 | Refactor 1: Dead Code | 11b36dbd |
| 2 | Refactor 2: Feature Envy | 8768859f |


# Refactor 1

## Code Smell: Dead Code

I developed a variety of utilities for my program. Over years of continued use, these utilities were seldom used. The code was reachable and functional, but not needed.

Some truly "dead" code was located in the `run()`, pertaining to `recoveryMode` whose purpose was to safely load my `.csv` files in the event that I accidentally ran the program from Command Prompt which would insert additional newline characters to my `.csv` files and be an absolute headache to fix manually. I later updated the regular `loadX()` methods to handle this case, rendering the `recoveryMode` section "dead".

## Solution: Delete Code

The methods for these utilities were all removed. The menus from which these utilities were invoked were updated accordingly.

The following files and methods were affected.
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

## Resulting Code

No new code was added.

## Testing

No testing was done because the removed methods/code were only invoked from a single location in `ui.py` and so the functionality of my program was unaffected by their removal.

## Justification

Removing the `recoveryMode` section prevents potential **runtime errors**. The section invoked methods that no longer existed, which would cause a runtime error.

Removing `editStudentUI()` helps ensure the integrity of my Student data entries. The ability to edit was a big risk because the method allowed me to modify the `Session` list whose integrity is paramount to integrity of the program.

Removing `openRecentInvoiceUI()` reduced some coupling between `invoiceManager.py` and `pdfManager.py`. The pdfManager file now **exclusively** deals with generating PDFs and has no UI methods.


# Refactor 2

## Code Smell: Feature Envy 

## Solution:

## Resulting Code

## Testing

## Justification


# Refactor 3

## Code Smell: 

## Solution:

## Resulting Code

## Testing

## Justification


# Refactor 4

## Code Smell: 

## Solution:

## Resulting Code

## Testing

## Justification


# Refactor 5

## Code Smell: 

## Solution:

## Resulting Code

## Testing

## Justification