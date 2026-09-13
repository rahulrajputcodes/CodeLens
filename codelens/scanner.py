from pathlib import Path


def scan_project(project_path):
    """
    Recursively scan a project directory and return all files found.
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

    # Recursively search through the entire project directory.
    for item in project_path.rglob("*"):
        if item.is_file():
            files.append(item)

    return files