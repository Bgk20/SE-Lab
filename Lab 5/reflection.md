# Lab 5: Static Code Analysis — Reflection

**Program:** `energy_system.py`

## Reflection Question 1: What were the major issues identified in the original energy tariff program, and which tools helped identify them?

**Answer:**

The original `energy_system.py` contained code-quality, security, and formatting issues. Pylint identified problems such as a mutable default argument (`history=[]`), missing docstrings, an unnecessary `elif`, modification of global variables, a bare `except` clause, file handling without an explicit encoding or context manager, old-style string formatting, and an unused `sys` import. Bandit identified the use of `eval()` as a security issue (B307). Flake8 reported formatting problems, including spacing, blank-line, and line-length violations. Running the program also revealed a functional problem that static analysis did not identify: negative meter readings could be accepted and produce an invalid negative bill.

## Reflection Question 2: Why was using `eval()` a security risk, and how was it fixed?

**Answer:**

The original program used `eval()` to process the user's input. This is unsafe because `eval()` can execute arbitrary Python expressions rather than simply interpreting the input as a number. Bandit reported this as issue B307. We replaced `eval()` with `int()`, which accepts integer input only, and handled invalid input using exception handling. This prevents arbitrary Python expressions from being evaluated and makes the input handling safer.

## Reflection Question 3: What changes were made to improve the code quality, reliability, and readability?

**Answer:**

Several improvements were made. The mutable default argument was changed from `history=[]` to `history=None`, with a new list initialized inside the function. Broad exception handling was replaced with specific exception handling. File operations were updated to use `with open(...)` and `encoding="utf-8"`, ensuring files are closed properly and text encoding is consistent. Unnecessary global-state modification was reduced, missing docstrings were added, the unused import was removed, and old-style string formatting was replaced with f-strings. Flake8 formatting issues were also corrected. Additionally, validation was added to reject negative meter readings and negative rate adjustments.

## Reflection Question 4: What did you learn from using Pylint, Bandit, and Flake8, and why is it important to test the program after fixing issues?

**Answer:**

I learned that the three tools focus on different aspects of a Python program. Pylint checks code quality and programming practices, Bandit checks for common security problems, and Flake8 checks coding style and formatting. Their reports helped identify problems systematically and verify whether the fixes worked. After the changes, Pylint improved from 6.14/10 to 10.00/10, Bandit reported no issues, and Flake8 reported no findings. However, static analysis alone is not enough: running and testing the program was also necessary to discover the negative meter-reading problem and to confirm that the corrected program still records readings, calculates bills, flags unusually high usage, and saves and reloads meter data correctly.
