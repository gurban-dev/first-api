# Introduction to Logging in Python & FastAPI

In a production environment (like a FastAPI application), you can't rely on `print()` statements to track down bugs or monitor behavior. **Logging provides a structured way to understand what happened, where it happened, and why it happened** when errors occur or workflows execute.

---

### The Base Configuration

To start logging, we use Python's built-in initialization pattern:

```python
import logging

# Configure global system settings
logging.basicConfig(level=logging.INFO)

# Create a scoped tracker for the current module
logger = logging.getLogger(__name__)
```

---

### Line-by-Line Breakdown

#### 1. `import logging`
* Imports Python's built-in logging module.
* Part of the standard library (no third-party installation required).

#### 2. `logging.basicConfig(level=logging.INFO)`
* Sets up default handlers and formats for the application.
* The `level` argument filters which messages get displayed or saved based on severity.

| Level | Severity | Purpose |
| :--- | :--- | :--- |
| **`DEBUG`** | 10 | Detailed debug diagnostics (omitted under `INFO` config). |
| **`INFO`** | 20 | Routine confirmations of expected application behavior. |
| **`WARNING`** | 30 | Indicators of an unexpected event (app keeps running). |
| **`ERROR`** | 40 | Severe functional failures preventing specific operations. |
| **`CRITICAL`** | 50 | Structural crash-level events that stall execution. |

*With `level=logging.INFO`, `DEBUG` traces are automatically suppressed, while all other higher levels emit messages.*

#### 3. `logger = logging.getLogger(__name__)`
* Instantiates or retrieves a dedicated logger object scoped to the current file context.
* Utilising `__name__` maps log entries safely to the current module (`"__main__"` when run directly, or the module name like `"main"` when loaded by Uvicorn).