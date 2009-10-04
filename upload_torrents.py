from paramiko import SSHClient
from common import  TorrentAddedEvent, DuplicatedTorrent, Error, UploadingTorrentEvent, logger, get_client
from StringIO import StringIO 
from lib import transmissionrpc
import sys, base64, os

torrent_files = sys.argv[1:]
client = get_client()

download_dir = client.session.download_dir

def upload_file(file_path):
    output = StringIO()
    base64.encode(file(file_path,"rb"), output)
    result = client.add(output.getvalue())
    logger.log(TorrentAddedEvent(file_path))

remove_files = True
for file_path in torrent_files:
    logger(UploadingTorrentEvent(file_path))
    try:
        upload_file(file_path)
        if remove_files: os.remove(file_path)
    except transmissionrpc.TransmissionError, e:
        if '"duplicate torrent"' in e.message:
            if remove_files: os.remove(file_path)
            logger.log(DuplicatedTorrent(file_path))
        else:
            logger.log(Error("Error uploading file", e))
    except Exception, e:
        logger.log(Error("Error uploading file", e))
    
