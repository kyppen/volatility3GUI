class commandData:
    def __init__(self):
        self.command = None
        self.filename = None
        self.output = None
        self.path = None

    def set_output(self, output):
        self.output = output

    def set_command(self, command):
        self.command = command

    def get_output(self):
        return self.output
    def get_command(self):
        return self.command


    def get_command_formatted(self):
        filename = ""
        pluginname = ""
        splitCommand = self.command.split(" ")
        count = 0
        flag = []
        countAtPlugin = 0

        for fileArg in splitCommand:
            if fileArg == "-f":
                print(f"word = {fileArg}")
                file = splitCommand[count+1]
                filename = file.split("/")[-1]

            count += 1
            for index, pluginArg in enumerate(splitCommand):
                if "windows" in pluginArg or "mac" in pluginArg or "linux" in pluginArg:
                    countAtPlugin = index+1
                    pluginname = pluginArg
            flag = splitCommand[countAtPlugin:]



        return f"{filename} {pluginname} {' '.join(flag)}".strip()

