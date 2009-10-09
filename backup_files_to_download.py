from paramiko import SSHClient, WarningPolicy
from socket import timeout
from config import Configuration
from os import remove
from common import logger as log
from time import time

remote_file = Configuration.Fetcher.directory+"/files_to_download.txt"

def get_ssh_client():
    client = SSHClient()
    client.set_missing_host_key_policy(WarningPolicy())
    client.load_system_host_keys()
    client.connect(Configuration.Fetcher.host, username = Configuration.Fetcher.username)
    return client

def still_moving_files(sftp):
    try:
        sftp.stat(remote_file)
        return True
    except IOError:
        return False

def remove_remote_file(sftp):
    sftp.remove(remote_file)

def read_until_timeout(chan):
    s = ""
    try:
        while True:
            s += chan.recv(1024)
    except timeout: return s

client = get_ssh_client()
sftp = client.open_sftp()
if still_moving_files(sftp):
    local_file_name = "files_to_download_%d.txt" % time()
    sftp.get(remote_file, local_file_name)
    log("Backed up file to %s" % local_file_name)
    sftp.remove(remote_file)
    log("Removed remote filename")
