import datetime
import os
import utils
import tkinter as tk
import commandData



def getFileNameFromCommand(selected_entry):
    words = selected_entry.get()
    print(words)
    words.strip()
    wordReplacedspace = words.replace(" ", ".")
    print(wordReplacedspace)
    wordList = wordReplacedspace.split(".")
    print(wordReplacedspace)
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
    #print(filename)
    return filename
def AppendCommandToHistory(current_command):
    commandFile = open(f"commandFile.txt", "a+")
    commandFile.write(current_command.to_string() + "\n")
    commandFile.close()


def AppendCommandAndOutput(command_list, output):
    print("AppendCommandAndOutput()")
    ts = datetime.datetime.now().timestamp()

    #len(full_command)
    filename = command_list[-1]
    command_string = " ".join(command_list)
    #filename = current_command.getOsAndPlugin()
    #print(filename)
    filepath = os.path.join('history', f'{filename}{ts}')
    f = open(filepath, "x")

    #if(command == ""):
        #f.write("command:" + "\n")
        #f.write(selected_entry.get() + "\n\n")

    #else:
    f.write("command:" + "\n")
    f.write(command_string + "\n\n")
    f.write(output)
    f.close()

def getHistoryFromFile():
    print("update_history()")
    path = "history"
    HistoryList = []
    output = ""

    for filename in os.listdir(path):
        Data = commandData.commandData()
        cmdOutput = ""
        filepath = os.path.join(path, filename)
        if (os.path.isfile(filepath)):

            file = open(filepath, "r")
            fileList = file.readlines()
            file.close()
            if fileList[0].strip() == 'command:':
                print(fileList[0])
                temp = fileList[1]
                Data.set_command(temp)

                for line in fileList:
                    output = output + line
                Data.set_output(output)
        HistoryList.append(Data)
    return HistoryList

def update_history(prevCommandList):
    print("update_history()")
    info = getHistoryFromFile()
    count = 0
    prevCommandList.delete(0, tk.END)
    for command in info:
        print(command.get_command())

        prevCommandList.insert(count, command.get_command_formatted())
        count += 1
    return info
