
## 2023-10-27 - [Lazy Imports in CLI]
**Learning:** Eagerly importing heavy libraries like `requests` and `tabulate` at the module level in a `click` CLI application significantly degrades startup time (from ~91ms to ~329ms in this case), even for simple commands like `--help`.
**Action:** Use lazy imports inside command functions for heavy dependencies to ensure fast CLI startup times.
