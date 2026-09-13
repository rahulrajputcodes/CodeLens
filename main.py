import argparse

from codelens.scanner import scan_project
from codelens.file_analyzer import analyze_files


# Create the command-line argument parser for CodeLens.
parser = argparse.ArgumentParser(
    description="CodeLens - Python Codebase Intelligence CLI"
)

# The first argument specifies the operation to perform.
parser.add_argument("command")

# The second argument specifies the project directory.
parser.add_argument("project")

# Read the arguments provided by the user.
args = parser.parse_args()


if args.command == "analyze":

    # Find every file inside the project.
    files = scan_project(args.project)

    # Analyze the discovered files and calculate basic statistics.
    analysis = analyze_files(files)

    print()
    print("========== CODELENS ==========")
    print()
    print("Project:", args.project)
    print()
    print("Files analyzed :", len(files))
    print("Python files   :", analysis["python_files"])
    print("Total lines    :", analysis["total_lines"])