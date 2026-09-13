from codelens.ast_analyzer import analyze_python_file, analyze_python_files


def test_analyze_python_file_detects_functions_and_classes(tmp_path):
    """
    Verify that the AST analyzer detects functions and classes.
    """

    source_file = tmp_path / "main.py"

    source_file.write_text(
        """
class Calculator:

    def add(self, a, b):
        return a + b


def greet(name):
    return f"Hello {name}"
""",
        encoding="utf-8",
    )

    result = analyze_python_file(source_file)

    assert "Calculator" in result["classes"]
    assert "add" in result["functions"]
    assert "greet" in result["functions"]

    assert result["class_count"] == 1
    assert result["function_count"] == 2


def test_analyze_python_file_detects_imports(tmp_path):
    """
    Verify that regular and from-style imports are detected.
    """

    source_file = tmp_path / "imports.py"

    source_file.write_text(
        """
import os
import json
from pathlib import Path
from collections import Counter
""",
        encoding="utf-8",
    )

    result = analyze_python_file(source_file)

    assert "os" in result["imports"]
    assert "json" in result["imports"]
    assert "pathlib.Path" in result["imports"]
    assert "collections.Counter" in result["imports"]

    assert result["import_count"] == 4


def test_analyze_python_file_detects_decorators(tmp_path):
    """
    Verify that function decorators are detected.
    """

    source_file = tmp_path / "decorators.py"

    source_file.write_text(
        """
@staticmethod
def calculate():
    return 42
""",
        encoding="utf-8",
    )

    result = analyze_python_file(source_file)

    assert "staticmethod" in result["decorators"]
    assert result["decorator_count"] == 1


def test_analyze_python_file_handles_syntax_errors(tmp_path):
    """
    Verify that invalid Python syntax does not crash the analyzer.
    """

    source_file = tmp_path / "broken.py"

    source_file.write_text(
        """
def broken_function(
    print("invalid")
""",
        encoding="utf-8",
    )

    result = analyze_python_file(source_file)

    assert result["syntax_error"] is True
    assert result["function_count"] == 0
    assert result["class_count"] == 0


def test_analyze_python_files_analyzes_only_python_files(tmp_path):
    """
    Verify that the batch analyzer ignores non-Python files.
    """

    python_file = tmp_path / "main.py"
    javascript_file = tmp_path / "app.js"

    python_file.write_text(
        """
def hello():
    return "hello"
""",
        encoding="utf-8",
    )

    javascript_file.write_text(
        "function hello() {}",
        encoding="utf-8",
    )

    results = analyze_python_files(
        [
            python_file,
            javascript_file,
        ]
    )

    assert len(results) == 1
    assert results[0]["file"] == str(python_file)