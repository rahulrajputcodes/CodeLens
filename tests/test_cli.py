import subprocess
import sys


def test_cli_shows_help_without_command():
    """
    Verify that running CodeLens without a command
    displays the CLI help message.
    """

    result = subprocess.run(
        [sys.executable, "main.py"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "CodeLens - Python Codebase Intelligence CLI" in result.stdout
    assert "analyze" in result.stdout
    assert "search" in result.stdout


def test_cli_shows_version():
    """
    Verify that the CodeLens version command
    displays the expected version.
    """

    result = subprocess.run(
        [sys.executable, "main.py", "--version"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "CodeLens 1.0.0"

def test_cli_handles_missing_project():
    """
    Verify that CodeLens reports a clean error when
    the requested project directory does not exist.
    """

    result = subprocess.run(
        [
            sys.executable,
            "main.py",
            "analyze",
            "./does_not_exist",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Error: Project path does not exist:" in result.stdout


def test_cli_handles_file_instead_of_directory():
    """
    Verify that CodeLens reports a clean error when
    a file is provided instead of a project directory.
    """

    result = subprocess.run(
        [
            sys.executable,
            "main.py",
            "analyze",
            "main.py",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Error: Project path is not a directory:" in result.stdout