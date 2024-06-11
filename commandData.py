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
        print("get_command_formatted()")
        print(self.command)
        splitCommand = self.command.split(" ")
        #for word in splitCommand:
        #    print(word)
        print(splitCommand[2])
        print(splitCommand[3])
        print(splitCommand[4])
        formatted = f"{splitCommand[2]} {splitCommand[3]} {splitCommand[4]}"
        return formatted.strip()

