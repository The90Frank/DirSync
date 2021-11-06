#server
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from urllib.parse import unquote

majorFolderPath = ""
crcFile = ""

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        token_key = ""
        try:    token_key = self.headers.get("TokenKey")
        except: pass

        if ( token_key in appTokenKeys()):
            env = unquote(self.path)
            if (env == "/ListOfAll"):
                body_bytes = bytes(scanFolder(), "utf-8")
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Content-Length", len(body_bytes))
                self.end_headers()
                self.wfile.write(body_bytes)

            elif(env[:6] == "/File?"):
                from urllib.parse import urlparse, parse_qs
                query_components = parse_qs(urlparse(env).query)
                filepath = query_components["FilePath"].pop()
                if(fileExist(filepath)):
                    body_bytes = getFileBytes(filepath)
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.send_header("Content-Length", len(body_bytes))
                    self.end_headers()
                    self.wfile.write(body_bytes)
                else: 
                    self.send_response(500)
                    self.end_headers()

            else:
                self.send_response(501)
                self.end_headers()
        else:
            self.send_response(502)
            self.end_headers()

def server(port):
    myServer = HTTPServer(("0.0.0.0", port), MyServer)

    print(time.asctime(), "Server Starts - %s:%s" % ("0.0.0.0", port))

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % ("0.0.0.0", port)) 

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

    return json.dumps(filedict)

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

def getFileBytes(filepath):
    global majorFolderPath
    path = majorFolderPath+"\\"+filepath
    try:
        in_file = open(path, "rb")
        data = in_file.read()
        in_file.close()
        return data
    except:
        return bytes("", "utf-8")

def appTokenKeys():
    return ["aaa","bbb"]

def main():
    import json
    from pathlib import Path

    global majorFolderPath
    global crcFile
    script_location = str(Path(__file__).absolute().parent)

    with open(script_location+'\\config.json') as f:
        conf = json.load(f)
        majorFolderPath = conf["majorFolderPath"]
        crcFile = conf["crcFile"]
        server(conf["port"])

if __name__ == "__main__":
    main()