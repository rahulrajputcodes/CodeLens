import argparse


# Create the command-line argument parser for CodeLens.
parser = argparse.ArgumentParser(
    description="CodeLens - Python Codebase Intelligence CLI"
)

# The first argument tells CodeLens what operation to perform.
parser.add_argument("command")

# The second argument specifies the project directory to analyze.
parser.add_argument("project")

# Read the arguments provided by the user.
args = parser.parse_args()


# Display the received arguments for now.
# More commands and analysis functionality will be added later.
print("CodeLens")
print("Command:", args.command)
print("Project:", args.project)