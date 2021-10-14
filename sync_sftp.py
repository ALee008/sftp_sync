import os
import logging
import sys
import time
import datetime

import tqdm
import paramiko.util
import socket

import local_settings as settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# paramiko has a named logger. Use it.
logging.getLogger('paramiko')
paramiko.util.log_to_file(settings.paths['logs'])


def ceil_to_next_full_minutes(now: int, next_full_minutes: int) -> int:
    for minute in range(0, next_full_minutes):
        if (now + minute) % next_full_minutes == 0:
            return minute * 60


def get_user_friendly_timestamp(seconds: float):
    dt = datetime.datetime.fromtimestamp(seconds)

    return dt.strftime("%Y-%m-%d %H:%M:00")


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
        seconds_to_next_run = ceil_to_next_full_minutes(time.gmtime().tm_min, 5)
        logging.info(f"Next run at approximately {get_user_friendly_timestamp(time.time() + seconds_to_next_run)}")
        time.sleep(seconds_to_next_run)
