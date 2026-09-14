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