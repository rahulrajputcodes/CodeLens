from codelens.search import search_project


def test_search_project_finds_matching_lines(tmp_path):
    """
    Verify that the search engine finds matching lines.
    """

    source_file = tmp_path / "main.py"

    source_file.write_text(
        "print('hello')\n"
        "TODO: improve this function\n"
        "print('done')\n",
        encoding="utf-8",
    )

    results = search_project(
        [source_file],
        "TODO",
    )

    assert len(results) == 1
    assert results[0]["line"] == 2
    assert results[0]["content"] == "TODO: improve this function"


def test_search_project_is_case_insensitive(tmp_path):
    """
    Verify that keyword matching ignores letter case.
    """

    source_file = tmp_path / "main.py"

    source_file.write_text(
        "print('hello')\n"
        "todo: improve this function\n",
        encoding="utf-8",
    )

    results = search_project(
        [source_file],
        "TODO",
    )

    assert len(results) == 1
    assert results[0]["line"] == 2


def test_search_project_finds_multiple_matches(tmp_path):
    """
    Verify that multiple matching lines are returned.
    """

    source_file = tmp_path / "main.py"

    source_file.write_text(
        "TODO: first task\n"
        "print('hello')\n"
        "TODO: second task\n"
        "TODO: third task\n",
        encoding="utf-8",
    )

    results = search_project(
        [source_file],
        "TODO",
    )

    assert len(results) == 3


def test_search_project_ignores_unsupported_files(tmp_path):
    """
    Verify that unsupported file types are not searched.
    """

    source_file = tmp_path / "main.py"
    binary_file = tmp_path / "image.png"

    source_file.write_text(
        "TODO: fix this\n",
        encoding="utf-8",
    )

    binary_file.write_bytes(
        b"TODO: binary content"
    )

    results = search_project(
        [
            source_file,
            binary_file,
        ],
        "TODO",
    )

    assert len(results) == 1
    assert results[0]["file"] == str(source_file)