Software Engineering Lab
A collection of seven Software Engineering laboratory submissions. The repository includes requirements and UML documentation, Jira work, Python applications, code-quality analysis, test coverage exercises, fuzz testing, reports, and supporting evidence.
requirements & UML ─► project documentation ─► implementation
                                              └─► code analysis ─► testing & validation
Repository layout
Folder / file	Content
[`Lab 1/`](./Lab%201/)	Pharmacy Expiry & Re-order Dispatch Engine — functional and non-functional requirements, UML use-case diagram, and FEFO dispensing-list use-case specification (Lab1.docx).
[`Lab 2/`](./Lab%202/)	Jira lab — Jira-related lab documentation/report.
[`Lab 3/`](./Lab%203/)	Software Engineering Lab 3 — lab submission document.
[`Lab 4/`](./Lab%204/)	Catch-the-fish game — Python game implementation, supporting modules, test file, videos, and LLM-chat evidence.
[`Lab 5/`](./Lab%205/)	Code quality and security analysis — energy-system application, input data, Bandit, Flake8 and Pylint reports, issue notes, and reflection.
[`Lab 6/`](./Lab%206/)	Code and branch coverage analysis — coffee-shop order application, separate line-coverage and branch-coverage tests, and coverage screenshots. The test suites achieved 100% line coverage and 100% branch coverage.
[`Lab 7/`](./Lab%207/)	Fuzz testing and input validation — Python input-processing application, Hypothesis-based tests, fixed implementation, fuzzing report PDF, and screenshots. All three fuzz tests passed on the fixed implementation.
.gitignore	Excludes Python cache files, pytest cache, coverage data, and compiled Python files.


Testing highlights
- Lab 6: 20 line-coverage tests and 15 branch-coverage tests; both suites achieved 100% coverage.
- Lab 7: Hypothesis-based fuzz tests used to check that the input-processing functions handle unexpected inputs without crashing. The three tests passed after input validation was added.
Getting the repository
Clone the repository:
git clone https://github.com/Bgk20/SE-Lab.git
cd SE-Lab
Browsing the labs
- Open the lab folder from the table above to view its submission files.
- For document-based labs, open the included .docx or .pdf file.
- For programming labs, review the source files together with the corresponding tests, reports, and screenshots.
- Check each lab's own README or report for experiment-specific details and instructions.DME or report for any experiment details and instructions.
This repository is maintained as a collection of Software Engineering laboratory submissions and supporting evidence.
