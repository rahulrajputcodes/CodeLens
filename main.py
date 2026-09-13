import argparse

from codelens.scanner import scan_project
from codelens.file_analyzer import analyze_files
from codelens.search import search_project
from codelens.ast_analyzer import analyze_python_files
from codelens.quality import analyze_quality
from codelens.reporter import build_report, save_report


def analyze_command(project_path):
    """
    Run the complete CodeLens analysis pipeline.
    """

    print()
    print("========== CODELENS ANALYSIS ==========")
    print()
    print("Project:", project_path)
    print()

    # Step 1: Discover all files in the project.
    files = scan_project(project_path)

    print("Files discovered:", len(files))

    # Step 2: Analyze basic file statistics.
    file_analysis = analyze_files(files)

    print("Python files:", file_analysis["python_files"])
    print("Total lines:", file_analysis["total_lines"])

    # Step 3: Analyze Python source code using the AST.
    ast_analysis = analyze_python_files(files)

    print("Python files analyzed:", len(ast_analysis))

    # Step 4: Analyze basic code-quality indicators.
    quality_analysis = analyze_quality(files)

    print("TODOs:", len(quality_analysis["todos"]))
    print("FIXMEs:", len(quality_analysis["fixmes"]))
    print("BUGs:", len(quality_analysis["bugs"]))
    print("HACKs:", len(quality_analysis["hacks"]))
    print("Large files:", len(quality_analysis["large_files"]))
    print("Duplicate lines:", len(quality_analysis["duplicate_lines"]))

    # Step 5: Combine all analysis results into one report.
    report = build_report(
        project_path,
        files,
        file_analysis,
        ast_analysis,
        quality_analysis,
    )

    # Step 6: Save the final report as JSON.
    report_path = save_report(report)

    print()
    print("Report generated:", report_path)
    print()
    print("========== ANALYSIS COMPLETE ==========")


def search_command(project_path, keyword):
    """
    Search the project for a keyword.
    """

    print()
    print("========== CODELENS SEARCH ==========")
    print()
    print("Keyword:", keyword)
    print()

    # Discover all project files.
    files = scan_project(project_path)

    # Search all supported files for the keyword.
    results = search_project(files, keyword)

    if not results:
        print("No matches found.")
        return

    # Display every search result.
    for result in results:
        print(
            f'{result["file"]}:{result["line"]} → '
            f'{result["content"]}'
        )

    print()
    print("Matches found:", len(results))


def main():
    """
    Parse command-line arguments and run the requested command.
    """

    parser = argparse.ArgumentParser(
        description="CodeLens - Python Codebase Intelligence CLI"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # Analyze command.
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a project",
    )

    analyze_parser.add_argument(
        "project",
        help="Path to the project directory",
    )

    # Search command.
    search_parser = subparsers.add_parser(
        "search",
        help="Search for a keyword",
    )

    search_parser.add_argument(
        "project",
        help="Path to the project directory",
    )

    search_parser.add_argument(
        "keyword",
        help="Keyword to search for",
    )

    args = parser.parse_args()

    if args.command == "analyze":
        analyze_command(args.project)

    elif args.command == "search":
        search_command(args.project, args.keyword)


if __name__ == "__main__":
    main()