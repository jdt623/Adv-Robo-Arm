"""Hardware driver subpackages.

Each driver is self-contained:
- A class exposing `read()`, `calibrate()`, `close()` as appropriate
- A `__main__.py` with a console-output test harness
- Runnable via `python -m robo_arm.drivers.<name>`
"""
