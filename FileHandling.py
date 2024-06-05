import datetime
import os
import utils



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
    print(filename)
    return filename
def AppendCommandToHistory(selected_entry):
    commandFile = open(f"commandFile.txt", "a+")
    commandFile.write(selected_entry.get() + "\n")
    commandFile.close()


def AppendCommandAndOutput(current_command, output, selected_entry):
    ts = datetime.datetime.now().timestamp()
    filename = getFileNameFromCommand(selected_entry)
    print(filename)
    f = open(f"output/{filename}{ts}", "x")
    command = current_command.to_string(utils.detect_os())
    if(command == ""):
        f.write("command:" + "\n")
        f.write(selected_entry.get() + "\n\n")

    else:
        f.write("command:" + "\n")
        f.write(command + "\n\n")
    f.write(output)
    f.close()

def update_history(prevCommandList):
    print("update_history()")
    path = "output"
    HistoryList = []
    outputHistoryList = []
    for filename in os.listdir(path):
        output = ""
        filepath = os.path.join(path, filename)
        if(os.path.isfile(filepath)):
            file = open(filepath, "r")
            fileList = file.readlines()
            file.close()
            print(fileList[0])
            if(fileList[0].strip() == 'command:'):
                print("Line 0 == command:")
                command = fileList[1]
                print(command)
                HistoryList.append(command)
                for line in fileList:
                    output = output + line + "\n"
                outputHistoryList.append(output)
    info = []
    info.append(HistoryList)
    info.append(outputHistoryList)
    count = 0
    for command in HistoryList:
        print(command)
        prevCommandList.insert(count, command)
        count += 1
    return info
