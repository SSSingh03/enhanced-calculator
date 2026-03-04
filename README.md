# Enhanced Calculator

![CI](https://github.com/SSSingh03/enhanced-calculator/actions/workflows/python-app.yml/badge.svg)

A modular, test-driven calculator application built in Python that demonstrates professional software engineering practices including object-oriented design, design patterns, configuration management, logging, persistence, and continuous integration.

This project was developed as part of a **Python for Web API Development** course midterm assignment and emphasizes building maintainable, testable, and extensible software systems.

---

# Project Description

The **Enhanced Calculator** is a command-line application that performs arithmetic operations while maintaining a persistent history of calculations. The system is designed using several software engineering best practices including:

- Object-Oriented Programming
- Design Patterns
- Configuration Management
- Logging and Observability
- Persistent Data Storage
- Automated Testing
- Continuous Integration

---

# Features

- Multiple arithmetic operations
- Persistent calculation history stored in CSV
- Undo and redo functionality
- Logging of calculator activity
- Configurable system via `.env` environment variables
- Modular architecture with clean separation of concerns
- Comprehensive unit testing
- Continuous integration using GitHub Actions
- Test coverage enforcement (minimum 90%)
- Color-coded REPL output (Colorama)

---

# Supported Operations

The calculator supports the following operations:

| Command | Description |
|--------|------------|
| add | Addition |
| subtract | Subtraction |
| multiply | Multiplication |
| divide | Division |
| power | Exponentiation |
| root | Root calculation |
| modulus | Modulus operation |
| int_divide | Integer division |
| percent | Percentage calculation |
| abs_diff | Absolute difference |

Example usage:

```
add 2 3
multiply 4 5
divide 10 2
```


---

# Project Architecture

The project follows a modular architecture located inside the `app/` directory.
```
app/
├── calculator.py
├── calculation.py
├── operations.py
├── history.py
├── logger.py
├── calculator_config.py
├── calculator_memento.py
├── exceptions.py
└── input_validators.py

tests/
├── unit tests for all components

.github/workflows/
└── python-app.yml
```


---

# Design Patterns

### Factory Pattern

The `OperationFactory` dynamically creates operation objects based on user commands. This allows the calculator to support many operations without tightly coupling operation logic to the calculator core.

### Memento Pattern

The calculator uses the **Memento pattern** to implement undo and redo functionality. The system stores snapshots of the calculator state so that previous states can be restored.

### Observer Pattern

Observers are used to react to new calculations.

Two observers are implemented:

- **LoggingObserver** – logs calculator activity
- **AutoSaveObserver** – automatically saves calculation history to CSV

This design keeps logging and persistence separate from the calculator core logic.

---

# Installation Instructions

## Clone the Repository
git clone https://github.com/SSSingh03/enhanced-calculator.git

cd enhanced-calculator


---

## Create a Virtual Environment
python3 -m venv venv


Activate the environment:

### Mac / Linux
source venv/bin/activate


### Windows
venv\Scripts\activate


---

## Install Dependencies
pip install -r requirements.txt


Dependencies include:

- pandas
- python-dotenv
- colorama
- pytest
- pytest-cov

---

# Configuration Setup

The application uses environment variables to configure logging, history storage, and calculator behavior.

Create a `.env` file in the project root.

Example `.env` file:

```
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=6
CALCULATOR_MAX_INPUT_VALUE=1000000000
CALCULATOR_DEFAULT_ENCODING=utf-8
CALCULATOR_LOG_FILE=calculator.log
CALCULATOR_HISTORY_FILE=history.csv
```


---

## Configuration Explanation

| Variable | Description |
|--------|------------|
| CALCULATOR_LOG_DIR | Directory where log files are stored |
| CALCULATOR_HISTORY_DIR | Directory for calculation history |
| CALCULATOR_MAX_HISTORY_SIZE | Maximum number of history records |
| CALCULATOR_AUTO_SAVE | Enables automatic saving of history |
| CALCULATOR_PRECISION | Decimal precision for results |
| CALCULATOR_MAX_INPUT_VALUE | Maximum allowed numeric input |
| CALCULATOR_DEFAULT_ENCODING | File encoding |
| CALCULATOR_LOG_FILE | Log file name |
| CALCULATOR_HISTORY_FILE | CSV history file name |

The `.env` file is **not committed to Git** and is listed in `.gitignore`.

---

# Usage Guide

The calculator provides an interactive **REPL (Read–Eval–Print Loop)** interface.

Start the application with:

python -c "from app.calculator import run_repl; run_repl()"


You will see a command prompt:


Example session:

add 2 3
5

multiply 4 6
24

history

add 2 3 = 5

multiply 4 6 = 24


---

# Additional Commands

| Command | Description |
|--------|------------|
| history | Display calculation history |
| clear | Clear history |
| undo | Undo last calculation |
| redo | Redo last undone calculation |
| help | Display help menu |
| exit | Exit the calculator |

---

# Logging

All calculator operations are recorded using the Python logging module.

Log files are stored in the directory defined by:

CALCULATOR_LOG_DIR


Example log entry:
INFO: Calculation performed: add 2 3 = 5


Logging helps monitor system behavior and debug issues.

---

# History Persistence

The calculator automatically saves history to a CSV file when autosave is enabled.

Location:
history/history.csv


The CSV file contains:

- operation
- operands
- result
- timestamp

This allows calculation history to persist between program runs.

---

# Running Tests

Unit tests are located in the `tests/` directory.

Run all tests with:
pytest


---

# Test Coverage

The project enforces a **minimum of 90% test coverage**.

Run tests with coverage:
pytest --cov=app --cov-fail-under=90

Current coverage:
96.79%


This ensures that the majority of application logic is validated through automated testing.

---

# Continuous Integration (CI/CD)

This project uses **GitHub Actions** to automatically run tests on every push.

Workflow file:
.github/workflows/python-app.yml


The CI pipeline performs the following steps:

1. Set up Python environment
2. Install project dependencies
3. Run unit tests
4. Enforce minimum test coverage

CI command executed:
pytest --cov=app --cov-fail-under=90


This ensures that new code does not break the system or reduce test coverage.

---

# Code Documentation

The codebase includes:

- Meaningful **docstrings**
- Inline comments explaining logic
- Modular file organization

This improves readability, maintainability, and ease of future development.

---

# Author

Sahaj Singh

GitHub Repository:

https://github.com/SSSingh03/enhanced-calculator


