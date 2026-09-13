import ast


def analyze_python_file(file):
    """
    Analyze a Python file using Python's Abstract Syntax Tree (AST).

    Returns information about:
    - Functions
    - Classes
    - Imports
    - Decorators
    """

    try:
        # Read the Python source code.
        with open(file, "r", encoding="utf-8") as f:
            code = f.read()

        # Convert the source code into an Abstract Syntax Tree.
        tree = ast.parse(code)

    except (UnicodeDecodeError, PermissionError):
        # Skip files that cannot be safely read.
        return {
            "file": str(file),
            "functions": [],
            "classes": [],
            "imports": [],
            "decorators": [],
            "function_count": 0,
            "class_count": 0,
            "import_count": 0,
            "decorator_count": 0,
            "syntax_error": False,
        }

    except SyntaxError as error:
        # Keep the analyzer running even if one Python file
        # contains invalid syntax.
        return {
            "file": str(file),
            "functions": [],
            "classes": [],
            "imports": [],
            "decorators": [],
            "function_count": 0,
            "class_count": 0,
            "import_count": 0,
            "decorator_count": 0,
            "syntax_error": True,
            "syntax_error_message": str(error),
        }

    functions = []
    classes = []
    imports = []
    decorators = []

    # Walk through every node in the AST.
    for node in ast.walk(tree):

        # Find normal functions and methods.
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

            # Collect decorators attached to the function.
            for decorator in node.decorator_list:
                decorators.append(ast.unparse(decorator))

        # Find classes.
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

        # Find regular import statements.
        elif isinstance(node, ast.Import):
            for name in node.names:
                imports.append(name.name)

        # Find "from module import name" statements.
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""

            for name in node.names:
                imports.append(f"{module}.{name.name}")

    return {
        "file": str(file),
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "decorators": decorators,
        "function_count": len(functions),
        "class_count": len(classes),
        "import_count": len(imports),
        "decorator_count": len(decorators),
        "syntax_error": False,
    }


def analyze_python_files(files):
    """
    Analyze every Python file discovered in the project.
    """

    results = []

    for file in files:

        # Only Python files should be passed to the AST analyzer.
        if file.suffix != ".py":
            continue

        result = analyze_python_file(file)
        results.append(result)

    return results