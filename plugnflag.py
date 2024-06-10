import os

def read_plugins_from_file(input_file):
    plugins = {}
    current_plugin = None
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if not line.startswith('-'):
                current_plugin = line.lower()
                plugins[current_plugin] = []
            else:
                if current_plugin:
                    plugins[current_plugin].append(f"--{line.strip('-').strip().lower()}")
    return plugins

def generate_plugin_code(plugins):
    plugin_code = ""
    for plugin, flags in plugins.items():
        plugin_title = plugin.capitalize()
        plugin_code += f"    # {plugin_title}_plugin\n"
        plugin_code += f"    {plugin_title}_plugin = Menu(commands_menu, tearoff=0)\n"
        for flag in flags:
            var_name = f"{plugin}_{flag.strip('--')}_var"
            plugin_code += f"    {var_name} = tk.BooleanVar()\n"
            plugin_code += f"    {plugin_title}_plugin.add_checkbutton(label=\"{flag}\", variable={var_name}, command=lambda: add_to_command(\"{plugin}\", \"{flag}\", command_list))\n"
        plugin_code += f"    commands_menu.add_cascade(label=\"{plugin_title}\", menu={plugin_title}_plugin)\n\n"
    return plugin_code

def insert_code_into_file(volgui_file, plugin_code):
    with open(volgui_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the line where to insert the plugin code
    insert_line = None
    for i, line in enumerate(lines):
        if 'commands_menu = Menu(frame_center, tearoff=0)' in line:
            insert_line = i + 1
            break

    if insert_line is None:
        raise ValueError("Could not find the appropriate place to insert the plugin code in the volGUI3.py file.")

    # Insert the plugin code
    lines.insert(insert_line, plugin_code)

    # Write the updated content back to the file
    with open(volgui_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)

if __name__ == "__main__":
    input_file = input("Enter the path to the input text file with plugins and flags: ")
    volgui_file = input("Enter the path to the volGUI3.py file: ")

    # Read plugins and flags from the input file
    plugins = read_plugins_from_file(input_file)

    # Generate the plugin code
    plugin_code = generate_plugin_code(plugins)

    # Insert the plugin code into the volGUI3.py file
    insert_code_into_file(volgui_file, plugin_code)

    print(f"Plugin code successfully inserted into {volgui_file}")
