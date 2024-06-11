import os
import ast


def parse_plugin_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)

    flags_with_input = []

    for stmt in ast.walk(tree):
        if isinstance(stmt, ast.Call) and hasattr(stmt.func, 'attr'):
            if stmt.func.attr == 'ListRequirement':
                for keyword in stmt.keywords:
                    if keyword.arg == 'name':
                        # Use .value instead of .s for compatibility with future Python versions
                        flag_name = keyword.value.value
                        flags_with_input.append(flag_name)

    return flags_with_input


def parse_plugins_in_folder(folder_path, output_file):
    all_flags_with_input = set()

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                flags_with_input = parse_plugin_file(file_path)
                all_flags_with_input.update(flags_with_input)

    with open(output_file, 'w', encoding='utf-8') as output:
        for flag in sorted(all_flags_with_input):
            output.write(f'{flag} takes input\n')


if __name__ == "__main__":
    folder_path = input("Enter the path to the folder containing the plugin files: ")
    output_file = input("Enter the output file path: ")
    parse_plugins_in_folder(folder_path, output_file)
    print(f"Flags that take input have been written to {output_file}")
