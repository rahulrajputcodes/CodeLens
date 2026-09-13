from pathlib import Path

import pytest

from codelens.scanner import scan_project


def test_scan_project_finds_files(tmp_path):
    """
    Verify that the scanner discovers files inside a project directory.
    """

    project = tmp_path / "sample_project"
    project.mkdir()

    (project / "main.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )

    (project / "README.md").write_text(
        "# Sample Project",
        encoding="utf-8",
    )

    files = scan_project(project)

    file_names = {file.name for file in files}

    assert "main.py" in file_names
    assert "README.md" in file_names


def test_scan_project_ignores_excluded_directories(tmp_path):
    """
    Verify that generated and dependency directories are ignored.
    """

    project = tmp_path / "sample_project"
    project.mkdir()

    (project / "main.py").write_text(
        "print('hello')",
        encoding="utf-8",
    )

    git_directory = project / ".git"
    git_directory.mkdir()

    (git_directory / "config").write_text(
        "git configuration",
        encoding="utf-8",
    )

    reports_directory = project / "reports"
    reports_directory.mkdir()

    (reports_directory / "analysis.json").write_text(
        "{}",
        encoding="utf-8",
    )

    files = scan_project(project)

    file_paths = {
        Path(file).relative_to(project)
        for file in files
    }

    assert Path("main.py") in file_paths
    assert Path(".git/config") not in file_paths
    assert Path("reports/analysis.json") not in file_paths


def test_scan_project_rejects_missing_path(tmp_path):
    """
    Verify that scanning a nonexistent project raises FileNotFoundError.
    """

    missing_project = tmp_path / "does_not_exist"

    with pytest.raises(FileNotFoundError):
        scan_project(missing_project)


def test_scan_project_rejects_file_path(tmp_path):
    """
    Verify that scanning an individual file raises NotADirectoryError.
    """

    file_path = tmp_path / "main.py"

    file_path.write_text(
        "print('hello')",
        encoding="utf-8",
    )

    with pytest.raises(NotADirectoryError):
        scan_project(file_path)