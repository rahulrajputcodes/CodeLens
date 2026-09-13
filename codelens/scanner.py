from pathlib import Path


# Directories that should never be analyzed by CodeLens.
# These contain generated files, dependencies, caches, or Git metadata.
IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "reports",
}


def scan_project(project_path):
    """
    Recursively scan a project directory and return all relevant files.
    """

    project_path = Path(project_path)

    # Make sure the provided path exists.
    if not project_path.exists():
        raise FileNotFoundError(
            f"Project path does not exist: {project_path}"
        )

    # CodeLens analyzes directories, not individual files.
    if not project_path.is_dir():
        raise NotADirectoryError(
            f"Project path is not a directory: {project_path}"
        )

    files = []

    # Recursively walk through the project while skipping
    # directories that should not be analyzed.
    for item in project_path.rglob("*"):

        if item.is_file():

            # Ignore files located inside excluded directories.
            if any(
                ignored in item.parts
                for ignored in IGNORED_DIRECTORIES
            ):
                continue

            files.append(item)

    return files