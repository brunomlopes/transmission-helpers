from paramiko import SSHClient, WarningPolicy
from socket import timeout
from config import Configuration
from os import remove
from common import logger as log

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
    log("Still moving files")
else:
    result = sftp.put("files_to_download.txt", remote_file)
    log("uploaded files_to_download")
    chan = client.invoke_shell(width=400, height = 24)
    chan.settimeout(2)

    read_until_timeout(chan)
    command = 'screen -S lftp lftp -c "open sftp://%(remote_username)s@%(remote_host)s ; lcd /mnt/40/movement/ ; source files_to_download.txt" \n' % dict(remote_username = Configuration.username, remote_host = Configuration.host)
    chan.send(command)
    read_until_timeout(chan)
    chan.send("\n")
    read_until_timeout(chan)
    chan.close()
    remove("files_to_download.txt")
    log("screen started. local file deleted")

