import os
import logging
import sys
import time

import tqdm
import paramiko.util
import socket
import pandas as pd

import local_settings as settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# paramiko has a named logger. Use it.
logging.getLogger('paramiko')
paramiko.util.log_to_file(settings.paths['logs'])


def ceil_to_next_full_minutes(now: pd.Timestamp, next_full_minutes: int) -> float:
    delta = pd.Timedelta(minutes=next_full_minutes)
    next_run = now + delta
    logging.info(f"Next run at approximately {next_run}")
    return (next_run - now).total_seconds()


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
        logging.warning(f"A timeout was ignored: Actual exception message: {msg}")
        pass

    return None


if __name__ == '__main__':

    while True:
        download_files()
        seconds_to_next_run = ceil_to_next_full_minutes(pd.Timestamp.now(), 5)
        logging.info(f"Seconds to next run: {seconds_to_next_run}")
        time.sleep(seconds_to_next_run)
