import datetime
import subprocess


def AppendCommandToHistory(current_command):
    ts = datetime.datetime.now().timestamp()

    f = open(f"output/{current_command.getOsAndPlugin()}{ts}", "x")  # this creates the file
    commandFile = open(f"commandFile.txt", "a+")
    commandFile.write(current_command.to_string() + "\n")
    commandFile.close()

def AppendCommandAndOutput(current_command, output):
    ts = datetime.datetime.now().timestamp()
    f = open(f"output/{current_command.getOsAndPlugin()}{ts}", "x")
    f.write(current_command.to_string())
    f.write(output)
    f.close()
def update_history(command_list):
    f = open("commandFile.txt", "r")
    count = 0
    for i in f.readlines():
        command_list.insert(count, i)
