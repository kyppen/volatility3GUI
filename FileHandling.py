import datetime


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
    fuckOff = current_command.to_string()
    if(fuckOff == ""):
        f.write(selected_entry.get())
    else:
        f.write(current_command.to_string())
    f.write(output)
    f.close()
def update_history(command_list):
    f = open("commandFile.txt", "r")
    count = 0
    for i in f.readlines():
        command_list.insert(count, i)
