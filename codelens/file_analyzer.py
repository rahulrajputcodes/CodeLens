from pathlib import Path


# File types that CodeLens can safely analyze as text.
SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".c",
    ".cpp",
    ".html",
    ".css",
}


def analyze_files(files):
    """
    Analyze supported source files and return basic project statistics.
    """

    python_files = 0
    total_lines = 0

    for file in files:

        # Ignore unsupported or binary file types.
        if file.suffix not in SUPPORTED_EXTENSIONS:
            continue

        try:
            # Read the file as UTF-8 text so we can count its lines.
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()

        except (UnicodeDecodeError, PermissionError):
            # Skip files that cannot be safely read.
            continue

        total_lines += len(lines)

        # Keep track of Python source files separately.
        if file.suffix == ".py":
            python_files += 1

    return {
        "python_files": python_files,
        "total_lines": total_lines,
    }