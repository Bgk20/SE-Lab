# Lab 5: Static Code Analysis — Issues Identified

**Program:** `energy_system.py`

The line numbers below refer to the original, uncorrected version of `energy_system.py`.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Unsafe use of `eval()` | Security — Bandit B307 (Medium) | 63 | `eval()` evaluates arbitrary Python expressions and can execute unintended code. | Replaced `eval()` with `int()` to accept only integer input. |
| Bare `except` clause | Reliability / style — Pylint W0702; Flake8 E722 | 43–44 | A bare `except` catches every exception, including exceptions that should not be hidden. | Caught specific expected exceptions and handled them explicitly. |
| Mutable default argument | Code quality — Pylint W0102 | 10 | Using `history=[]` as a default can cause separate calls to share the same list. | Changed the default to `None` and created a new list inside the function. |
| Global state modification | Maintainability — Pylint W0603 | 25–29, 38–40 | Functions modify global data, making behaviour harder to reason about and test. | Passed the rates as an argument and returned the updated rates; retained in-place meter updates where needed by the program. |
| File opened without encoding | Portability — Pylint W1514 | 41, 47 | Text file encoding depends on the environment when it is not specified. | Opened JSON files with `encoding="utf-8"`. |
| File not managed with a context manager | Resource handling — Pylint R1732 | 41, 47–49 | Files may not be closed reliably if an error occurs. | Used `with open(...)` so files close automatically. |
| Unused `sys` import | Code quality — Pylint W0611; Flake8 F401 | 2 | The imported module is not used. | Removed the unused import. |
| Missing module and function docstrings | Documentation — Pylint C0114, C0116 | 1 and function definitions | The module and functions do not explain their purpose. | Added module and function docstrings. |
| Unnecessary `elif` after `return` | Readability — Pylint R1705 | 18–19 | The `elif` is unnecessary because the preceding branch already returns. | Replaced it with a simpler conditional structure. |
| Old-style string formatting | Style — Pylint C0209 | 56, 57, 64 | Percent-based formatting is less consistent with modern Python formatting. | Replaced it with f-strings. |
| Flake8 spacing and line-length violations | Style — Flake8 E302, E305, E501 | Multiple | Blank-line spacing and long lines do not follow the expected style. | Corrected blank lines and wrapped long lines. |
| Negative meter readings accepted | Functional validation — Manual observation | Input validation | The original program accepts negative usage, which can produce an invalid negative bill (for example, M-03). | Added validation to reject negative readings with `ValueError`. |
| Input evaluated as Python code | Security — Bandit B307 | 63 | The user input is evaluated as an expression rather than parsed as a number. | Replaced expression evaluation with integer parsing and handled invalid input. |

## Analysis results

| Tool | Before fixes | After fixes |
|---|---:|---:|
| Pylint | 6.14/10 | 10.00/10 |
| Bandit | B307 finding reported | No issues identified |
| Flake8 | 12 findings | No findings |

**Note:** The negative-reading issue was found by running and inspecting the program; it is not necessarily reported by Pylint, Bandit, or Flake8. The unsafe `eval()` issue is described once in the main table as a security finding; the final row clarifies its effect on user input.
