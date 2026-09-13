from collections import Counter
import io
import tokenize


# Maximum number of lines a file can have before CodeLens
# considers it a large file.
LARGE_FILE_THRESHOLD = 500


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
    ".md",
    ".txt",
}


# Minimum length required for a line to be considered
# meaningful when detecting duplicate lines.
MIN_DUPLICATE_LINE_LENGTH = 20


def _record_quality_marker(
    marker,
    file,
    line_number,
    content,
    todos,
    fixmes,
    bugs,
    hacks,
):
    """
    Store a detected quality marker in its corresponding result list.
    """

    result = {
        "file": str(file),
        "line": line_number,
        "content": content,
    }

    if marker == "TODO":
        todos.append(result)

    elif marker == "FIXME":
        fixmes.append(result)

    elif marker == "BUG":
        bugs.append(result)

    elif marker == "HACK":
        hacks.append(result)


def _analyze_python_comments(
    file,
    code,
    todos,
    fixmes,
    bugs,
    hacks,
):
    """
    Analyze Python comments using the tokenize module.

    Using Python tokens prevents CodeLens from incorrectly treating
    strings such as "TODO" or variable names containing "BUG"
    as quality markers.
    """

    try:
        tokens = tokenize.generate_tokens(
            io.StringIO(code).readline
        )

        for token in tokens:

            # Only actual Python comments should be inspected.
            if token.type != tokenize.COMMENT:
                continue

            comment = token.string
            upper_comment = comment.upper()

            line_number = token.start[0]

            for marker in ("TODO", "FIXME", "BUG", "HACK"):

                if marker in upper_comment:

                    _record_quality_marker(
                        marker,
                        file,
                        line_number,
                        comment.strip(),
                        todos,
                        fixmes,
                        bugs,
                        hacks,
                    )

    except tokenize.TokenError:
        # A partially invalid Python file should not stop the
        # complete CodeLens analysis pipeline.
        return


def _analyze_generic_comments(
    file,
    lines,
    todos,
    fixmes,
    bugs,
    hacks,
):
    """
    Analyze common comment formats used by non-Python files.

    This is intentionally conservative so that normal source-code
    strings containing marker words are not reported unnecessarily.
    """

    comment_prefixes = (
        "#",
        "//",
        "/*",
        "*",
    )

    for line_number, line in enumerate(lines, start=1):

        stripped = line.strip()

        # Only inspect lines that begin with a recognized
        # comment prefix.
        if not stripped.startswith(comment_prefixes):
            continue

        upper_line = stripped.upper()

        for marker in ("TODO", "FIXME", "BUG", "HACK"):

            if marker in upper_line:

                _record_quality_marker(
                    marker,
                    file,
                    line_number,
                    stripped,
                    todos,
                    fixmes,
                    bugs,
                    hacks,
                )


def _find_duplicate_lines(file, lines):
    """
    Find repeated meaningful lines within a file.

    Very short lines, blank lines, comments, and syntax-only lines
    are ignored because they commonly repeat in normal source code
    and do not provide useful duplication information.
    """

    meaningful_lines = []

    for line_number, line in enumerate(lines, start=1):

        normalized = " ".join(line.strip().split())

        if not normalized:
            continue

        if normalized.startswith(("#", "//", "/*", "*")):
            continue

        if len(normalized) < MIN_DUPLICATE_LINE_LENGTH:
            continue

        # Ignore lines consisting only of structural punctuation.
        if all(character in "{}[]():,;" for character in normalized):
            continue

        meaningful_lines.append(
            (line_number, normalized)
        )

    line_counts = Counter(
        line
        for _, line in meaningful_lines
    )

    duplicate_lines = []

    for line, count in line_counts.items():

        if count <= 1:
            continue

        line_numbers = [
            line_number
            for line_number, current_line in meaningful_lines
            if current_line == line
        ]

        duplicate_lines.append(
            {
                "file": str(file),
                "line": line,
                "count": count,
                "line_numbers": line_numbers,
            }
        )

    return duplicate_lines


def analyze_quality(files):
    """
    Analyze project files for basic code-quality indicators.

    The analyzer detects:
    - TODO comments
    - FIXME comments
    - BUG markers
    - HACK markers
    - Large files
    - Meaningful duplicate lines
    """

    todos = []
    fixmes = []
    bugs = []
    hacks = []
    large_files = []
    duplicate_lines = []

    for file in files:

        # Ignore unsupported or binary file types.
        if file.suffix not in SUPPORTED_EXTENSIONS:
            continue

        try:
            with open(file, "r", encoding="utf-8") as f:
                code = f.read()

        except (UnicodeDecodeError, PermissionError):
            continue

        lines = code.splitlines()

        # Detect files that exceed the configured size threshold.
        if len(lines) > LARGE_FILE_THRESHOLD:
            large_files.append(
                {
                    "file": str(file),
                    "lines": len(lines),
                }
            )

        # Python files receive token-based comment analysis.
        if file.suffix == ".py":

            _analyze_python_comments(
                file,
                code,
                todos,
                fixmes,
                bugs,
                hacks,
            )

        else:

            _analyze_generic_comments(
                file,
                lines,
                todos,
                fixmes,
                bugs,
                hacks,
            )

        # Detect meaningful repeated lines.
        duplicate_lines.extend(
            _find_duplicate_lines(file, lines)
        )

    return {
        "todos": todos,
        "fixmes": fixmes,
        "bugs": bugs,
        "hacks": hacks,
        "large_files": large_files,
        "duplicate_lines": duplicate_lines,
    }