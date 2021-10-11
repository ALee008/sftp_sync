import os
import logging
import sys

import tqdm
import paramiko.util
import schedule
import socket

import local_settings as settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# paramiko has a named logger. Use it.
logging.getLogger('paramiko')
paramiko.util.log_to_file(settings.paths['logs'])


def download_files():
    # create sftp object
    try:
        with paramiko.Transport((settings.server['server'], settings.server['port'])) as transport:
            transport.connect(username=settings.login['user'], password=settings.login['password'])
            sftp = paramiko.SFTPClient.from_transport(transport)
            for file_name in tqdm.tqdm(settings.files, file=sys.stdout):
                source = os.path.join(settings.paths['source'], file_name)
                destination = os.path.join(settings.paths['destination'], file_name)
                sftp.get(source, destination)
    except socket.timeout as msg:
        logging.WARNING(f"A timeout was ignored: Actual exception message: {msg}")
        pass

    return None


schedule.every(5).minutes.do(download_files)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
