from common import get_client, logger, MarkToDownload
from time import time
import os.path

already_downloaded = []
if os.path.exists("already_downloaded.txt"):
    already_downloaded = [x.strip() for x in file("already_downloaded.txt").readlines()]

client = get_client()

torrent_list = client.info()
finished_torrents = [torrent for torrent in [torrent_list[i] for i in torrent_list] 
                     if torrent.progress == 100]
finished_torrents_with_new_files = sorted([torrent for torrent in finished_torrents
                                           if torrent.name not in already_downloaded]
                                          , key = lambda t : t.date_done)

transmission_home_dir = client.session.download_dir

if not transmission_home_dir.endswith("/"):
    transmission_home_dir += "/"
count = 0
for torrent in finished_torrents_with_new_files:
    files = [f["name"] for f in client.get_files(torrent.id)[torrent.id].values()
             if f["completed"] == f["size"]]
    f = file("files_to_download.txt","ab")
    for name in files:
        full_remote_path = transmission_home_dir+name
        local_dir = name.rsplit("/",1)[0]
        f.write('!mkdir -p "%s"\n' % local_dir)
        f.write('get -c "%s" -o "%s"\n' % (full_remote_path, name))
    f.close()
    
    f = file("already_downloaded.txt","a")
    f.write(torrent.name+"\n")
    f.close()

    logger(MarkToDownload(torrent.name))
    count += 1

if count == 0:
    logger(NoNewTorrents())

f = file("files_to_download.txt","ab")
f.write('!rm files_to_download.txt\n')
f.close()

