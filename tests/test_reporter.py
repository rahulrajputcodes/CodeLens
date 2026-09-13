import json

from codelens.reporter import build_report, save_report


def test_build_report_contains_project_summary():
    """
    Verify that build_report creates the expected project
    summary from the analysis results.
    """

    files = [
        "project/main.py",
        "project/utils.py",
    ]

    file_analysis = {
        "python_files": 2,
        "total_lines": 100,
    }

    ast_analysis = [
        {
            "file": "project/main.py",
            "functions": ["main", "run"],
            "classes": ["Application"],
            "imports": ["os", "sys"],
            "decorators": ["staticmethod"],
            "function_count": 2,
            "class_count": 1,
            "import_count": 2,
            "decorator_count": 1,
            "syntax_error": False,
        },
        {
            "file": "project/utils.py",
            "functions": ["helper"],
            "classes": [],
            "imports": ["json"],
            "decorators": [],
            "function_count": 1,
            "class_count": 0,
            "import_count": 1,
            "decorator_count": 0,
            "syntax_error": False,
        },
    ]

    quality_analysis = {
        "todos": [],
        "fixmes": [],
        "bugs": [],
        "hacks": [],
        "large_files": [],
        "duplicate_lines": [],
    }

    report = build_report(
        "project",
        files,
        file_analysis,
        ast_analysis,
        quality_analysis,
    )

    assert "project" in report
    assert "summary" in report
    assert "python_analysis" in report
    assert "code_quality" in report

    assert report["summary"]["files_analyzed"] == 2
    assert report["summary"]["python_files"] == 2
    assert report["summary"]["total_lines"] == 100
    assert report["summary"]["total_functions"] == 3
    assert report["summary"]["total_classes"] == 1
    assert report["summary"]["total_imports"] == 3
    assert report["summary"]["total_decorators"] == 1
    assert report["summary"]["syntax_errors"] == 0


def test_build_report_counts_syntax_errors():
    """
    Verify that the report correctly counts Python files
    containing syntax errors.
    """

    files = [
        "project/main.py",
        "project/broken.py",
    ]

    file_analysis = {
        "python_files": 2,
        "total_lines": 50,
    }

    ast_analysis = [
        {
            "file": "project/main.py",
            "functions": [],
            "classes": [],
            "imports": [],
            "decorators": [],
            "function_count": 0,
            "class_count": 0,
            "import_count": 0,
            "decorator_count": 0,
            "syntax_error": False,
        },
        {
            "file": "project/broken.py",
            "functions": [],
            "classes": [],
            "imports": [],
            "decorators": [],
            "function_count": 0,
            "class_count": 0,
            "import_count": 0,
            "decorator_count": 0,
            "syntax_error": True,
            "syntax_error_message": "invalid syntax",
        },
    ]

    quality_analysis = {
        "todos": [],
        "fixmes": [],
        "bugs": [],
        "hacks": [],
        "large_files": [],
        "duplicate_lines": [],
    }

    report = build_report(
        "project",
        files,
        file_analysis,
        ast_analysis,
        quality_analysis,
    )

    assert report["summary"]["syntax_errors"] == 1


def test_save_report_creates_json_file(tmp_path):
    """
    Verify that save_report creates the output directory and
    writes a valid JSON report to disk.
    """

    report = {
        "project": "/tmp/project",
        "summary": {
            "files_analyzed": 2,
            "python_files": 2,
            "total_lines": 100,
        },
        "python_analysis": [],
        "code_quality": {},
    }

    output_path = tmp_path / "reports" / "analysis.json"

    result = save_report(
        report,
        output_path,
    )

    assert result == output_path
    assert output_path.exists()

    with open(output_path, "r", encoding="utf-8") as f:
        saved_report = json.load(f)

    assert saved_report == report
    