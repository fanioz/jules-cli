## 2024-03-24 - CLI Startup Time
**Learning:** Eager imports of heavy dependencies like `requests` and `tabulate` at the module level in a CLI application slow down command execution significantly, as they are imported even for simple commands like `jules --help`.
**Action:** Use lazy imports inside command functions rather than module-level eager imports for heavy dependencies.
