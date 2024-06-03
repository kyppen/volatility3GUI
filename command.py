import tkinter as tk
from tkinter import ttk, Menu, filedialog
class command:
    def __init__(self):
        self.flag = None
        self.plugin = None
        self.os = None
        self.filename = None

    #Allows the button's text to equal the current selected OS
    def set_os_button(self, os_button, os):
        #os_button = ttk.Menubutton(top_frame, text=self.os, menu=os_menu)
        self.os = os
        os_button.config(text=self.os)

    #This is called usually when the OS is being selected from intro screen
    def set_os(self, os):
        self.os = os

    def set_flag_button(self, flag_button, flag):
        self.flag = flag
        print(f"set_flag() to {flag}")
        flag_button.config(text=self.flag)
    def set_plugin(self, plugin):
        self.plugin = plugin
        print(f"set_plugin to {self.plugin} ")

    def set_plugin_button(self, plugin_button, plugin):
        self.plugin = plugin
        print(f"set_plugin to {self.plugin} ")
        plugin_button.config(text=self.plugin)
    def set_flag(self, flag):
        print(f"set_flag() to {flag}")
        self.flag = flag
    def set_filepath(self, file_path):
        self.filename = file_path.split("/")[-1]

    def getOsAndPlugin(self):
        return self.os + '.' + self.plugin
    def getLinuxCommandList(self):
        print(self.flag)
        print(self.filename)
        print(self.os)
        print(self.plugin)
        list = ["/home/fam/volatility3/volatility3/vol.py", self.flag, self.filename, self.getOsAndPlugin()]
        return list
    def getWindowsCommandList(self): #untested\
        print(self.flag)
        print(self.filename)
        print(self.os)
        print(self.plugin)
        list = ["python", "volatility3/vol.py", self.flag, self.filename, self.getOsAndPlugin()]
        return list
    def getOSXCommandList(self):
        #TODO
        return

    def to_string(self):
        if not all([self.os, self.plugin, self.flag, self.filename]):
            raise ValueError("All components (OS, command, flag, and file path) must be set")
        return f"{self.flag} {self.filename} {self.os}.{self.plugin}"
    def printString(self):
        print(self.os)
        print(self.plugin)
        print(self.flag)
        print(self.filename)
