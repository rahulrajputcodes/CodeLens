from pathlib import Path


# File types that can be safely searched as text.
SEARCHABLE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".c",
    ".cpp",
    ".html",
    ".css",
    ".md",
    ".txt",
}


def search_project(files, keyword):
    """
    Search for a keyword across all supported project files.

    Returns a list containing the file, line number,
    and matching line for every match found.
    """

    results = []

    # Search through every file discovered by the scanner.
    for file in files:

        # Ignore files that are not supported text files.
        if file.suffix not in SEARCHABLE_EXTENSIONS:
            continue

        try:
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()

        except (UnicodeDecodeError, PermissionError):
            # Skip files that cannot be safely read.
            continue

        # Check every line for the requested keyword.
        for line_number, line in enumerate(lines, start=1):

            # Perform a case-insensitive search.
            if keyword.lower() in line.lower():

                results.append(
                    {
                        "file": str(file),
                        "line": line_number,
                        "content": line.strip(),
                    }
                )

    return results