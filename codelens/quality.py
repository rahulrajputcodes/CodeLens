from collections import Counter


# Maximum number of lines a file can have before CodeLens
# considers it a large file.
LARGE_FILE_THRESHOLD = 500


# Keywords commonly used to mark unfinished or suspicious code.
QUALITY_KEYWORDS = {
    "TODO": "TODO",
    "FIXME": "FIXME",
    "BUG": "BUG",
    "HACK": "HACK",
}


def analyze_quality(files):
    """
    Analyze project files for basic code-quality indicators.

    The analyzer detects:
    - TODO comments
    - FIXME comments
    - BUG markers
    - HACK markers
    - Large files
    - Duplicate lines
    """

    todos = []
    fixmes = []
    bugs = []
    hacks = []
    large_files = []
    duplicate_lines = []

    for file in files:

        # Only analyze supported text files.
        if file.suffix not in {
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
        }:
            continue

        try:
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()

        except (UnicodeDecodeError, PermissionError):
            continue

        # Detect files that exceed the configured size threshold.
        if len(lines) > LARGE_FILE_THRESHOLD:
            large_files.append(
                {
                    "file": str(file),
                    "lines": len(lines),
                }
            )

        # Track the number of times each non-empty line appears.
        line_counts = Counter(
            line.strip()
            for line in lines
            if line.strip()
        )

        # Record lines that appear more than once.
        for line, count in line_counts.items():
            if count > 1:
                duplicate_lines.append(
                    {
                        "file": str(file),
                        "line": line,
                        "count": count,
                    }
                )

        # Search for common code-quality markers.
        for line_number, line in enumerate(lines, start=1):

            upper_line = line.upper()

            for keyword, category in QUALITY_KEYWORDS.items():

                if keyword in upper_line:

                    result = {
                        "file": str(file),
                        "line": line_number,
                        "content": line.strip(),
                    }

                    if category == "TODO":
                        todos.append(result)

                    elif category == "FIXME":
                        fixmes.append(result)

                    elif category == "BUG":
                        bugs.append(result)

                    elif category == "HACK":
                        hacks.append(result)

    return {
        "todos": todos,
        "fixmes": fixmes,
        "bugs": bugs,
        "hacks": hacks,
        "large_files": large_files,
        "duplicate_lines": duplicate_lines,
    }