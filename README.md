# CodeLens

CodeLens is a Python-based command-line tool that analyzes software
codebases and generates structured insights about their source code.

It helps developers quickly understand a project's structure, Python
code, code-quality indicators, and searchable content without manually
inspecting every file.

## Features

- Recursively scans project directories
- Detects supported source files
- Counts Python files and total lines of code
- Analyzes Python code using the Abstract Syntax Tree (AST)
- Detects functions, classes, imports, and decorators
- Detects TODO, FIXME, BUG, and HACK markers
- Identifies large files
- Detects meaningful duplicate lines
- Searches project files for keywords
- Handles Python syntax errors without stopping the analysis
- Generates a structured JSON analysis report
- Includes automated tests for core modules

## Project Structure

```text
CodeLens/
│
├── main.py
├── README.md
├── .gitignore
│
├── codelens/
│   ├── __init__.py
│   ├── scanner.py
│   ├── file_analyzer.py
│   ├── search.py
│   ├── ast_analyzer.py
│   ├── quality.py
│   └── reporter.py
│
├── reports/
│   └── analysis.json
│
└── tests/
    ├── __init__.py
    ├── test_scanner.py
    ├── test_file_analyzer.py
    ├── test_search.py
    ├── test_ast_analyzer.py
    ├── test_quality.py
    └── test_reporter.py
