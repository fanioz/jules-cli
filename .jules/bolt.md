## 2025-02-28 - Lazy import heavy dependencies to speed up Python CLI startup
**Learning:** In click-based CLI apps, top-level imports of heavy libraries like `requests` and `tabulate` (even indirectly through API clients or formatters) block the main thread and significantly slow down command parsing and help menus (e.g. `jules --help`). This app saw startup drop from ~0.6s to ~0.1s.
**Action:** Always import heavy external dependencies locally within the specific command functions where they are actually used rather than at the module level.
