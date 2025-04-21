import ast, subprocess, sys, os

def extract_imports(file_path):
    """Extract all imported modules from a Python file."""
    with open(file_path, "r") as file:
        tree = ast.parse(file.read())
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.add(name.name.split(".")[0])  # Get the top-level module
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])  # Get the top-level module
    return imports

def generate_requirements(imports, output_file):
    """Generate a requirements file based on the imports."""
    installed_packages = subprocess.check_output(["pip", "freeze"]).decode("utf-8")
    installed_packages = installed_packages.splitlines()
    requirements = []
    for package in installed_packages:
        package_name = package.split("==")[0]
        if package_name in imports:
            requirements.append(package)
    with open(output_file, "w") as file:
        file.write("\n".join(requirements))
    print(f"Requirements saved to {output_file}")

def main():
    # Check if the user provided a file path as an argument
    if len(sys.argv) < 2:
        print("Usage: python generate_requirements.py <path_to_python_file>")
        sys.exit(1)

    # Get the file path from the command-line arguments
    file_path = sys.argv[1]

    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    # Extract the base name of the file (without extension) for naming the output file
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = f"{base_name}_requirements.txt"

    # Extract imports and generate requirements
    print(f"Analyzing imports in '{file_path}'...")
    imports = extract_imports(file_path)
    if not imports:
        print("No imports found in the file.")
        sys.exit(0)

    print(f"Found imports: {', '.join(imports)}")
    generate_requirements(imports, output_file)

if __name__ == "__main__":
    main()
