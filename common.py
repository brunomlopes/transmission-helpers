import os, traceback, subprocess
from os import path
from lib import transmissionrpc

class Result:
    def __init__(self, result):
        self.result = result
    
    def __str__(self):
        return "Result: %s\n%s" % (str(self.result), repr(self.result.__dict__))

class UploadingTorrentEvent:
    def __init__(self, localFileName):
        self.localFileName = localFileName

    def __str__(self):
        return "Uploading %s" % path.split(self.localFileName)[-1]

class TorrentAddedEvent:
    def __init__(self, localFileName):
        self.localFileName = localFileName

    def __str__(self):
        return "Added %s" % path.split(self.localFileName)[-1]

class DuplicatedTorrent:
    def __init__(self, localFileName):
        self.localFileName = localFileName
    def __str__(self):
        return "Duplicated torrent %s. Removing local file" % path.split(self.localFileName)[-1]

class MarkToDownload:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "Mark to download %s." % self.name


class Error:
    def __init__(self, message, exception):
        self.exception = exception
        self.message = message

    def __str__(self):
        return "Error %s - %s" % (self.message, traceback.format_exc())

class EventLogger:
    def log(self, event):
        print str(event)

    def __call__(self, event):
        return self.log(event)

class SnarlLogger(EventLogger):
    def __init__(self, snarl):
        self.snarl = snarl

    def log(self, event):
        self.snarl.snShowMessage("Transmission", str(event), timeout=5)

class GrowlLogger(EventLogger):
    def log(self, event):
        if event.__class__ is Error:
            print str(event)
            
        message = str(event).replace('"',"'").replace("\n","\\n")
        subprocess.call(['growlnotify', '/t:T', message])

logger = EventLogger()
try:
    from lib import pysnarl
    if (pysnarl.snGetVersion):
        logger = SnarlLogger
except:
    pass

try:
    subprocess.call("growlnotify")
    logger = GrowlLogger()
except WindowsError:
    pass


def get_client():
    from config import Configuration
    return transmissionrpc.Client(Configuration.host, Configuration.port, 
                                  Configuration.username, Configuration.password)

