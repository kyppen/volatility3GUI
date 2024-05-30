import tkinter as tk
class command:
    def __init__(self):
        self.flag = None
        self.plugin = None
        self.os = None
        self.filename = None

    def set_os(self, os):
        self.os = os
    def set_plugin(self, plugin):
        self.plugin = plugin
    def set_flag(self, flag):
        self.flag = flag
    def set_filepath(self, file_path):
        filename2 = file_path.split("/")[-1]
        self.filename = filename2
    def getOsAndPlugin(self):
        return self.os + '.' + self.plugin
    def getCommandList(self):
        list = ["/opt/volatility3/volatility3/volatility3/vol.py", self.flag, self.filename, self.getOsAndPlugin()]
        return list
    def to_string(self):
        if not all([self.os, self.plugin, self.flag, self.filename]):
            raise ValueError("All components (OS, command, flag, and file path) must be set")
        return f"python3 opt/volatility3/vol.py {self.flag} {self.filename} {self.os}.{self.plugin}"
    def printString(self):
        print(self.os)
        print(self.plugin)
        print(self.flag)
        print(self.filename)
