#crc routine
crcFile = ""
majorFolderPath = ""

def crcIter(path):
    import os

    for root, dirs, files in os.walk(path):
        for file in files:
            if file == crcFile:
                try:            
                    os.remove(os.path.join(root,file))
                except:
                    pass
        for file in files:
            absFile = os.path.join(root,file)
            crcOfFile(absFile)
    return

def crcOfFile(absFile):
    import os
    from pathlib import Path
    import json
    global majorFolderPath
    folderPath = os.path.dirname(absFile)
    crcPath = folderPath+"\\"+crcFile
    
    crcs = {}
    try:
        with open(crcPath, 'r') as f:
            crcs = json.load(f)
    except:
        pass

    with open(crcPath, 'w') as json_file:
        if not(absFile.endswith(crcFile)) and Path(absFile).is_file() :
            crcs[absFile.removeprefix(majorFolderPath)] = crc(absFile)

        json.dump(crcs, json_file)
    return

def crc(fileName):
    import zlib
    prev = 0
    for eachLine in open(fileName,"rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X"%(prev & 0xFFFFFFFF)

def main():
    import json
    from pathlib import Path
    global crcFile
    global majorFolderPath
    script_location = str(Path(__file__).absolute().parent)

    with open(script_location+'\\config.json') as f:
        conf = json.load(f)
        majorFolderPath = conf["majorFolderPath"]
        crcFile = conf["crcFile"]
    crcIter(majorFolderPath)

if __name__ == "__main__":
    main()