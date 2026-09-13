import json
from pathlib import Path


def build_report(project_path, files, file_analysis, ast_analysis, quality_analysis):
    """
    Combine all CodeLens analysis results into one structured report.
    """

    return {
        "project": str(Path(project_path).resolve()),
        "summary": {
            "files_analyzed": len(files),
            "python_files": file_analysis["python_files"],
            "total_lines": file_analysis["total_lines"],
        },
        "python_analysis": ast_analysis,
        "code_quality": quality_analysis,
    }


def save_report(report, output_path="reports/analysis.json"):
    """
    Save the complete CodeLens report as formatted JSON.
    """

    output_file = Path(output_path)

    # Create the reports directory if it does not already exist.
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write the report to disk in a human-readable format.
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    return output_file