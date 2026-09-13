from pathlib import Path

from codelens.file_analyzer import analyze_files


def test_analyze_files_counts_python_files(tmp_path):
    """
    Verify that Python files are counted correctly.
    """

    python_file_1 = tmp_path / "main.py"
    python_file_2 = tmp_path / "utils.py"

    python_file_1.write_text(
        "print('hello')\nprint('world')\n",
        encoding="utf-8",
    )

    python_file_2.write_text(
        "x = 10\n",
        encoding="utf-8",
    )

    result = analyze_files(
        [
            python_file_1,
            python_file_2,
        ]
    )

    assert result["python_files"] == 2


def test_analyze_files_counts_total_lines(tmp_path):
    """
    Verify that total source-code lines are counted correctly.
    """

    python_file = tmp_path / "main.py"
    javascript_file = tmp_path / "app.js"

    python_file.write_text(
        "line 1\nline 2\nline 3\n",
        encoding="utf-8",
    )

    javascript_file.write_text(
        "line 1\nline 2\n",
        encoding="utf-8",
    )

    result = analyze_files(
        [
            python_file,
            javascript_file,
        ]
    )

    assert result["total_lines"] == 5


def test_analyze_files_ignores_unsupported_files(tmp_path):
    """
    Verify that unsupported file types are excluded from analysis.
    """

    python_file = tmp_path / "main.py"
    image_file = tmp_path / "image.png"

    python_file.write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    image_file.write_bytes(
        b"binary data"
    )

    result = analyze_files(
        [
            python_file,
            image_file,
        ]
    )

    assert result["python_files"] == 1
    assert result["total_lines"] == 1


def test_analyze_files_handles_empty_files(tmp_path):
    """
    Verify that empty source files are handled correctly.
    """

    empty_file = tmp_path / "empty.py"

    empty_file.write_text(
        "",
        encoding="utf-8",
    )

    result = analyze_files([empty_file])

    assert result["python_files"] == 1
    assert result["total_lines"] == 0