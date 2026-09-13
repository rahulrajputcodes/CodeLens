from codelens.quality import analyze_quality


def test_quality_detects_python_comment_markers(tmp_path):
    """
    Verify that quality markers inside Python comments are detected.
    """

    source_file = tmp_path / "main.py"

    source_file.write_text(
        """
# TODO: improve this function
# FIXME: handle invalid input
# BUG: incorrect calculation
# HACK: temporary workaround

print("TODO")
print("FIXME")
print("BUG")
print("HACK")
""",
        encoding="utf-8",
    )

    result = analyze_quality([source_file])

    assert len(result["todos"]) == 1
    assert len(result["fixmes"]) == 1
    assert len(result["bugs"]) == 1
    assert len(result["hacks"]) == 1


def test_quality_ignores_marker_words_inside_strings(tmp_path):
    """
    Verify that marker words inside Python strings are ignored.
    """

    source_file = tmp_path / "main.py"

    source_file.write_text(
        """
message = "TODO: this is just a string"
status = "FIXME"
description = "BUG found"
note = "HACK implementation"
""",
        encoding="utf-8",
    )

    result = analyze_quality([source_file])

    assert result["todos"] == []
    assert result["fixmes"] == []
    assert result["bugs"] == []
    assert result["hacks"] == []


def test_quality_detects_large_files(tmp_path):
    """
    Verify that files exceeding the size threshold are detected.
    """

    source_file = tmp_path / "large.py"

    source_file.write_text(
        ("print('hello')\n" * 501),
        encoding="utf-8",
    )

    result = analyze_quality([source_file])

    assert len(result["large_files"]) == 1
    assert result["large_files"][0]["lines"] == 501


def test_quality_detects_duplicate_meaningful_lines(tmp_path):
    """
    Verify that meaningful repeated lines are detected.
    """

    source_file = tmp_path / "duplicate.py"

    source_file.write_text(
        """
message = "This is a meaningful repeated line"
message = "This is a meaningful repeated line"
print(message)
""",
        encoding="utf-8",
    )

    result = analyze_quality([source_file])

    assert len(result["duplicate_lines"]) == 1
    assert result["duplicate_lines"][0]["count"] == 2


def test_quality_ignores_short_and_empty_duplicate_lines(tmp_path):
    """
    Verify that short structural lines do not create duplicate warnings.
    """

    source_file = tmp_path / "normal.py"

    source_file.write_text(
        """
()
()
{}
{}
print("hello")
print("hello")
""",
        encoding="utf-8",
    )

    result = analyze_quality([source_file])

    assert result["duplicate_lines"] == []