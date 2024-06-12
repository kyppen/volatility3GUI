import datetime
import os
import utils
import tkinter as tk
import commandData



def getFileNameFromCommand(selected_entry):
    words = selected_entry.get()
    words.strip()
    wordReplacedspace = words.replace(" ", ".")
    wordList = wordReplacedspace.split(".")
    filename = "undefined"
    count = 0
    for word in wordList:
        count = count + 1
        if (word == 'windows'):
            filename = word
            break
        if (word == 'mac'):
            filename = word
            break
        if (word == 'linux'):
            filename = word
            break

    filename = filename + "." + wordList[count]
    return filename
def AppendCommandToHistory(current_command):
    commandFile = open(f"commandFile.txt", "a+")
    commandFile.write(current_command.to_string() + "\n")
    commandFile.close()


def AppendCommandAndOutput(command_list, output):
    ts = datetime.datetime.now().timestamp()

    filename = command_list[-1]
    command_string = " ".join(command_list)
    filepath = os.path.join('history', f'{filename}{ts}')
    f = open(filepath, "x")

    f.write("command:" + "\n")
    f.write(command_string + "\n\n")
    f.write(output)
    f.close()

def getHistoryFromFile():
    path = "history"
    HistoryList = []
    historypath = os.path.join(os.path.curdir, 'history')
    if not os.path.exists(historypath):
        os.makedirs(historypath)

    for filename in os.listdir(path):
        Data = commandData.commandData()
        Data.set_command("")
        Data.set_output("")
        filepath = os.path.join(path, filename)
        if (os.path.isfile(filepath)):

            file = open(filepath, "r")
            fileList = file.readlines()
            file.close()
            if fileList[0].strip() == 'command:':
                temp = fileList[1]
                Data.set_command(temp)

                output = ''.join(fileList)
                Data.set_output(output)
        HistoryList.append(Data)


    print(f"History Length: {len(HistoryList)}")
    return HistoryList

def update_history(prevCommandList):
    info = getHistoryFromFile()
    count = 0
    prevCommandList.delete(0, tk.END)
    for command in info:

        prevCommandList.insert(count, command.get_command_formatted())
        count += 1
    return info
