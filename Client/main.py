#client
# -*- coding: utf-8 -*-

majorFolderPath = ""
crcFile = ""
ip = 0
port = ""

def downloadCRCS():
    import requests
    h = {
        "TokenKey":"aaa"
    }
    r = requests.get("http://"+ip+":"+str(port)+"/ListOfAll",headers=h)
    return r.text

def downloadFile(filepath):
    import requests
    import urllib
    h = {
        "TokenKey":"aaa"
    }
    p = {
        "FilePath":filepath
    }
    par = urllib.parse.urlencode(p, quote_via=urllib.parse.quote)
    r = requests.get("http://"+ip+":"+str(port)+"/File",headers=h,params=par)
    return r.content

def scanFolder():
    global majorFolderPath
    import os
    import json

    filedict = {}
    for root, dirs, files in os.walk(majorFolderPath):
        for file in files:
            filePath = os.path.join(root,file)
            if (file.endswith(crcFile)):
                with open(filePath) as f:
                    crcs = json.load(f)
                    filedict.update(crcs)

    return filedict

def dictReduce(masterDict, minorDict):
    for k in minorDict.keys():
        if (minorDict[k] == masterDict[k]):
            del masterDict[k]
    return masterDict

def main():
    import json
    import os
    from pathlib import Path

    global majorFolderPath
    global crcFile
    global ip
    global port
    script_location = str(Path(__file__).absolute().parent)

    with open(script_location+'\\config.json') as f:
        conf = json.load(f)
        majorFolderPath = conf["majorFolderPath"]
        crcFile = conf["crcFile"]
        port = conf["port"]
        ip = conf["ip"]
        subToSync = conf["subToSync"]
    
    serverCrcs = json.loads(downloadCRCS())
    clientCrcs = scanFolder()
    serverCrcs = dictReduce(serverCrcs, clientCrcs)
    serverCrcsFilteredKeys = list(filter(lambda k: k.startswith(tuple(subToSync)),serverCrcs.keys()))
    folderList = list( set([os.path.dirname(f) for f in serverCrcsFilteredKeys])) 
    folderList.sort()
    
    for f in folderList:
        absPath = majorFolderPath+"\\"+f
        try:
            os.stat(absPath)
        except:
            os.mkdir(absPath)

    print(str(len(serverCrcsFilteredKeys))+" to download(s)")
    
    i = 0
    for k in serverCrcsFilteredKeys:
        i = i+1
        absPath = majorFolderPath+"\\"+k
        print("["+str(i)+"]Start download of:"+k)
        b = downloadFile(k)
        f = open(absPath, "wb")
        f.write(b)
        f.close()
        print("["+str(i)+"]End download of:"+k)

def fileExist(filepath):
    global majorFolderPath
    from pathlib import Path
    if not(filepath is None) and len(filepath) > 0:
        path = majorFolderPath+"\\"+filepath
        exist = Path(path).exists()
        isfile = Path(path).is_file()
        return (exist and isfile)
    else:
        return False

if __name__ == "__main__":
    main()
