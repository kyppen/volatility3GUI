import datetime
import os
import utils
import tkinter as tk



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


def AppendCommandAndOutput(current_command, output):
    ts = datetime.datetime.now().timestamp()
    filename = current_command.getOsAndPlugin()
    #print(filename)
    filepath = os.path.join('history', f'{filename}{ts}')
    f = open(filepath, "x")

    #if(command == ""):
        #f.write("command:" + "\n")
        #f.write(selected_entry.get() + "\n\n")

    #else:
    f.write("command:" + "\n")
    f.write(current_command.to_string() + "\n\n")
    f.write(output)
    f.close()

def update_history2(prevCommandList):
    print("update_history()")
    path = "history"
    HistoryList = []
    outputHistoryList = []
    for filename in os.listdir(path):
        output = ""
        filepath = os.path.join(path, filename)
        if (os.path.isfile(filepath)):

            file = open(filepath, "r")
            fileList = file.readlines()
            file.close()
            #print(fileList[0])
            #if(len(fileList) < 3):
            #    break
            if (fileList[0].strip() == 'command:'):
                print("Line 0 == command:")
                command = fileList[1]
                #print(command)
                HistoryList.append(command)
                for line in fileList:
                    output = output + line
                outputHistoryList.append(output)
    info = []
    info.append(HistoryList)
    info.append(outputHistoryList)
    count = 0
    prevCommandList.delete(0, tk.END)
    for command in HistoryList:
        print(command)

        prevCommandList.insert(count, command)
        count += 1
    return info

def getHistoryFromFile():
    print("update_history()")
    path = "history"
    HistoryList = []
    output = ""

    for filename in os.listdir(path):
        cmdOutput = ""
        print("for loop")
        filepath = os.path.join(path, filename)
        Data = commandData.commandData()
        if (os.path.isfile(filepath)):

            file = open(filepath, "r")
            fileList = file.readlines()
            file.close()
            #print(fileList[0])
            #if (fileList[0].strip() == 'command:'):

            temp = fileList[1]
            Data.set_command(temp)

            for line in fileList:
                output = output + line
            Data.set_output(output)
        HistoryList.append(Data)
    return HistoryList

def update_history(prevCommandList):
    info = getHistoryFromFile()
    count = 0
    prevCommandList.delete(0, tk.END)
    for command in info:
        print(command.get_command())

        prevCommandList.insert(count, command.get_command_formatted())
        count += 1
    return info
