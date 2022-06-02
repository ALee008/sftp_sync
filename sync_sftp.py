import os
import sys
import pathlib
import datetime
import logging

import tqdm
import paramiko.util
import socket

import local_settings as settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# paramiko has a named logger. Use it.
logging.getLogger('paramiko')
paramiko.util.log_to_file(settings.paths['logs'])


def download_files():
    """Download file based on configuration in local_settings.py
    :return: None
    """
    # create sftp object
    try:
        with paramiko.Transport((settings.server['server'], settings.server['port'])) as transport:
            transport.connect(username=settings.login['user'], password=settings.login['password'])
            sftp = paramiko.SFTPClient.from_transport(transport)
            for file_name in tqdm.tqdm(settings.files, file=sys.stdout):
                source = os.path.join(settings.paths['source'], file_name)
                destination = os.path.join(settings.paths['destination'], file_name)
                remote_timestamp, destination_timestamp = sftp.stat(source).st_mtime, pathlib.Path(
                    destination).stat().st_mtime
                if remote_timestamp > destination_timestamp:
                    sftp.get(source, destination)
                else:
                    logging.info(f"Remote file {file_name} - {ts(remote_timestamp)} has lower or equal timestamp "
                                 f"as destination file {destination} - {ts(destination_timestamp)}. Download skipped.")
    except socket.timeout as msg:
        logging.warning(f"A timeout was ignored: Actual exception message: {msg}")
        pass

    return None


def ts(timestamp: float) -> str:
    """Return human-readable time from `timestamp`.

    :param timestamp: st_mtime from file.
    """
    dt = datetime.datetime.fromtimestamp(timestamp)

    return dt.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    download_files()
